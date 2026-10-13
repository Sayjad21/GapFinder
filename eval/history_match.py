"""Multi-claim history matching over recorded runs (offline; free). Phase 2, item 10, validated on logs.

    python eval/history_match.py --targets eval/external/mc-dropout/targets_mcd.json \
        eval/external/mc-dropout/posthoc/run eval/external/mc-dropout/confirm

For every measured configuration x and every claim i (targets and held-out claims), the implausibility is

    I_i(x) = |z_i - m_i(x)| / sqrt(s_i^2 / p + s_i^2 / n_x + (d * z_i)^2)

where:
- z_i is the paper's number;
- m_i(x) is the mean of the n_x runs at x;
- s_i is the run-to-run standard deviation at the naive configuration. It enters twice: the paper's
  number is itself noisy (an average of p runs; p = 1 is the conservative default for a real paper,
  while GapBench's generator uses the median of 7, so p is about 7 / 1.57), and our mean at x is uncertain
  by s_i^2 / n_x;
- d is a discrepancy fraction for scaled surrogates (pre-registered; reported under several values).

A configuration is Not Ruled Out Yet (NROY) for claim i if I_i(x) <= 3 (Pukelsheim's 3-sigma rule), and
jointly NROY if it is NROY for every claim. The diagnosis:

| Situation | Diagnosis |
|---|---|
| the naive configuration is jointly NROY | reproduced within noise |
| some other configuration is jointly NROY | in-space explanation possible (list the set) |
| every claim has its own NROY configurations, but none is joint | **out-of-space suspected**: the claims are mutually inconsistent under every tested condition |
| some claim has no NROY configuration at all | **out-of-space likely** for that claim |

Only *tested* configurations count: an empty set means "not found among these", not "proven impossible".
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
from pathlib import Path


def load_runs(run_dirs: list[Path]) -> dict[tuple, list[dict]]:
    """Frozen config -> parsed metrics of every successful branch, over all the event logs."""
    out: dict[tuple, list[dict]] = {}
    for d in run_dirs:
        f = d / "events.jsonl" if d.is_dir() else d
        if not f.exists():  # a crashed run that never wrote a log
            continue
        for line in f.read_text(encoding="utf-8").splitlines():
            e = json.loads(line)
            if e.get("type") == "branch_finished" and e["branch"]["status"] == "succeeded":
                key = tuple(sorted(e["branch"]["knob_changes"].items()))
                out.setdefault(key, []).append(e["branch"]["parsed_metrics"])
    return out


def analyse(runs: dict[tuple, list[dict]], targets: list[dict], disc: float, cutoff: float = 3.0,
            paper_n: float = 1.0) -> dict:
    naive = runs.get((), [])
    sd = {}
    for t in targets:
        vals = [m[t["metric"]] for m in naive if t["metric"] in m]
        sd[t["metric"]] = statistics.stdev(vals) if len(vals) >= 2 else 0.0
    rows = []
    for key, ms in runs.items():
        row = {"config": dict(key), "n": len(ms), "I": {}, "mean": {}}
        for t in targets:
            vals = [m[t["metric"]] for m in ms if t["metric"] in m]
            if not vals:
                continue
            mean, s, z = statistics.fmean(vals), sd[t["metric"]], t["paper_value"]
            denom = math.sqrt(s ** 2 / paper_n + s ** 2 / len(vals) + (disc * z) ** 2) or 1e-12
            row["I"][t["claim_id"]] = round(abs(z - mean) / denom, 2)
            row["mean"][t["claim_id"]] = round(mean, 4)
        if len(row["I"]) == len(targets):
            rows.append(row)
    ids = [t["claim_id"] for t in targets]
    per_claim = {c: [r["config"] for r in rows if r["I"][c] <= cutoff] for c in ids}
    joint = [r for r in rows if max(r["I"].values()) <= cutoff]
    naive_ok = any(r["config"] == {} for r in joint)
    if naive_ok:
        diagnosis = "reproduced within noise"
    elif joint:
        diagnosis = "in-space explanation possible"
    elif all(per_claim[c] for c in ids):
        diagnosis = "out-of-space suspected: every claim fits some tested condition, but no tested condition fits them all"
    else:
        missing = [c for c in ids if not per_claim[c]]
        diagnosis = f"out-of-space likely for {', '.join(missing)}: no tested condition comes within {cutoff:g} sigma"
    return {"disc_frac": disc, "cutoff": cutoff, "paper_n": paper_n, "noise_sd": {k: round(v, 4) for k, v in sd.items()},
            "configs": len(rows), "diagnosis": diagnosis,
            "per_claim_nroy": {c: len(v) for c, v in per_claim.items()},
            "joint_nroy": sorted(({"config": r["config"], "I": r["I"], "n": r["n"]} for r in joint),
                                 key=lambda r: max(r["I"].values())),
            "closest_joint": sorted(({"config": r["config"], "I": r["I"], "mean": r["mean"], "n": r["n"]} for r in rows),
                                    key=lambda r: max(r["I"].values()))[:5]}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("runs", nargs="+", type=Path, help="run directories (or events.jsonl files) of one artifact")
    ap.add_argument("--targets", type=Path, required=True)
    ap.add_argument("--disc", default="0,0.05,0.1", help="discrepancy fractions to report (sensitivity)")
    ap.add_argument("--paper-n", type=float, default=1.0,
                    help="runs the paper's number averages (1 = conservative; GapBench's median of 7 ~ 4.5)")
    ap.add_argument("--out", type=Path)
    a = ap.parse_args()
    targets = json.loads(a.targets.read_text(encoding="utf-8"))
    runs = load_runs(a.runs)
    res = [analyse(runs, targets, float(d), paper_n=a.paper_n) for d in a.disc.split(",")]
    for r in res:
        print(f"disc {r['disc_frac']:.2f}: {r['diagnosis']}  (per-claim NROY {r['per_claim_nroy']}, joint {len(r['joint_nroy'])})")
        for c in r["closest_joint"][:3]:
            print(f"     {c['config'] or 'naive'}  I={c['I']}  mean={c['mean']}  n={c['n']}")
    if a.out:
        a.out.parent.mkdir(parents=True, exist_ok=True)
        a.out.write_text(json.dumps(res, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
