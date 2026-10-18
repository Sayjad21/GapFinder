"""Draft a harness spec from a repo: the one hand-written artifact, written by the model instead.

    gapfinder spec-draft <repo> --out spec.yaml [--paper-ledger runs/ledger] [--backend local|contree]

Steps (see `draft_spec`):
  1. gather inputs in plain code: the repo map (every flag with file:line), the build files, the
     README's usage section and, optionally, the paper's assumptions from a ledger directory;
  2. one Nemotron call (Super; Ultra once Super failed validation twice) drafts the spec;
  3. the draft is loaded through the real `HarnessSpec` loader. Schema errors go back to the model;
  4. a smoke test builds, loads and runs the artifact once on a sandbox backend and parses the
     metrics. A failure goes back to the model as a focused redraft, at most `max_attempts` times.

A person reads the YAML and approves it. Nothing here edits the artifact's code, and every model
call goes through the router, so the spend cap and the response cache apply as everywhere else.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from pydantic import BaseModel, Field, ValidationError

from gapfinder.ingest.repo_map import _KIND_RANK, RepoMap

MAX_FILE_CHARS = 3000  # per build file in the prompt
MAX_README_CHARS = 3500
MAX_LEDGER_CHARS = 5000
MAX_FLAGS_IN_PROMPT = 300

BUILD_FILE_GLOBS = ("setup.py", "requirements*.txt", "pyproject.toml", "CMakeLists.txt", "Makefile")
_USAGE_HEADING = re.compile(
    r"^(#{1,4})\s*.*\b(usage|quick\s*start|getting\s+started|running|how\s+to\s+run|example|reproduc\w*)\b.*$",
    re.IGNORECASE | re.MULTILINE,
)
# flag kinds that name a user-facing setting; env vars and make variables are noisier
_STRONG_KINDS = {"argparse", "gflags", "absl", "usage", "option_field", "cmake"}


def norm_name(name: str) -> str:
    """`--Batch-Size` and `batch_size` are the same knob."""
    return name.strip().lstrip("-").replace("-", "_").lower()


# ----------------------------------------------------------------------- inputs


@dataclass
class DraftContext:
    """Everything the model is allowed to see about the repo, already trimmed."""

    repo_name: str
    repo_path: Path
    flags_text: str
    flag_names: list[str]  # normalized names of the flags shown (and so expected in the spec)
    flags_total: int
    flags_shown: int
    build_files_text: str
    readme_usage: str
    paper_text: str = ""
    file_listing: str = ""

    def prompt_block(self) -> str:
        parts = [
            f"REPO: {self.repo_name}",
            f"FILES (top of tree):\n{self.file_listing}",
            f"FLAGS AND DEFAULTS (name = default @ file:line [kind]); {self.flags_shown} of {self.flags_total} shown:\n"
            f"{self.flags_text or '(none found)'}",
            f"BUILD FILES:\n{self.build_files_text or '(none found)'}",
            f"README USAGE SECTION:\n{self.readme_usage or '(none found)'}",
        ]
        if self.paper_text:
            parts.append(f"PAPER SETUP / ASSUMPTIONS (from the claim ledger):\n{self.paper_text}")
        return "\n\n".join(parts)


def readme_usage_section(readme: str, limit: int = MAX_README_CHARS) -> str:
    """The README section that explains how to run things; the top of the README if there is none."""
    if not readme.strip():
        return ""
    m = _USAGE_HEADING.search(readme)
    if not m:
        return readme[:limit]
    level = len(m.group(1))
    rest = readme[m.start():]
    # the section ends at the next heading of the same or a higher level
    nxt = re.search(rf"^#{{1,{level}}}\s", rest[len(m.group(0)):], re.MULTILINE)
    section = rest[: len(m.group(0)) + nxt.start()] if nxt else rest
    return section[:limit]


def _read_text(path: Path, limit: int) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")[:limit]
    except OSError:
        return ""


def build_files_text(root: Path, rm: RepoMap, limit: int = MAX_FILE_CHARS) -> str:
    """setup.py, requirements*.txt, pyproject.toml, CMakeLists.txt, Makefile: root first, then the map's."""
    seen: list[str] = []
    for pattern in BUILD_FILE_GLOBS:
        seen += [p.name for p in sorted(root.glob(pattern)) if p.is_file()]
    wanted = {"setup.py", "pyproject.toml", "CMakeLists.txt", "Makefile", "build.sh"}
    for rel in rm.build_files:
        if rel not in seen and Path(rel).name in wanted:
            seen.append(rel)
    chunks = []
    for rel in seen[:8]:
        body = _read_text(root / rel, limit)
        if body.strip():
            chunks.append(f"--- {rel} ---\n{body}")
    return "\n".join(chunks)


