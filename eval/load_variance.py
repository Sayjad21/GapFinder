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


def naive_by_load(run_dir: Path) -> dict[str, list[dict]]:
    """Parsed metrics of every successful naive branch, keyed by the checkpoint it forked from."""
    ev = [json.loads(x) for x in (run_dir / "events.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
    by_parent: dict[str, list[dict]] = {}
    for e in ev:
        b = e.get("branch") if e["type"] == "branch_finished" else None
        if b and b["knob_changes"] == {} and b["status"] == "succeeded":
            by_parent.setdefault(b["parent_checkpoint"], []).append(b["parsed_metrics"])
    return by_parent


def loads(run_dir: Path) -> list[dict]:
    by_parent = naive_by_load(run_dir)
    return [{"run": str(run_dir).replace("\\", "/"), "load": p, "n": len(ms),
             **{c: round(statistics.median(m[k] for m in ms), 3) for c, k in METRICS.items()}}
            for p, ms in by_parent.items()]


def _mad(xs: list[float]) -> float:
    m = statistics.median(xs)
    return statistics.median(abs(x - m) for x in xs)


def _stats(xs: list[float]) -> dict:
    return {"n": len(xs), "median": round(statistics.median(xs), 3), "mad": round(_mad(xs), 3),
            "min": round(min(xs), 3), "max": round(max(xs), 3)}


def comparability(runs: list[Path]) -> dict:
    """Naive runs forked from a shared load (a load with 2+ naive runs) vs runs on a fresh, independent
    load (a load with exactly one naive run). Band = fresh median +/- 2 MAD, and the fresh min-max."""
    forked_loads: dict[str, list[dict]] = {}
    fresh: list[dict] = []
    for d in runs:
        for load, ms in naive_by_load(d).items():
            if len(ms) >= 2:
                forked_loads[load] = ms
            else:
                fresh.extend(ms)
    forked = [m for ms in forked_loads.values() for m in ms]
    out = {"forked_loads": len(forked_loads), "forked_runs": len(forked), "fresh_loads": len(fresh), "metrics": {}}
    for c, k in METRICS.items():
        f, g = [m[k] for m in forked], [m[k] for m in fresh]
        if not f or not g:
            continue
        band = (statistics.median(g) - 2 * _mad(g), statistics.median(g) + 2 * _mad(g))
        per_load = {l: round(statistics.median(m[k] for m in ms), 3) for l, ms in forked_loads.items()}
        inside = [band[0] <= x <= band[1] for x in per_load.values()]
        in_range = [min(g) <= x <= max(g) for x in per_load.values()]
        out["metrics"][c] = {
            "metric": k, "forked": _stats(f), "fresh": _stats(g),
            "fresh_band_2mad": [round(band[0], 3), round(band[1], 3)],
            "forked_load_medians": per_load,
            "forked_within_load_mad": {l: round(_mad([m[k] for m in ms]), 3) for l, ms in forked_loads.items()},
            "forked_runs_inside_band": sum(band[0] <= x <= band[1] for x in f),
            "forked_load_medians_inside_band": sum(inside),
            "forked_load_medians_inside_minmax": sum(in_range),
            "forked_loads": len(per_load),
            "forked_median_inside_band": all(inside),
            "forked_spread_vs_fresh": round(_mad(f) / _mad(g), 3) if _mad(g) else None,
        }
    return out


def comparability_text(res: dict) -> str:
    lines = [f"forked: {res['forked_runs']} runs from {res['forked_loads']} loads; fresh: {res['fresh_loads']} independent loads (1 run each)"]
    for c, m in res["metrics"].items():
        verdict = "inside" if m["forked_median_inside_band"] else "OUTSIDE"
        lines.append(f"{c}: forked median {m['forked']['median']} (MAD {m['forked']['mad']}, {m['forked']['min']}-{m['forked']['max']}); "
                     f"fresh median {m['fresh']['median']} (MAD {m['fresh']['mad']}, {m['fresh']['min']}-{m['fresh']['max']}); "
                     f"band {m['fresh_band_2mad'][0]}-{m['fresh_band_2mad'][1]}; forked load medians {list(m['forked_load_medians'].values())}: "
                     f"{m['forked_load_medians_inside_band']}/{m['forked_loads']} {verdict} the band")
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("runs", nargs="+", type=Path)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--comparability-out", type=Path, help="write forked-vs-fresh comparability here")
    a = ap.parse_args()
    rows = [r for d in a.runs for r in loads(d)]
    summary = {c: {"paper": PAPER[c], "min": min(r[c] for r in rows), "median": round(statistics.median(r[c] for r in rows), 3),
                   "max": max(r[c] for r in rows)} for c in METRICS}
    res = {"loads": len(rows), "distinct_checkpoints": len({r["load"] for r in rows}), "summary": summary, "rows": rows}
    print(f"{len(rows)} loads")
    for c, s in summary.items():
        print(f"{c}: paper {s['paper']}, across loads {s['min']}-{s['max']} (median {s['median']})")
    comp = comparability(a.runs)
    print(comparability_text(comp))
    if a.comparability_out:
        a.comparability_out.parent.mkdir(parents=True, exist_ok=True)
        a.comparability_out.write_text(json.dumps(comp, indent=1))
    if a.out:
        a.out.parent.mkdir(parents=True, exist_ok=True)
        a.out.write_text(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
