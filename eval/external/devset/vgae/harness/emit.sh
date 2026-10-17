#!/usr/bin/env bash
# devset VGAE: one key=value line per (model, dataset) run of a cell, in percent like the paper's Table 1.
# Each run writes out/<model>_<dataset>.log; train.py ends with "Test ROC score: x" and "Test AP score: y".
cd "$(dirname "$0")/.." || exit 1
for f in out/*.log; do
  name=$(basename "$f" .log)
  auc=$(grep -a 'Test ROC score:' "$f" | tail -1 | sed 's/.*: //')
  ap=$(grep -a 'Test AP score:' "$f" | tail -1 | sed 's/.*: //')
  if [ -z "$auc" ] || [ -z "$ap" ]; then
    echo "--- $f (no test scores) ---" >&2; tail -12 "$f" >&2; continue
  fi
  awk -v n="$name" -v a="$auc" -v p="$ap" 'BEGIN { printf "%s_auc=%.3f\n%s_ap=%.3f\n", n, a * 100, n, p * 100 }'
done