def paper_text_from_ledger(ledger_dir: str | Path, limit: int = MAX_LEDGER_CHARS) -> str:
    """The paper's own words about the setup: `paper_setup.txt` if present, then the assumptions' paper values."""
    d = Path(ledger_dir)
    out: list[str] = []
    setup = d / "paper_setup.txt"
    if setup.exists():
        out.append(_read_text(setup, limit))
    ap = d / "assumptions.json"
    if ap.exists():
        raw = json.loads(ap.read_text(encoding="utf-8"))
        for a in raw["assumptions"] if isinstance(raw, dict) else raw:
            quote = next((e["quote"] for e in a.get("evidence", []) if e.get("kind") == "paper"), "")
            line = (f"- {a['knob']} ({a.get('layer', '?')}): paper={a.get('paper_value')!r} "
                    f"code_default={a.get('code_default')!r}")
            out.append(line + (f'  "{quote[:200]}"' if quote else ""))
    return "\n".join(out)[:limit]


def gather_inputs(repo_map: RepoMap, *, paper_ledger: str | Path | None = None,
                  max_flags: int = MAX_FLAGS_IN_PROMPT) -> DraftContext:
    """Plain code, no model: turn a repo map (+ ledger) into the trimmed text the draft prompt carries."""
    # one line per flag name, preferring the definition over wrappers
    by_name: dict[str, object] = {}
    for f in repo_map.flags:
        key = norm_name(f.name)
        cur = by_name.get(key)
        if cur is None or _KIND_RANK.get(f.kind, 9) < _KIND_RANK.get(cur.kind, 9):
            by_name[key] = f
    flags = sorted(by_name.values(), key=lambda f: (f.kind not in _STRONG_KINDS, f.file, f.line))
    shown = flags[:max_flags]
    return DraftContext(
        repo_name=repo_map.root.name,
        repo_path=repo_map.root,
        flags_text="\n".join(f"{f.name} = {f.default}  @ {f.ref}  [{f.kind}]" for f in shown),
        flag_names=[norm_name(f.name) for f in shown],
        flags_total=len(flags),
        flags_shown=len(shown),
        build_files_text=build_files_text(repo_map.root, repo_map),
        readme_usage=readme_usage_section(repo_map.readme),
        paper_text=paper_text_from_ledger(paper_ledger) if paper_ledger else "",
        file_listing="\n".join(repo_map.files[:60]),
    )


# ------------------------------------------------------------------------ prompt

SPEC_PROMPT = """You write the harness spec for a research artifact. A harness spec is a small YAML that tells
an automated search how to build, load and run the artifact, and which settings (knobs) exist.
You are given the repo map (every flag with its default and file:line), build files, the README's
usage section and, when available, what the paper says about its setup. Never invent a flag: every
knob must come from the flags list, the README or the code you were shown.

Return ONE JSON object with these fields:

name: short lowercase identifier for the artifact.
base: "local:." for a repo that is run from its own checkout (almost always). Only give an image reference
  if the README says the artifact needs one.
build: {"command": ..., "timeout": seconds} or null if nothing needs building (plain Python scripts).
load: {"command": ..., "timeout": seconds} or null. The step that creates the dataset or database the
  benchmark reads, when it is separate from the run. null if the run script generates its own data.
run: {"command": ..., "output": ..., "format": ..., "timeout": seconds}. ONE naive run of the benchmark with
  the repo's default settings. "output" is a file path relative to the repo root that the run writes the
  metrics to (make the command write it, e.g. `--out out/result.json` or `> out/run.log`), or "stdout".
  "format" is how the metrics are printed: "kv" (lines `name: 1.23`), "jsonl" (JSON objects on a line each,
  numeric fields are the metrics), "db_bench" (RocksDB db_bench output) or "auto".
knobs: an object with an entry for EVERY flag in the flags list that a person could change to get a
  different result (skip pure debugging and output-path flags only if they can't change a measurement, and
  say so in "notes"). Each entry: {"layer": ..., "default": ..., "env": false, "source": "file:line"}.
  - The knob name is the flag name without leading dashes, with hyphens turned into underscores, unless it
    is an environment variable, which keeps its name and gets "env": true.
  - "default" is the value the code uses when the flag is not given, written as a string ("1.0", "true").
    For a switch that is off by default use "". The command then contains the placeholder where the switch
    belongs, and a knob value "--crash" would turn it on.
  - "layer" is where a change takes effect: "build" (needs a rebuild), "dataset" (needs the data reloaded),
    "config" (a run-time setting), "workload" (what the benchmark asks of the system), "environment"
    (environment variables, hardware, OS limits).
  - "source" is the file:line of the declaration, copied from the flags list.
Every knob must appear as a {placeholder} in the build, load or run command (or have "env": true). Write
each command with placeholders in the place where its value goes, e.g.
  python3 bench.py --alpha {alpha} --beta {beta}
Use "${PYTHON:-python3}" (in double quotes) instead of a bare python. Commands run with `bash -c` in a copy
of the repo at the working directory, files are relative to it, no network is available, and no processes
survive from one stage to the next: state must be on disk. A placeholder is a knob name in braces; do not
use braces for anything else (use $VAR or ${VAR} for shell variables).
allowed_paths: the repo-relative paths a configuration change may touch ("out/", "configs/"); anything else is
  algorithm code. Never list source files.
metrics: the names of the numbers the run reports, exactly as the parser will produce them (for "kv" the
  left-hand names, for "jsonl" the JSON keys). Leave [] if you cannot tell.
notes: one or two sentences on what you were unsure about.

Keep commands short and runnable as given. Prefer the smallest faithful default run (the repo's own default
sizes), not a scaled-down one."""

