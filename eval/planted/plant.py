"""Planted-cause benchmark on real repositories: measure a rate, not a case.

    python eval/planted/plant.py make  --case vgae --n 3 --seed 1     # sample causes, run them, write tasks
    python eval/planted/plant.py search --task vgae-s1-1 --code <frozen worktree> --max-runs 120
    python eval/planted/plant.py score                                 # score every searched task

A task is a real dev-set repository (its built Sandboxes image and harness spec) with one hidden change:
a flag set to another value, or a named numeric literal in the code patched in memory (the same hook the
patch round uses; no file is edited). The "paper" numbers are the mean of `--repeats` runs with the change.
GapFinder then searches with the case's spec and targets, no ledger and no paper (`--hypotheses repomap`),
so it measures the search, the trace and the patch round on real code, not paper reading.

Why: every case so far was scored after looking at it. Causes sampled here are drawn by a seeded random
generator from a fixed distribution, before any search, so a rate over them is not shaped by the tool.
Rules (docs/CONTEXT_v11.md section 7):
- these tasks are measurement only: no change is judged on, or tuned to, a planted task;
- answers go to eval/planted/sealed/ and are read only by `score`.

Kinds (plan D7.4, `--kinds`): `setting` (below), and the archetypes behind the sealed misses, as the acceptance
suite of plans D1, D2 and D5 (development only: the builder knows them, so they are not blind evidence):
- `scale`: a numeric flag the paper sweeps in other units: the paper's v is the code's c x v (c in {2, 1/2}, and
  1/100 for a fraction the paper gives in percent; every planted value valid for the flag's type); the target and
  two sweep points are the code's runs at c x v. Correct: the answer sets the flag to c x its default (the scale
  probe's relation).
- `code`: a code defect: the paper's numbers come from the code with one mutant on (an arithmetic, reduction or
  data-pipeline edit from gapfinder/search/mutation.py's operators, at a site the patch hook reaches); the
  reproduction runs the released code. Correct: the answer is that mutant (a code lead).
- `reporting`: the paper reports the best epoch by the test metric: its numbers are the as-run runs' `__x_best`
  trajectory statistic (zero extra runs; only for a spec whose emitter records trajectories). Correct: the
  reporting rule `best` or `best+attarget`.
- `library`: the paper ran an older release: its numbers are the runs with `gf_paper_year_env` set to one package
  (only for a spec with paper-year pins). Correct: the answer switches that package on.

Settings distribution: a cause is a flag with probability 1/2, else a literal. Numeric values are scaled by a factor
drawn from {1/4, 1/2, 2, 4} (integers rounded, at least 1; a flag's `max` respected); a choice flag takes
another choice. Literals: any named numeric literal (not 0 or +-1, not a flag's default) in a file the patch hook can reach. A draw
is kept if the target claim moves by more than 3 pooled standard deviations (6 unchanged runs, `--repeats`
changed ones) and 0.5% of its value; otherwise it is redrawn (`--tries`). The draws, kept and rejected, are all recorded.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import math
import os
import random
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEVSET = ROOT / "eval" / "external" / "devset"


def case_dir(case: str) -> Path:
    """A case's folder: the dev set's, or any external batch's (eval/external/<batch>/<case>/<case>.yaml)."""
    d = DEVSET / case
    if (d / f"{case}.yaml").exists():
        return d
    hits = sorted((ROOT / "eval" / "external").glob(f"*/{case}/{case}.yaml"))
    if not hits:
        sys.exit(f"no case folder with {case}.yaml under eval/external/")
    return hits[0].parent
HERE = Path(os.environ.get("GF_PLANTED_DIR") or ROOT / "eval" / "planted")  # overridable for tests
TASKS = HERE / "tasks"
SEALED = HERE / "sealed"
KINDS = ("setting", "scale", "code", "reporting", "library")
SCALE_C = (2.0, 0.5)
UNIT_C = (0.01,)
FACTORS = (0.25, 0.5, 2.0, 4.0)


