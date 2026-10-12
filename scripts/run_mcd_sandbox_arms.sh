#!/usr/bin/env bash
# Run the four pre-registered MC Dropout arms (eval/external/mc-dropout/FROZEN.md) in parallel on
# Token Factory Sandboxes (FROZEN.md, Deviation 2). Run from the repo root (the main checkout, where
# .env, .venv, runs/mcd-ledger and runs/mcd-ledger-nodocs live):
#
#   bash scripts/run_mcd_sandbox_arms.sh
#
# Same commands, knobs, budget and ledgers as FROZEN.md; only the spec (mcd_sandbox.yaml) and the
# backend (contree) differ. 4 arms x GF_MAX_CONCURRENCY=10 = 40 simultaneous sandbox operations,
# under the Beta limit of 50. Sandboxes aren't billed in the Beta, but every run reports a diagnostic
# `cost`, so the guard on that reported cost and the per-process CPU limit are raised on purpose.
# Keys are read from .env by gapfinder/config.py; nothing secret is in this file.
set -u
cd "$(dirname "$0")/.." || exit 1
export PATH="/c/Program Files/Git/usr/bin:$PATH"

# Sandboxes checkpoint of the frozen image (python:3.6-slim + pinned stack + repo at 6eb4497 with
# T = 100 + run_cell.sh), tag gf/mcd/base-v1. See FROZEN.md, Deviation 2.
export GF_MCD_SANDBOX_BASE="${GF_MCD_SANDBOX_BASE:-75aeac20-b2f1-4fed-83df-1554a229d51f}"
export GF_SPEND_TAG=ext-mcd-sandbox
export GF_MAX_CONCURRENCY=10
export GF_SANDBOX_GUARD_USD=20000
export GF_SANDBOX_CPU_LIMIT_S=60000

PY=.venv/Scripts/python
SPEC=eval/external/mc-dropout/mcd_sandbox.yaml
TARGETS=eval/external/mc-dropout/targets_mcd.json
OUT=eval/external/mc-dropout
mkdir -p runs

arm() {  # arm <name> <search args...>
  local name=$1; shift
  echo "[$(date '+%F %T')] start $name" >> runs/mcd-sbx-arms.log
  $PY -m gapfinder.cli search --spec "$SPEC" --targets "$TARGETS" "$@" --backend contree \
      --max-runs 40 --candidates-per-knob 2 --cap 0.5 --out "$OUT/run-$name" > "runs/mcd-sbx-arm-$name.log" 2>&1
  echo "[$(date '+%F %T')] end $name exit $?" >> runs/mcd-sbx-arms.log
}

arm normal --assumptions runs/mcd-ledger/assumptions.json --claims runs/mcd-ledger/claim_ledger.json &
arm evidence-off --assumptions runs/mcd-ledger/assumptions.json --claims runs/mcd-ledger/claim_ledger.json \
    --no-evidence-gate &
arm no-README --assumptions runs/mcd-ledger-nodocs/assumptions.json --claims runs/mcd-ledger-nodocs/claim_ledger.json \
    --no-evidence-gate &
arm all-flags-random --hypotheses repomap --rank random --seed 0 &
wait
echo "[$(date '+%F %T')] all four arms finished" >> runs/mcd-sbx-arms.log
