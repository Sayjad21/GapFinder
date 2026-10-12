#!/usr/bin/env bash
# One MC Dropout experiment cell: run experiment.py for one or more UCI datasets and print one
# key=value line per metric, so GapFinder's `kv` parser reads it.
#
# Usage (every argument is key=value; unset or "default" means "what the repo does out of the box"):
#   bash run_cell.sh dir=yacht [epochx=500] [hidden=2] \
#        [n_splits=20] [n_epochs=40] [n_hidden=50] \
#        [dropout_rates=0.005,0.01,0.05,0.1] [tau_values=0.25,0.5,0.75]
#   bash run_cell.sh dir=yacht,energy,concrete tau_values_concrete=0.05,0.1 ...
#
# epochx and hidden are experiment.py's flags (--epochx, --hidden). The others are the
# per-dataset data files in UCI_Datasets/<dir>/data/ (n_splits.txt, n_epochs.txt, n_hidden.txt,
# dropout_rates.txt, tau_values.txt). A value is written only when it is passed. Lists are
# comma-separated here and written one value per line, as the repo's files are. The repo's
# tau grid differs per dataset (Concrete's is 0.025 0.05 0.075), so tau_values_<dir> overrides
# tau_values for that dataset.
#
# Noise between repeats (RUN_TAG): the repo seeds everything, so the same settings on the same splits
# are bit-identical. GapFinder gives every run a fresh RUN_TAG, and the cell turns it into the splits:
# the tag seeds a draw of n_splits distinct splits out of the dataset's available splits (sampling
# without replacement, a small LCG in bash so it is the same on every machine), and the drawn splits
# are used as splits 0..n_splits-1. Repeats of one configuration therefore see different data
# splits, as across real reruns (the same idea as rlbench's RUN_TAG seeding). The draw is
# deterministic per tag; two tags may share some splits but rarely draw the same set. With RUN_TAG
# unset the run uses splits 0..n_splits-1 as before. The draw is not a knob. split_offset=<k>
# (development only) overrides it with splits k, k+1, ...; the splits used are printed as
# splits_used=. `print_splits=1 [n_splits=..] [total_splits=20]` prints the draw for the current
# RUN_TAG and exits (used by tests).
#
# With several datasets they run in parallel (one process each) and every metric is prefixed
# with the dataset name: yacht_rmse=..., energy_rmse=... With one dataset there is no prefix.
#
# Sharded execution (procs=<N|auto>, FROZEN.md Deviation 3; for Token Factory Sandboxes, which cap an
# operation at 3,600 s and give a VM several cores): instead of one experiment.py per dataset that
# loops over its splits, every (dataset, split) is its own experiment.py process with n_splits=1 on
# that split, run in its own copy of the dataset and net folders, at most N at a time (auto = nproc),
# longest dataset first. The split draw, the split swapping and the settings are exactly the ones
# above (each shard is this script run unsharded with split_offset=<its split>). When all shards are
# done, their per-split result lines are put back in split order and aggregated by the same code
# as the unsharded run, so the printed metrics have the same names and formulas. Differences: wall_s
# is the longest shard, cpu_s the sum over shards, and shards=, procs= and shards_wall_s= are added.
# Seeding: experiment.py calls np.random.seed(1) once per process. Unsharded, split k continues the
# random stream where split k-1 left it; sharded, every split starts it fresh. So the first split
# of each dataset is bit-identical to the unsharded run and the others differ by noise of the same
# size as the noise between repeats. Without procs= nothing changes.
#
# experiment.py prints no summary of its own. It appends one number per split to
# UCI_Datasets/<dir>/results/test_{rmse,MC_rmse,ll,tau}_<epochx>_xepochs_<hidden>_hidden_layers.txt
# and writes the mean and standard deviation to log_*.txt. This script reads the per-split files.
set -uo pipefail
cd "$(dirname "$0")"
self="$PWD/$(basename "$0")"

for kv in "$@"; do declare "${kv%%=*}=${kv#*=}"; done