def _fmt(v: float, like: str) -> str:
    if "." not in like and "e" not in like.lower():
        return str(max(1, int(round(v))))
    return f"{v:.6g}"


def _num(s: str) -> float | None:
    try:
        return float(str(s).strip().strip("\"'"))
    except ValueError:
        return None


def _bool(s: str) -> str | None:
    x = str(s).strip().lower()
    return {"true": "false", "false": "true", "1": "0", "0": "1"}.get(x)


def candidates(spec, root: Path) -> tuple[list[tuple], list[tuple]]:
    """(flag causes, literal causes) the generator draws from: (knob, default) pairs."""
    from gapfinder.ingest.code_checks import named_literals
    from gapfinder.sandbox import ast_patch

    flags = [(k, kn) for k, kn in spec.knobs.items() if "seed" not in k.lower()]
    lits = []
    for x in named_literals(root):
        v = _num(x.value)
        if v is None or v in (0.0, 1.0, -1.0) or "seed" in x.name.lower():
            continue
        if x.name == "default" or "add_argument" in x.detail or "DEFINE_" in x.detail:
            continue  # a flag's default: the harness passes the flag, so the literal never matters
        if ast_patch.entry_script(root / x.file) and not ast_patch.direct_entry(spec.run.command, x.file):
            continue  # the hook can't reach it
        lits.append((ast_patch.knob_name(x.file, x.line, x.name), x.value))
    return flags, lits


def draw(rng: random.Random, flags, lits) -> tuple[str, str, str] | None:
    """(kind, knob, planted value)."""
    if flags and (not lits or rng.random() < 0.5):
        k, kn = rng.choice(flags)
        if kn.choices:
            others = [c for c in kn.choices if c != kn.default]
            return ("flag", k, rng.choice(others)) if others else None
        if (b := _bool(kn.default)) is not None and _num(kn.default) is None:
            return "flag", k, b
        v = _num(kn.default)
        if v is None:
            return None
        if v == 0:
            return "flag", k, rng.choice(["0.1", "0.5"]) if "." in kn.default else rng.choice(["1", "4"])
        new = _fmt(v * rng.choice(FACTORS), kn.default)
        if kn.max is not None and float(new) > kn.max:
            new = _fmt(v * 0.5, kn.default)
        return ("flag", k, new) if new != kn.default else None
    if not lits:
        return None
    k, lit = rng.choice(lits)
    new = _fmt(float(lit) * rng.choice(FACTORS), lit)
    return ("literal", k, new) if _num(new) != _num(lit) else None


def _is_int(like: str) -> bool:
    return "." not in like and "e" not in like.lower()


def scale_values(d: float, c: float, is_int: bool) -> list[float]:
    """Two paper-unit sweep values u (besides the default) with u and c x u both valid for the flag."""
    out = []
    for mult in (0.5, 2.0, 4.0, 3.0, 0.25):
        u = d * mult
        ok = all(abs(x - round(x)) < 1e-9 and round(x) >= 1 for x in (u, c * u)) if is_int else u > 0
        if ok and u != d and u not in out:
            out.append(u)
        if len(out) == 2:
            break
    return out


def draw_scale(rng: random.Random, flags) -> tuple[str, str, float] | None:
    """(kind, flag, c): a numeric flag whose paper values u are the code's c x u (the paper states the code's
    default, and its numbers come from c x that). The factor keeps every planted value valid for the flag: an integer
    stays an integer, a fraction stays below 1; the percent convention (1/100) only for a fraction."""
    pool = []
    for k, kn in flags:
        d = _num(kn.default)
        if d is None or d <= 0 or kn.choices or _bool(kn.default) is not None:
            continue
        is_int = _is_int(kn.default)
        cs = [c for c in SCALE_C if (not is_int or abs(c * d - round(c * d)) < 1e-9 and round(c * d) >= 1)
              and (is_int or d >= 1 or c * d < 1)]
        if not is_int and 0 < d < 1:
            cs.append(0.01)  # the code holds a fraction where the paper's numbers are percents
        cs = [c for c in cs if len(scale_values(d, c, is_int)) == 2 and (kn.max is None or c * d * 2 <= kn.max)]
        pool += [(k, c) for c in cs]
    if not pool:
        return None
    k, c = rng.choice(pool)
    return "scale", k, c


