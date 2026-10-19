#!/usr/bin/env bash
# batch-4 b4a (RippleNet): the case's protocol, the test AUC and ACC printed at the last epoch, averaged over the
# cell's runs. train.py prints "epoch N  train auc: a  acc: b  eval auc: c  acc: d  test auc: e  acc: f" per epoch.
cd "$(dirname "$0")/.." || exit 1
python - <<'EOF'
import glob, re, statistics
pat = re.compile(r"epoch (\d+)\s+train auc: ([0-9.]+)\s+acc: ([0-9.]+)\s+eval auc: ([0-9.]+)\s+acc: ([0-9.]+)\s+test auc: ([0-9.]+)\s+acc: ([0-9.]+)")
last = []
for f in sorted(glob.glob("out/run*.log")):
    rows = pat.findall(open(f, errors="replace").read())
    if rows:
        last.append(rows[-1])
if last:
    print("book_auc=%.4f" % statistics.mean(float(r[5]) for r in last))
    print("book_acc=%.4f" % statistics.mean(float(r[6]) for r in last))
    print("book_eval_auc=%.4f" % statistics.mean(float(r[3]) for r in last))
    print("book_eval_acc=%.4f" % statistics.mean(float(r[4]) for r in last))
    print("book_train_auc=%.4f" % statistics.mean(float(r[1]) for r in last))
    print("book_runs=%d" % len(last))
EOF