REDRAFT_PROMPT = """The draft was not accepted.

{kind}:
{errors}

Fix exactly these problems and return the complete corrected JSON object (same schema, all fields).
Change nothing that was not a problem. Do not remove knobs to make an error go away; fix the command so each
knob is used."""

_VALID_FORMATS = {"kv", "jsonl", "db_bench", "auto"}
_VALID_LAYERS = {"build", "dataset", "config", "workload", "environment"}

# ---------------------------------------------------------------- draft schema


class DraftStage(BaseModel):
    command: str
    timeout: float | None = None


class DraftRun(BaseModel):
    command: str
    output: str = "stdout"
    format: str = "auto"
    timeout: float | None = None


class DraftKnob(BaseModel):
    layer: str
    default: str | int | float | bool | None = ""
    env: bool = False
    source: str | None = Field(default=None, description="file:line of the declaration")


class SpecDraft(BaseModel):
    """What the model returns. Looser than HarnessSpec on purpose (defaults may be numbers); the real
    loader is what accepts or rejects the result."""

    name: str
    base: str = "local:."
    build: DraftStage | None = None
    load: DraftStage | None = None
    run: DraftRun
    knobs: dict[str, DraftKnob] = Field(default_factory=dict)
    allowed_paths: list[str] = Field(default_factory=list)
    metrics: list[str] = Field(default_factory=list)
    notes: str = ""


def _str_default(v) -> str:
    if v is None:
        return ""
    if isinstance(v, bool):
        return "true" if v else "false"
    return str(v)


def draft_to_dict(draft: SpecDraft, repo_path: Path) -> dict:
    """The YAML-ready spec dict. The repo checkout is the base unless the model named an image."""
    base = draft.base.strip()
    if base in ("", ".") or base.startswith("local:"):
        base = "local:" + Path(repo_path).resolve().as_posix()
    out: dict = {"name": re.sub(r"[^\w.-]", "-", draft.name.strip()) or "artifact", "base": base}
    for stage_name in ("build", "load"):
        stage = getattr(draft, stage_name)
        if stage and stage.command.strip():
            out[stage_name] = {"command": stage.command.strip()}
            if stage.timeout:
                out[stage_name]["timeout"] = stage.timeout
    run = {"command": draft.run.command.strip(), "output": draft.run.output.strip() or "stdout",
           "format": draft.run.format.strip() or "auto"}
    if draft.run.timeout:
        run["timeout"] = draft.run.timeout
    out["run"] = run
    knobs = {}
    for name, k in draft.knobs.items():
        knobs[name] = {"layer": k.layer.strip().lower(), "default": _str_default(k.default)}
        if k.env:
            knobs[name]["env"] = True
    out["knobs"] = knobs
    out["allowed_paths"] = list(draft.allowed_paths)
    out["metrics"] = list(draft.metrics)
    return out


# ------------------------------------------------------------------ validation


@dataclass
class Validation:
    spec: object | None  # a HarnessSpec when valid
    errors: list[str]
    warnings: list[str]

    @property
    def ok(self) -> bool:
        return self.spec is not None and not self.errors


