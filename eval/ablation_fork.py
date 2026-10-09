"""Fork vs no-fork ablation on RusKey: what checkpoint forking saves. Free: reads event logs only.

    python eval/ablation_fork.py papers/ruskey/ablation/fork papers/ruskey/ablation/nofork \
        --relabel <fork re-label run dir> <nofork re-label run dir> \
        --reference papers/ruskey/search_final --wall papers/ruskey/ablation/wall_times.txt \
        --out eval/results/ablation_ruskey.json

(The re-label dirs come from `gapfinder search --resume <arm>/events.jsonl --max-runs 22`, which
labels again from the recorded runs only; their reports are kept as <arm>/gap_report_relabelled.*.)

Both arms ran the same bounded search (same spec, ledger, targets, 30-run budget). With forking,
every branch starts from one loaded-database checkpoint; without it, every branch rebuilds and
reloads the database first. Setup work is read from checkpoint events, branch work from
branch_finished events. Costs are the sandbox's reported cost (Sandboxes are unbilled in Beta).
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
from pathlib import Path


def _load(run_dir: Path) -> list[dict]:
    return [json.loads(x) for x in (run_dir / "events.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]


def _cv(vals: list[float]) -> float | None:
    return round(statistics.stdev(vals) / statistics.mean(vals), 3) if len(vals) >= 2 and statistics.mean(vals) else None


def _labels(report: dict) -> dict:
    return {c["target"]["claim_id"]: (c["attribution"] or {}).get("confidence_label", "Reproduced")
            for c in report.get("claims", [])}


def arm(run_dir: Path, metrics: list[str]) -> dict:
    ev = _load(run_dir)
    # setups: build/load stages that ran (branch results are checkpoints too, stage "branch")
    setups = [e["node"] for e in ev if e["type"] == "checkpoint" and e["node"].get("command")
              and e["node"]["stage"] != "branch"]
    branches = [e["branch"] for e in ev if e["type"] == "branch_finished"]
    created = {e["branch"]["id"] for e in ev if e["type"] == "branch_created"}
    loads = [n for n in setups if n["stage"] == "loaded"]
    noise = [b for b in branches if b.get("note") == "noise" and b["status"] == "succeeded"]
    report = json.loads((run_dir / "gap_report.json").read_text(encoding="utf-8"))
    return {
        "branches_recorded": len(branches),
        "branches_unrecorded": len(created - {b["id"] for b in branches}),
        "setup_runs": len(setups),
        "setup_runs_by_stage": {st: sum(n["stage"] == st for n in setups) for st in ("built", "loaded")},
        "database_loads": len(loads),
        "distinct_loaded_checkpoints": len({n["id"] for n in loads}),
        "setup_elapsed_s": round(sum(n["elapsed_s"] for n in setups), 1),
        "setup_cost_usd": round(sum(n["cost_usd"] for n in setups), 3),
        "branch_elapsed_s": round(sum(b["resources"]["elapsed_s"] for b in branches), 1),
        "branch_cost_usd": round(sum(b["resources"]["cost_usd"] for b in branches), 3),
        "total_cost_usd": round(sum(n["cost_usd"] for n in setups) + sum(b["resources"]["cost_usd"] for b in branches), 3),
        "noise_runs": {m: [round(b["parsed_metrics"][m], 4) for b in noise if m in b["parsed_metrics"]] for m in metrics},
        "noise_cv": {m: _cv([b["parsed_metrics"][m] for b in noise if m in b["parsed_metrics"]]) for m in metrics},
        "noise_parents": len({b["parent_checkpoint"] for b in noise}),
        "labels": _labels(report),
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("fork", type=Path)
    p.add_argument("nofork", type=Path)
    p.add_argument("--relabel", nargs=2, type=Path, help="re-labelled reports (fork, nofork)")
    p.add_argument("--reference", type=Path, help="a full search on the same spec (e.g. papers/ruskey/search_final)")
    p.add_argument("--wall", type=Path, help="ablation_summary.txt with '<arm> wall_s=N' lines")
    p.add_argument("--out", type=Path)
    a = p.parse_args()
    metrics = ["balanced_ratio_k10_k5", "balanced_ratio_k1_k5", "writeheavy_ratio_k1_k10"]
    res = {"fork": arm(a.fork, metrics), "nofork": arm(a.nofork, metrics)}
    if a.wall and a.wall.exists():
        for m in re.finditer(r"^(fork|nofork) wall_s=(\d+)", a.wall.read_text(), re.M):
            res[m.group(1)]["wall_s"] = int(m.group(2))
    if a.relabel:
        for k, d in zip(("fork", "nofork"), a.relabel):
            rep = json.loads((d / "gap_report.json").read_text(encoding="utf-8"))
            res[k]["labels_relabelled"] = _labels(rep)
    if a.reference:
        ref = _load(a.reference)
        noise = [e["branch"] for e in ref if e["type"] == "branch_finished" and e["branch"].get("note") == "noise"
                 and e["branch"]["status"] == "succeeded"]
        res["reference_load"] = {"noise_runs": {m: [round(b["parsed_metrics"][m], 4) for b in noise] for m in metrics},
                                 "noise_cv": {m: _cv([b["parsed_metrics"][m] for b in noise]) for m in metrics}}
    f, n = res["fork"], res["nofork"]
    per = lambda d, k: d[k] / max(d["branches_recorded"], 1)  # noqa: E731
    res["per_branch"] = {
        "setup_cost_usd": {"fork": round(per(f, "setup_cost_usd"), 4), "nofork": round(per(n, "setup_cost_usd"), 4)},
        "total_cost_usd": {k: round((d["setup_cost_usd"] + d["branch_cost_usd"]) / max(d["branches_recorded"], 1), 4)
                           for k, d in (("fork", f), ("nofork", n))},
        "setup_elapsed_s": {"fork": round(per(f, "setup_elapsed_s"), 2), "nofork": round(per(n, "setup_elapsed_s"), 2)},
    }
    print(json.dumps(res, indent=1))
    if a.out:
        a.out.parent.mkdir(parents=True, exist_ok=True)
        a.out.write_text(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
