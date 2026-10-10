# Gap Report: dev-ml-normalize

Artifact `mlbench` · generated 2026-10-10 17:14 · 45 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -40.2% | +0.0% | ±2.0% | `normalize=zscore` |

## C1: test_accuracy (paper 0.8292)
**Fits but unsupported** · gap -40.2% → +0.0% · 8 hypotheses tested

Evidence:
- `normalize=zscore`: UNSUPPORTED, no evidence mentions 'zscore'; it fits, but nothing says the authors used it

Counterfactual (revert one knob; the gap must come back):
- without `normalize`: gap -40.2% (ok)

Held-out claims (must not get worse beyond noise):
- C2: -39.4% → +0.0% (ok)

Replay: fork checkpoint `ca600ec6-e613-4eaa-a122-895fc0d30d96` and run
```
RUN_TAG=a343b5367ae5 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
```
(result checkpoint `88d338c8-27f6-4e13-a0ba-93c2df7ead75`; 5 repeat(s) recorded)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore` | 5 | +0.0% | +0.0% | 0.0% |
| `lr_schedule=cosine`, `normalize=zscore` | 5 | +0.0% | +0.0% | 0.0% |
| `class_weight=balanced`, `normalize=zscore` | 5 | -5.5% | -3.1% | 4.3% |
| `lr_schedule=cosine` | 5 | -25.6% | -23.8% | 24.7% |
| `class_weight=balanced`, `lr_schedule=cosine` | 5 | -27.1% | -24.3% | 25.7% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `median aggregation over runs`, `shuffling seed per run`, `SCALES`, `WEIGHTS`, `hardware`, `OS`, `Python version`, `--out`