# split_sample <tag> <n_splits> <total_splits>: n distinct split indices out of 0..total-1, drawn
# without replacement (partial Fisher-Yates) from an LCG seeded by the tag; space-separated.
split_sample() {
  local tag=$1 n=$2 total=$3 h i j t x
  local -a pool
  [ "$n" -le "$total" ] || n=$total
  h=$(printf %s "$tag" | cksum | cut -d' ' -f1)  # POSIX CRC of the whole tag: same everywhere
  for ((i = 0; i < total; i++)); do pool[i]=$i; done
  x=$(( (h % 2147483648) * 7 + 12345 ))
  for ((i = 0; i < 4; i++)); do x=$(( (x * 1103515245 + 12345) % 2147483648 )); done  # warm-up
  for ((i = 0; i < n; i++)); do
    x=$(( (x * 1103515245 + 12345) % 2147483648 ))
    j=$(( i + (x >> 8) % (total - i) ))
    t=${pool[i]}; pool[i]=${pool[j]}; pool[j]=$t
  done
  echo "${pool[@]:0:n}"
}
if [ -n "${print_splits:-}" ]; then
  split_sample "${RUN_TAG:-}" "${n_splits:-3}" "${total_splits:-20}"
  exit 0
fi

: "${dir:?dir=<dataset>[,<dataset>...] is required, e.g. dir=yacht}"
: "${epochx:=500}" "${hidden:=2}"
mkdir -p out    # an empty results/ folder is dropped by uploads, so results/ is made below too

# "default" is the spec's way of saying "leave the repo's own file alone"
for v in n_splits n_epochs n_hidden dropout_rates tau_values split_offset; do
  [ "${!v:-}" = default ] && declare "$v="
done

# experiment.py reads the two lists with np.loadtxt, which returns a bare float for a
# one-line file, and then crashes iterating it. So each list needs at least two values.
check_list() {
  if [ -n "$2" ] && [ "$2" != default ] && [[ "$2" != *,* ]]; then
    echo "error: $1 needs at least two comma-separated values (experiment.py cannot loop over one)" >&2
    exit 2
  fi
}
check_list dropout_rates "${dropout_rates:-}"
check_list tau_values "${tau_values:-}"

# mean, standard deviation (population, as experiment.py's np.std) and count of one result file
stats() {
  awk '{ s += $1; q += $1 * $1; n++ }
       END { if (n == 0) { print "nan nan 0"; exit 1 }
             m = s / n; v = q / n - m * m; if (v < 0) v = 0; printf "%.6f %.6f %d\n", m, sqrt(v), n }' "$1"
}

