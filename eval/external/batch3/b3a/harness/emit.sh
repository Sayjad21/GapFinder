#!/usr/bin/env bash
# batch-3 b3a: per (option, dataset), the mean over the seed logs of what the script prints last:
# - objective: the last "clustering energy = X" line (the discrete clustering objective);
# - fairness_error, balance (the min balance: the paper's "balance = min_k balance(S_k)"), avg_balance: the last
#   printed block.
# key=value lines; a config with no parsable seed log prints nothing (the run then fails to parse).
cd "$(dirname "$0")/.." || exit 1
python - <<'EOF'
import glob, re, statistics
cfg = {"kmeans": "kmeans", "kmedian": "kmedian"}
for c in ("kmeans", "kmedian"):
    for d, short in (("Synthetic", "synthetic"), ("Synthetic-unequal", "unequal")):
        vals = {"objective": [], "fairness_error": [], "balance": [], "avg_balance": []}
        for f in sorted(glob.glob(f"out/{c}_{d}_s*.log")):
            t = open(f, errors="replace").read()
            e = re.findall(r"clustering energy = ([-+0-9.eE]+)", t)
            fe = re.findall(r"fairness_error\s+([-+0-9.eE]+)\s+and", t)
            ab = re.findall(r"avg_balance =\s+([-+0-9.eE]+)", t)
            mb = re.findall(r"min_balance =\s+([-+0-9.eE]+)", t)
            if e and fe and ab and mb:
                vals["objective"].append(float(e[-1]))
                vals["fairness_error"].append(float(fe[-1]))
                vals["avg_balance"].append(float(ab[-1]))
                vals["balance"].append(float(mb[-1]))
        for k, v in vals.items():
            if v:
                print(f"{c}_{short}_{k}={statistics.mean(v):.4f}")
        if vals["objective"]:
            print(f"{c}_{short}_seeds={len(vals['objective'])}")
EOF
