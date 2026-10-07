# Gap Report: dev-ml-threshold

Artifact `mlbench` · generated 2026-10-07 16:20 · 21 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -29.1% | +0.0% | ±0.7% | `normalize=zscore`, `threshold=0.3` |

## C1: test_accuracy (paper 0.7583)
**Fits but unsupported** · gap -29.1% → +0.0% · 5 hypotheses tested

Evidence:
- `normalize=zscore`: UNSUPPORTED, no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- `threshold=0.3`: UNSUPPORTED, no evidence mentions '0.3'; it fits, but nothing says the authors used it

Counterfactual (revert one knob; the gap must come back):
- without `normalize`: gap -37.4% (ok)
- without `threshold`: gap +8.8% (ok)

Held-out claims (must not get worse beyond noise):
- C2: -30.8% → +0.0% (ok)

Replay: fork checkpoint `983a1cdc-10fc-496b-8b5e-d50aabd091fe` and run
```
RUN_TAG=5327ce2e8b4e "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.3 --data_seed 7 --out out/result.json
```
(result checkpoint `3cbea909-3e29-4e6e-9efd-00c78a86bb00`; 3 repeat(s) recorded)

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`
