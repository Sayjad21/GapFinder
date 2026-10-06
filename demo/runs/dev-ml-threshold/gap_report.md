# Gap Report: dev-ml-threshold

Artifact `mlbench` · generated 2026-10-06 21:37 · 31 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -29.7% | +0.0% | ±2.2% | `normalize=zscore`, `threshold=0.3` |

## C1: test_accuracy (paper 0.7583)
**Fits but unsupported** · gap -29.7% → +0.0% · 5 hypotheses tested

Evidence:
- `normalize=zscore`: UNSUPPORTED, no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- `threshold=0.3`: UNSUPPORTED, no evidence mentions '0.3'; it fits, but nothing says the authors used it

Counterfactual (revert one knob; the gap must come back):
- without `normalize`: gap -29.1% (ok)
- without `threshold`: gap +9.3% (ok)

Held-out claims (must not get worse beyond noise):
- C2: -31.3% → +0.0% (ok)

Replay: fork checkpoint `3b437beb-8cf3-470f-98a1-f432bc788915` and run
```
RUN_TAG=5f3ea205fb67 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.3 --data_seed 7 --out out/result.json
```
(result checkpoint `bd2e00a3-caac-4c6b-9a3d-c4af9a6ff90f`; 5 repeat(s) recorded)

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`
