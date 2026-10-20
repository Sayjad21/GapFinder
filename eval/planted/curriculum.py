"""A progressive planted-gap curriculum on papers GapFinder already reproduces (plan D7.4, docs/CONTEXT_v11.md 7.3).

    python eval/planted/curriculum.py make   --level 1 --cases pygcn,fastgcn,b3a --per-case 2 --seed 1
    python eval/planted/curriculum.py search --level 1 --code <frozen worktree> [--parallel 3]
    python eval/planted/curriculum.py score  [--level 1]
    python eval/planted/curriculum.py run    --cases ... --code <frozen worktree>     # levels in turn, gated

Each task is a real paper's container and harness with hidden changes: the "paper's" numbers are the mean of runs
with them, the reproduction runs without. GapFinder searches with the case's spec and the task's targets, no paper
and no ledger (`--hypotheses repomap`, no model call). Causes are drawn by a seeded generator before any search,
from the families below; the answers are sealed (eval/planted/curriculum/sealed/) and read only by `score`.

Levels (each mixes in gap-free controls, about one task in five):
1. one clear cause (>= 5 pooled standard deviations; a draw between 3 and 5 is banked as a level-2 task): a setting,
   a scale or unit convention, a code defect, a data-pipeline defect, and on a rebuilt harness (`<case>-h`:
   eval/planted/rebuild_harnesses.py) a reporting rule (each metric's best epoch), the paper-era code, or a package
   release from the paper's time;
2. one subtle cause (3 to 5 standard deviations), the same families;
3. two causes of one family, each moving the target by >= 2 standard deviations alone, the gap closed only by both;
4. two causes of different families (a setting and a code defect, a scale convention and a data defect, ...);
5. adversarial: a cause outside every family GapFinder searches (a string choice in the code: `relu` -> `tanh`,
   `mean` -> `sum`), alone (the right answer is to say it can't explain it) or with a setting (the right answer is
   the setting and "partially explained"); and gap-free controls.
A level opens only when the previous one reaches `--pass` correct (0.7) with no confidently wrong answer.

Verdicts: correct (every planted part found), partial (some), missed, confidently wrong (Explained, Paper-artifact
inconsistency or a reporting rule without the planted parts; for a control or an outside cause, any of those).
These are development measurements: the builder knows every family. They are never blind evidence, and no change
is judged on a planted task (a failure counts when its family keeps failing on fresh draws).
"""

from __future__ import annotations

import argparse
import asyncio
import json
import math
import os
import random
import statistics
import subprocess
import sys
from pathlib import Path

HERE_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE_ROOT))
import plant  # noqa: E402  (the draws, the scorer's matching)

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(os.environ.get("GF_CURRICULUM_DIR") or HERE_ROOT / "curriculum")
TASKS, SEALED, WORK = HERE / "tasks", HERE / "sealed", HERE / "work"
SCRATCH = os.environ.get("GF_SCRATCH", "")
EXT = ROOT / "eval" / "external"
CASES = {  # name -> (spec, a recorded run whose events hold the base checkpoint and the local source)
    "pygcn": ("devset/pygcn/pygcn.yaml", "devset/pygcn/run"),
    "fastgcn": ("blind-1/fastgcn.yaml", "blind-1/run"),
    "b3a": ("batch3/b3a/b3a.yaml", "batch3/b3a/run"),
    "b3c": ("batch3/b3c/b3c.yaml", "batch3/b3c/run"),
    "b4a": ("batch4/b4a/b4a.yaml", "batch4/b4a/run"),
    "vgae": ("devset/vgae/vgae.yaml", "devset/vgae/run"),
}
CONFIDENT = ("Explained", "Paper-artifact inconsistency", "Explained by the reporting rule")
LEVELS = {
    1: {"families": ["setting", "scale", "code", "data", "reporting", "era", "library"], "causes": 1, "min_sd": 5.0,
        "max_sd": None},
    2: {"families": ["setting", "scale", "code", "data", "reporting", "era", "library"], "causes": 1, "min_sd": 3.0,
        "max_sd": 5.0},
    3: {"families": ["setting", "code"], "causes": 2, "same": True, "min_sd": 5.0, "each_sd": 2.0},
    4: {"families": ["setting", "scale", "code", "data"], "causes": 2, "same": False, "min_sd": 5.0, "each_sd": 2.0},
    5: {"families": ["outside", "outside+setting"], "causes": 1, "min_sd": 5.0},
}
# string choices a program makes that no GapFinder family searches (they are neither flags nor numbers)
ACTIVATIONS = {"relu", "elu", "tanh", "sigmoid", "leaky_relu", "selu", "softplus"}
# the families only a rebuilt harness (`<case>-h`) can plant: a `<case>-h` draws from these alone, so its tasks are
# the ones the hand harness can't make; the hand harness draws the others
HARNESS_FAMILIES = {"reporting", "era", "library"}
CHOICE_GROUPS = [{"relu", "tanh", "elu", "sigmoid", "gelu", "leaky_relu", "selu"}, {"mean", "sum", "max", "add"},
                 {"adam", "sgd", "adagrad", "rmsprop", "adamw"}, {"both", "right", "left", "none"},
                 {"xavier", "kaiming", "normal", "uniform", "orthogonal"}, {"l1", "l2", "max"}]