_FROZEN = None


def frozen_mutants(root: Path, knobs: list[str], limit: int = 400):
    """Plan H5: the mutants of GapFinder's operators as frozen at tag planted-c1 (eval/planted/operators_c1.py), so a
    planted code or data task never comes from the engine under test."""
    global _FROZEN
    if _FROZEN is None:
        import importlib.util

        spec = importlib.util.spec_from_file_location("operators_c1", Path(__file__).resolve().parent / "operators_c1.py")
        mod = importlib.util.module_from_spec(spec)
        sys.modules["operators_c1"] = mod  # its dataclasses look their module up while it loads
        spec.loader.exec_module(mod)
        _FROZEN = mod
    return _FROZEN.find_mutants(root, knobs, limit=limit)


def draw_code(rng: random.Random, root: Path, spec) -> tuple[str, str, str] | None:
    """(kind, mutant knob, its description): one mutant the patch hook reaches, from the mutation operators."""
    from gapfinder.sandbox import ast_patch

    ms = [m for m in frozen_mutants(root, [k for k in spec.knobs if not k.startswith("@")], limit=400)
          if not (ast_patch.entry_script(root / m.file) and not ast_patch.direct_entry(spec.run.command, m.file))
          and not m.op.startswith(("xmul10", "xdiv10", "mul10", "div10"))]
    if not ms:
        return None
    m = rng.choice(ms)
    return "code", m.name, m.describe()


def _fmt_c(v: float, like: str) -> str:
    if "." not in like and "e" not in like.lower() and abs(v - round(v)) < 1e-9:
        return str(int(round(v)))
    return f"{v:.6g}"


def _paper(targets: list[dict], got: list[dict]) -> list[dict]:
    dec = lambda x: len(str(x).split(".")[1]) if "." in str(x) else 0  # noqa: E731  the paper's precision
    out = []
    for t in targets:
        vals = [x[t["metric"]] for x in got if t["metric"] in x]
        if vals:
            out.append({**t, "paper_value": round(statistics.mean(vals), max(dec(t["paper_value"]), 2))})
    return out


