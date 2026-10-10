# Gap Report: dev-ml-threshold

Artifact `mlbench` · generated 2026-10-10 17:14 · 54 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -28.0% | +0.0% | ±5.5% | `normalize=zscore`, `threshold=0.3` |

## C1: test_accuracy (paper 0.7583)
**Fits but unsupported** · gap -28.0% → +0.0% · 13 hypotheses tested

Evidence:
- `normalize=zscore`: UNSUPPORTED, no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- `threshold=0.3`: UNSUPPORTED, no evidence mentions '0.3'; it fits, but nothing says the authors used it

Counterfactual (revert one knob; the gap must come back):
- without `normalize`: gap -29.1% (ok)
- without `threshold`: gap +9.3% (ok)

Held-out claims (must not get worse beyond noise):
- C2: -30.4% → +0.0% (ok)

Replay: fork checkpoint `3125b398-b4d2-4440-9f6d-fee59c199a46` and run
```
RUN_TAG=617a5753ac33 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.3 --data_seed 7 --out out/result.json
```
(result checkpoint `2fe720f9-9b42-406d-84fd-25f7da1d3f79`; 5 repeat(s) recorded)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `threshold=0.3`, `normalize=zscore` | 5 | +0.0% | +0.0% | 0.0% |
| `normalize=zscore`, `class_weight=balanced` | 5 | +3.3% | +0.1% | 1.7% |
| `normalize=zscore` | 5 | +9.3% | +3.4% | 6.4% |
| `lr_schedule=cosine`, `normalize=zscore` | 5 | +9.3% | +3.4% | 6.4% |
| `lr_schedule=cosine` | 5 | -19.2% | -21.3% | 20.3% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `threshold=auto`: invalid_value, The program expects a numeric float for --threshold, but received the string 'auto', which is not a valid float; suggested `0.3`, already measured

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`
