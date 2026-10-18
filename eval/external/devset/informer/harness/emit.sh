#!/usr/bin/env bash
# devset informer: the test MSE and MAE of one ETTh2 multivariate horizon-24 run (normalized data, like the
# paper's Table 2). exp_informer.test prints "mse:x, mae:y".
cd "$(dirname "$0")/.." || exit 1
rm -rf out/checkpoints out/results  # model weights and saved predictions: not needed, keep the VM small
line=$(grep -a '^mse:' out/run.log | tail -1)
mse=$(printf %s "$line" | sed -n 's/^mse:\([^,]*\), mae:\(.*\)$/\1/p')
mae=$(printf %s "$line" | sed -n 's/^mse:\([^,]*\), mae:\(.*\)$/\2/p')
if [ -z "$mse" ] || [ -z "$mae" ]; then echo "--- out/run.log (no test result) ---" >&2; tail -15 out/run.log >&2; exit 0; fi
awk -v a="$mse" -v b="$mae" 'BEGIN { printf "etth2_24_mse=%.4f\netth2_24_mae=%.4f\n", a, b }'
