#!/usr/bin/env bash
# devset GAT: one cell = execute_cora_sparse.py (as shipped, apart from the constants passed here) on
# cora, citeseer and pubmed, the three in parallel, each from its own copy of the script.
# Usage: bash gf_harness/run_cell.sh NAME=VALUE ...   (module-level constants; dataset and checkpt_file are
# set here per dataset: each run saves its early-stopping checkpoint under out/<dataset>/, not over the
# shipped pre_trained/cora/ model, so parallel runs don't share one file)
cd "$(dirname "$0")/.." || exit 1
export TF_CPP_MIN_LOG_LEVEL=2
mkdir -p out
for ds in cora citeseer pubmed; do
  mkdir -p out/$ds
  python gf_harness/set_constants.py out/$ds/execute.py "dataset='$ds'" "checkpt_file='out/$ds/mod.ckpt'" "$@" \
    || { echo "set_constants failed for $ds" >&2; continue; }
  PYTHONPATH="/work${PYTHONPATH:+:$PYTHONPATH}" python gf_harness/measure.py python out/$ds/execute.py \
    > out/$ds.log 2> out/$ds.err &
done
wait
bash gf_harness/emit.sh