# ------------------------------------------------------------------ the case's container

def case_env(name: str) -> dict[str, str]:
    """GF_DEV_BASE and GF_DEV_SOURCE from the case's recorded run (the checkpoint its spec ran on)."""
    spec_rel, run_rel = CASES[name]
    ev = EXT / run_rel / "events.jsonl"
    for line in ev.read_text(encoding="utf-8").splitlines():
        d = json.loads(line)
        if d.get("type") == "run_started":
            s = d["spec"]
            src = (s.get("source") or "").replace("<scratch>", SCRATCH).replace("\\", "/")
            return {"GF_DEV_BASE": s["base"], "GF_DEV_SOURCE": src}
    raise SystemExit(f"{name}: no run_started event in {ev}")


def rebuilt(name: str) -> Path | None:
    """`<case>-h`: the case's harness rebuilt by `gapfinder harness` (eval/planted/rebuild_harnesses.py), whose spec
    has per-epoch values, the paper-year packages and the paper-era commit (the reporting, library and era families)."""
    if not name.endswith("-h"):
        return None
    p = HERE / "harness" / name[:-2] / "spec.yaml"
    return p if p.exists() else None


def resolved_spec(name: str) -> Path:
    """The case's spec with the recorded base checkpoint and local source written in (specs name their variables
    differently: GF_DEV_BASE, GF_B1_BASE, ...)."""
    import yaml

    if (h := rebuilt(name)) is not None:
        return h  # its base and source are written in already
    spec_rel, _ = CASES[name]
    d = yaml.safe_load((EXT / spec_rel).read_text(encoding="utf-8"))
    e = case_env(name)
    d["base"], d["source"] = e["GF_DEV_BASE"], e["GF_DEV_SOURCE"]
    out = WORK / "specs" / f"{name}.yaml"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(yaml.safe_dump(d, sort_keys=False, width=400), encoding="utf-8")
    return out


def load_case(name: str):
    from gapfinder.sandbox.spec import HarnessSpec

    p = resolved_spec(name)
    spec = HarnessSpec.load_yaml(p)
    if rebuilt(name) is not None:
        targets = json.loads((p.parent / "targets.json").read_text(encoding="utf-8"))
    else:
        spec_rel, _ = CASES[name]
        targets = json.loads(((EXT / spec_rel).parent / "targets.json").read_text(encoding="utf-8"))
    return spec, targets, p


# ------------------------------------------------------------------ the families

def draw_data(rng: random.Random, root: Path, spec) -> tuple[str, str, str] | None:
    from gapfinder.sandbox import ast_patch
    from gapfinder.search.mutation import find_mutants

    ms = [m for m in find_mutants(root, [k for k in spec.knobs if not k.startswith("@")], limit=400)
          if "data pipeline" in m.tags
          and not (ast_patch.entry_script(root / m.file) and not ast_patch.direct_entry(spec.run.command, m.file))]
    if not ms:
        return None
    m = rng.choice(ms)
    return "data", m.name, m.describe()


def draw_code_only(rng: random.Random, root: Path, spec) -> tuple[str, str, str] | None:
    """A code defect that is not a data-pipeline edit (those are their own family)."""
    for _ in range(30):
        c = plant.draw_code(rng, root, spec)
        if c is None:
            return None
        if "data pipeline" not in c[2]:
            return c
    return None


