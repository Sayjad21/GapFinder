#!/usr/bin/env bash
# Figure 6 cells: fixed K=1, 5, 10 on copies of the same loaded DB, in one VM, for each
# workload in `workloads` (name:lookup_ratio,...). Latencies are compared as ratios within
# the VM so machine speed cancels. Prints one JSON line, metrics prefixed by workload name:
#   <w>_us_k{1,5,10}  mean us/op over the second half of missions
#   <w>_ratio_k1_k5, <w>_ratio_k10_k5, <w>_ratio_k1_k10
#   <w>_wamp_k{1,10}  bytes compacted+flushed per user byte written (hardware-independent)
set -euo pipefail
source "$(dirname "$0")/common.sh"
: "${missions:=40}" "${ops_per_mission:=20000}" "${workloads:=balanced:0.5}" "${scratch:=/tmp/fig6db}"
mkdir -p out
IFS=, read -ra cells <<< "$workloads"
for cell in "${cells[@]}"; do
  name=${cell%%:*}; ratio=${cell#*:}
  for K in 1 5 10; do
    rm -rf "$scratch"; cp -a "$db" "$scratch"
    # one K per logical level ("yes | head" would die of SIGPIPE under pipefail)
    policy=$(for _ in $(seq "$logical_levels"); do printf '%s,' "$K"; done); policy=${policy%,}
    "$bench" --db "$scratch" --skip_load "${common[@]}" --missions "$missions" \
      --ops_per_mission "$ops_per_mission" --lookup_ratio "$ratio" --zero_result_ratio "$zero_result_ratio" \
      --policy "$policy" > "out/${name}_k$K.jsonl" 2> "out/${name}_k$K.log"
  done
done
rm -rf "$scratch"
# Summary in awk (no Python on the bare image): second half of missions per K.
summ() {  # <jsonl file> <bytes per entry>  ->  "<mean us/op> <write amp>"
  awk -v entry="$2" '
    function val(s, k,   m) { if (match(s, "\"" k "\":[-0-9.eE+]+")) { m = substr(s, RSTART + length(k) + 3, RLENGTH - length(k) - 3); return m + 0 } return 0 }
    /^\{/ { n++; line[n] = $0 }
    END {
      start = int(n / 2) + 1; cnt = 0; us = 0; upd = 0; wb = 0
      for (i = start; i <= n; i++) { us += val(line[i], "us_per_op"); upd += val(line[i], "updates"); wb += val(line[i], "c_write_b") + val(line[i], "flush_b"); cnt++ }
      if (cnt == 0) { print "nan nan"; exit 1 }
      printf "%.4f %.4f\n", us / cnt, (upd > 0 ? wb / (upd * entry) : 0)
    }' "$1"
}
entry=$((key_size + value_size))
json="{"
for cell in "${cells[@]}"; do
  w=${cell%%:*}
  read -r u1 a1 <<< "$(summ "out/${w}_k1.jsonl" "$entry")"
  read -r u5 a5 <<< "$(summ "out/${w}_k5.jsonl" "$entry")"
  read -r u10 a10 <<< "$(summ "out/${w}_k10.jsonl" "$entry")"
  json+=$(awk -v w="$w" -v u1="$u1" -v u5="$u5" -v u10="$u10" -v a1="$a1" -v a5="$a5" -v a10="$a10" 'BEGIN {
    printf "\"%s_us_k1\": %.4f, \"%s_us_k5\": %.4f, \"%s_us_k10\": %.4f, ", w, u1, w, u5, w, u10
    printf "\"%s_wamp_k1\": %.4f, \"%s_wamp_k5\": %.4f, \"%s_wamp_k10\": %.4f, ", w, a1, w, a5, w, a10
    printf "\"%s_ratio_k1_k5\": %.4f, \"%s_ratio_k10_k5\": %.4f, \"%s_ratio_k1_k10\": %.4f, ", w, u1/u5, w, u10/u5, w, u1/u10 }')
done
json="${json%, }}"
echo "$json" > out/result.json
echo "$json"
