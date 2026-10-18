#!/usr/bin/env bash
# devbatch-2 NCF: one key=value line per number the scripts print, as fractions like the paper's tables.
# Each of NeuMF.py, GMF.py and MLP.py writes out/<model>.log and ends with
#   "End. Best Iteration <i>:  HR = <hr>, NDCG = <ndcg>."  -> <model>_hr, <model>_ndcg, <model>_best_iter
# (the script's own final result). Extras: the init line and every logged epoch
#   "Iteration <e> [..]: HR = <hr>, NDCG = <ndcg>, loss = <loss> [..]" -> <model>_hr_e<e>, _ndcg_e<e>, _loss_e<e>
cd "$(dirname "$0")/.." || exit 1
N='\([0-9]*\.[0-9]*\)'
for m in neumf gmf mlp; do
  f=out/$m.log
  [ -f "$f" ] || continue
  end=$(grep -a '^End\. Best Iteration' "$f" | tail -1)
  if [ -z "$end" ]; then
    echo "--- $f (no final result) ---" >&2; tail -15 "$f" >&2; continue
  fi
  echo "$end" | sed -n "s/^End\. Best Iteration \(-\{0,1\}[0-9]*\): *HR = $N, NDCG = $N.*/${m}_hr=\2\n${m}_ndcg=\3\n${m}_best_iter=\1/p"
  grep -a '^Init: HR' "$f" | tail -1 | sed -n "s/^Init: HR = $N, NDCG = $N.*/${m}_hr_init=\1\n${m}_ndcg_init=\2/p"
  grep -a '^Iteration [0-9]* \[' "$f" | sed -n "s/^Iteration \([0-9]*\) \[[^]]*\]: HR = $N, NDCG = $N, loss = \([0-9.a-z]*\) .*/${m}_hr_e\1=\2\n${m}_ndcg_e\1=\3\n${m}_loss_e\1=\4/p"
done
