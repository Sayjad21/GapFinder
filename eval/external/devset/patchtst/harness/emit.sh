#!/usr/bin/env bash
# devset PatchTST: one key=value pair per horizon run of a cell. Each run writes out/h<pred_len>.log;
# Exp_Main.test() ends with "mse:x, mae:y, rse:z" (normalised-scale test metrics, as in the paper's Table 3).
cd "$(dirname "$0")/.." || exit 1
for f in out/h*.log; do
  [ -f "$f" ] || continue
  pl=$(basename "$f" .log | sed 's/^h//')
  line=$(grep -a '^mse:' "$f" | tail -1)
  mse=$(printf %s "$line" | sed -n 's/^mse:\([^,]*\),.*/\1/p')
  mae=$(printf %s "$line" | sed -n 's/.*mae:\([^,]*\),.*/\1/p')
  if [ -z "$mse" ] || [ -z "$mae" ]; then
    echo "--- $f (no test result) ---" >&2; tail -12 "$f" >&2; continue
  fi
  awk -v p="$pl" -v a="$mse" -v b="$mae" 'BEGIN { printf "etth1_%s_mse=%.4f\netth1_%s_mae=%.4f\n", p, a, p, b }'
done
