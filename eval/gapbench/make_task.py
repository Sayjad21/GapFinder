"""Build a GapBench-mini task from its task.yaml: run the hidden config, write the mini-paper.

    python eval/gapbench/make_task.py eval/gapbench/tasks/dev-ml-normalize

task.yaml fields:
    id, family (rlbench|mlbench|...), split (dev|test), type
      (single_unstated | stated_code_differs | interaction | no_cause)
    hidden:  knob changes the "authors" used (the answer key)
    offset:  no_cause only: {metric: factor} applied to the naive numbers
    claims:  [{claim_id, metric, figure, held_out}]
    paper:   mini-paper text with {metric:.3f}-style placeholders
    repeats: runs per configuration (default 7)

Writes, next to task.yaml:
    paper.md        what agents read (no hidden values unless the paper states them)
    targets.json    claims with the paper's numbers (also in paper.md)
    answer.json     the answer key: hidden config and expected label. Agents never see it.
    calibration.json naive vs hidden medians, noise bands, effect in noise units

A task is rejected unless its primary claim's gap is at least `min_units` noise bands.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import statistics
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from gapfinder.sandbox.backend import LocalBackend  # noqa: E402
from gapfinder.sandbox.events import EventLog  # noqa: E402
from gapfinder.sandbox.noise import noise_band  # noqa: E402
from gapfinder.sandbox.runner import Orchestrator  # noqa: E402
from gapfinder.sandbox.spec import HarnessSpec  # noqa: E402

EXPECTED = {
    "single_unstated": "Explained",
    "stated_code_differs": "Paper-artifact inconsistency",
    "interaction": "Explained",
    "no_cause": "Unexplained",
}


async def build(task_dir: Path, min_units: float = 3.0) -> dict:
    task = yaml.safe_load((task_dir / "task.yaml").read_text(encoding="utf-8"))
    spec = HarnessSpec.load_yaml(ROOT / "eval" / "gapbench" / f"{task['family']}.yaml")
    n = task.get("repeats", 7)
    with tempfile.TemporaryDirectory() as tmp:
        orch = Orchestrator(LocalBackend(Path(tmp) / "sbx"), spec, EventLog(Path(tmp) / "ev.jsonl"))
        naive_runs, hidden_runs = await asyncio.gather(orch.fanout([{}] * n), orch.fanout([task["hidden"]] * n))
    metrics = [c["metric"] for c in task["claims"]]

    def med(runs, m):
        return statistics.median(b.parsed_metrics[m] for b in runs if m in b.parsed_metrics)

    calib, paper_vals = {}, {}
    for m in metrics:
        vals = [b.parsed_metrics[m] for b in naive_runs if m in b.parsed_metrics]
        band = noise_band(m, vals, floor_frac=0.01).band
        naive = statistics.median(vals)
        value = naive * task["offset"][m] if task["type"] == "no_cause" else med(hidden_runs, m)
        paper_vals[m] = round(value, 4)
        calib[m] = {"naive": naive, "paper": paper_vals[m], "band": band,
                    "units": abs(paper_vals[m] - naive) / band if band else float("inf")}
    primary = [c for c in task["claims"] if not c.get("held_out")]
    weak = [c["metric"] for c in primary if calib[c["metric"]]["units"] < min_units]
    if weak:
        raise SystemExit(f"{task['id']}: gap on {weak} is under {min_units} noise bands: {calib}")

    paper = task["paper"].format(**paper_vals)
    (task_dir / "paper.md").write_text(paper, encoding="utf-8", newline="\n")
    targets = [{"claim_id": c["claim_id"], "metric": c["metric"], "paper_value": paper_vals[c["metric"]],
                "held_out": bool(c.get("held_out"))} for c in task["claims"]]
    (task_dir / "targets.json").write_text(json.dumps(targets, indent=1), encoding="utf-8", newline="\n")
    answer = {"id": task["id"], "type": task["type"], "hidden": task.get("hidden", {}),
              "expected_label": EXPECTED[task["type"]], "primary_claims": [c["claim_id"] for c in primary]}
    (task_dir / "answer.json").write_text(json.dumps(answer, indent=1), encoding="utf-8", newline="\n")
    (task_dir / "calibration.json").write_text(json.dumps({"repeats": n, "metrics": calib}, indent=1),
                                               encoding="utf-8", newline="\n")
    return {"id": task["id"], "calibration": calib}


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("task_dirs", nargs="+", type=Path)
    p.add_argument("--min-units", type=float, default=3.0)
    a = p.parse_args()
    for d in a.task_dirs:
        r = asyncio.run(build(d, a.min_units))
        print(r["id"], {m: f"naive {v['naive']:.3f} -> paper {v['paper']:.3f} ({v['units']:.1f} bands)"
                        for m, v in r["calibration"].items()})
