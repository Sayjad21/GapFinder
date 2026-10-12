"""Summarise the Step 5 confirmation runs (run.json in this folder) against the paper (ICML Table 1)
and the naive noise band (GapFinder's definition: 2 x MAD of the naive repeats).
Usage: python summarize.py  (writes summary.json next to this file, prints a table)"""
import json
import statistics as st
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXT = HERE.parent
PAPER = {"energy_rmse": 1.66, "yacht_rmse": 1.11}
NAMES = {"": "naive defaults (epochx=500 hidden=2)", "epochx=10,hidden=1": "documented cause (epochx=10 hidden=1)",
         "epochx=10": "epochx=10 alone", "hidden=1": "hidden=1 alone"}


def band(v):
    m = st.median(v)
    return 2 * st.median(abs(x - m) for x in v)


def naive_from_events(path):
    out = {"energy_rmse": [], "yacht_rmse": []}
    for line in path.read_text(encoding="utf-8").splitlines():
        e = json.loads(line)
        if e["type"] == "branch_finished" and not e["branch"]["knob_changes"] and e["branch"]["status"] == "succeeded":
            for k in out:
                out[k].append(e["branch"]["parsed_metrics"][k])
    return out


run = json.loads((HERE / "run.json").read_text(encoding="utf-8"))
cfg = {}
for b in run["branches"]:
    key = ",".join(f"{k}={v}" for k, v in sorted(b["knob_changes"].items()))
    cfg.setdefault(key, []).append(b)
naive = {m: [b["parsed_metrics"][m] for b in cfg[""]] for m in PAPER}
pooled = {m: [] for m in PAPER}
arms = {"run-normal (local)": EXT / "attempt2-local/run-normal", "run-evidence-off (local)": EXT / "attempt2-local/run-evidence-off",
        "run-no-README": EXT / "run-no-README", "run-all-flags-random": EXT / "run-all-flags-random"}
arm_naive = {}
for name, d in arms.items():
    v = naive_from_events(d / "events.jsonl")
    arm_naive[name] = {m: {"n": len(v[m]), "median": st.median(v[m]), "band": band(v[m])} for m in PAPER}
    for m in PAPER:
        pooled[m] += v[m]
summary = {"paper": PAPER, "naive_band_this_batch": {m: band(naive[m]) for m in PAPER},
           "naive_pooled_all_arms_plus_this_batch": {m: {"n": len(pooled[m]) + len(naive[m]), "median": st.median(pooled[m] + naive[m]),
                                                        "sd": st.stdev(pooled[m] + naive[m]), "band": band(pooled[m] + naive[m])} for m in PAPER},
           "arm_naive_bands": arm_naive, "configs": {}}
print(f"{'configuration':42s} {'metric':12s} runs{'':22s} median  gap to paper")
for key in ["epochx=10,hidden=1", "epochx=10", "hidden=1", ""]:
    row = {}
    for m, paper in PAPER.items():
        vals = [b["parsed_metrics"][m] for b in cfg[key]]
        med = st.median(vals)
        row[m] = {"runs": vals, "median": med, "gap_to_paper_abs": med - paper, "gap_to_paper_pct": 100 * (med - paper) / paper,
                  "shift_from_naive": med - st.median(naive[m])}
        print(f"{NAMES[key]:42s} {m:12s} {', '.join(f'{x:.3f}' for x in vals):26s} {med:.3f}  {med - paper:+.3f} ({100 * (med - paper) / paper:+.1f}%)")
    row["run_tags"] = [b["run_tag"] for b in cfg[key]]
    row["elapsed_s"] = [round(b["resources"]["elapsed_s"]) for b in cfg[key]]
    summary["configs"][key or "naive"] = row
print("naive band (2xMAD, this batch):", {m: round(v, 4) for m, v in summary["naive_band_this_batch"].items()})
print("naive pooled over 23 runs:", {m: {k: round(x, 4) for k, x in v.items()} for m, v in summary["naive_pooled_all_arms_plus_this_batch"].items()})
(HERE / "summary.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