def draw_outside(rng: random.Random, root: Path, spec) -> tuple[str, str, str] | None:
    """A string choice in the code swapped for another of its kind (no GapFinder family changes strings)."""
    import ast

    from gapfinder.harness_auto import _import_closure
    from gapfinder.sandbox import ast_patch

    sites = []
    for p, tree in _import_closure(root.resolve()):
        if tree is None or not p.is_relative_to(root.resolve()):
            continue
        rel = p.relative_to(root.resolve()).as_posix()
        if ast_patch.entry_script(p) and not ast_patch.direct_entry(spec.run.command, rel):
            continue
        parents = {id(c): q for q in ast.walk(tree) for c in ast.iter_child_nodes(q)}
        for n in ast.walk(tree):
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr in ACTIVATIONS:
                # an activation called by name (F.relu, tf.nn.relu): renamed to another (GapFinder's operators rename
                # reductions only)
                sites.append((rel, n, sorted(ACTIVATIONS - {n.func.attr}), "call"))
                continue
            if isinstance(n, ast.Attribute) and n.attr in ACTIVATIONS and not (
                    isinstance(parents.get(id(n)), ast.Call) and parents[id(n)].func is n):
                # an activation passed as a value (act=tf.nn.relu): the reference replaced
                sites.append((rel, n, sorted(ACTIVATIONS - {n.attr}), "ref"))
                continue
            if not (isinstance(n, ast.Constant) and isinstance(n.value, str)):
                continue
            p = parents.get(id(n))
            if not (isinstance(p, ast.keyword) or (isinstance(p, ast.Call) and n in p.args)
                    or isinstance(p, (ast.Assign, ast.Compare))):
                continue  # a choice passed or assigned, not a message or a path
            v = n.value.lower()
            group = next((g for g in CHOICE_GROUPS if v in g), None)
            if group is None or n.value != v:
                continue
            sites.append((rel, n, sorted(group - {v}), "string"))
    if not sites:
        return None
    rel, n, others, how = rng.choice(sites)
    new = rng.choice(others)
    if how == "call":
        knob = f"@ast:{rel}:{n.lineno}:@mut.{n.col_offset}.Call.red.{new}"
        return "outside", knob, f"{rel}:{n.lineno}: {n.func.attr}() -> {new}()"
    if how == "ref":
        expr = ast.unparse(n.value) + "." + new
        knob = f"@ast:{rel}:{n.lineno}:@mut.{n.col_offset}.Attribute.{ast_patch.set_op(expr)}"
        return "outside", knob, f"{rel}:{n.lineno}: {ast.unparse(n)} -> {expr}"
    knob = f"@ast:{rel}:{n.lineno}:@mut.{n.col_offset}.Constant.{ast_patch.set_op(repr(new))}"
    return "outside", knob, f"{rel}:{n.lineno}: {n.value!r} -> {new!r}"


def draw_family(fam: str, rng, spec, root, flags, lits):
    """(family, knob, value, description, extra) for one cause of a family, or None."""
    if fam == "setting":
        c = plant.draw(rng, flags, lits)
        if c is None:
            return None
        kind, k, v = c
        return ("setting", k, v, f"{k} = {v}", {"literal": kind == "literal", "default": dict(lits).get(k)})
    if fam == "scale":
        c = plant.draw_scale(rng, flags)
        if c is None:
            return None
        _, k, factor = c
        d0 = spec.knobs[k].default
        return ("scale", k, plant._fmt_c(plant._num(d0) * factor, d0), f"{k}: the paper's v is the code's {factor:g} x v",
                {"factor": factor})
    if fam == "code":
        c = draw_code_only(rng, root, spec)
        return None if c is None else ("code", c[1], "1", c[2], {})
    if fam == "data":
        c = draw_data(rng, root, spec)
        return None if c is None else ("data", c[1], "1", c[2], {})
    if fam == "outside":
        c = draw_outside(rng, root, spec)
        return None if c is None else ("outside", c[1], "1", c[2], {})
    from gapfinder import env_year

    if fam == "era":  # the paper ran the repository's code as of its date; the reproduction runs a later commit
        if env_year.ERA_KNOB not in spec.knobs:
            return None
        return ("era", env_year.ERA_KNOB, "1", "the paper-era commit's code", {})
    if fam == "library":  # the paper ran package releases from its time: one, or all of them
        pins = (spec.library or {}).get("pins") or {}
        kn = spec.knobs.get(env_year.KNOB)
        values = [c for c in (kn.choices if kn else []) if c != "0"]
        if not pins or not values:
            return None
        v = rng.choice(values)
        dists = [d for d, x in pins.items() if v == "all" or x.get("dir", d) in v.split(",")]
        return ("library", env_year.KNOB, v,
                ", ".join(f"{d}=={pins[d]['old']}" for d in dists) + " (as of the paper's date)", {"dists": dists})
    if fam == "reporting":  # the paper reports each metric's best epoch (chosen on the test labels)
        if not any(m.endswith("__x_best") for m in spec.metrics):
            return None
        return ("reporting", "@reporting", "best", "each metric's best epoch, chosen with the test labels", {})
    raise ValueError(fam)


# ------------------------------------------------------------------ making tasks

API_HOST = "api.tokenfactory.nebius.com"


