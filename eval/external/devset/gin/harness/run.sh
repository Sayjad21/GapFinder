#!/usr/bin/env bash
# devset GIN: one run = the full 10-fold cross-validation of main.py on each dataset of the GIN-0 row
# (Table 1), every fold a separate `python main.py --fold_idx k` process, 4 at a time (a Sandboxes VM has
# 4 vCPUs). Arguments after the script name go to every main.py call (the knobs and --seed).
# The social datasets (IMDB-B, IMDB-M) get --degree_as_tag, as the README says ("for the COLLAB and IMDB
# datasets, you need to add --degree_as_tag"). Each fold writes out/<DATASET>_f<k>.log; emit.sh reads them.
cd "$(dirname "$0")/.." || exit 1
mkdir -p out
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 TQDM_DISABLE=1 PYTHONWARNINGS=ignore
export GF_ARGS="$*"
DATASETS="${GF_DATASETS:-IMDBBINARY IMDBMULTI PTC MUTAG}"  # largest first, for packing; PROTEINS and NCI1 left out (HARNESS.md)
for ds in $DATASETS; do for f in 0 1 2 3 4 5 6 7 8 9; do echo "$ds $f"; done; done |
  xargs -P 4 -L 1 bash -c '
    ds=$0; f=$1; extra=""
    case $ds in IMDB*|COLLAB) extra="--degree_as_tag";; esac
    t=$(date +%s)
    python main.py --dataset $ds --fold_idx $f $extra $GF_ARGS > out/${ds}_f$f.log 2>&1; rc=$?
    echo "fold_wall_s=$(( $(date +%s) - t )) exit=$rc" >> out/${ds}_f$f.log'
