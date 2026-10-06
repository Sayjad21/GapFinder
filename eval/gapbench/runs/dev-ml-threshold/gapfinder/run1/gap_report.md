# Gap Report: dev-ml-threshold

Artifact `mlbench` · generated 2026-10-06 21:03 · 31 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -35.7% | +0.0% | ±5.5% | `normalize=zscore`, `threshold=0.3` |

## C1: test_accuracy (paper 0.7583)
**Fits but unsupported** · gap -35.7% → +0.0% · 5 hypotheses tested

Evidence:
- `normalize=zscore`: supported, code evidence at train.py:15: 'p.add_argument("--normalize", choices=["none", "zscore", "minmax"], default="none")'
- `threshold=0.3`: UNSUPPORTED, no evidence mentions '0.3'; it fits, but nothing says the authors used it

Counterfactual (revert one knob; the gap must come back):
- without `normalize`: gap -29.1% (ok)
- without `threshold`: gap +8.8% (ok)

Held-out claims (must not get worse beyond noise):
- C2: -38.3% → +0.0% (ok)

Replay: fork checkpoint `f3344a3a-d585-4e9c-9168-f3d85bce7a85` and run
```
RUN_TAG=56d0991b10c3 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.3 --data_seed 7 --out out/result.json
```
(result checkpoint `f92cef33-a49a-4bee-8c35-09e5204830ea`; 5 repeat(s) recorded)

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`