def _online() -> bool:
    import socket

    try:
        socket.getaddrinfo(API_HOST, 443)
        return True
    except OSError:
        return False


async def _wait_online(name: str) -> None:
    """A run started while the machine is offline fails at once (2026-10-21: DNS gone for several minutes; a
    whole case's draws failed in a row): wait for the Sandboxes API's name to resolve."""
    if _online():
        return
    print(f"  {name}: offline; waiting", flush=True)
    while not _online():
        await asyncio.sleep(30)


def _infra(runs) -> bool:
    """Every run of a draw ended in a Sandboxes or network error: the draw was never measured."""
    return bool(runs) and all(str(getattr(b.status, "value", b.status)) == "infra_error" for b in runs)


def _band_ok(level: int, moved: float) -> bool:
    lv = LEVELS[level]
    return moved >= lv["min_sd"] and (lv.get("max_sd") is None or moved < lv["max_sd"])


def _made(level: int, name: str, seed: int) -> int:
    return len(list(TASKS.glob(f"L{level}-{name}-s{seed}-*"))) if TASKS.exists() else 0


def _next_tag(level: int, name: str, seed: int) -> str:
    """One past the highest task number of the level on the case (a removed task's number is not reused)."""
    nums = [int(d.name.rsplit("-", 1)[1]) for d in TASKS.glob(f"L{level}-{name}-s{seed}-*")
            if d.name.rsplit("-", 1)[1].isdigit()] if TASKS.exists() else []
    return f"L{level}-{name}-s{seed}-{max(nums, default=0) + 1}"


def _controls(name: str, seed: int, levels: list[int]) -> int:
    """Controls already made on the case at these levels (the maker's own bookkeeping; nothing is printed)."""
    n = 0
    for lv_ in levels:
        for f in SEALED.glob(f"L{lv_}-{name}-s{seed}-*.json") if SEALED.exists() else []:
            n += json.loads(f.read_text(encoding="utf-8")).get("kind") == "control"
    return n


async def make(level: int, cases: list[str], per_case: int, seed: int, repeats: int = 3, tries: int = 10,
               concurrency: int = 8, control_rate: float = 0.2, parallel: int = 3) -> None:
    """Tasks for `level` on each case, `parallel` cases at a time. The single-cause levels (1 and 2) share one
    stream of draws: each draw is measured, then banked at the level whose band holds its effect (a setting drawn
    for level 1 that moves the target 3.5 sd is a level-2 task), so a measured draw is not wasted; a level's tasks
    made earlier count toward its `per_case`."""
    from gapfinder.sandbox.backend import InfraError

    sem = asyncio.Semaphore(parallel)

    async def one(name):
        async with sem:
            for attempt in range(4):  # a case resumes: made tasks count, measured draws are not measured again
                try:
                    await _make_case(level, name, per_case, seed, repeats, tries, concurrency, control_rate)
                    return
                except InfraError as exc:
                    print(f"{name}: Sandboxes error (attempt {attempt + 1} of 4): {str(exc)[:160]}", flush=True)
                    await asyncio.sleep(60 * (attempt + 1))
                except Exception as exc:  # noqa: BLE001 (one case's failure doesn't stop the others)
                    print(f"{name}: failed: {type(exc).__name__}: {str(exc)[:300]}", flush=True)
                    return

    await asyncio.gather(*(one(n) for n in cases))


