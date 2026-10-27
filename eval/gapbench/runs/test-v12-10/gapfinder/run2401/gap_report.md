# Gap Report: test-v12-10

Artifact `mlbench` · generated 2026-10-16 01:32 · 42 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -35.2% | +0.0% | ±0.6% | `normalize=zscore` |

## C1: test_accuracy (paper 0.8292)
**Fits but unsupported** · gap -35.2% → +0.0% · 13 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0006`, `B0011`, `B0012`, `B0013` (4 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Command:

  Replay: fork checkpoint `b83126e4-57dd-4bc0-bfc1-9c39d3ee0103` and run
  ```
  RUN_TAG=791bed8f6c04 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.8292, 0.8292, 0.8292, 0.825; gap after +0.0%; result checkpoint `48ed0d1f-654a-4ed3-a17e-85b938576851`
- Effect: candidate 0.8292 minus naive 0.5375 = +0.2917, 95% bootstrap interval [+0.2875, +0.3217] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.829 test accuracy.

- p. 1; value used: `test_accuracy` = 0.8292 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5375, 0.5375, 0.5375, 0.4875, 0.5375
- Spread: range 0.4875 to 0.5375, noise band ±0.005375 (2 x MAD), CV 4.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -35.2% (noise band ±0.6% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -35.2% (it comes back)
- PASS · Held-out claim: C2: -33.1% to +0.0% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2917 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (17.82 noise units, gap -23.6%); `normalize=minmax` (10.85 noise units, gap -28.1%); `lr_schedule=step` (1.54 noise units, gap -34.2%)
- Near alternatives (closest across all claims):
  - `lr_schedule=cosine`, `normalize=zscore`: this claim +0.0%, mean |gap| 0.0% (3 runs)
  - `lr_schedule=step`, `normalize=zscore`: this claim +0.0%, mean |gap| 0.0% (3 runs)
  - `class_weight=balanced`, `normalize=zscore`: this claim -5.5%, mean |gap| 4.3% (3 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `normalize=zscore` (reported)
- `lr_schedule=cosine, normalize=zscore`
- `lr_schedule=step, normalize=zscore`

### History matching (every measured configuration, all claims together)
- 5 of 13 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 5 configurations
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 0); lr_schedule=step, normalize=zscore (max I 0)
  - `normalize`: normalize=zscore (max I 0.02)
  - `class_weight, normalize`: class_weight=balanced, normalize=zscore (max I 1.06); class_weight=balanced, normalize=minmax (max I 1.68)

Notes:
- configurations the target claim can't tell apart from the answer: normalize=zscore; lr_schedule=cosine, normalize=zscore; lr_schedule=step, normalize=zscore

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore` | 4 | +0.0% | +0.0% | 0.0% |
| `lr_schedule=cosine`, `normalize=zscore` | 3 | +0.0% | +0.0% | 0.0% |
| `lr_schedule=step`, `normalize=zscore` | 3 | +0.0% | +0.0% | 0.0% |
| `class_weight=balanced`, `normalize=zscore` | 3 | -5.5% | -3.1% | 4.3% |
| `normalize=minmax`, `class_weight=balanced` | 3 | -9.6% | -5.1% | 7.3% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
