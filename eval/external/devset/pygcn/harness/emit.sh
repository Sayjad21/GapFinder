#!/usr/bin/env bash
# devset pygcn: the test accuracy of one run, in percent like the paper (train.py prints
# "Test set results: loss= x accuracy= y").
cd "$(dirname "$0")/.." || exit 1
acc=$(grep -a 'Test set results' out/run.log | tail -1 | sed -n 's/.*accuracy= \([0-9.]*\).*/\1/p')
if [ -z "$acc" ]; then echo "--- out/run.log (no test result) ---" >&2; tail -12 out/run.log >&2; exit 0; fi
awk -v a="$acc" 'BEGIN { printf "cora_acc=%.2f\n", a * 100 }'