async def _make_case(level, name, per_case, seed, repeats, tries, concurrency, control_rate) -> None:
    from gapfinder.sandbox.backend import make_backend
    from gapfinder.sandbox.events import EventLog
    from gapfinder.sandbox.runner import Orchestrator
    from gapfinder.sandbox.spec import Knob

    lv = LEVELS[level]
    bank = [1, 2] if level == 1 else [level]
    if all(_made(lv_, name, seed) >= per_case for lv_ in bank):
        print(f"{name}: its level {'/'.join(map(str, bank))} tasks are made", flush=True)
        return
    SEALED.mkdir(parents=True, exist_ok=True)
    spec, targets, spec_p = load_case(name)
    root = spec.code_root()
    if root is None or not root.exists():
        print(f"{name}: no local source ({spec.source}); skipped", flush=True)
        return
    main = next(t for t in targets if not t.get("held_out"))
    m = main["metric"]
    flags, lits = plant.candidates(spec, root)
    rng = random.Random(f"curriculum:{level}:{name}:{seed}")
    orch = Orchestrator(make_backend("contree"), spec, EventLog(WORK / f"L{level}-{name}-s{seed}.jsonl"),
                        concurrency=concurrency)
    base = await orch.fanout([{}] * 6, [f"base-{i}" for i in range(6)])
    good = [b for b in base if b.status == "succeeded" and m in b.parsed_metrics]
    if len(good) < 3:
        print(f"{name}: baseline failed ({len(good)} of 6 ran); skipped", flush=True)
        return
    ok = [b.parsed_metrics for b in good]
    mu0, sd0 = statistics.mean(x[m] for x in ok), statistics.stdev([x[m] for x in ok])
    # a drawn setting can make a run far slower (Fair Clustering's lmbda_tune runs a grid of fits): cut at five times
    # the slowest baseline run, and a cut draw is redrawn
    slow = max(b.resources.elapsed_s for b in good)
    spec.run.timeout = min(spec.run.timeout, max(120.0, 5 * slow))
    if sd0 == 0:  # a deterministic target: no subtle band in standard deviations, and two runs show a change
        bank = [lv_ for lv_ in bank if LEVELS[lv_].get("max_sd") is None]
        repeats = 2
    need = {lv_: per_case - _made(lv_, name, seed) for lv_ in bank}
    # controls are about one task in five of the case's tasks, however many real draws are redrawn
    quota = max(1, round(control_rate * per_case * len(bank))) - _controls(name, seed, bank)
    print(f"L{level} {name}: baseline {m} {mu0:.4g} +- {sd0:.3g} (slowest run {slow:.0f} s, cut at "
          f"{spec.run.timeout:.0f} s); to make: " + ", ".join(f"L{k} {v}" for k, v in need.items() if v > 0), flush=True)
    # each drawn change set is measured once (the era knob is a single draw), across resumed attempts: the kept
    # ones from the case's sealed answers, the rest from the maker's file (its own bookkeeping; nothing is printed)
    mfile = WORK / f"measured-L{level}-{name}-s{seed}.json"
    measured: set[tuple] = {tuple(tuple(x) for x in k) for k in
                            (json.loads(mfile.read_text(encoding="utf-8")) if mfile.exists() else [])}
    for lv_ in bank:
        for f in SEALED.glob(f"L{lv_}-{name}-s{seed}-*.json") if SEALED.exists() else []:
            a = json.loads(f.read_text(encoding="utf-8"))
            if a.get("parts"):
                measured.add(tuple(sorted((q["family"], q["knob"], q["value"]) for q in a["parts"])))
    i, lost = 0, 0
    while i < tries * per_case * len(bank) and lost < 20:
        i += 1
        open_ = [lv_ for lv_ in bank if need[lv_] > 0]
        if not open_:
            break
        await _wait_online(name)
        if quota > 0 and rng.random() < control_rate:  # a gap-free control: another draw of the same runs
            lc = rng.choice(open_)
            tag = _next_tag(lc, name, seed)
            runs = await orch.fanout([{}] * repeats, [f"{tag}-c{j}" for j in range(repeats)])
            got = [b.parsed_metrics for b in runs if b.status == "succeeded" and m in b.parsed_metrics]
            if _infra(runs):
                i, lost = i - 1, lost + 1
                await asyncio.sleep(60)
                continue
            if len(got) < 2:
                continue
            _write(tag, name, lc, plant._paper(targets, got), {"kind": "control", "parts": []})
            need[lc] -= 1
            quota -= 1
            print(f"  {name} draw {i}: kept as {tag}", flush=True)  # the log never says what a task is
            continue
        fams = [f for f in lv["families"] if (f.split("+")[0] in HARNESS_FAMILIES) == (rebuilt(name) is not None)]
        if not fams:
            print(f"{name}: no family of level {level} applies", flush=True)
            break
        if lv["causes"] == 2:
            f1 = rng.choice(fams)
            f2 = f1 if lv.get("same") else rng.choice([f for f in fams if f != f1])
            picks = [f1, f2]
        else:
            picks = rng.choice(fams).split("+")
        parts = []
        for f in picks:
            c = draw_family(f, rng, spec, root, flags, lits)
            if c is None or any(c[1] == q[1] for q in parts):
                break
            parts.append(c)
        if len(parts) != len(picks):
            continue
        key = tuple(sorted((q[0], q[1], q[2]) for q in parts))
        if key in measured:
            continue
        measured.add(key)
        mfile.write_text(json.dumps(sorted(measured)), encoding="utf-8")
        changes = {}
        for fam, k, v, desc, extra in parts:
            if fam == "reporting":
                continue  # a reading of the runs, not a change to them
            if k.startswith("@ast:"):
                spec.knobs.setdefault(k, Knob(layer="environment", default=extra.get("default") or "0", env=True,
                                              choices=[] if extra.get("literal") else ["0", "1"]))
            changes[k] = v
        tag0 = f"L{level}-{name}-s{seed}-d{i}-{lost}"
        runs = await orch.fanout([changes] * repeats, [f"{tag0}-{j}" for j in range(repeats)])
        got = [b.parsed_metrics for b in runs if b.status == "succeeded" and m in b.parsed_metrics]
        if _infra(runs):  # not measured: drawn again later, and not counted as a try
            measured.discard(key)
            mfile.write_text(json.dumps(sorted(measured)), encoding="utf-8")
            print(f"  {name} draw {i}: Sandboxes or network error; not counted", flush=True)
            i, lost = i - 1, lost + 1
            await asyncio.sleep(60)
            continue
        if any(q[0] == "reporting" for q in parts):  # the paper's numbers: each run's best epoch, per metric
            got = [{**x, **{t["metric"]: x[f"{t['metric']}__x_best"] for t in targets
                            if f"{t['metric']}__x_best" in x}} for x in got]
        if len(got) < 2:
            print(f"  {name} draw {i}: runs failed", flush=True)
            continue
        mu = statistics.mean(x[m] for x in got)
        pooled = math.sqrt((sd0 ** 2 + statistics.stdev([x[m] for x in got]) ** 2) / 2) or 1e-12
        moved = abs(mu - mu0) / pooled
        fits = [lv_ for lv_ in open_ if _band_ok(lv_, moved)] if abs(mu - mu0) > 0.005 * abs(mu0) else []
        if fits and len(parts) == 2:  # each cause must matter alone, and both are needed
            for fam, k, v, desc, extra in parts:
                one = await orch.fanout([{k: v}] * 2, [f"{tag0}-alone-{j}" for j in range(2)])
                g1 = [b.parsed_metrics[m] for b in one if b.status == "succeeded" and m in b.parsed_metrics]
                if not g1 or abs(statistics.mean(g1) - mu0) / pooled < lv["each_sd"] or \
                        abs(statistics.mean(g1) - mu) / pooled < lv["each_sd"]:
                    fits = []
                    break
        if not fits:
            print(f"  {name} draw {i}: moved {moved:.1f} sd: redrawn", flush=True)
            continue
        lk = fits[0]
        tag = _next_tag(lk, name, seed)
        extra_targets = []
        for fam, k, v, desc, extra in parts:
            if fam == "scale":  # the paper's sweep in its own units, run in the code's
                d0 = spec.knobs[k].default
                for u in plant.scale_values(plant._num(d0), extra["factor"], plant._is_int(d0)):
                    pv = plant._fmt_c(u, d0)
                    pr = await orch.fanout([{**changes, k: plant._fmt_c(u * extra["factor"], d0)}] * repeats,
                                           [f"{tag}-{pv}-{j}" for j in range(repeats)])
                    pg = [b.parsed_metrics for b in pr if b.status == "succeeded" and m in b.parsed_metrics]
                    if len(pg) >= 2:
                        extra_targets.append({**main, "claim_id": f"{main['claim_id']}@{k}={pv}", "held_out": True,
                                              "at": {k: pv}, "paper_value": round(statistics.mean(x[m] for x in pg), 4)})
        kind = "+".join(q[0] for q in parts)
        _write(tag, name, lk, plant._paper(targets, got) + extra_targets,
               {"kind": kind, "moved_sd": round(moved, 2),
                "parts": [{"family": f, "knob": k, "value": v, "desc": desc, **ex} for f, k, v, desc, ex in parts]})
        need[lk] -= 1
        print(f"  {name} draw {i}: kept as {tag}", flush=True)
    left = {k: v for k, v in need.items() if v > 0}
    if left:
        print(f"{name}: short of tasks after {i} draws ({lost} lost to the infrastructure): "
              + ", ".join(f"L{k} {v}" for k, v in left.items()), flush=True)


