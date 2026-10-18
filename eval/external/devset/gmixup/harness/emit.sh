#!/usr/bin/env bash
# devset gmixup: one key=value line per (dataset, method) of a cell, test accuracy in percent like Table 2.
# Each training run writes out/<dataset>_<gmixup True|False>_<k>.log; src/gmixup.py logs one line per epoch,
# "Epoch: NNN, ... Val Acc:  v, Test Acc:  t", and selects nothing itself. As the paper says ("best test epoch
# is selected on a validation set"), a run's accuracy is the test accuracy at the epoch with the highest
# validation accuracy (the first such epoch on ties). A metric is the mean over the cell's seeds.
cd "$(dirname "$0")/.." || exit 1
for ds in IMDB-BINARY IMDB-MULTI; do
  for gm in False True; do
    case $ds in IMDB-BINARY) d=imdbb ;; IMDB-MULTI) d=imdbm ;; esac
    case $gm in True) m=gmixup ;; False) m=vanilla ;; esac
    accs=""
    for f in out/${ds}_${gm}_*.log; do
      [ -f "$f" ] || continue
      a=$(grep -a 'Epoch: ' "$f" | sed -n 's/.*Val Acc: *\([0-9.]*\), Test Acc: *\([0-9.]*\).*/\1 \2/p' \
          | awk 'BEGIN { bv = -1 } { if ($1 > bv) { bv = $1; bt = $2 } } END { if (bv >= 0) print bt }')
      if [ -z "$a" ]; then echo "--- $f (no epoch lines) ---" >&2; tail -12 "$f" >&2; continue; fi
      accs="$accs $a"
    done
    [ -n "$accs" ] || continue
    echo "$accs" | awk -v n="gin_${d}_${m}_acc" '{ s = 0; for (i = 1; i <= NF; i++) s += $i; printf "%s=%.2f\n", n, 100 * s / NF }'
  done
done
