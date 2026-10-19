"""Harness spec: one small YAML per paper. The one human checkpoint in the pipeline.

    name: toy
    base: local:eval/toy/hidden_knob     # or an OCI ref / checkpoint uuid
    build: {command: "make -j BUILD_MODE={build_mode}", timeout: 1800}
    load:  {command: "python load.py --n {num_keys}", timeout: 1800}
    run:
      command: "python bench.py --alpha {alpha} > out/run.log"
      output: out/run.log                 # file under /work, or "stdout"
      format: kv                          # kv | jsonl | db_bench | auto
      timeout: 600
    knobs:
      alpha: {layer: config, default: "1.0"}
      SEED_ENV: {layer: environment, default: "0", env: true}
    allowed_paths: ["configs/", "out/"]   # diff guard: anything else is algorithm code
    metrics: [throughput, write_amp]

Every `{knob}` in a stage command is filled with the knob's value for that
branch (default unless the branch changes it). `env: true` knobs are passed as
environment variables instead.
"""

from __future__ import annotations

import fnmatch
import os
import re
from pathlib import Path

import yaml
from pydantic import BaseModel, Field, model_validator

from gapfinder.ledger.schemas import Layer


class Stage(BaseModel):
    command: str
    timeout: float = 1800


class RunStage(Stage):
    output: str = "stdout"
    format: str = "auto"
    timeout: float = 600
    # A Sandboxes operation runs at most 3600 s, so a longer cell is split (the timeout is per piece):
    # - shards: a cell made of independent jobs (datasets x horizons, folds, seeds). Each value replaces {shard} in
    #   the command and runs in its own VM, in parallel; the outputs are joined and parsed as one run.
    # - segments: training that resumes from files on disk. The command runs `segments` times in sequence, {segment}
    #   = 1, 2, ..., each from the previous one's checkpoint; the joined outputs are parsed.
    shards: list[str] = Field(default_factory=list)
    segments: int = 1
    # shards that are repeats of one cell (seeds): each shard's metrics are parsed alone and averaged, instead of
    # the joined output's last value of each metric (output "stdout" only)
    shard_mean: bool = False


class Knob(BaseModel):
    layer: Layer
    default: str
    env: bool = False
    candidates: list[str] = Field(default_factory=list)
    choices: list[str] = Field(default_factory=list)  # every value the program accepts (argparse choices)
    multiplier: bool = False  # scales another quantity (e.g. epochs = base x epochx): literal factors are candidates
    scales: list[str] = Field(default_factory=list)  # what the code multiplies by this knob (static config flow)
    max: float | None = None  # values above this are too costly to test (reported, not run)
    # what a dry-run trace saw the value do (gapfinder/search/trace.py): rate, rate0, fraction, size, count,
    # multiplier or seed. None: not traced, so candidate values fall back to the name rules
    role: str | None = None

    def affordable(self, value: str) -> bool:
        if self.max is None:
            return True
        try:
            return float(value) <= self.max
        except ValueError:
            return True