def _write(tag: str, case: str, level: int, targets: list[dict], answer: dict) -> None:
    d = TASKS / tag
    d.mkdir(parents=True, exist_ok=True)
    (d / "targets.json").write_text(json.dumps(targets, indent=1), encoding="utf-8")
    (d / "task.json").write_text(json.dumps({"case": case, "level": level}, indent=1), encoding="utf-8")
    (SEALED / f"{tag}.json").write_text(json.dumps({**answer, "case": case, "level": level}, indent=1), encoding="utf-8")


# ------------------------------------------------------------------ searching

def search_one(tag: str, code: Path, max_runs: int, concurrency: int) -> int:
    """One task's search; a search that ended on a Sandboxes or network error (InfraError) is started again from
    scratch, up to four times, once the API's name resolves."""
    import shutil
    import time

    for attempt in range(4):
        while not _online():
            time.sleep(30)
        rc = _search_once(tag, code, max_runs, concurrency)
        err = (TASKS / tag / "search.err").read_text(encoding="utf-8", errors="replace")[-4000:]
        if rc == 0 or "InfraError" not in err:
            return rc
        shutil.copy(TASKS / tag / "search.err", TASKS / tag / f"search.err.infra{attempt + 1}")
        shutil.rmtree(TASKS / tag / "run", ignore_errors=True)
        time.sleep(120 * (attempt + 1))
    return rc


