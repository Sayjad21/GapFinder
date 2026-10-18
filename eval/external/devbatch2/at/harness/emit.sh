#!/usr/bin/env bash
# devbatch-2 at: the SMD test result of one train+test run, in percent like the paper's Table 1.
# solver.py test() ends with "Accuracy : a, Precision : p, Recall : r, F-score : f " (fractions).
cd "$(dirname "$0")/.." || exit 1
line=$(grep -a 'Precision :' out/test.log 2>/dev/null | tail -1)
p=$(printf %s "$line" | sed -n 's/.*Precision : \([0-9.]*\).*/\1/p')
r=$(printf %s "$line" | sed -n 's/.*Recall : \([0-9.]*\).*/\1/p')
f=$(printf %s "$line" | sed -n 's/.*F-score : \([0-9.]*\).*/\1/p')
if [ -z "$p" ] || [ -z "$r" ] || [ -z "$f" ]; then
  for g in out/train.log out/test.log; do echo "--- $g (no test result) ---" >&2; tail -12 "$g" >&2; done
  exit 0
fi
awk -v p="$p" -v r="$r" -v f="$f" 'BEGIN { printf "smd_precision=%.2f\nsmd_recall=%.2f\nsmd_f1=%.2f\n", p * 100, r * 100, f * 100 }'