async def make(case: str, n: int, seed: int, repeats: int, tries: int, concurrency: int,
               kinds: tuple[str, ...] = ("setting",), backend: str = "contree", case_path: Path | None = None) -> None:
    from gapfinder.sandbox.backend import make_backend
    from gapfinder.sandbox.events import EventLog
    from gapfinder.sandbox.runner import Orchestrator
    from gapfinder.sandbox.spec import HarnessSpec, Knob

    d = case_path or case_dir(case)
    spec = HarnessSpec.load_yaml(d / f"{case}.yaml")
    root = spec.code_root()
    if root is None:
        sys.exit("set GF_DEV_SOURCE to the case's local checkout (its code is read for literals)")
    targets = json.loads((d / "targets.json").read_text(encoding="utf-8"))
    main = next(t for t in targets if not t.get("held_out"))
    flags, lits = candidates(spec, root)
    print(f"{case}: {len(flags)} flags, {len(lits)} reachable literals", flush=True)
    rng = random.Random(f"{case}:{seed}")
    work = HERE / "work" / f"{case}-s{seed}"
    orch = Orchestrator(make_backend(backend), spec, EventLog(work / "events.jsonl"), concurrency=concurrency)
    nb = max(6, repeats)  # three runs underestimate the noise (pygcn: sd 0.21 once, 0.95 another time)
    base = await orch.fanout([{}] * nb, [f"base-{i}" for i in range(nb)])
    ok = [b.parsed_metrics for b in base if b.status == "succeeded"]
    if len(ok) < 2:
        sys.exit(f"baseline failed: {[b.notes for b in base]}")
    m = main["metric"]
    mu0 = statistics.mean(x[m] for x in ok)
    sd0 = statistics.stdev([x[m] for x in ok]) if len(ok) > 1 else 0.0
    print(f"baseline {m}: {mu0:.4g} +- {sd0:.3g} over {len(ok)}", flush=True)
    SEALED.mkdir(parents=True, exist_ok=True)
    log = []
    made = 0
    from gapfinder import env_year

    lib_dirs = sorted(((spec.library or {}).get("pins") or {}).keys()) if env_year.KNOB in spec.knobs else []
    traj = [t for t in targets if any(f"{t['metric']}__x_best" in x for x in ok)]
    avail = {"setting": bool(flags or lits), "scale": bool(flags), "code": True, "reporting": bool(traj),
             "library": bool(lib_dirs)}
    kinds = tuple(x for x in kinds if avail.get(x))
    if not kinds:
        sys.exit(f"none of the kinds asked for applies to {case}: {avail}")
    print(f"{case}: kinds {', '.join(kinds)}", flush=True)
    for i in range(n * tries):
        if made >= n:
            break
        kind = rng.choice(kinds)
        extra_targets: list[dict] = []
        if kind == "setting":
            c = draw(rng, flags, lits)
            if c is None:
                continue
            kind, k, v = c
            if kind == "literal":
                spec.knobs.setdefault(k, Knob(layer="environment", default=dict(lits)[k], env=True))
        elif kind == "scale":
            c = draw_scale(rng, flags)
            if c is None:
                continue
            _, k, factor = c
            d0 = spec.knobs[k].default
            v = _fmt_c(_num(d0) * factor, d0)
            # the paper's sweep in its own units (two values besides its default); the code runs c x each
            for u in scale_values(_num(d0), factor, _is_int(d0)):
                pv = _fmt_c(u, d0)
                pr = await orch.fanout([{k: _fmt_c(u * factor, d0)}] * repeats,
                                       [f"plant-{i}-{pv}-{j}" for j in range(repeats)])
                pg = [b.parsed_metrics for b in pr if b.status == "succeeded" and m in b.parsed_metrics]
                if len(pg) >= 2:
                    extra_targets.append({**main, "claim_id": f"{main['claim_id']}@{k}={pv}", "held_out": True,
                                          "at": {k: pv}, "paper_value": round(statistics.mean(x[m] for x in pg), 4)})
        elif kind == "code":
            c = draw_code(rng, root, spec)
            if c is None:
                continue
            _, k, desc = c
            v = "1"
            spec.knobs.setdefault(k, Knob(layer="environment", default="0", env=True, choices=["0", "1"]))
        elif kind == "reporting":
            k, v = "@reporting", "best"
        else:
            k, v = env_year.KNOB, rng.choice(lib_dirs)
        if kind == "reporting":  # the paper's numbers are the as-run runs' best epochs: no new run
            got = [{t["metric"]: x[f"{t['metric']}__x_best"] for t in targets if f"{t['metric']}__x_best" in x}
                   for x in ok]
        else:
            runs = await orch.fanout([{k: v}] * repeats, [f"plant-{i}-{j}" for j in range(repeats)])
            got = [b.parsed_metrics for b in runs if b.status == "succeeded" and m in b.parsed_metrics]
        entry = {"kind": kind, "knob": k, "value": v, "ok_runs": len(got)}
        if kind == "scale":
            entry["factor"] = factor
        if kind == "code":
            entry["mutant"] = desc
        if len(got) < 2:
            entry["kept"] = False
            entry["why"] = "runs failed"
            log.append(entry)
            print(f"draw {i}: {kind}: runs failed", flush=True)
            continue
        mu = statistics.mean(x[m] for x in got)
        moved = abs(mu - mu0)
        sd1 = statistics.stdev([x[m] for x in got])
        pooled = math.sqrt((sd0 ** 2 + sd1 ** 2) / 2)
        entry.update({"main": round(mu, 6), "moved": round(moved, 6), "pooled_sd": round(pooled, 6),
                      "kept": moved > max(3 * pooled, 0.005 * abs(mu0)) and math.isfinite(mu)})
        log.append(entry)
        # the cause is not printed: the answers are read only by `score`
        print(f"draw {i}: {kind}: {m} moved {moved:.3g} (3 sd {3 * pooled:.3g}): {'kept' if entry['kept'] else 'no gap'}", flush=True)
        if not entry["kept"]:
            continue
        made += 1
        name = f"{case}-s{seed}-{made}"
        t_dir = TASKS / name
        t_dir.mkdir(parents=True, exist_ok=True)
        planted = _paper(targets, got) + extra_targets
        (t_dir / "targets.json").write_text(json.dumps(planted, indent=1), encoding="utf-8")
        (t_dir / "task.json").write_text(json.dumps({"case": case, "seed": seed, "index": made}, indent=1), encoding="utf-8")
        (SEALED / f"{name}.json").write_text(json.dumps({**entry, "baseline": round(mu0, 6), "baseline_sd": sd0},
                                                         indent=1), encoding="utf-8")
    (SEALED / f"draws-{case}-s{seed}.json").write_text(json.dumps(log, indent=1), encoding="utf-8")
    print(f"{made} task(s) written to {TASKS}; {len(log)} draws recorded (sealed)", flush=True)