def _search_once(tag: str, code: Path, max_runs: int, concurrency: int) -> int:
    t = json.loads((TASKS / tag / "task.json").read_text(encoding="utf-8"))
    spec_p = resolved_spec(t["case"])
    env = {**os.environ, "PYTHONPATH": str(code), "PYTHONIOENCODING": "utf-8"}
    py = str(ROOT / ".venv" / "Scripts" / "python.exe") if os.name == "nt" else sys.executable
    cmd = [py, "-P", "-m", "gapfinder.cli", "search", "--spec", str(spec_p), "--targets",
           str(TASKS / tag / "targets.json"), "--hypotheses", "repomap", "--backend", "contree", "--concurrency",
           str(concurrency), "--max-runs", str(max_runs), "--paper", f"planted {tag}", "--out", str(TASKS / tag / "run")]
    with open(TASKS / tag / "search.log", "w", encoding="utf-8") as out, \
            open(TASKS / tag / "search.err", "w", encoding="utf-8") as err:
        return subprocess.call(cmd, env=env, cwd=str(code), stdout=out, stderr=err)


def _unsearched(level: int | None, started: set[str]) -> list[str]:
    return [d.name for d in sorted(TASKS.iterdir()) if (level is None or d.name.startswith(f"L{level}-"))
            and (d / "task.json").exists() and d.name not in started
            and not (d / "run" / "gap_report.json").exists()] if TASKS.exists() else []


def search(level: int | None, code: Path, max_runs: int, concurrency: int, parallel: int,
           watch: Path | None = None) -> None:
    """Each task without a report, `parallel` at a time. With `watch`, tasks made meanwhile are searched too,
    until the file `watch` exists and nothing is left."""
    import time
    from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait

    started: set[str] = set()
    running = {}
    with ThreadPoolExecutor(parallel) as ex:
        while True:
            for tag in _unsearched(level, started)[: max(0, parallel - len(running))]:
                started.add(tag)
                running[ex.submit(search_one, tag, code, max_runs, concurrency)] = tag
                print(f"  {tag}: searching", flush=True)
            if not running and (watch is None or (watch.exists() and not _unsearched(level, started))):
                break
            done, _ = wait(list(running), timeout=60, return_when=FIRST_COMPLETED) if running else (set(), None)
            for f in done:
                print(f"  {running.pop(f)}: exit {f.result()}", flush=True)
            if not running and not done:
                time.sleep(30)


# ------------------------------------------------------------------ scoring

def _part_found(p: dict, res: dict) -> bool:
    changes, sets = res.get("changes") or {}, res.get("value_sets") or {}
    notes = " ".join(res.get("notes") or [])
    fam = p["family"]
    if fam == "reporting":
        return (res.get("reporting") or {}).get("rule") in ("best", "best+attarget")
    if fam == "era":
        return str(changes.get(p["knob"], "0")) not in ("0", "")
    if fam == "library":
        v = str(changes.get(p["knob"], "0"))
        if p["value"] == "all":  # every old release planted: the library probe's minimal subset is the answer
            return v not in ("0", "")
        return v == "all" or bool(set(p["value"].split(",")) & set(v.split(",")))
    if fam in ("code", "data"):
        site = p["desc"].split(": ", 1)[0]
        return p["knob"] in changes or bool(site and site in notes and "code change" in notes)
    return any(plant._knob_matches(k, p["knob"]) and (plant._same(v, p["value"]) or
                                                       any(plant._same(s, p["value"]) for s in sets.get(k, [])))
               for k, v in changes.items())


def verdict(a: dict, res: dict) -> str:
    attr = res.get("attribution") or {}
    label = attr.get("confidence_label") or ("Reproduced" if res.get("status") == "reproduced" else "Unexplained")
    if a["kind"] == "control":
        return "confidently wrong" if label in CONFIDENT else "correct"
    if a["kind"] == "outside":
        return "confidently wrong" if label in CONFIDENT else "correct"
    parts = [p for p in a["parts"] if p["family"] != "outside"]
    found = [p for p in parts if _part_found(p, res)]
    if "outside" in a["kind"]:  # a setting plus a cause outside every family: the setting, and not fully explained
        if label == "Explained" and found:
            return "partial"
        if found:
            return "correct"
        return "confidently wrong" if label in CONFIDENT else "missed"
    if len(found) == len(parts) and label not in ("Unexplained", "Inconclusive", "Reproduced"):
        return "correct"
    if found:
        return "partial"
    return "confidently wrong" if label in CONFIDENT else "missed"


