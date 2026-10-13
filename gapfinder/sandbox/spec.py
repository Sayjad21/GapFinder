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


class Knob(BaseModel):
    layer: Layer
    default: str
    env: bool = False
    candidates: list[str] = Field(default_factory=list)
    choices: list[str] = Field(default_factory=list)  # every value the program accepts (argparse choices)
    multiplier: bool = False  # scales another quantity (e.g. epochs = base x epochx): literal factors are candidates
    max: float | None = None  # values above this are too costly to test (reported, not run)

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
    build: Stage | None = None
    load: Stage | None = None
    run: RunStage
    knobs: dict[str, Knob] = Field(default_factory=dict)
    allowed_paths: list[str] = Field(default_factory=list)
    metrics: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def _placeholders_known(self):
        for stage_name in ("build", "load", "run"):
            stage = getattr(self, stage_name)
            if stage is None:
                continue
            for field in _placeholders(stage.command):
                if field not in self.knobs:
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
        return spec

    def values(self, changes: dict[str, str]) -> dict[str, str]:
        unknown = set(changes) - set(self.knobs)
        if unknown:
            raise KeyError(f"changes to knobs not in spec: {sorted(unknown)}")
        return {k: changes.get(k, kn.default) for k, kn in self.knobs.items()}

    def render(self, stage: Stage, changes: dict[str, str]) -> tuple[str, dict[str, str]]:
        vals = self.values(changes)
        cmd_vals = {k: _shell_safe(v) for k, v in vals.items() if not self.knobs[k].env}
        env = {k: v for k, v in vals.items() if self.knobs[k].env}
        cmd = _PLACEHOLDER.sub(lambda m: cmd_vals.get(m.group(1), ""), stage.command)
        return cmd, env

    def changes_for_layers(self, changes: dict[str, str], layers: set[str]) -> dict[str, str]:
        return {k: v for k, v in changes.items() if self.knobs[k].layer in layers}


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
