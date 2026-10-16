#!/usr/bin/env bash
# Prints one key=value line per FastGCN run of a cell, for GapFinder's kv parser (see ../HARNESS.md).
# The cell's run command writes out/<script>_<dataset>.log for <script> in trans, ind and <dataset> in
# cora, pubmed. Each script ends with one line "rank1 = ... cost= X accuracy= Y training time= T ...".
# Accuracy on these single-label datasets is the micro-F1 the paper's Table 5 reports.
# A run without that line prints no metric (its tail goes to stderr), so the cell counts as failed for it.
cd "$(dirname "$0")/.." || exit 1
for f in out/trans_cora.log out/trans_pubmed.log out/ind_cora.log out/ind_pubmed.log; do
  name=$(basename "$f" .log)
  line=$(grep -a 'accuracy=' "$f" 2>/dev/null | grep -a 'rank1 =' | tail -1)
  if [ -z "$line" ]; then
    echo "--- $f (no result line) ---" >&2
    tail -15 "$f" >&2 2>/dev/null
    continue
  fi
  acc=$(printf '%s\n' "$line" | sed -n 's/.*accuracy= \([0-9.eE+-]*\).*/\1/p')
  secs=$(printf '%s\n' "$line" | sed -n 's/.*training time= \([0-9.eE+-]*\).*/\1/p')
  echo "${name}_acc=${acc}"
  echo "${name}_train_s=${secs}"
done
