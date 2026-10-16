#!/usr/bin/env bash
# blind-2: one key=value line per dataset of a cell, for GapFinder's kv parser (see ../HARNESS.md).
# Each run writes out/<DATASET>.log; main_graph.py ends with "# final_acc: 0.xxxx±0.xxxx" (mean 10-fold SVM
# accuracy over the --seeds given; the cell passes one seed). Printed in percent, as the paper's Table 2.
# A run without that line prints no metric (its tail goes to stderr), so the cell counts as failed for it.
cd "$(dirname "$0")/.." || exit 1
for f in out/*.log; do
  ds=$(basename "$f" .log)
  name=$(printf '%s' "$ds" | tr 'A-Z-' 'a-z_' | sed 's/imdb_binary/imdb_b/; s/imdb_multi/imdb_m/; s/reddit_binary/reddit_b/')
  acc=$(grep -a 'final_acc:' "$f" | tail -1 | sed -n 's/.*final_acc: \([0-9.]*\).*/\1/p')
  if [ -z "$acc" ]; then
    echo "--- $f (no final_acc line) ---" >&2
    tail -15 "$f" >&2
    continue
  fi
  echo "${name}_acc=$(awk -v a="$acc" 'BEGIN { printf "%.2f", a * 100 }')"
  secs=$(grep -a '^gf_wall_s=' "$f" | tail -1 | cut -d= -f2)
  [ -n "$secs" ] && echo "${name}_wall_s=${secs}"
done
