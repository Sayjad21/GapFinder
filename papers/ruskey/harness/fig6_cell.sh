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
python3 - "$key_size" "$value_size" "$workloads" <<'PY'
import json, sys
entry = int(sys.argv[1]) + int(sys.argv[2])
res = {}
for cell in sys.argv[3].split(","):
    w = cell.split(":")[0]
    for k in (1, 5, 10):
        rows = [json.loads(l) for l in open(f"out/{w}_k{k}.jsonl") if l.startswith("{")]
        half = rows[len(rows) // 2:]
        res[f"{w}_us_k{k}"] = round(sum(r["us_per_op"] for r in half) / len(half), 4)
        upd = sum(r["updates"] for r in half)
        res[f"{w}_wamp_k{k}"] = round(sum(r["c_write_b"] + r["flush_b"] for r in half) / max(upd * entry, 1), 4)
    res[f"{w}_ratio_k1_k5"] = round(res[f"{w}_us_k1"] / res[f"{w}_us_k5"], 4)
    res[f"{w}_ratio_k10_k5"] = round(res[f"{w}_us_k10"] / res[f"{w}_us_k5"], 4)
    res[f"{w}_ratio_k1_k10"] = round(res[f"{w}_us_k1"] / res[f"{w}_us_k10"], 4)
line = json.dumps(res)
open("out/result.json", "w").write(line + "\n")
print(line)
PY
