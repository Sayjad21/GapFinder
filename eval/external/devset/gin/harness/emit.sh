#!/usr/bin/env bash
# devset GIN: one key=value line per dataset, the 10-fold cross-validation accuracy in percent, computed
# the way the README says the paper did it: "after obtaining 10 validation curves corresponding to 10 folds,
# we first took average of validation curves across the 10 folds ... and then selected a single epoch that
# achieved the maximum averaged validation accuracy." main.py prints "accuracy train: x test: y" per epoch;
# the "test" fold is that validation fold. A dataset with a missing or short fold prints nothing (stderr says why).
cd "$(dirname "$0")/.." || exit 1
python - <<'EOF'
import os, re, sys
names = {"IMDBBINARY": "imdbb_acc", "IMDBMULTI": "imdbm_acc", "MUTAG": "mutag_acc",
         "PROTEINS": "proteins_acc", "PTC": "ptc_acc", "NCI1": "nci1_acc"}
for ds, metric in names.items():
    curves = []
    for f in range(10):
        p = f"out/{ds}_f{f}.log"
        if not os.path.exists(p):
            break
        txt = open(p, errors="replace").read()
        curves.append([float(x) for x in re.findall(r"accuracy train: \S+ test: ([0-9.]+)", txt)])
    if not curves:
        continue
    lens = [len(c) for c in curves]
    if len(curves) < 10 or min(lens) == 0 or min(lens) != max(lens):
        print(f"--- {ds}: incomplete folds, epochs per fold {lens} ---", file=sys.stderr)
        for f in range(10):
            p = f"out/{ds}_f{f}.log"
            if os.path.exists(p) and (f >= len(lens) or lens[f] < max(lens)):
                print(open(p, errors="replace").read()[-1500:], file=sys.stderr)
                break
        continue
    n = lens[0]
    mean = [sum(c[e] for c in curves) / 10 for e in range(n)]
    best = max(range(n), key=lambda e: mean[e])
    print(f"{metric}={mean[best] * 100:.2f}")
    print(f"{ds}: best epoch {best + 1} of {n}", file=sys.stderr)
EOF