def validate_draft(draft: SpecDraft, ctx: DraftContext | None = None) -> Validation:
    """Load the draft through the real spec loader, then check what the loader doesn't: every knob
    is used, defaults render, and (a warning, not an error) which repo-map flags are not knobs."""
    import tempfile

    import yaml

    from gapfinder.sandbox.spec import HarnessSpec, _placeholders

    data = draft_to_dict(draft, ctx.repo_path if ctx else Path("."))
    errors: list[str] = []
    warnings: list[str] = []
    if data["run"]["format"] not in _VALID_FORMATS:
        errors.append(f"run.format {data['run']['format']!r} is not one of {sorted(_VALID_FORMATS)}")
    for name, k in data["knobs"].items():
        if k["layer"] not in _VALID_LAYERS:
            errors.append(f"knob {name!r}: layer {k['layer']!r} is not one of {sorted(_VALID_LAYERS)}")
        if not re.fullmatch(r"\w+", name):
            errors.append(f"knob name {name!r} must be letters, digits and underscores only (it is a {{placeholder}})")
    spec = None
    if not errors:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "spec.yaml"
            path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
            try:
                spec = HarnessSpec.load_yaml(path)
            except (ValidationError, ValueError, KeyError, yaml.YAMLError) as exc:
                errors.append(f"spec loader: {str(exc)[:1200]}")
    if spec is not None:
        used: set[str] = set()
        for stage in (spec.build, spec.load, spec.run):
            if stage:
                used |= _placeholders(stage.command)
        for name, knob in spec.knobs.items():
            if not knob.env and name not in used:
                errors.append(f"knob {name!r} is not used in any command (put {{{name}}} where its value goes, "
                              "or set env: true)")
        for stage_name in ("build", "load", "run"):
            stage = getattr(spec, stage_name)
            if stage:
                try:
                    spec.render(stage, {})
                except ValueError as exc:
                    errors.append(f"{stage_name}: {exc}")
    if ctx is not None and not errors:
        have = {norm_name(k) for k in draft.knobs}
        missing = [n for n in ctx.flag_names if n not in have]
        if missing:
            warnings.append(f"{len(missing)} repo-map flags are not knobs: {', '.join(missing[:40])}")
    return Validation(spec if not errors else None, errors, warnings)


# ------------------------------------------------------------- the model call


async def request_draft(router, tier: str, messages: list[dict]) -> tuple[SpecDraft | None, str, str | None]:
    """One router call. Returns (draft, raw_answer, parse_error). Spend cap, cache and retries are the
    router's; a budget error propagates instead of being swallowed."""
    from gapfinder.models.router import BadJSONError, EmptyAnswerError, extract_json

    try:
        _, answer, _ = await router.complete(tier, messages, schema=SpecDraft.model_json_schema())
    except EmptyAnswerError as exc:
        return None, "", f"the model returned no answer ({exc})"
    try:
        return SpecDraft.model_validate(extract_json(answer)), answer, None
    except (BadJSONError, EmptyAnswerError) as exc:
        return None, answer, f"the answer was not a JSON object: {str(exc)[:300]}"
    except ValidationError as exc:
        return None, answer, f"the JSON does not match the draft schema: {str(exc)[:1200]}"


# ------------------------------------------------------------------- smoke test

SMOKE_TIMEOUT_S = 900  # cap on each stage during the smoke test, whatever the draft asked for


@dataclass
class SmokeResult:
    ok: bool
    stage: str  # build | load | run | parse | ok
    error: str = ""
    command: str = ""
    metrics: dict[str, float] | None = None
    sandbox_usd: float = 0.0
    elapsed_s: float = 0.0
    infra: bool = False  # sandbox trouble: a different draft would not help
    metrics2: dict[str, float] | None = None  # a second run (another RUN_TAG): do seeds vary?
    max_rss_kb: int = 0
    run_s: float = 0.0  # the run stage alone