def _same(a: str, b: str, rel: float = 0.1) -> bool:
    x, y = _num(a), _num(b)
    if x is not None and y is not None:
        return abs(x - y) <= rel * max(abs(x), abs(y), 1e-12)
    return str(a).strip().lower() == str(b).strip().lower()


def _knob_matches(found: str, planted: str) -> bool:
    from gapfinder.sandbox import ast_patch

    if found == planted:
        return True
    if ast_patch.is_patch(found) and ast_patch.is_patch(planted):
        (f1, _, n1), (f2, _, n2) = ast_patch.parse(found), ast_patch.parse(planted)
        return f1 == f2 and n1 == n2
    return False


def _hit(a: dict, res: dict, changes: dict, sets: dict) -> bool:
    """Whether the answer is the planted cause, by kind."""
    kind = a["kind"]
    if kind == "reporting":
        return (res.get("reporting") or {}).get("rule") in ("best", "best+attarget")
    if kind == "library":
        from gapfinder import env_year

        v = str(changes.get(env_year.KNOB, ""))
        return v == "all" or a["value"] in v.split(",")
    if kind == "code":
        notes = " ".join(res.get("notes") or [])
        site = a.get("mutant", "").split(": ", 1)[0]  # "file.py:LINE" (Mutant.describe)
        return a["knob"] in changes or bool(site and site in notes and "code change" in notes)
    return any(_knob_matches(k, a["knob"]) and (_same(v, a["value"]) or any(_same(s, a["value"]) for s in sets.get(k, [])))
               for k, v in changes.items())


def score() -> None:
    """correct: the answer sets the planted knob to its value (10%, or one of its equally good values);
    confidently wrong: Explained or Paper-artifact inconsistency without it; missed: anything else. A miss whose
    planted change is among the history-matching fits was measured but can't be told apart from the claims."""
    rows = []
    for t_dir in sorted(TASKS.iterdir()) if TASKS.exists() else []:
        rep = t_dir / "run" / "gap_report.json"
        ans = SEALED / f"{t_dir.name}.json"
        if not rep.exists() or not ans.exists():
            continue
        a = json.loads(ans.read_text(encoding="utf-8"))
        r = json.loads(rep.read_text(encoding="utf-8"))
        res = (r.get("results") or r.get("claims") or [{}])[0]
        attr = res.get("attribution") or {}
        label = attr.get("confidence_label") or "Reproduced"
        changes = res.get("changes") or {}
        sets = res.get("value_sets") or {}
        hit = _hit(a, res, changes, sets)
        verdict = ("correct" if hit and label not in ("Unexplained", "Inconclusive", "Reproduced") else
                   "confidently wrong" if label in ("Explained", "Paper-artifact inconsistency") else "missed")
        # identifiability vs search: was the planted change measured and among the configurations that fit?
        fits = [x["config"] for v in ((res.get("diagnosis") or {}).get("per_claim") or {}).values() for x in v]
        among = any(any(_knob_matches(k, a["knob"]) and _same(v, a["value"]) for k, v in c.items()) for c in fits)
        rows.append({"task": t_dir.name, "kind": a["kind"], "planted": f"{a['knob']}={a['value']}", "label": label,
                     "found": changes, "verdict": verdict, "planted_among_fits": among, "fits": len(fits)})
    for x in rows:
        print(f"{x['task']:24s} {x['kind']:8s} {x['verdict']:18s} {x['label']:30s} among {x['fits']} fits: "
              f"{'yes' if x['planted_among_fits'] else 'no ':3s}  planted {x['planted']}  found {x['found']}")
    if rows:
        c = sum(x["verdict"] == "correct" for x in rows)
        w = sum(x["verdict"] == "confidently wrong" for x in rows)
        among = sum(x["planted_among_fits"] for x in rows if x["verdict"] == "missed")
        print(f"\n{c}/{len(rows)} correct, {w} confidently wrong; of the misses, {among} had the planted change "
              "among the fits (not identifiable from these claims), the rest were not found")
        (HERE / "scores.json").write_text(json.dumps(rows, indent=1), encoding="utf-8")


