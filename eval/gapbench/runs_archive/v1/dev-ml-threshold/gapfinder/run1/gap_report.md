# Gap Report: dev-ml-threshold

Artifact `mlbench` · generated 2026-10-06 20:39 · 85 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Partially explained | -35.7% | +1.1% | ±1.1% | `normalize=zscore`, `split=0.9` |

## C1: test_accuracy (paper 0.7583)
**Partially explained** · gap -35.7% → +1.1% · 32 hypotheses tested

Evidence:
- `normalize=zscore`: supported, code evidence at train.py:15: 'p.add_argument("--normalize", choices=["none", "zscore", "minmax"], default="none")'
- `split=0.9`: UNSUPPORTED, no evidence mentions '0.9'; it fits, but nothing says the authors used it

Counterfactual (revert one knob; the gap must come back):
- without `normalize`: gap -24.2% (ok)
- without `split`: gap +8.8% (ok)

Held-out claims (must not get worse beyond noise):
- C2: -38.3% → -4.5% (ok)

Replay: fork checkpoint `c01eb1d3-62f4-451f-95c0-b459df7fd838` and run
```
RUN_TAG=71e278973d09 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.9 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
```
(result checkpoint `5d95625d-e641-4eaa-ab0f-685aef7f4077`; 3 repeat(s) recorded)

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`