async def smoke_test(spec, backend, *, stage_timeout: float = SMOKE_TIMEOUT_S, repeat: bool = False) -> SmokeResult:
    """Build, load and run the artifact once with its default settings, and parse the metrics.

    This is the orchestrator's own `run_branch({})`, so the drafted spec is exercised exactly the way the
    search will use it (same rendering, same parser, values must appear in the raw log)."""
    import tempfile
    import time

    from gapfinder.sandbox.backend import InfraError
    from gapfinder.sandbox.events import EventLog
    from gapfinder.sandbox.runner import Orchestrator

    spec = spec.model_copy(deep=True)
    spec.metrics = []  # parse everything the run prints; the caller compares it with the declared metrics
    for stage in (spec.build, spec.load, spec.run):
        if stage is not None:
            stage.timeout = min(stage.timeout, stage_timeout)
    start = time.monotonic()
    with tempfile.TemporaryDirectory() as tmp:
        orch = Orchestrator(backend, spec, EventLog(Path(tmp) / "events.jsonl"), infra_retries=1)
        try:
            branch = await orch.run_branch({}, label="smoke")
        except InfraError as exc:
            return SmokeResult(False, "run", f"sandbox error: {exc}", infra=True, elapsed_s=time.monotonic() - start)
        except RuntimeError as exc:  # a build or load stage failed ("built failed (exit 2): ...")
            text = str(exc)
            stage = "load" if text.startswith("loaded") else "build"
            cmd = (spec.load if stage == "load" else spec.build).command
            return SmokeResult(False, stage, text[-2500:], command=cmd, sandbox_usd=orch.cost.sandbox_usd,
                               elapsed_s=time.monotonic() - start)
        second = None
        if repeat and branch.status == "succeeded":  # same checkpoints, another RUN_TAG: is there run-to-run noise?
            try:
                b2 = await orch.run_branch({}, label="smoke-2")
                second = dict(b2.parsed_metrics) if b2.status == "succeeded" else None
            except (InfraError, RuntimeError):
                second = None
    elapsed = time.monotonic() - start
    usd = orch.cost.sandbox_usd
    if branch.status == "timed_out":
        return SmokeResult(False, "run", f"the run did not finish within {spec.run.timeout:.0f}s",
                           command=branch.command, sandbox_usd=usd, elapsed_s=elapsed)
    if branch.status == "infra_error":
        return SmokeResult(False, "run", f"sandbox error: {branch.note}", command=branch.command, sandbox_usd=usd,
                           elapsed_s=elapsed, infra=True)
    if branch.status != "succeeded":
        stage = "run" if branch.exit_code else "parse"
        return SmokeResult(False, stage, str(branch.note or "")[-2500:], command=branch.command, sandbox_usd=usd,
                           elapsed_s=elapsed)
    return SmokeResult(True, "ok", command=branch.command, metrics=dict(branch.parsed_metrics),
                       sandbox_usd=orch.cost.sandbox_usd, elapsed_s=elapsed, metrics2=second,
                       max_rss_kb=branch.resources.max_rss_kb, run_s=branch.resources.elapsed_s)


SANDBOX_RAM_KB = 3_900_000  # a Sandboxes VM
SANDBOX_MAX_S = 3600


def self_checks(smoke: SmokeResult) -> tuple[list[str], list[str]]:
    """(problems worth one redraft, warnings) after a smoke run that passed."""
    problems, warnings = [], []
    if smoke.metrics2 is not None and smoke.metrics and smoke.metrics2 == smoke.metrics:
        problems.append("two runs with different $RUN_TAG printed identical metrics, so the search would see no "
                        "run-to-run noise. If the program has a seed flag, set it from $RUN_TAG in the run command, "
                        'e.g. --seed $(( $(printf %s "$RUN_TAG" | cksum | cut -d" " -f1) % 100000 )); if it has none, '
                        "leave the command as it is.")
    if smoke.max_rss_kb > 0.9 * SANDBOX_RAM_KB:
        warnings.append(f"the run peaked at {smoke.max_rss_kb / 1e6:.1f} GB of the VM's 3.9 GB: lower its parallelism")
    if smoke.run_s > 0.8 * SANDBOX_MAX_S:
        warnings.append(f"the run took {smoke.run_s:.0f} s of the 3600 s limit: a larger setting will not fit")
    return problems, warnings


# ------------------------------------------------------------- the redraft loop

MAX_INVALID_DRAFTS = 4  # drafts that fail validation, over the whole run (Super, Super, then Ultra twice)


@dataclass
class Attempt:
    n: int
    tier: str
    stage: str  # schema | build | load | run | parse | ok
    errors: list[str]
    smoke: bool  # False when the draft never reached the smoke test
    cost_usd: float = 0.0


@dataclass
class DraftResult:
    ok: bool  # the final spec passed validation and the smoke test
    spec_dict: dict | None  # the last draft that validated (also when its smoke test failed)
    attempts: list[Attempt]
    warnings: list[str]
    knobs_found: list[str]
    metrics_found: list[str]
    notes: str
    cost_usd: float  # Nemotron, as billed (cache hits are free)
    fresh_cost_usd: float  # what the same calls cost without the cache
    sandbox_usd: float
    flags_total: int
    flags_shown: int
    backend: str
    gave_up: str = ""  # why, when no usable spec came out

    @property
    def smoke_attempts(self) -> int:
        return sum(a.smoke for a in self.attempts)


def _feedback(kind: str, errors: list[str]) -> dict:
    return {"role": "user", "content": REDRAFT_PROMPT.format(kind=kind, errors="\n".join(f"- {e}" for e in errors))}


