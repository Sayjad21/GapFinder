"""Naive-configuration results per database load, across RusKey runs. Free: reads event logs only.

    python eval/load_variance.py papers/ruskey/search_final papers/ruskey/ablation/fork \
        papers/ruskey/ablation/nofork papers/ruskey/search_setups --out eval/results/ruskey_load_variance.json

Every load runs the same command on the same binary. A branch's parent checkpoint identifies the
load it forked from, so grouping naive runs by parent gives one row per load.
"""

from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path

METRICS = {"C5": "balanced_ratio_k10_k5", "C5b": "balanced_ratio_k1_k5", "C3": "writeheavy_ratio_k1_k10"}
PAPER = {"C5": 1.48, "C5b": 1.341, "C3": 3.051}


def loads(run_dir: Path) -> list[dict]:
    ev = [json.loads(x) for x in (run_dir / "events.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
    by_parent: dict[str, list[dict]] = {}
    for e in ev:
        b = e.get("branch") if e["type"] == "branch_finished" else None
        if b and b["knob_changes"] == {} and b["status"] == "succeeded":
            by_parent.setdefault(b["parent_checkpoint"], []).append(b["parsed_metrics"])
    return [{"run": str(run_dir).replace("\\", "/"), "load": p, "n": len(ms),
             **{c: round(statistics.median(m[k] for m in ms), 3) for c, k in METRICS.items()}}
            for p, ms in by_parent.items()]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("runs", nargs="+", type=Path)
    ap.add_argument("--out", type=Path)
    a = ap.parse_args()
    rows = [r for d in a.runs for r in loads(d)]
    summary = {c: {"paper": PAPER[c], "min": min(r[c] for r in rows), "median": round(statistics.median(r[c] for r in rows), 3),
                   "max": max(r[c] for r in rows)} for c in METRICS}
    res = {"loads": len(rows), "distinct_checkpoints": len({r["load"] for r in rows}), "summary": summary, "rows": rows}
    print(f"{len(rows)} loads")
    for c, s in summary.items():
        print(f"{c}: paper {s['paper']}, across loads {s['min']}-{s['max']} (median {s['median']})")
    if a.out:
        a.out.parent.mkdir(parents=True, exist_ok=True)
        a.out.write_text(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
