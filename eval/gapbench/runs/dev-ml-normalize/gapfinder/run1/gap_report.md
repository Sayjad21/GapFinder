# Gap Report: dev-ml-normalize

Artifact `mlbench` · generated 2026-10-06 20:45 · 15 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -35.2% | -0.5% | ±6.0% | `normalize=zscore` |

## C1: test_accuracy (paper 0.8292)
**Fits but unsupported** · gap -35.2% → -0.5% · 2 hypotheses tested

Evidence:
- `normalize=zscore`: UNSUPPORTED, no evidence mentions 'zscore'; it fits, but nothing says the authors used it

Counterfactual (revert one knob; the gap must come back):
- without `normalize`: gap -35.2% (ok)

Held-out claims (must not get worse beyond noise):
- C2: -33.1% → -0.4% (ok)

Replay: fork checkpoint `7e34c8e9-0e0e-4a76-b37d-2a3a25d401d9` and run
```
RUN_TAG=f71b7e6886a7 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
```
(result checkpoint `8efacb0c-a65c-4dcf-b88d-6191e390cba4`; 5 repeat(s) recorded)

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `median aggregation over runs`, `shuffling seed per run`, `SCALES`, `WEIGHTS`, `hardware`, `OS`, `Python version`, `--out`
