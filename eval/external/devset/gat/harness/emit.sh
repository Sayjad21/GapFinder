#!/usr/bin/env bash
# devset GAT: one key=value line per dataset, test accuracy in percent like the paper's Table 2.
# execute_cora_sparse.py ends with "Test loss: x ; Test accuracy: y".
cd "$(dirname "$0")/.." || exit 1
for ds in cora citeseer pubmed; do
  acc=$(grep -a 'Test accuracy:' out/$ds.log 2>/dev/null | tail -1 | sed 's/.*Test accuracy: *//')
  ep=$(grep -ac '^Training: loss' out/$ds.log 2>/dev/null)
  res=$(grep -a '^exit=' out/$ds.err 2>/dev/null | tail -1)
  echo "--- $ds: epochs=$ep $res" >&2
  if [ -z "$acc" ]; then echo "--- out/$ds.log (no test result) ---" >&2; tail -n 8 out/$ds.log out/$ds.err >&2; continue; fi
  awk -v n="$ds" -v a="$acc" 'BEGIN { printf "gat_%s_acc=%.2f\n", n, a * 100 }'
done