def _smoke_feedback(smoke: SmokeResult) -> dict:
    what = {"build": "the build command failed", "load": "the load command failed",
            "run": "the run command failed", "parse": "the run finished but no metrics could be parsed from its output"}
    kind = f"The draft is valid YAML but failed its smoke test: {what.get(smoke.stage, smoke.stage)}"
    detail = f"command: {smoke.command}\n{smoke.error}" if smoke.command else smoke.error
    return _feedback(kind, [detail])


async def draft_spec(router, ctx: DraftContext, backend, *, max_attempts: int = 3, smoke: bool = True,
                     smoke_timeout: float = SMOKE_TIMEOUT_S, self_check: bool = False) -> DraftResult:
    """Draft, validate, smoke-test, redraft. At most `max_attempts` drafts get a smoke test; drafts that
    fail validation are fed their errors and don't use one of those (but are capped overall).

    `self_check`: a passing smoke test is run a second time with another RUN_TAG, and the run's memory and time
    are compared with a Sandboxes VM. Identical metrics (no run-to-run noise) get one redraft; the limits are
    warnings."""
    messages: list[dict] = [{"role": "system", "content": SPEC_PROMPT},
                            {"role": "user", "content": ctx.prompt_block()}]
    attempts: list[Attempt] = []
    invalid = 0
    sandbox_usd = 0.0
    last_valid: tuple[SpecDraft, Validation] | None = None
    last_smoke: SmokeResult | None = None
    gave_up = ""
    spent_before = router.meter.total_cost()
    self_checked = False
    check_warnings: list[str] = []

    def _cost() -> float:
        return router.meter.total_cost()

    n = 0
    while sum(a.smoke for a in attempts) < max_attempts:
        n += 1
        tier = "ultra" if invalid >= 2 else "super"  # Ultra once Super failed validation twice
        before = _cost()
        draft, raw, parse_error = await request_draft(router, tier, messages)
        problems: list[str] = []
        validation: Validation | None = None
        if parse_error:
            problems = [parse_error]
        else:
            validation = validate_draft(draft, ctx)
            problems = validation.errors
        if problems:
            invalid += 1
            attempts.append(Attempt(n, tier, "schema", problems, False, _cost() - before))
            if invalid >= MAX_INVALID_DRAFTS:
                gave_up = f"{invalid} drafts failed validation; last errors: {problems[0][:300]}"
                break
            messages += [{"role": "assistant", "content": raw or "(no answer)"},
                         _feedback("The draft failed validation", problems)]
            continue

        last_valid = (draft, validation)
        if not smoke:
            attempts.append(Attempt(n, tier, "ok", [], False, _cost() - before))
            break
        result = await smoke_test(validation.spec, backend, stage_timeout=smoke_timeout, repeat=self_check)
        last_smoke = result
        sandbox_usd += result.sandbox_usd
        missing = []
        if result.ok and validation.spec.metrics:
            missing = [m for m in validation.spec.metrics if m not in (result.metrics or {})]
        if result.ok and not missing:
            problems, notes = self_checks(result)
            check_warnings[:] = notes
            if problems and not self_checked and sum(a.smoke for a in attempts) + 1 < max_attempts:
                self_checked = True  # one redraft for a self-check; after that the draft stands, with a warning
                attempts.append(Attempt(n, tier, "self-check", problems, True, _cost() - before))
                messages += [{"role": "assistant", "content": raw},
                             _feedback("The draft runs, but a self-check failed", problems)]
                continue
            check_warnings.extend(problems)
            attempts.append(Attempt(n, tier, "ok", [], True, _cost() - before))
            break
        if result.ok:  # ran, but the declared metrics aren't in the output: a parse problem
            result = SmokeResult(False, "parse", f"declared metrics {missing} were not found; the output "
                                 f"contains {sorted(result.metrics or {})}", command=result.command)
            last_smoke = result
        attempts.append(Attempt(n, tier, result.stage, [result.error[-600:]], True, _cost() - before))
        if result.infra:
            gave_up = f"sandbox trouble, not a spec problem: {result.error[:300]}"
            break
        messages += [{"role": "assistant", "content": raw}, _smoke_feedback(result)]

    ok = bool(attempts) and attempts[-1].stage == "ok"
    if not ok and not gave_up:
        err = attempts[-1].errors[0][:300] if attempts and attempts[-1].errors else ""
        gave_up = f"no spec passed the smoke test in {max_attempts} attempts; last failure at stage " \
                  f"{attempts[-1].stage if attempts else '?'}: {err}"
    spec_dict = None
    warnings: list[str] = []
    if last_valid:
        draft, validation = last_valid
        spec_dict = draft_to_dict(draft, ctx.repo_path)
        warnings = list(validation.warnings) + check_warnings
        if ok and last_smoke and last_smoke.metrics and not spec_dict["metrics"]:
            spec_dict["metrics"] = sorted(last_smoke.metrics)  # the model couldn't tell; the run did
    meter = router.meter
    return DraftResult(
        ok=ok, spec_dict=spec_dict, attempts=attempts, warnings=warnings,
        knobs_found=list(spec_dict["knobs"]) if spec_dict else [],
        metrics_found=sorted(last_smoke.metrics) if last_smoke and last_smoke.metrics else [],
        notes=last_valid[0].notes if last_valid else "",
        cost_usd=_cost() - spent_before, fresh_cost_usd=meter.total_fresh_cost(), sandbox_usd=sandbox_usd,
        flags_total=ctx.flags_total, flags_shown=ctx.flags_shown,
        backend=getattr(backend, "name", "?") if smoke else "none", gave_up="" if ok else gave_up,
    )