# choose_splits <dataset> <n>: sets the array `chosen` to the n split indices used as splits 0..n-1.
# split_offset=k (development only: k, k+1, ...), else the RUN_TAG's draw of n distinct splits (see
# the header), else 0, 1, ... The repo seeds everything, so the same splits give the identical
# result; different draws are how repeats differ. Not a knob.
choose_splits() {
  local d=$1 n=$2 i
  chosen=()
  if [ -n "${split_offset:-}" ]; then
    for ((i = 0; i < n; i++)); do chosen+=($((i + split_offset))); done
  elif [ -n "${RUN_TAG:-}" ]; then
    local idx=("UCI_Datasets/$d/data"/index_train_*.txt)
    read -ra chosen <<< "$(split_sample "$RUN_TAG" "$n" "${#idx[@]}")"
  else
    for ((i = 0; i < n; i++)); do chosen+=("$i"); done
  fi
}

# emit_metrics <prefix> <results dir> <file suffix> <splits_used> <wall> <cpu>: aggregate the
# per-split result files (one line per split) and print one key=value line per metric
emit_metrics() {
  local p=$1 results=$2 suffix=$3 splits_used=$4 wall=$5 cpu=$6
  local rmse_mc rmse_mc_sd n rmse_single rmse_single_sd ll ll_sd mean_tau
  read -r rmse_mc rmse_mc_sd n < <(stats "$results/test_MC_rmse_$suffix")
  read -r rmse_single rmse_single_sd _ < <(stats "$results/test_rmse_$suffix")
  read -r ll ll_sd _ < <(stats "$results/test_ll_$suffix")
  read -r mean_tau _ _ < <(stats "$results/test_tau_$suffix")

  # rmse is the MC-dropout predictive mean's RMSE (the second number experiment.py logs);
  # rmse_single is the first (one stochastic pass). ll is the test log-likelihood.
  echo "${p}rmse=$rmse_mc"
  echo "${p}rmse_sd=$rmse_mc_sd"
  echo "${p}rmse_single=$rmse_single"
  echo "${p}rmse_single_sd=$rmse_single_sd"
  echo "${p}ll=$ll"
  echo "${p}ll_sd=$ll_sd"
  echo "${p}mean_tau=$mean_tau"
  echo "${p}splits_done=$n"
  echo "${p}splits_used=$splits_used"
  echo "${p}wall_s=$wall"
  echo "${p}cpu_s=$cpu"
}

# run_one <dataset> <prefix>: configure the data files, run experiment.py, print the metrics
run_one() {
  local d=$1 p=$2
  local data="UCI_Datasets/$d/data" results="UCI_Datasets/$d/results"
  [ -d "$data" ] || { echo "error: no dataset directory $data" >&2; return 2; }
  mkdir -p "$results"

  local tau_var="tau_values_${d//[^A-Za-z0-9]/_}" tau="${tau_values:-}"
  [ -n "${!tau_var:-}" ] && [ "${!tau_var}" != default ] && tau="${!tau_var}"
  check_list "$tau_var" "$tau"

  [ -n "${n_splits:-}" ] && echo "$n_splits" > "$data/n_splits.txt"
  [ -n "${n_epochs:-}" ] && echo "$n_epochs" > "$data/n_epochs.txt"
  [ -n "${n_hidden:-}" ] && echo "$n_hidden" > "$data/n_hidden.txt"
  [ -n "${dropout_rates:-}" ] && echo "${dropout_rates//,/$'\n'}" > "$data/dropout_rates.txt"
  [ -n "$tau" ] && echo "${tau//,/$'\n'}" > "$data/tau_values.txt"

  # Splits: the chosen split indices become splits 0, 1, ... by renaming the index files. The
  # choice is split_offset=k when given (development only: k, k+1, ...), else the RUN_TAG's draw
  # of n_splits distinct splits (see the header), else 0, 1, ... The repo seeds everything, so
  # the same splits give the identical result; different draws are how repeats differ. Not a knob.
  local nsp=$(( ${n_splits:-$(cat "$data/n_splits.txt")} )) i kind
  choose_splits "$d" "$nsp"
  mkdir -p "out/splits_$d"
  for ((i = 0; i < nsp; i++)); do
    for kind in train test; do
      cp "$data/index_${kind}_${chosen[i]}.txt" "out/splits_$d/index_${kind}_$i.txt"
    done
  done
  cp "out/splits_$d"/index_*.txt "$data/"
  local splits_used="${chosen[*]}"; splits_used=${splits_used// /,}

  local start status wall cpu suffix
  start=$(date +%s)
  python experiment.py --dir "$d" --epochx "$epochx" --hidden "$hidden" > "out/experiment_$d.log" 2>&1
  status=$?
  if [ "$status" -ne 0 ]; then
    tail -n 30 "out/experiment_$d.log" >&2
    echo "error: experiment.py ($d) exited with status $status" >&2
    return "$status"
  fi
  wall=$(( $(date +%s) - start ))
  # CPU seconds of this process's children (experiment.py), user + system, from bash's `times`
  times > "out/times_$d.txt"
  cpu=$(awk 'NR == 2 { for (i = 1; i <= 2; i++) { split($i, a, /[ms]/); t += a[1] * 60 + a[2] } printf "%.1f", t }' "out/times_$d.txt")

  suffix="${epochx}_xepochs_${hidden}_hidden_layers.txt"
  emit_metrics "$p" "$results" "$suffix" "$splits_used" "$wall" "$cpu"
}

IFS=, read -ra datasets <<< "$dir"

# Sharded execution (see the header): one experiment.py process per (dataset, split).
[ "${procs:-}" = default ] && procs=
if [ -n "${procs:-}" ]; then
  # nproc honours OMP_NUM_THREADS, which the spec sets to 1 for the BLAS caps: ignore it here
  [ "$procs" = auto ] && procs=$(env -u OMP_NUM_THREADS -u OMP_THREAD_LIMIT nproc 2>/dev/null || echo 1)
  case "$procs" in
    '' | *[!0-9]* | 0) echo "error: procs must be a positive integer or auto, got '$procs'" >&2; exit 2 ;;
  esac
  suffix="${epochx}_xepochs_${hidden}_hidden_layers.txt"
  t_start=$(date +%s)

  # every argument except the ones a shard sets for itself is passed on unchanged
  pass=()
  for kv in "$@"; do
    case "${kv%%=*}" in dir | n_splits | split_offset | procs) ;; *) pass+=("$kv") ;; esac
  done

  # datasets with more rows first (they take longest), then the jobs in split order
  mapfile -t ordered < <(for d in "${datasets[@]}"; do
    [ -f "UCI_Datasets/$d/data/data.txt" ] || { echo "error: no dataset directory UCI_Datasets/$d" >&2; exit 2; }
    echo "$(wc -l < "UCI_Datasets/$d/data/data.txt") $d"
  done | sort -s -k1,1nr | cut -d' ' -f2)
  [ "${#ordered[@]}" -eq "${#datasets[@]}" ] || exit 2
  declare -A nshards=()
  jobs_list=()
  for d in "${ordered[@]}"; do
    nsp=$(( ${n_splits:-$(cat "UCI_Datasets/$d/data/n_splits.txt")} ))
    choose_splits "$d" "$nsp"
    nshards[$d]=${#chosen[@]}
    for ((i = 0; i < ${#chosen[@]}; i++)); do jobs_list+=("$d $i ${chosen[i]}"); done
  done

  running=0
  for job in "${jobs_list[@]}"; do
    read -r d i k <<< "$job"
    while [ "$running" -ge "$procs" ]; do wait -n; running=$((running - 1)); done
    sd="out/shards/${d}_$i"
    rm -rf "$sd"
    mkdir -p "$sd/UCI_Datasets/$d"
    cp "$self" "$sd/run_cell.sh"
    cp experiment.py "$sd/experiment.py"
    cp -r net "$sd/net"
    cp -r "UCI_Datasets/$d/data" "$sd/UCI_Datasets/$d/data"
    (cd "$sd" && bash run_cell.sh "${pass[@]}" "dir=$d" "n_splits=1" "split_offset=$k" > kv.txt 2> err.txt
     echo $? > status.txt) &
    running=$((running + 1))
  done
  wait

  failed=0
  multi=$(( ${#datasets[@]} > 1 ))
  for d in "${datasets[@]}"; do
    p=""; [ "$multi" -eq 1 ] && p="${d//[^A-Za-z0-9]/_}_"
    results="UCI_Datasets/$d/results"
    mkdir -p "$results"
    for f in test_MC_rmse test_rmse test_ll test_tau; do : > "$results/${f}_$suffix"; done
    ok=1; wall=0; cpu=0; used=()
    for ((i = 0; i < ${nshards[$d]}; i++)); do
      sd="out/shards/${d}_$i"
      st=$(cat "$sd/status.txt" 2>/dev/null || echo 1)
      if [ "$st" -ne 0 ]; then
        tail -n 30 "$sd/err.txt" >&2
        echo "error: shard $i of $d exited with status $st" >&2
        ok=0; continue
      fi
      for f in test_MC_rmse test_rmse test_ll test_tau; do
        cat "$sd/UCI_Datasets/$d/results/${f}_$suffix" >> "$results/${f}_$suffix"
      done
      s_wall=$(sed -n 's/^wall_s=//p' "$sd/kv.txt"); s_cpu=$(sed -n 's/^cpu_s=//p' "$sd/kv.txt")
      wall=$(awk -v a="$wall" -v b="${s_wall:-0}" 'BEGIN { print (b > a ? b : a) }')
      cpu=$(awk -v a="$cpu" -v b="${s_cpu:-0}" 'BEGIN { printf "%.1f", a + b }')
      used+=("$(sed -n 's/^splits_used=//p' "$sd/kv.txt")")
    done
    if [ "$ok" -eq 1 ]; then
      splits_used=$(IFS=,; echo "${used[*]}")
      emit_metrics "$p" "$results" "$suffix" "$splits_used" "$wall" "$cpu"
      echo "${p}shards=${nshards[$d]}"
    else
      failed=1
    fi
  done
  echo "procs=$procs"
  echo "shards_wall_s=$(( $(date +%s) - t_start ))"
  exit $failed
fi
if [ "${#datasets[@]}" -eq 1 ]; then
  run_one "${datasets[0]}" ""
  exit $?
fi

pids=()
for d in "${datasets[@]}"; do
  run_one "$d" "${d//[^A-Za-z0-9]/_}_" > "out/kv_$d.txt" &
  pids+=($!)
done
failed=0
for pid in "${pids[@]}"; do wait "$pid" || failed=1; done
for d in "${datasets[@]}"; do cat "out/kv_$d.txt"; done
exit $failed
