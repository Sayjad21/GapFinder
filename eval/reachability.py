"""Reachability of the true cause, from recorded runs. Free: reads event logs and answer keys only.

    python eval/reachability.py --runs 4,5,6 --out eval/results/reachability_v10.json
    python eval/reachability.py --runs 14,15,16 --arms gapfinder

For every run of a task whose answer is known, it reports:
- whether every true value was ever measured in any branch;
- whether each was measured as a single change;
- whether the true combination was ever run;
- the position of each true value among the distinct configurations screened;
- the scored outcome.

"Never reached" misses are coverage failures, which no verification can fix. "Reached but missed" is a
selection failure (an equally good fit chosen instead, or the truth rejected).

Answer keys come from eval/gapbench/sealed/<task>/answer.json (published after the v1.0 test runs)
or from the task folder (dev tasks). Outcomes come from the published score files when available.
"""

from __future__ import annotations

import argparse
import collections
import json
from pathlib import Path

GB = Path(__file__).resolve().parent / "gapbench"


def _norm(v) -> str | float:
    try:
        return round(float(v), 9)
    except (TypeError, ValueError):
        return str(v).strip().lower()


def answer_for(task: str) -> dict | None:
    for p in (GB / "sealed" / task / "answer.json", GB / "tasks" / task / "answer.json"):
        if p.exists():
            return json.loads(p.read_text(encoding="utf-8"))
    return None


def analyse_run(run_dir: Path, hidden: dict) -> dict:
    ev_path = run_dir / "events.jsonl"
    configs: list[dict] = []
    if ev_path.exists():
        for line in ev_path.read_text(encoding="utf-8").splitlines():
            e = json.loads(line)
            if e.get("type") == "branch_finished":
                kc = {k: _norm(v) for k, v in e["branch"]["knob_changes"].items()}
                if kc and kc not in configs:
                    configs.append(kc)
    truth = {k: _norm(v) for k, v in hidden.items()}
    reached = {k: any(c.get(k) == v for c in configs) for k, v in truth.items()}
    alone = {k: {k: v} in configs for k, v in truth.items()}
    position = {k: next((i for i, c in enumerate(configs) if c == {k: v}), None) for k, v in truth.items()}
    combo = any(all(c.get(k) == v for k, v in truth.items()) for c in configs) if len(truth) > 1 else None
    pred = json.loads((run_dir / "prediction.json").read_text(encoding="utf-8")) if (run_dir / "prediction.json").exists() else {}
    return {"reached_all": all(reached.values()), "reached": reached, "tested_alone": alone,
            "position_alone": position, "combo_tested": combo, "configs_tested": len(configs),
            "prediction": {c: v.get("knobs") for c, v in (pred.get("claims") or {}).items()}}


def outcomes() -> dict:
    """(task, arm, run) -> scored outcome, from every published or post-hoc score file."""
    out = {}
    for f in sorted((Path(__file__).resolve().parent / "results").glob("gapbench_*.json")):
        try:
            rows = json.loads(f.read_text(encoding="utf-8")).get("rows", [])
        except (json.JSONDecodeError, AttributeError):
            continue
        for r in rows:
            if isinstance(r, dict) and "outcome" in r:
                out[(r["task"], r["arm"], r["run"])] = r["outcome"]
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", help="comma-separated run numbers (default: all)")
    ap.add_argument("--arms", default="gapfinder,gapfinder-noevidence,gapfinder-random,gapfinder-noverify")
    ap.add_argument("--out", type=Path)
    a = ap.parse_args()
    runs = {int(x) for x in a.runs.split(",")} if a.runs else None
    arms = a.arms.split(",")
    scored = outcomes()
    rows = []
    for task_dir in sorted((GB / "runs").iterdir()):
        ans = answer_for(task_dir.name)
        if not ans or not ans.get("hidden"):
            continue  # no planted cause (no_cause, noise only): nothing to reach
        for arm in arms:
            for run_dir in sorted((task_dir / arm).glob("run*")) if (task_dir / arm).exists() else []:
                k = int(run_dir.name[3:])
                if runs and k not in runs:
                    continue
                r = analyse_run(run_dir, ans["hidden"])
                rows.append({"task": task_dir.name, "category": ans.get("category", ans.get("type")), "arm": arm,
                             "run": k, "hidden": ans["hidden"], "outcome": scored.get((task_dir.name, arm, k)), **r})
    summ: dict = collections.defaultdict(lambda: collections.Counter())
    for r in rows:
        key = (r["arm"], r["category"])
        summ[key]["runs"] += 1
        summ[key]["reached_all"] += r["reached_all"]
        if r["combo_tested"] is not None:
            summ[key]["combo_tested"] += r["combo_tested"]
        if r["outcome"]:
            summ[key][f"outcome:{r['outcome']}"] += 1
            if r["outcome"] in ("missed", "partial", "confidently_wrong"):  # a correct abstention isn't a miss
                summ[key]["miss_never_reached" if not r["reached_all"] else "miss_reached"] += 1
    summary = {f"{arm} / {cat}": dict(c) for (arm, cat), c in sorted(summ.items())}
    for k, v in summary.items():
        print(f"{k:40s} reached {v.get('reached_all', 0)}/{v['runs']}  misses: never reached {v.get('miss_never_reached', 0)}, "
              f"reached {v.get('miss_reached', 0)}")
    if a.out:
        a.out.parent.mkdir(parents=True, exist_ok=True)
        a.out.write_text(json.dumps({"summary": summary, "rows": rows}, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
