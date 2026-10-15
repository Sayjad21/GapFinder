"""Score predictions against answer keys; re-measure every proposed configuration.

    python eval/gapbench/score.py [--split dev|test] [--remeasure 3] [--out eval/results/gapbench_dev.json]
                                  [--answers eval/gapbench/sealed]

Per task, arm and run (primary claims only):
    correct          identified: the proposed knob set equals the hidden one (values compared
                     numerically when both parse), at any label except Unexplained. A hedged
                     "Fits but unsupported" with the right knobs still counts as found.
                     For no_cause tasks, correct = no confident attribution.
    confident        Explained / Paper-artifact inconsistency / Partially explained, or any
                     baseline answer with knobs (baselines don't hedge)
    false_attr       confident and not correct: the failure the verification step exists to prevent
    gap_closed       share of the paper gap closed by the arm's proposed config, measured by
                     re-running it (never taken from the arm's own report)

Added per run: category (answer key `category`, else derived from `type`), outcome (correct, partial,
confidently_wrong, correct_abstention, missed; rules in PROTOCOL.md), the trust-matrix column and a
comparable answer signature. Added per arm: outcome counts and rates with 95% Wilson intervals, the
trust matrix, answer stability across runs, totals and medians of cost, wall time and experiments.
`by_source` repeats the per-arm summary for generator (test-gen-*), AI-author (test-ai-*) and dev tasks.
false_attr is outcome == confidently_wrong; a confident answer naming only part of an interacting
cause is `partial`, not false. A missing prediction (crashed run) is never a correct abstention.

Scoring is deterministic given the prediction files and the re-measurements, which are cached
in each run directory, so rescoring from saved logs reproduces every number.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import math
import statistics
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from gapfinder.sandbox.backend import LocalBackend  # noqa: E402
from gapfinder.sandbox.events import EventLog  # noqa: E402
from gapfinder.sandbox.runner import Orchestrator  # noqa: E402
from gapfinder.sandbox.spec import HarnessSpec  # noqa: E402

GB = ROOT / "eval" / "gapbench"
CONFIDENT = {"Explained", "Paper-artifact inconsistency", "Partially explained", "Attributed"}
NOT_AN_ANSWER = {"Unexplained", "Reproduced", "Inconclusive", "missing"}  # abstentions


def _norm_knob(k: str) -> str:
    return k.strip().lstrip("-").replace("-", "_").lower()


def _norm_val(v) -> str | float:
    s = str(v).strip().strip("\"'").lower()
    try:
        return round(float(s), 9)
    except ValueError:
        return s.replace("-", "").replace("_", "")


def same_knobs(pred: dict, hidden: dict) -> bool:
    p = {_norm_knob(k): _norm_val(v) for k, v in pred.items()}
    h = {_norm_knob(k): _norm_val(v) for k, v in hidden.items()}
    return p == h


def wilson(k: int, n: int, z: float = 1.959964) -> dict:
    """k successes out of n, with the 95% Wilson score interval (no scipy; z = 1.96)."""
    if n <= 0:
        return {"k": k, "n": n, "rate": None, "lo": None, "hi": None}
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return {"k": k, "n": n, "rate": round(p, 3), "lo": round(max(0.0, centre - half), 3),
            "hi": round(min(1.0, centre + half), 3)}


def _binom_cdf(k: int, n: int, p: float) -> float:
    """P(X <= k) for X ~ Binomial(n, p)."""
    if k < 0:
        return 0.0
    if k >= n:
        return 1.0
    term, total = (1 - p) ** n, 0.0
    for i in range(k + 1):
        total += term
        term *= (n - i) / (i + 1) * p / (1 - p) if p < 1 else 0.0
    return min(1.0, total)


def clopper_pearson(k: int, n: int, alpha: float = 0.05) -> dict:
    """Exact (Clopper-Pearson) 95% interval for k out of n, by bisection (no scipy). For k = 0 the
    upper bound is 1 - (alpha/2)^(1/n): with 0 of 48 confidently wrong, the rate is below 7.4%."""
    if n <= 0:
        return {"k": k, "n": n, "rate": None, "lo": None, "hi": None}

    def solve(f, lo=0.0, hi=1.0):
        for _ in range(60):
            mid = (lo + hi) / 2
            lo, hi = (mid, hi) if f(mid) else (lo, mid)
        return (lo + hi) / 2

    lo = 0.0 if k == 0 else solve(lambda p: 1 - _binom_cdf(k - 1, n, p) < alpha / 2)
    hi = 1.0 if k == n else solve(lambda p: _binom_cdf(k, n, p) > alpha / 2)
    return {"k": k, "n": n, "rate": round(k / n, 3), "lo": round(lo, 4), "hi": round(hi, 4)}


CATEGORY_OF_TYPE = {"single_unstated": "known_cause", "stated_code_differs": "known_cause",
                    "interaction": "interaction", "no_cause": "no_cause"}
CAUSE_CATEGORIES = ("known_cause", "interaction", "decoy")  # a findable cause exists
ABSTAIN_CATEGORIES = ("no_cause", "noise_only", "incomplete", "out_of_space")  # the right answer is not to attribute
OUT_OF_SPACE_CATEGORIES = ("out_of_space", "incomplete")  # the cause exists but no exposed setting reaches it
OUTCOMES = ("correct", "partial", "confidently_wrong", "correct_abstention", "missed")
SET_K = 3  # a set answer earns `correct_in_set` only with at most this many configurations (pre-registered)


def category_of(key: dict) -> str:
    """The task's category: the key's `category` field, else derived from its `type`."""
    cat = key.get("category") or CATEGORY_OF_TYPE.get(key.get("type"))
    if cat not in CAUSE_CATEGORIES + ABSTAIN_CATEGORIES:
        raise ValueError(f"task {key.get('id')}: unknown category {cat!r} (type {key.get('type')!r})")
    return cat


def _knob_dict(knobs: dict) -> dict:
    return {_norm_knob(k): _norm_val(v) for k, v in knobs.items()}


def score_claim(key: dict, pred: dict | None) -> dict:
    """Score one claim's prediction against the answer key.

    outcome is one of OUTCOMES. For cause categories: correct (exact knobs), partial (a non-empty
    part of the true knobs and nothing else), confidently_wrong, else missed. For abstention
    categories: confidently_wrong if a confident attribution was made, else correct_abstention.
    A missing prediction (crashed run) is always missed. `column` is the trust-matrix column.
    """
    cat = category_of(key)
    missing = pred is None
    pred = pred or {"label": "missing", "knobs": {}}
    knobs = pred["knobs"] or {}
    proposed = pred["label"] not in NOT_AN_ANSWER and bool(knobs)
    confident = pred["label"] in CONFIDENT and bool(knobs)
    if cat in ABSTAIN_CATEGORIES:
        outcome = "missed" if missing else "confidently_wrong" if confident else "correct_abstention"
    else:
        hidden = _knob_dict(key["hidden"])
        got = _knob_dict(knobs)
        if proposed and got == hidden:
            outcome = "correct"
        elif proposed and got and hidden.items() > got.items():
            outcome = "partial"
        elif confident:
            outcome = "confidently_wrong"
        else:
            outcome = "missed"
    # set-valued credit (reported next to the exact score, never instead of it): the right knobs, and each
    # true value inside the set of values the run found to fit equally well
    sets = {_norm_knob(k): {_norm_val(x) for x in v} for k, v in (pred.get("value_sets") or {}).items()}
    correct_set = outcome == "correct"
    if not correct_set and cat not in ABSTAIN_CATEGORIES and proposed:
        got, truth = _knob_dict(knobs), _knob_dict(key["hidden"])
        correct_set = set(got) == set(truth) and all(v in sets.get(k, {got[k]}) for k, v in truth.items())
    # configuration-set credit (reported next to the exact score, never instead of it): the run's set of
    # configurations the target can't tell apart contains the true one, and has at most SET_K members
    equivalent = [_knob_dict(c) for c in (pred.get("equivalent") or [])] or ([_knob_dict(knobs)] if knobs else [])
    correct_in_set = outcome == "correct" or (
        cat not in ABSTAIN_CATEGORIES and proposed and len(equivalent) <= SET_K
        and _knob_dict(key["hidden"]) in equivalent)
    abstained = not missing and not proposed
    column = {"correct": "correct_cause", "partial": "partial", "confidently_wrong": "wrong_confident",
              "correct_abstention": "abstained", "missed": "abstained" if abstained else "missed"}[outcome]
    return {"label": pred["label"], "knobs": pred["knobs"], "confident": confident,
            "correct": outcome in ("correct", "correct_abstention"),
            "false_attr": outcome == "confidently_wrong", "outcome": outcome, "column": column,
            "correct_set": correct_set, "correct_in_set": correct_in_set, "set_size": len(equivalent),
            # the diagnosis bonus no trivial abstainer can earn: "out of space" said where it is true
            "oos_diagnosed": (pred.get("diagnosis") or "").startswith("out_of_space")}


def combine_claims(claims: dict[str, dict]) -> tuple[str, str]:
    """One outcome and matrix column for a run from its primary claims (all must be right)."""
    cs = list(claims.values())
    outs = {c["outcome"] for c in cs}
    if "confidently_wrong" in outs:
        return "confidently_wrong", "wrong_confident"
    if outs <= {"correct", "correct_abstention"}:
        return cs[0]["outcome"], cs[0]["column"]
    if "partial" in outs:
        return "partial", "partial"
    return "missed", "abstained" if all(c["column"] == "abstained" for c in cs) else "missed"


async def remeasure(task_dir: Path, knobs: dict, n: int, cache: Path) -> dict[str, float] | None:
    """Median metrics of a proposed config (cached in the run dir so rescoring is exact)."""
    key = json.dumps(sorted(knobs.items()))
    store = json.loads(cache.read_text()) if cache.exists() else {}
    if key in store:
        return store[key]
    import yaml

    task = yaml.safe_load((task_dir / "task.yaml").read_text(encoding="utf-8"))
    spec = HarnessSpec.load_yaml(GB / f"{task['family']}.yaml")
    spec_knobs = {_norm_knob(k): k for k in spec.knobs}
    changes = {spec_knobs[_norm_knob(k)]: str(v) for k, v in knobs.items() if _norm_knob(k) in spec_knobs}
    if len(changes) != len(knobs):
        result = None  # proposed a knob the artifact doesn't have: can't be re-run
    else:
        with tempfile.TemporaryDirectory() as tmp:
            orch = Orchestrator(LocalBackend(Path(tmp) / "sbx"), spec, EventLog(Path(tmp) / "e.jsonl"))
            try:
                runs = await orch.fanout([changes] * n)
            except ValueError:  # unrenderable value
                runs = []
        ok = [b for b in runs if b.status == "succeeded"]
        result = {m: statistics.median(b.parsed_metrics[m] for b in ok) for m in spec.metrics} if ok else None
    store[key] = result
    cache.write_text(json.dumps(store, indent=1))
    return result


HIDDEN_FIELDS = ("hidden", "category", "type")  # task fields that reveal the answer


def load_key(task_dir: Path, answers_dir: Path | None = None) -> dict:
    """The answer key of one task, and the only place hidden answers are read from.

    The key is `answer.json` in `<answers_dir>/<task>/` when --answers is given, else in the task
    folder. Any of HIDDEN_FIELDS the key lacks is filled from a `task.yaml` next to it (the sealed
    copy), then from the task's own visible `task.yaml`. `category` falls back to the task `type`.
    """
    import yaml

    src = answers_dir / task_dir.name if answers_dir else task_dir
    key = json.loads((src / "answer.json").read_text())
    for yml in (src / "task.yaml", task_dir / "task.yaml"):
        if yml.exists():
            task = yaml.safe_load(yml.read_text(encoding="utf-8")) or {}
            for field in HIDDEN_FIELDS:
                if task.get(field) is not None:
                    key.setdefault(field, task[field])
    if not key.get("category"):
        key["category"] = CATEGORY_OF_TYPE.get(key.get("type"))
    return key


async def score_run(task_dir: Path, run_dir: Path, n: int, answers_dir: Path | None = None) -> dict:
    answer = load_key(task_dir, answers_dir)
    cat = category_of(answer)
    # generated tasks keep the full calibration (paper values, noise bands) with the sealed answers
    sealed_calib = answers_dir / task_dir.name / "calibration.json" if answers_dir else None
    calib = json.loads((sealed_calib if sealed_calib and sealed_calib.exists() else task_dir / "calibration.json")
                       .read_text())["metrics"]
    targets = {t["claim_id"]: t for t in json.loads((task_dir / "targets.json").read_text())}
    pred = json.loads((run_dir / "prediction.json").read_text())
    claims = {}
    for cid in answer["primary_claims"]:
        sc = score_claim(answer, pred["claims"].get(cid))
        t = targets[cid]
        if cat in CAUSE_CATEGORIES and sc["knobs"]:
            m = await remeasure(task_dir, sc["knobs"], n, run_dir / "remeasure.json")
            g0 = abs(calib[t["metric"]]["naive"] - t["paper_value"])
            sc["gap_closed"] = None if m is None else round(1 - abs(m[t["metric"]] - t["paper_value"]) / g0, 3)
        else:
            sc["gap_closed"] = 0.0 if cat in CAUSE_CATEGORIES else None
        claims[cid] = sc
    outcome, column = combine_claims(claims)
    return {"task": answer["id"], "type": answer["type"], "category": cat, "arm": pred["arm"], "run": pred["run"],
            "truth": "cause" if cat in CAUSE_CATEGORIES else "no_cause", "outcome": outcome, "column": column,
            "source": source_of(answer["id"]), "answer": answer_signature(claims),
            "correct": all(c["correct"] for c in claims.values()),
            "correct_set": all(c.get("correct_set", c["correct"]) for c in claims.values()),
            "correct_in_set": all(c.get("correct_in_set", c["correct"]) for c in claims.values()),
            "oos_diagnosed": any(c.get("oos_diagnosed") for c in claims.values()),
            "false_attr": any(c["false_attr"] for c in claims.values()),
            "gap_closed": next(iter(claims.values()))["gap_closed"], "claims": claims,
            "cost_usd": round(pred["cost_usd"], 5), "wall_s": pred["wall_s"], "runs": pred["runs"],
            "setup_runs": pred["setup_runs"]}


MATRIX_COLUMNS = ("correct_cause", "partial", "wrong_confident", "abstained", "missed")


def trust_matrix(rs: list[dict]) -> dict:
    """Rows: what the truth was ("cause", "no_cause"). Columns: what the arm said (MATRIX_COLUMNS).

    "abstained" is an honest no-answer (Unexplained, Inconclusive, Reproduced, or a hedge on a task
    with no cause); "missed" is a crashed run or a hedged answer with the wrong knobs; "partial"
    names only some of an interacting cause. Each row sums to its number of runs.
    """
    return {truth: {**{c: sum(r.get("truth") == truth and r.get("column") == c for r in rs)
                       for c in MATRIX_COLUMNS},
                    "runs": sum(r.get("truth") == truth for r in rs)}
            for truth in ("cause", "no_cause")}


def answer_signature(claims: dict[str, dict]) -> str:
    """What a run answered, comparable across runs: the normalised knobs per claim, or "abstain"."""
    parts = []
    for cid in sorted(claims):
        c = claims[cid]
        if not c["knobs"] or c["label"] in NOT_AN_ANSWER:
            parts.append(f"{cid}:abstain")
        else:
            parts.append(f"{cid}:" + ",".join(f"{k}={v}" for k, v in sorted(_knob_dict(c["knobs"]).items())))
    return ";".join(parts)


def answer_stability(rs: list[dict]) -> dict:
    """Per task, the share of runs that gave the most common answer (1.0 = the same every time).
    Only tasks with at least two runs count. `mean` averages over those tasks."""
    per_task = {}
    for t in sorted({r["task"] for r in rs}):
        sigs = [r["answer"] for r in rs if r["task"] == t and "answer" in r]
        if len(sigs) >= 2:
            per_task[t] = round(max(map(sigs.count, set(sigs))) / len(sigs), 3)
    return {"mean": round(statistics.mean(per_task.values()), 3) if per_task else None,
            "tasks_compared": len(per_task), "per_task": per_task}


def source_of(task_id: str) -> str:
    """Where a task came from, by id: the sealed generator, the AI author, or the dev set."""
    for prefix, source in (("test-gen-", "generator"), ("test-v11-", "generator_v11"), ("test-v12-", "generator_v12"), ("test-v13-", "generator_v13"), ("test-ai-", "ai_author"),
                           ("dev-", "dev")):
        if task_id.startswith(prefix):
            return source
    return "other"


def summarise_by_source(rows: list[dict]) -> dict:
    return {src: summarise([r for r in rows if source_of(r["task"]) == src])
            for src in sorted({source_of(r["task"]) for r in rows})}


def outcome_stats(rs: list[dict]) -> dict:
    """Counts of each outcome and the rates (with 95% Wilson intervals) for one group of runs.

    Denominators: correct, partial and missed are out of the runs on tasks that have a cause;
    correct_abstention is out of the runs on tasks that have none; confidently_wrong is out of all.
    """
    n_cause = sum(r.get("truth") == "cause" for r in rs)
    n_none = len(rs) - n_cause

    def count(outcome: str) -> int:
        return sum(r.get("outcome") == outcome for r in rs)

    denom = {"correct": n_cause, "partial": n_cause, "missed": n_cause, "confidently_wrong": len(rs),
             "correct_abstention": n_none}
    return {"counts": {o: count(o) for o in OUTCOMES}, "runs_with_cause": n_cause, "runs_without_cause": n_none,
            # the safety number, first and exact: Wilson is optimistic near 0
            "confidently_wrong_exact": clopper_pearson(count("confidently_wrong"), len(rs)),
            "rates": {o: wilson(count(o), denom[o]) for o in OUTCOMES}, "trust_matrix": trust_matrix(rs)}


def balanced_scores(rs: list[dict]) -> dict:
    """In-space recall, out-of-space/no-cause specificity, their mean, and the out-of-space diagnosis rate.
    The always-'Unexplained' abstainer scores recall 0, specificity 1, balanced 0.5 and diagnosis 0."""
    cause = [r for r in rs if r.get("truth") == "cause"]
    none = [r for r in rs if r.get("truth") != "cause"]
    oos = [r for r in rs if r.get("category") in OUT_OF_SPACE_CATEGORIES]
    recall = sum(r.get("outcome") == "correct" for r in cause) / len(cause) if cause else None
    spec = sum(r.get("outcome") == "correct_abstention" for r in none) / len(none) if none else None
    return {"in_space_recall": None if recall is None else round(recall, 3),
            "no_cause_specificity": None if spec is None else round(spec, 3),
            "balanced_accuracy": round((recall + spec) / 2, 3) if recall is not None and spec is not None else None,
            "out_of_space_diagnosed": f"{sum(r.get('oos_diagnosed', False) for r in oos)}/{len(oos)}" if oos else None}


def trivial_abstainer(rows: list[dict]) -> dict:
    """The always-'Unexplained' system, scored on the same runs: shown next to every arm."""
    arm = rows[0]["arm"] if rows else None
    rs = [r for r in rows if r["arm"] == arm]
    cause = sum(r.get("truth") == "cause" for r in rs)
    return {"runs": len(rs), "correct_causes": 0, "confidently_wrong": 0,
            "correct_abstentions": len(rs) - cause, "in_space_recall": 0.0 if cause else None,
            "no_cause_specificity": 1.0 if len(rs) - cause else None,
            "balanced_accuracy": 0.5 if cause and len(rs) - cause else None, "out_of_space_diagnosed": 0}


def summarise(rows: list[dict]) -> dict:
    out = {}
    for arm in sorted({r["arm"] for r in rows}):
        rs = [r for r in rows if r["arm"] == arm]
        tasks = sorted({r["task"] for r in rs})
        per_task_correct = {t: [r["correct"] for r in rs if r["task"] == t] for t in tasks}
        solved = sum(statistics.median(map(int, v)) >= 0.5 for v in per_task_correct.values())
        closed = [r["gap_closed"] for r in rs if r.get("gap_closed") is not None]
        out[arm] = {
            "tasks": len(tasks),
            "runs": len(rs),
            "solved_median_run": solved,
            "solved_median_run_ci": wilson(solved, len(tasks)),  # over tasks: runs of one task are correlated
            "solved_best_run": sum(any(v) for v in per_task_correct.values()),
            "false_attribution_rate": round(sum(r["false_attr"] for r in rs) / len(rs), 3),
            "median_cost_usd": round(statistics.median(r["cost_usd"] for r in rs), 4),
            "median_wall_s": statistics.median(r["wall_s"] for r in rs),
            "total_cost_usd": round(sum(r["cost_usd"] for r in rs), 4),
            "total_wall_s": round(sum(r["wall_s"] for r in rs), 1),
            "median_gap_closed": round(statistics.median(closed), 3) if closed else None,
            "mean_experiments": round(statistics.mean(r.get("runs", 0) for r in rs), 1),
            "total_experiments": sum(r.get("runs", 0) for r in rs),
            "answer_stability": answer_stability(rs),
            # cause runs whose answer was right as a set (true values inside the equally-good sets)
            "correct_set_causes": sum(r.get("correct_set", False) for r in rs if r.get("truth") == "cause"),
            # cause runs whose configuration set (at most SET_K) contains the true configuration
            "correct_in_set_causes": sum(r.get("correct_in_set", False) for r in rs if r.get("truth") == "cause"),
            **balanced_scores(rs),
            **outcome_stats(rs),
        }
    return out


async def main_async(split: str, n: int, out: Path | None, answers_dir: Path | None = None,
                     runs: set[int] | None = None) -> None:
    import yaml

    rows = []
    for task_dir in sorted((GB / "tasks").iterdir()):
        if not (task_dir / "task.yaml").exists():
            continue
        task = yaml.safe_load((task_dir / "task.yaml").read_text(encoding="utf-8"))
        if task["split"] != split:
            continue
        for run_dir in sorted((GB / "runs" / task["id"]).glob("*/run*")):
            if runs is not None and run_dir.name not in {f"run{k}" for k in runs}:
                continue
            if (run_dir / "prediction.json").exists():
                rows.append(await score_run(task_dir, run_dir, n, answers_dir))
    for r in rows:
        print(f"{r['task']:20s} {r['arm']:20s} run{r['run']}  correct={r['correct']!s:5s} "
              f"false_attr={r['false_attr']!s:5s} gap_closed={r['gap_closed']}  ${r['cost_usd']:.4f}  "
              f"{ {c: (v['label'], v['knobs']) for c, v in r['claims'].items()} }")
    summary = summarise(rows) if rows else {}
    if rows:  # the trivial system every safety number must be read against
        summary["always-unexplained (trivial)"] = trivial_abstainer(rows)
    by_source = summarise_by_source(rows) if rows else {}
    print(json.dumps(summary, indent=1))
    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({"split": split, "summary": summary, "by_source": by_source, "rows": rows}, indent=1))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--split", default="dev")
    p.add_argument("--remeasure", type=int, default=3)
    p.add_argument("--out", type=Path)
    p.add_argument("--answers", type=Path,
                   help="read answer.json (and hidden task fields) from <dir>/<task>/ instead of the task folder")
    p.add_argument("--runs", help="comma-separated run numbers to score, e.g. 4,5,6 (default: all runs)")
    a = p.parse_args()
    runs = {int(k) for k in a.runs.split(",")} if a.runs else None
    asyncio.run(main_async(a.split, a.remeasure, a.out, a.answers, runs))
