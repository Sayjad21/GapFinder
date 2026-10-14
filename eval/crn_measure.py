"""Common random numbers (TODO B3 item 7): does pairing seeds across configurations reduce noise here?

    python eval/crn_measure.py [--k 8]

For each pair of configurations (A, B) on the GapBench artifacts, run both with the same k RUN_TAGs
(paired) and compare:
    independent variance of A - B   = var(A) + var(B)
    paired variance of A - B        = var(A_i - B_i)
    variance reduction factor (VRF) = independent / paired
A VRF near 1 means CRN buys nothing; the plan adopts CRN only if it is at least about 1.5. Local, free.
"""

from __future__ import annotations

import argparse
import json
import os
import statistics
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

GB = Path(__file__).resolve().parents[1] / "eval" / "gapbench"
PAIRS = {
    "rlbench": ("cartpole_q.py", "mean_reward", [({}, {"max_steps": "100"}), ({}, {"lr": "0.2"}),
                                                 ({"eps_decay": "0.995"}, {}), ({"max_steps": "500"}, {"max_steps": "1000"})]),
    "mlbench": ("train.py", "test_accuracy", [({}, {"epochs": "30"}), ({"normalize": "zscore"}, {"normalize": "minmax"}),
                                              ({"normalize": "minmax"}, {"normalize": "minmax", "epochs": "75"}),
                                              ({}, {"batch_size": "64"})]),
}


def run(family: str, script: str, metric: str, cfg: dict, tag: str) -> float:
    with tempfile.TemporaryDirectory() as d:
        out = Path(d) / "r.json"
        args = [sys.executable, str(GB / "artifacts" / family / script), "--out", str(out)]
        for k, v in cfg.items():
            args += [f"--{k}", v]
        subprocess.run(args, env={**os.environ, "RUN_TAG": tag}, capture_output=True, check=True,
                       cwd=GB / "artifacts" / family)
        return json.loads(out.read_text().splitlines()[0])[metric]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--k", type=int, default=8)
    a = ap.parse_args()
    tags = [f"{0xa10000 + 7919 * i:06x}" for i in range(a.k)]
    other = [f"{0xb20000 + 104729 * i:06x}" for i in range(a.k)]
    out = []
    with ThreadPoolExecutor(8) as ex:
        for family, (script, metric, pairs) in PAIRS.items():
            for ca, cb in pairs:
                A = list(ex.map(lambda t: run(family, script, metric, ca, t), tags))
                B = list(ex.map(lambda t: run(family, script, metric, cb, t), tags))  # same tags: paired
                Bi = list(ex.map(lambda t: run(family, script, metric, cb, t), other))  # other tags: independent
                paired = statistics.variance([x - y for x, y in zip(A, B)])
                indep = statistics.variance(A) + statistics.variance(Bi)
                vrf = indep / paired if paired else float("inf")
                row = {"family": family, "A": ca, "B": cb, "var_A": round(statistics.variance(A), 6),
                       "var_B": round(statistics.variance(Bi), 6), "var_paired_diff": round(paired, 6),
                       "vrf": round(vrf, 2)}
                out.append(row)
                print(row, flush=True)
    res = Path(__file__).resolve().parents[1] / "eval" / "results" / "crn_measure.json"
    res.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print("->", res)


if __name__ == "__main__":
    main()