# ----------------------------------------------------------------------- output

YAML_HEADER = """# Harness spec drafted by `gapfinder spec-draft`. A person must read and approve it before a search uses it.
# base is the repo checkout; knob defaults come from the code (see the draft report for file:line).
"""


def spec_yaml(spec_dict: dict, out_path: str | Path) -> str:
    """YAML text for `spec_dict`, with a local base written relative to the spec file when it can be."""
    import os

    import yaml

    d = dict(spec_dict)
    base = d["base"]
    if base.startswith("local:"):
        try:
            rel = os.path.relpath(base[6:], Path(out_path).resolve().parent)
            d["base"] = "local:" + Path(rel).as_posix()
        except ValueError:  # another drive on Windows: keep the absolute path
            pass
    return YAML_HEADER + yaml.safe_dump(d, sort_keys=False, width=120)


def write_spec(result: DraftResult, out_path: str | Path) -> Path | None:
    """Write the drafted YAML (also when the smoke test failed: a person may only need to fix one line)."""
    if result.spec_dict is None:
        return None
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(spec_yaml(result.spec_dict, out), encoding="utf-8")
    return out


# --------------------------------------------------------- compare, report, diff


@dataclass
class KnobComparison:
    """Knob recall of a drafted spec against a hand-written one (P1-0, item 2)."""

    hand_name: str
    found: list[str]  # hand-written knobs the draft also has
    missing: list[str]  # hand-written knobs the draft lacks
    extra: list[str]  # draft knobs the hand-written spec lacks
    default_match: int  # of `found`, how many have the same default
    layer_match: int  # of `found`, how many have the same layer
    default_diffs: dict[str, tuple[str, str]]  # knob -> (hand default, draft default)
    layer_diffs: dict[str, tuple[str, str]]

    @property
    def recall(self) -> float:
        total = len(self.found) + len(self.missing)
        return len(self.found) / total if total else 1.0

    def to_dict(self) -> dict:
        return {"hand": self.hand_name, "recall": round(self.recall, 4), "found": self.found,
                "missing": self.missing, "extra": self.extra, "default_match": self.default_match,
                "layer_match": self.layer_match, "default_diffs": self.default_diffs,
                "layer_diffs": self.layer_diffs}


def _hand_knobs(hand_yaml: str | Path) -> tuple[str, dict[str, dict]]:
    import yaml

    data = yaml.safe_load(Path(hand_yaml).read_text(encoding="utf-8"))
    return str(data.get("name", Path(hand_yaml).stem)), {k: dict(v) for k, v in (data.get("knobs") or {}).items()}


def compare_knobs(draft_knobs: dict[str, dict], hand_yaml: str | Path) -> KnobComparison:
    """Match knobs by normalized name (`--Batch-Size` = `batch_size`). Defaults compare as strings."""
    hand_name, hand = _hand_knobs(hand_yaml)
    draft_by = {norm_name(k): (k, v) for k, v in draft_knobs.items()}
    hand_by = {norm_name(k): (k, v) for k, v in hand.items()}
    found = [hand_by[n][0] for n in hand_by if n in draft_by]
    missing = [hand_by[n][0] for n in hand_by if n not in draft_by]
    extra = [draft_by[n][0] for n in draft_by if n not in hand_by]
    ddiff: dict[str, tuple[str, str]] = {}
    ldiff: dict[str, tuple[str, str]] = {}
    for n in hand_by:
        if n not in draft_by:
            continue
        hk, hv = hand_by[n]
        _, dv = draft_by[n]
        h_def, d_def = _str_default(hv.get("default")), _str_default(dv.get("default"))
        if h_def != d_def:
            ddiff[hk] = (h_def, d_def)
        if str(hv.get("layer")) != str(dv.get("layer")):
            ldiff[hk] = (str(hv.get("layer")), str(dv.get("layer")))
    return KnobComparison(hand_name, found, missing, extra, len(found) - len(ddiff), len(found) - len(ldiff),
                          ddiff, ldiff)