class HarnessSpec(BaseModel):
    name: str
    base: str
    # local copy of the artifact's code, for static analysis only (repo map, out-of-space code checks)
    # when `base` is an image or a checkpoint; a local `base` is used directly
    source: str | None = None
    build: Stage | None = None
    load: Stage | None = None
    run: RunStage
    knobs: dict[str, Knob] = Field(default_factory=dict)
    # the CPU shim and allocator settings on every run (gapfinder/sandbox/runtime_shim.py); off only for a harness
    # that must see the program exactly as it fails without them
    runtime_shim: bool = True
    allowed_paths: list[str] = Field(default_factory=list)
    metrics: list[str] = Field(default_factory=list)
    # history matching's model-discrepancy allowance, as a fraction of the paper's value: how far a correct
    # configuration may still sit from the paper because the reproduction differs (a scaled-down surrogate:
    # MC Dropout's T and splits, 0.05). None: a full-scale reproduction, and `gapfinder search` uses 0.01.
    # 0.05 for every case made a 5.8% gap (VGAE), 2.3% (FastGCN) and 2.2% (GraphMAE) look like noise
    discrepancy: float | None = None

    @model_validator(mode="after")
    def _placeholders_known(self):
        for stage_name in ("build", "load", "run"):
            stage = getattr(self, stage_name)
            if stage is None:
                continue
            for field in _placeholders(stage.command):
                if field not in self.knobs and not (stage_name == "run" and field in RESERVED):
                    raise ValueError(f"{stage_name} command uses unknown knob {{{field}}}")
        return self

    @classmethod
    def load_yaml(cls, path: str | Path) -> "HarnessSpec":
        data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
        data["base"] = os.path.expandvars(str(data.get("base", "")))  # e.g. ${GF_RUSKEY_SOURCE}
        if "$" in data["base"]:
            raise ValueError(f"{path}: base {data['base']!r} needs an environment variable that isn't set")
        spec = cls.model_validate(data)
        if spec.base.startswith("local:"):  # resolve relative to the spec file
            p = Path(spec.base[6:])
            if not p.is_absolute():
                spec.base = "local:" + str((Path(path).parent / p).resolve())
        if spec.source:
            spec.source = os.path.expandvars(spec.source)
            if not Path(spec.source).is_absolute():
                spec.source = str((Path(path).parent / spec.source).resolve())
        return spec

    def code_root(self) -> Path | None:
        """The artifact's code on this machine, if any (for static analysis)."""
        for p in (self.source, self.base.removeprefix("local:") if self.base.startswith("local:") else None):
            if p and "$" not in p and Path(p).is_dir():
                return Path(p)
        return None

    def values(self, changes: dict[str, str]) -> dict[str, str]:
        unknown = set(changes) - set(self.knobs)
        if unknown:
            raise KeyError(f"changes to knobs not in spec: {sorted(unknown)}")
        return {k: changes.get(k, kn.default) for k, kn in self.knobs.items()}

    def render(self, stage: Stage, changes: dict[str, str]) -> tuple[str, dict[str, str]]:
        vals = self.values(changes)
        cmd_vals = {k: _shell_safe(v) for k, v in vals.items() if not self.knobs[k].env}
        env = {k: v for k, v in vals.items() if self.knobs[k].env}
        # {shard} and {segment} are filled per piece by the runner (RunStage.shards / .segments)
        cmd = _PLACEHOLDER.sub(lambda m: m.group(0) if m.group(1) in RESERVED and m.group(1) not in cmd_vals
                               else cmd_vals.get(m.group(1), ""), stage.command)
        return cmd, env

    def changes_for_layers(self, changes: dict[str, str], layers: set[str]) -> dict[str, str]:
        return {k: v for k, v in changes.items() if self.knobs[k].layer in layers}


RESERVED = {"shard", "segment"}  # run-command placeholders the runner fills, not knobs

# `{knob}` placeholders; `${VAR}` shell expansions are left alone.
_PLACEHOLDER = re.compile(r"(?<!\$)\{(\w+)\}")


def _placeholders(template: str) -> set[str]:
    return set(_PLACEHOLDER.findall(template))


_SAFE = re.compile(r"^[\w.,:/+=@%-]*$")


def _shell_safe(v: str) -> str:
    if not _SAFE.match(v):
        raise ValueError(f"knob value {v!r} has shell metacharacters")
    return v


def diff_guard(changed_paths: list[str], allowed: list[str]) -> list[str]:
    """Return the changed paths that fall outside the allowed set (empty = OK)."""
    bad = []
    for p in changed_paths:
        p = p.replace("\\", "/").lstrip("./")
        ok = any(p.startswith(a.rstrip("*")) if not any(c in a for c in "*?[") else fnmatch.fnmatch(p, a) for a in allowed)
        if not ok:
            bad.append(p)
    return bad
