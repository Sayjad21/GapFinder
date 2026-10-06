# Gap Report: dev-ml-threshold

Artifact `mlbench` · generated 2026-10-06 20:45 · 31 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -36.3% | +0.0% | ±4.4% | `normalize=zscore`, `threshold=0.3` |

## C1: test_accuracy (paper 0.7583)
**Fits but unsupported** · gap -36.3% → +0.0% · 5 hypotheses tested

Evidence:
- `normalize=zscore`: supported, code evidence at train.py:15: 'p.add_argument("--normalize", choices=["none", "zscore", "minmax"], default="none")'
- `threshold=0.3`: UNSUPPORTED, no evidence mentions '0.3'; it fits, but nothing says the authors used it

Counterfactual (revert one knob; the gap must come back):
- without `normalize`: gap -29.7% (ok)
- without `threshold`: gap +8.8% (ok)

Held-out claims (must not get worse beyond noise):
- C2: -38.9% → +0.0% (ok)

Replay: fork checkpoint `56b5d328-69e4-4ede-a04d-2897b47275e8` and run
```
RUN_TAG=e1ca25c4c9a4 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.3 --data_seed 7 --out out/result.json
```
(result checkpoint `5028955f-5b20-4d2d-a5f9-680f74fcc4b5`; 5 repeat(s) recorded)

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`
