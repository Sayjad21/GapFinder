# Gap Report: test-v13-05

Artifact `mlbench` · generated 2026-10-15 23:42 · 194 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -31.0% | +0.5% | ±0.7% | `normalize=zscore`, `label_noise=0.905` |

## C1: test_accuracy (paper 0.7792)
**Fits but unsupported** · gap -31.0% → +0.5% · 73 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0128`, `B0130`, `B0173` (3 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Config: `label_noise` naive `0.05`, changed to `0.905`
- Command:

  Replay: fork checkpoint `00195ab2-0d2a-4c73-9a71-90c324e5f3ce` and run
  ```
  RUN_TAG=bddc89c81762 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.905 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7833, 0.7833, 0.7833; gap after +0.5%; result checkpoint `a29a8fb8-8f58-4e15-b2c2-285abaab1f79`
- Effect: candidate 0.7833 minus naive 0.5375 = +0.2458, 95% bootstrap interval [+0.2458, +0.2766] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.779 test accuracy and 0.750 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7792 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5375, 0.5, 0.5333, 0.5375, 0.5375
- Spread: range 0.5 to 0.5375, noise band ±0.005375 (2 x MAD), CV 3.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -31.0% (noise band ±0.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -40.1% (it comes back)
- PASS · Counterfactual (reversal test): without `label_noise` the gap is +6.1% (it comes back)
- PASS · Held-out claim: C2: -28.2% to +1.8% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- FAIL · Evidence: `label_noise=0.905`: no evidence mentions '0.905'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2458 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `number_of_runs`, `aggregation_method`, `SCALES`, `WEIGHTS`, `shuffling_seed_generation`, `out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `epochs=750` (37.99 noise units, gap -4.8%); `lr_schedule=cosine` (14.73 noise units, gap -20.9%); `normalize=minmax` (10.85 noise units, gap -23.5%); `class_weight=balanced` (4.65 noise units, gap -27.8%); `label_noise=0.01` (3.11 noise units, gap -28.9%) (and 4 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=cosine`, `epochs=750`: this claim +1.6%, mean |gap| 1.4% (3 runs)
  - `class_weight=balanced`, `normalize=minmax`: this claim -1.1%, mean |gap| 2.5% (3 runs)
  - `normalize=zscore`, `class_weight=balanced`: this claim +1.1%, mean |gap| 3.1% (3 runs)

### Equally good configurations
The target claim can't tell these 4 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `label_noise=0.905, normalize=zscore` (reported)
- `class_weight=balanced, normalize=zscore`
- `epochs=750, lr_schedule=cosine`
- `class_weight=balanced, normalize=minmax`

### History matching (every measured configuration, all claims together)
- 27 of 73 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `epochs, lr_schedule`: epochs=750, lr_schedule=cosine (max I 0.27)
  - `label_noise, normalize`: label_noise=0.905, normalize=zscore (max I 0.34); label_noise=0.1, normalize=zscore (max I 0.97); label_noise=0.981, normalize=zscore (max I 1.25)
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 0.57); class_weight=balanced, normalize=zscore (max I 0.93)
  - `epochs, normalize`: epochs=1, normalize=zscore (max I 1.24); epochs=2, normalize=zscore (max I 1.31); epochs=30, normalize=zscore (max I 1.32); epochs=750, normalize=minmax (max I 1.34)
- 2 separate islands (no single-knob move joins them): label_noise=0.905, normalize=zscore; class_weight=balanced, normalize=minmax; class_weight=balanced, normalize=zscore | epochs=750, lr_schedule=cosine; epochs=750, lr_schedule=step

Notes:
- configurations the target claim can't tell apart from the answer: label_noise=0.905, normalize=zscore; class_weight=balanced, normalize=zscore; epochs=750, lr_schedule=cosine; class_weight=balanced, normalize=minmax

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore`, `label_noise=0.905` | 3 | +0.5% | +1.8% | 1.2% |
| `lr_schedule=cosine`, `epochs=750` | 3 | +1.6% | +1.2% | 1.4% |
| `class_weight=balanced`, `normalize=minmax` | 3 | -1.1% | +3.9% | 2.5% |
| `normalize=zscore`, `class_weight=balanced` | 3 | +1.1% | +5.1% | 3.1% |
| `normalize=zscore`, `label_noise=0.1` | 3 | +3.7% | +5.0% | 4.4% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `number_of_runs`, `aggregation_method`, `SCALES`, `WEIGHTS`, `shuffling_seed_generation`, `out`

## Provenance
- GapFinder commit: `e9c31fd1405f5c8aae4bd880eadcdc8d491fad02` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0483, sandbox reported $0.0000 (total $0.0483; this search; ledger extraction is included only if it shared the search's router)