def search(task: str, code: Path, max_runs: int, concurrency: int) -> int:
    """Run GapFinder (the frozen checkout at `code`, `python -P` so this checkout isn't imported) on a task."""
    import subprocess

    t_dir = TASKS / task
    case = json.loads((t_dir / "task.json").read_text(encoding="utf-8"))["case"]
    spec = case_dir(case) / f"{case}.yaml"
    env = {**os.environ, "PYTHONPATH": str(code), "PYTHONIOENCODING": "utf-8"}
    cmd = [str(ROOT / ".venv" / "Scripts" / "python.exe") if os.name == "nt" else sys.executable, "-P", "-m", "gapfinder.cli",
           "search", "--spec", str(spec), "--targets", str(t_dir / "targets.json"), "--hypotheses", "repomap",
           "--backend", "contree", "--concurrency", str(concurrency), "--max-runs", str(max_runs),
           "--paper", f"planted task {task}", "--out", str(t_dir / "run")]
    with open(t_dir / "search.log", "w", encoding="utf-8") as out, open(t_dir / "search.err", "w", encoding="utf-8") as err:
        return subprocess.call(cmd, env=env, cwd=str(code), stdout=out, stderr=err)


def main() -> None:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    pm = sub.add_parser("make")
    pm.add_argument("--case", required=True)
    pm.add_argument("--n", type=int, default=3)
    pm.add_argument("--seed", type=int, default=1)
    pm.add_argument("--repeats", type=int, default=3)
    pm.add_argument("--tries", type=int, default=3, help="draws per kept task, at most")
    pm.add_argument("--concurrency", type=int, default=6)
    pm.add_argument("--kinds", default="setting", help=f"comma list of {', '.join(KINDS)}")
    pm.add_argument("--backend", default="contree")
    pm.add_argument("--case-dir", type=Path, default=None, help="a case folder outside eval/external (tests)")
    ps = sub.add_parser("search")
    ps.add_argument("--task", required=True)
    ps.add_argument("--code", type=Path, required=True, help="a frozen worktree (tag + .env)")
    ps.add_argument("--max-runs", type=int, default=120)
    ps.add_argument("--concurrency", type=int, default=6)
    sub.add_parser("score")
    a = p.parse_args()
    if a.cmd == "make":
        kinds = tuple(x.strip() for x in a.kinds.split(",") if x.strip())
        bad = [x for x in kinds if x not in KINDS]
        if bad:
            sys.exit(f"unknown kinds {bad}; choose from {KINDS}")
        asyncio.run(make(a.case, a.n, a.seed, a.repeats, a.tries, a.concurrency, kinds, a.backend, a.case_dir))
    elif a.cmd == "search":
        sys.exit(search(a.task, a.code.resolve(), a.max_runs, a.concurrency))
    else:
        score()


if __name__ == "__main__":
    main()
