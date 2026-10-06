"""Score predictions against answer keys; re-measure every proposed configuration.

    python eval/gapbench/score.py [--split dev|test] [--remeasure 3] [--out eval/results/gapbench_dev.json]

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

Scoring is deterministic given the prediction files and the re-measurements, which are cached
in each run directory, so rescoring from saved logs reproduces every number.
"""

from __future__ import annotations

import argparse
import asyncio
import json
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
NOT_AN_ANSWER = {"Unexplained", "Reproduced", "missing"}


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


def score_claim(answer: dict, pred: dict | None) -> dict:
    pred = pred or {"label": "missing", "knobs": {}}
    proposed = pred["label"] not in NOT_AN_ANSWER and bool(pred["knobs"])
    confident = pred["label"] in CONFIDENT and bool(pred["knobs"])
    if answer["type"] == "no_cause":
        correct = not confident
    else:
        correct = proposed and same_knobs(pred["knobs"], answer["hidden"])
    return {"label": pred["label"], "knobs": pred["knobs"], "confident": confident,
            "correct": correct, "false_attr": confident and not correct}


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


async def score_run(task_dir: Path, run_dir: Path, n: int) -> dict:
    answer = json.loads((task_dir / "answer.json").read_text())
    calib = json.loads((task_dir / "calibration.json").read_text())["metrics"]
    targets = {t["claim_id"]: t for t in json.loads((task_dir / "targets.json").read_text())}
    pred = json.loads((run_dir / "prediction.json").read_text())
    claims = {}
    for cid in answer["primary_claims"]:
        sc = score_claim(answer, pred["claims"].get(cid))
        t = targets[cid]
        if answer["type"] != "no_cause" and sc["knobs"]:
            m = await remeasure(task_dir, sc["knobs"], n, run_dir / "remeasure.json")
            g0 = abs(calib[t["metric"]]["naive"] - t["paper_value"])
            sc["gap_closed"] = None if m is None else round(1 - abs(m[t["metric"]] - t["paper_value"]) / g0, 3)
        else:
            sc["gap_closed"] = 0.0 if answer["type"] != "no_cause" else None
        claims[cid] = sc
    return {"task": answer["id"], "type": answer["type"], "arm": pred["arm"], "run": pred["run"],
            "correct": all(c["correct"] for c in claims.values()),
            "false_attr": any(c["false_attr"] for c in claims.values()),
            "gap_closed": next(iter(claims.values()))["gap_closed"], "claims": claims,
            "cost_usd": round(pred["cost_usd"], 5), "wall_s": pred["wall_s"], "runs": pred["runs"],
            "setup_runs": pred["setup_runs"]}


def summarise(rows: list[dict]) -> dict:
    out = {}
    for arm in sorted({r["arm"] for r in rows}):
        rs = [r for r in rows if r["arm"] == arm]
        tasks = sorted({r["task"] for r in rs})
        per_task_correct = {t: [r["correct"] for r in rs if r["task"] == t] for t in tasks}
        out[arm] = {
            "tasks": len(tasks),
            "runs": len(rs),
            "solved_median_run": sum(statistics.median(map(int, v)) >= 0.5 for v in per_task_correct.values()),
            "solved_best_run": sum(any(v) for v in per_task_correct.values()),
            "false_attribution_rate": round(sum(r["false_attr"] for r in rs) / len(rs), 3),
            "median_cost_usd": round(statistics.median(r["cost_usd"] for r in rs), 4),
            "median_wall_s": statistics.median(r["wall_s"] for r in rs),
        }
    return out


async def main_async(split: str, n: int, out: Path | None) -> None:
    import yaml

    rows = []
    for task_dir in sorted((GB / "tasks").iterdir()):
        if not (task_dir / "task.yaml").exists():
            continue
        task = yaml.safe_load((task_dir / "task.yaml").read_text(encoding="utf-8"))
        if task["split"] != split:
            continue
        for run_dir in sorted((GB / "runs" / task["id"]).glob("*/run*")):
            if (run_dir / "prediction.json").exists():
                rows.append(await score_run(task_dir, run_dir, n))
    for r in rows:
        print(f"{r['task']:20s} {r['arm']:20s} run{r['run']}  correct={r['correct']!s:5s} "
              f"false_attr={r['false_attr']!s:5s} gap_closed={r['gap_closed']}  ${r['cost_usd']:.4f}  "
              f"{ {c: (v['label'], v['knobs']) for c, v in r['claims'].items()} }")
    summary = summarise(rows) if rows else {}
    print(json.dumps(summary, indent=1))
    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({"split": split, "summary": summary, "rows": rows}, indent=1))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--split", default="dev")
    p.add_argument("--remeasure", type=int, default=3)
    p.add_argument("--out", type=Path)
    a = p.parse_args()
    asyncio.run(main_async(a.split, a.remeasure, a.out))
