#!/usr/bin/env bash
# Run pre-registered MC Dropout arms (eval/external/mc-dropout/FROZEN.md) in parallel on Token Factory
# Sandboxes (Deviations 2 and 3). Run from the repo root (the main checkout, where .env, .venv,
# runs/mcd-ledger and runs/mcd-ledger-nodocs live):
#
#   bash scripts/run_mcd_sandbox_arms.sh                       # no-README and all-flags-random (default)
#   bash scripts/run_mcd_sandbox_arms.sh no-README normal      # a chosen subset, any of the four names
#   bash scripts/run_mcd_sandbox_arms.sh all                   # all four arms
#   MCD_ARMS_DRY_RUN=1 bash scripts/run_mcd_sandbox_arms.sh    # print the plan and the commands, run nothing
#
# Arm names: normal, evidence-off, no-README, all-flags-random. Arms 1-2 (normal, evidence-off) were
# completed locally (eval/external/mc-dropout/attempt2-local/), which is why the default is the other two.
#
# Same commands, knobs, budget and ledgers as FROZEN.md; only the spec (mcd_sandbox.yaml, which runs
# every cell sharded, Deviation 3) and the backend (contree) differ.
#
# Concurrency. The Sandboxes Beta allows 50 simultaneous operations in the project. Every branch run
# is one operation (its shards run inside the VM, on its 4 cores), and the orchestrator's semaphore
# (GF_MAX_CONCURRENCY) is per search process, so the arms' limits add up. This script gives each arm
# floor(48 / number of arms) (24 for two arms, 16 for three, 12 for four), so the total is at most 48.
# Set GF_MAX_CONCURRENCY yourself to override; the script refuses a total above 50.
#
# Sandboxes aren't billed in the Beta, but every run reports a diagnostic `cost`, so the guard on that
# reported cost and the per-process CPU limit are raised on purpose. Keys are read from .env by
# gapfinder/config.py; nothing secret is in this file.
set -u
cd "$(dirname "$0")/.." || exit 1
export PATH="/c/Program Files/Git/usr/bin:$PATH"

ALL_ARMS=(normal evidence-off no-README all-flags-random)
if [ "$#" -eq 0 ]; then
  arms=(no-README all-flags-random)
elif [ "$1" = all ]; then
  arms=("${ALL_ARMS[@]}")
else
  arms=("$@")
fi
for a in "${arms[@]}"; do
  case " ${ALL_ARMS[*]} " in
    *" $a "*) ;;
    *) echo "unknown arm '$a' (choose from: ${ALL_ARMS[*]}, or all)" >&2; exit 2 ;;
  esac
done
if [ "$(printf '%s\n' "${arms[@]}" | sort | uniq -d | wc -l)" -ne 0 ]; then
  echo "an arm is listed twice" >&2; exit 2
fi

# Sandboxes checkpoint of the frozen image (python:3.6-slim + pinned stack + repo at 6eb4497 with
# T = 100 + the sharded run_cell.sh), tag gf/mcd/base-v2. See FROZEN.md, Deviations 2 and 3.
export GF_MCD_SANDBOX_BASE="${GF_MCD_SANDBOX_BASE:-76b71887-d3e7-48ff-96d5-f16cefcf6779}"
export GF_SPEND_TAG=ext-mcd-sandbox
export GF_SANDBOX_GUARD_USD=20000
export GF_SANDBOX_CPU_LIMIT_S=60000
export GF_MAX_CONCURRENCY="${GF_MAX_CONCURRENCY:-$((48 / ${#arms[@]}))}"
if [ $((GF_MAX_CONCURRENCY * ${#arms[@]})) -gt 50 ]; then
  echo "refusing: ${#arms[@]} arms x GF_MAX_CONCURRENCY=$GF_MAX_CONCURRENCY = $((GF_MAX_CONCURRENCY * ${#arms[@]})) simultaneous operations, over the Beta limit of 50" >&2
  exit 2
fi

PY=.venv/Scripts/python
SPEC=eval/external/mc-dropout/mcd_sandbox.yaml
TARGETS=eval/external/mc-dropout/targets_mcd.json
OUT=eval/external/mc-dropout
LEDGER=runs/mcd-ledger
LEDGER_NODOCS=runs/mcd-ledger-nodocs
mkdir -p runs

# arm_args <name>: the search arguments that make the arm (FROZEN.md, "Arms")
arm_args() {
  case "$1" in
    normal) echo "--assumptions $LEDGER/assumptions.json --claims $LEDGER/claim_ledger.json" ;;
    evidence-off) echo "--assumptions $LEDGER/assumptions.json --claims $LEDGER/claim_ledger.json --no-evidence-gate" ;;
    no-README) echo "--assumptions $LEDGER_NODOCS/assumptions.json --claims $LEDGER_NODOCS/claim_ledger.json --no-evidence-gate" ;;
    all-flags-random) echo "--hypotheses repomap --rank random --seed 0" ;;
  esac
}

arm() {  # arm <name>
  local name=$1
  # shellcheck disable=SC2046
  set -- $(arm_args "$name")
  echo "[$(date '+%F %T')] start $name" >> runs/mcd-sbx-arms.log
  $PY -m gapfinder.cli search --spec "$SPEC" --targets "$TARGETS" "$@" --backend contree \
      --max-runs 40 --candidates-per-knob 2 --cap 0.5 --out "$OUT/run-$name" > "runs/mcd-sbx-arm-$name.log" 2>&1
  echo "[$(date '+%F %T')] end $name exit $?" >> runs/mcd-sbx-arms.log
}

echo "arms: ${arms[*]}; GF_MAX_CONCURRENCY=$GF_MAX_CONCURRENCY each ($((GF_MAX_CONCURRENCY * ${#arms[@]})) simultaneous operations at most); base $GF_MCD_SANDBOX_BASE"
if [ -n "${MCD_ARMS_DRY_RUN:-}" ]; then
  for a in "${arms[@]}"; do
    echo "$PY -m gapfinder.cli search --spec $SPEC --targets $TARGETS $(arm_args "$a") --backend contree --max-runs 40 --candidates-per-knob 2 --cap 0.5 --out $OUT/run-$a"
  done
  exit 0
fi

for a in "${arms[@]}"; do arm "$a" & done
wait
echo "[$(date '+%F %T')] arms finished: ${arms[*]}" >> runs/mcd-sbx-arms.log
