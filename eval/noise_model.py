"""Honest noise model from recorded runs (offline, free). Phase 2, item 12.

    python eval/noise_model.py papers/ruskey/search_final papers/ruskey/ablation/fork \
        papers/ruskey/ablation/nofork papers/ruskey/search_setups --targets papers/ruskey/targets_fig6.json

Every naive-configuration run is grouped by the checkpoint it forked from (its load). A one-way
random-effects ANOVA splits the variance into:
- within one load (fork-to-fork): what forked repeats measure;
- between loads (setup-to-setup): what forked repeats can't see.

Forks of one load are pseudo-replicates (Hurlbert 1984) for any claim about the paper's setup, so the
right error term is the total.

It also reports the minimum detectable effect (MDE) for comparing two configurations with n runs each:

    MDE = (t_{1-a/2, df} + t_{1-b, df}) * sigma * sqrt(2 / n),   a = 0.05, power 1 - b = 0.8

A gap smaller than the MDE should read Inconclusive, not Unexplained, and never be attributed.
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from gapfinder.sandbox.noise import mde  # noqa: E402


def naive_by_load(run_dirs: list[Path], metrics: list[str]) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    for d in run_dirs:
        f = d / "events.jsonl"
        if not f.exists():
            continue
        for line in f.read_text(encoding="utf-8").splitlines():
            e = json.loads(line)
            b = e.get("branch") if e.get("type") == "branch_finished" else None
            if b and b["knob_changes"] == {} and b["status"] == "succeeded" and all(m in b["parsed_metrics"] for m in metrics):
                out.setdefault(f"{d.name}:{b['parent_checkpoint'][:8]}", []).append(b["parsed_metrics"])
    return out


def components(groups: list[list[float]]) -> dict:
    """One-way random-effects ANOVA with unequal group sizes (method of moments)."""
    groups = [g for g in groups if g]
    k, N = len(groups), sum(len(g) for g in groups)
    grand = statistics.fmean(x for g in groups for x in g)
    ss_w = sum((x - statistics.fmean(g)) ** 2 for g in groups for x in g)
    ss_b = sum(len(g) * (statistics.fmean(g) - grand) ** 2 for g in groups)
    df_w, df_b = N - k, k - 1
    ms_w = ss_w / df_w if df_w > 0 else float("nan")
    ms_b = ss_b / df_b if df_b > 0 else float("nan")
    n0 = (N - sum(len(g) ** 2 for g in groups) / N) / df_b if df_b > 0 else float("nan")
    var_load = max(0.0, (ms_b - ms_w) / n0) if df_b > 0 and df_w > 0 else float("nan")
    return {"loads": k, "runs": N, "sd_within_load": math.sqrt(ms_w) if df_w > 0 else None,
            "sd_between_loads": math.sqrt(var_load) if not math.isnan(var_load) else None,
            "sd_total": math.sqrt(ms_w + var_load) if df_w > 0 and not math.isnan(var_load) else None,
            "grand_mean": grand}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("runs", nargs="+", type=Path)
    ap.add_argument("--targets", type=Path, required=True)
    ap.add_argument("--n", default="3,5", help="runs per arm for the MDE")
    ap.add_argument("--out", type=Path)
    a = ap.parse_args()
    targets = json.loads(a.targets.read_text(encoding="utf-8"))
    metrics = [t["metric"] for t in targets]
    loads = naive_by_load(a.runs, metrics)
    res = {"loads": {k: len(v) for k, v in loads.items()}, "claims": {}}
    for t in targets:
        c = components([[m[t["metric"]] for m in ms] for ms in loads.values()])
        z, mean = t["paper_value"], c["grand_mean"]
        gap = abs(z - mean)
        row = {**{k: (round(v, 4) if isinstance(v, float) else v) for k, v in c.items()}, "paper": z,
               "gap_abs": round(gap, 4), "gap_pct": round(100 * (mean - z) / z, 1), "mde": {}}
        for n in map(int, a.n.split(",")):
            row["mde"][n] = {"fork_sd": round(mde(c["sd_within_load"], n), 4) if c["sd_within_load"] else None,
                             "total_sd": round(mde(c["sd_total"], n), 4) if c["sd_total"] else None}
        sd = c["sd_total"] or c["sd_within_load"]
        row["verdict_n5"] = ("detectable" if sd and gap > mde(sd, 5) else "below the minimum detectable effect")
        res["claims"][t["claim_id"]] = row
        print(f"{t['claim_id']} ({t['metric']}): paper {z}, naive mean {mean:.3f} ({row['gap_pct']:+}%); "
              f"sd within load {c['sd_within_load'] and round(c['sd_within_load'], 3)}, between loads "
              f"{c['sd_between_loads'] and round(c['sd_between_loads'], 3)}, total {c['sd_total'] and round(c['sd_total'], 3)}; "
              f"MDE n=5: fork {row['mde'].get(5, {}).get('fork_sd')}, total {row['mde'].get(5, {}).get('total_sd')} "
              f"-> {row['verdict_n5']}")
    print(f"{len(loads)} loads, {sum(len(v) for v in loads.values())} naive runs")
    if a.out:
        a.out.parent.mkdir(parents=True, exist_ok=True)
        a.out.write_text(json.dumps(res, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