def report_markdown(result: DraftResult, spec_path: str | Path | None = None,
                    comparison: KnobComparison | None = None) -> str:
    """The short human-readable account of what spec-draft tried."""
    status = "verified: the spec built, ran and parsed its metrics" if result.ok else f"NOT verified: {result.gave_up}"
    lines = [f"# Spec draft report{f' for {Path(spec_path).name}' if spec_path else ''}", "",
             f"**Status:** {status}", "",
             f"- backend: {result.backend}; attempts with a smoke test: {result.smoke_attempts}; "
             f"model calls: {len(result.attempts)}",
             f"- Nemotron cost: ${result.cost_usd:.4f} billed, ${result.fresh_cost_usd:.4f} without the cache; "
             f"sandbox cost reported: ${result.sandbox_usd:.4f}",
             f"- knobs in the spec: {len(result.knobs_found)}; repo-map flags shown to the model: "
             f"{result.flags_shown} of {result.flags_total}", "",
             "## Attempts", "", "| # | tier | stage | cost | what happened |", "|---|---|---|---|---|"]
    for a in result.attempts:
        what = "ok" if a.stage == "ok" else " ".join(a.errors).replace("\n", " ").replace("|", "/")[:240]
        lines.append(f"| {a.n} | {a.tier} | {a.stage} | ${a.cost_usd:.4f} | {what} |")
    if result.metrics_found:
        lines += ["", "## Metrics parsed by the smoke test", "", ", ".join(result.metrics_found)]
    if result.spec_dict:
        lines += ["", "## Knobs", "", "| knob | layer | default | env |", "|---|---|---|---|"]
        for name, k in result.spec_dict["knobs"].items():
            lines.append(f"| {name} | {k['layer']} | `{k['default']}` | {'yes' if k.get('env') else ''} |")
    if result.warnings:
        lines += ["", "## Warnings", ""] + [f"- {w}" for w in result.warnings]
    if result.notes:
        lines += ["", "## The model's own uncertainty", "", result.notes]
    if comparison:
        c = comparison
        lines += ["", f"## Knob recall against the hand-written spec ({c.hand_name})", "",
                  f"- recall: {len(c.found)}/{len(c.found) + len(c.missing)} = {c.recall:.0%}",
                  f"- found: {', '.join(c.found) or '(none)'}",
                  f"- missing: {', '.join(c.missing) or '(none)'}",
                  f"- extra (in the draft only): {', '.join(c.extra) or '(none)'}",
                  f"- same default: {c.default_match}/{len(c.found)}; same layer: {c.layer_match}/{len(c.found)}"]
        for k, (h, d) in c.default_diffs.items():
            lines.append(f"  - default of {k}: hand `{h}`, draft `{d}`")
        for k, (h, d) in c.layer_diffs.items():
            lines.append(f"  - layer of {k}: hand {h}, draft {d}")
    lines += ["", "## For the person approving", "",
              "Read the commands and knob defaults against the repo, then use the spec. "
              "`gapfinder spec-draft --diff draft.yaml edited.yaml` shows what you changed."]
    return "\n".join(lines) + "\n"


def write_report(result: DraftResult, out_path: str | Path, comparison: KnobComparison | None = None) -> Path:
    """`<spec>.md` next to the spec."""
    md = Path(out_path).with_suffix(".md")
    md.parent.mkdir(parents=True, exist_ok=True)
    md.write_text(report_markdown(result, out_path, comparison), encoding="utf-8")
    return md


def diff_specs(draft_yaml: str | Path, edited_yaml: str | Path) -> str:
    """A unified diff of two specs after normalizing (comments, key order and quoting don't count)."""
    import difflib

    import yaml

    def norm(p):
        data = yaml.safe_load(Path(p).read_text(encoding="utf-8"))
        return yaml.safe_dump(data, sort_keys=True, width=100).splitlines(keepends=True)

    diff = list(difflib.unified_diff(norm(draft_yaml), norm(edited_yaml), str(draft_yaml), str(edited_yaml)))
    return "".join(diff) if diff else "no differences\n"
