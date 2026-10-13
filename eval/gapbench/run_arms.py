"""Run every arm on a set of GapBench tasks, with one shared ledger per task and run (about 75% cheaper).

    python eval/gapbench/run_arms.py --tasks "eval/gapbench/tasks/test-gen-*" --runs 1,2,3

For each task and run:
1. the `gapfinder` arm runs with --fresh, so it pays for the claim ledger and assumption space once;
2. every other GapFinder arm (noverify, noevidence, random) re-uses those exact recorded model answers
   (`harness.py --ledger-from`): no model call, and every GapFinder arm reads the same ledger, so the
   ablations differ only in the search;
3. the baseline arms run as usual (they have their own model loop).

Already-finished runs (a prediction.json without an error) are skipped, so an interrupted test can be
resumed. Every harness call is the same command a person would type; the per-task dollar cap applies to
each. Pre-register the arms, runs and caps in PROTOCOL.md before the first paid run.
"""

from __future__ import annotations

import argparse
import glob
import json
import subprocess
import sys
from pathlib import Path

GB = Path(__file__).resolve().parent
LEDGER_ARM = "gapfinder"
SHARED_ARMS = ("gapfinder-noverify", "gapfinder-noevidence", "gapfinder-random")


def done(task_id: str, arm: str, k: int) -> bool:
    p = GB / "runs" / task_id / arm / f"run{k}" / "prediction.json"
    return p.exists() and "error" not in json.loads(p.read_text(encoding="utf-8"))


def harness(task_dir: Path, arm: str, k: int, cap: float, extra: list[str]) -> int:
    cmd = [sys.executable, str(GB / "harness.py"), str(task_dir), "--arm", arm, "--run", str(k), "--cap", str(cap), *extra]
    print("$", " ".join(cmd[1:]), flush=True)
    return subprocess.call(cmd)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tasks", required=True, help="glob of task directories")
    ap.add_argument("--runs", default="1,2,3")
    ap.add_argument("--arms", default=",".join((LEDGER_ARM, *SHARED_ARMS)))
    ap.add_argument("--baselines", default="baseline-super", help="comma-separated baseline arms ('' for none)")
    ap.add_argument("--cap", type=float, default=0.5, help="dollar cap per arm per task")
    ap.add_argument("--steps", type=int, default=40, help="baseline step limit")
    ap.add_argument("--seed", type=int, default=0, help="gapfinder-random shuffle seed (offset by run number)")
    a = ap.parse_args()
    tasks = [Path(p) for p in sorted(glob.glob(a.tasks)) if (Path(p) / "task.yaml").exists()]
    arms = [x for x in a.arms.split(",") if x]
    baselines = [x for x in a.baselines.split(",") if x]
    for k in (int(x) for x in a.runs.split(",")):
        for task_dir in tasks:
            tid = task_dir.name
            ledger_dir = GB / "runs" / tid / LEDGER_ARM / f"run{k}"
            if LEDGER_ARM in arms and not done(tid, LEDGER_ARM, k):
                harness(task_dir, LEDGER_ARM, k, a.cap, ["--fresh"])
            for arm in arms:
                if arm == LEDGER_ARM or done(tid, arm, k):
                    continue
                extra = ["--seed", str(a.seed + k)] if arm == "gapfinder-random" else []
                if (ledger_dir / "assumptions.json").exists():
                    extra += ["--ledger-from", str(ledger_dir)]
                else:  # the ledger arm failed: this arm pays for its own ledger
                    extra += ["--fresh"]
                harness(task_dir, arm, k, a.cap, extra)
            for arm in baselines:
                if not done(tid, arm, k):
                    harness(task_dir, arm, k, a.cap, ["--steps", str(a.steps)])


if __name__ == "__main__":
    main()
