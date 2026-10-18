#!/usr/bin/env bash
# batch-3 b3c: what run_longExp.py prints as its test result, "mse:X, mae:Y, rse:Z", one line per --itr iteration;
# the mean over iterations (the paper's cells are a mean over runs). key=value lines.
cd "$(dirname "$0")/.." || exit 1
python - <<'EOF'
import glob, os, re, statistics
for f in sorted(glob.glob("out/ETTh*_*.log")):
    d, p = os.path.basename(f)[:-4].split("_")
    t = open(f, errors="replace").read()
    rows = re.findall(r"mse:([-+0-9.eE]+), mae:([-+0-9.eE]+)", t)
    if rows:
        print(f"{d.lower()}_{p}_mse={statistics.mean(float(a) for a, _ in rows):.6f}")
        print(f"{d.lower()}_{p}_mae={statistics.mean(float(b) for _, b in rows):.6f}")
EOF
