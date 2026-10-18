#!/usr/bin/env bash
# devbatch-2 pyg: one key=value pair per (model, dataset) script run, in percent like the paper's Table 2.
# Each run writes out/<model>_<Dataset>.log; train_eval.py ends with
# "Val Loss: v, Test Accuracy: m ± s, Duration: ds" (m, s: mean and std of test accuracy over --runs runs).
cd "$(dirname "$0")/.." || exit 1
for f in out/gcn_*.log out/gat_*.log; do
  [ -f "$f" ] || continue
  name=$(basename "$f" .log | tr 'A-Z' 'a-z')
  line=$(grep -a 'Test Accuracy:' "$f" | tail -1)
  if [ -z "$line" ]; then echo "--- $f (no test accuracy) ---" >&2; tail -12 "$f" >&2; continue; fi
  echo "$line" | awk -v n="$name" '{
    m = $0; sub(/.*Test Accuracy: /, "", m); split(m, a, " "); mean = a[1]
    s = $0; sub(/.*± */, "", s); sub(/,.*/, "", s)
    printf "%s_acc=%.2f\n", n, mean * 100
    if (s ~ /^[0-9.]+$/) printf "%s_std=%.2f\n", n, s * 100 }'
done