def score(level: int | None = None) -> dict:
    rows = []
    for d in sorted(TASKS.iterdir()) if TASKS.exists() else []:
        if level is not None and not d.name.startswith(f"L{level}-"):
            continue
        rep, ans = d / "run" / "gap_report.json", SEALED / f"{d.name}.json"
        if not rep.exists() or not ans.exists():
            continue
        a = json.loads(ans.read_text(encoding="utf-8"))
        r = json.loads(rep.read_text(encoding="utf-8"))
        res = (r.get("results") or r.get("claims") or [{}])[0]
        rows.append({"task": d.name, "level": a["level"], "case": a["case"], "kind": a["kind"],
                     "verdict": verdict(a, res), "label": (res.get("attribution") or {}).get("confidence_label"),
                     "found": res.get("changes") or {}, "planted": [f"{p['family']}: {p['desc']}" for p in a["parts"]]})
    by = {}
    for x in rows:
        by.setdefault((x["level"], x["kind"]), []).append(x["verdict"])
    for (lv, kind), vs in sorted(by.items()):
        print(f"L{lv} {kind:22s} " + ", ".join(f"{v} {vs.count(v)}" for v in
                                              ("correct", "partial", "missed", "confidently wrong") if vs.count(v)))
    lv_sum = {}
    for x in rows:
        s = lv_sum.setdefault(x["level"], {"n": 0, "correct": 0, "partial": 0, "missed": 0, "confidently wrong": 0})
        s["n"] += 1
        s[x["verdict"]] += 1
    for lv, s in sorted(lv_sum.items()):
        print(f"level {lv}: {s['correct']}/{s['n']} correct, {s['partial']} partial, {s['missed']} missed, "
              f"{s['confidently wrong']} confidently wrong")
    HERE.mkdir(parents=True, exist_ok=True)
    (HERE / "scores.json").write_text(json.dumps({"rows": rows, "levels": lv_sum}, indent=1), encoding="utf-8")
    return lv_sum


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("make", "run"):
        p = sub.add_parser(name)
        p.add_argument("--cases", default=",".join(CASES))
        p.add_argument("--per-case", type=int, default=2)
        p.add_argument("--seed", type=int, default=1)
        p.add_argument("--repeats", type=int, default=3)
        p.add_argument("--concurrency", type=int, default=8)
        p.add_argument("--tries", type=int, default=10)
        p.add_argument("--case-parallel", type=int, default=3)
        if name == "make":
            p.add_argument("--level", type=int, required=True)
        else:
            p.add_argument("--start", type=int, default=1)
            p.add_argument("--code", type=Path, required=True)
            p.add_argument("--max-runs", type=int, default=150)
            p.add_argument("--parallel", type=int, default=3)
            p.add_argument("--pass", dest="pass_rate", type=float, default=0.7)
    ps = sub.add_parser("search")
    ps.add_argument("--level", type=int)
    ps.add_argument("--code", type=Path, required=True)
    ps.add_argument("--max-runs", type=int, default=150)
    ps.add_argument("--concurrency", type=int, default=8)
    ps.add_argument("--parallel", type=int, default=3)
    ps.add_argument("--watch", type=Path, help="keep searching new tasks until this file exists")
    pc = sub.add_parser("score")
    pc.add_argument("--level", type=int)
    a = ap.parse_args()
    if a.cmd == "make":
        asyncio.run(make(a.level, a.cases.split(","), a.per_case, a.seed, a.repeats, a.tries, a.concurrency,
                         parallel=a.case_parallel))
    elif a.cmd == "search":
        search(a.level, a.code.resolve(), a.max_runs, a.concurrency, a.parallel, a.watch)
    elif a.cmd == "score":
        score(a.level)
    else:
        for level in range(a.start, 6):
            asyncio.run(make(level, a.cases.split(","), a.per_case, a.seed, a.repeats, a.tries, a.concurrency,
                             parallel=a.case_parallel))
            search(level, a.code.resolve(), a.max_runs, a.concurrency, a.parallel)
            s = score(level).get(level) or {"n": 0}
            if not s["n"] or s["correct"] / s["n"] < a.pass_rate or s["confidently wrong"]:
                print(f"level {level} not passed: the curriculum stops here", flush=True)
                break
            print(f"level {level} passed: next level", flush=True)


if __name__ == "__main__":
    main()
