# Gap Report: test-v13-01

Artifact `mlbench` · generated 2026-10-16 00:27 · 177 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -35.7% | +0.0% | ±5.5% | `normalize=zscore`, `threshold=0.3` |

## C1: test_accuracy (paper 0.7583)
**Fits but unsupported** · gap -35.7% → +0.0% · 61 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0060`, `B0103`, `B0133`, `B0134`, `B0135` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Config: `threshold` naive `0.5`, changed to `0.3`
- Command:

  Replay: fork checkpoint `4843a9b8-061c-4fcd-aa3b-31a3897edb32` and run
  ```
  RUN_TAG=7ec13c9f9782 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.3 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7625, 0.7583, 0.7583, 0.7625, 0.7583; gap after +0.0%; result checkpoint `7481e8ee-a609-4103-ba25-657c1fd7f9ff`
- Effect: candidate 0.7583 minus naive 0.4875 = +0.2708, 95% bootstrap interval [+0.2042, +0.29] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.758 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7583 (headline claim)

### What did we measure?
- Naive median 0.4875 over 5 runs; repeats: 0.4667, 0.5375, 0.475, 0.4875, 0.5625
- Spread: range 0.4667 to 0.5625, noise band ±0.0416 (2 x MAD), CV 8.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -35.7% (noise band ±5.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -29.1% (it comes back)
- PASS · Counterfactual (reversal test): without `threshold` the gap is +9.3% (it comes back)
- PASS · Held-out claim: C2: -35.5% to +4.9% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- FAIL · Evidence: `threshold=0.3`: no evidence mentions '0.3'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2708 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `median_over_7_runs`, `SCALES`, `WEIGHTS`, `PYTHON_VERSION`, `OS`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (3.2 noise units, gap -18.1%); `normalize=minmax` (2.6 noise units, gap -21.4%); `threshold=0.7` (1.8 noise units, gap -25.8%); `threshold=0.9` (1.6 noise units, gap -26.9%); `threshold=0.95` (1.1 noise units, gap -29.7%) (and 2 more in the JSON)
- Near alternatives (closest across all claims):
  - `normalize=minmax`, `class_weight=balanced`: this claim +1.6%, mean |gap| 3.0% (5 runs)
  - `threshold=0.25`, `normalize=zscore`: this claim -5.5%, mean |gap| 3.1% (5 runs)
  - `class_weight=balanced`, `normalize=zscore`: this claim +3.3%, mean |gap| 4.2% (5 runs)

### Equally good configurations
The target claim can't tell these 2 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `normalize=zscore, threshold=0.3` (reported)
- `class_weight=balanced, normalize=minmax`

### History matching (every measured configuration, all claims together)
- 11 of 61 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 0.67); class_weight=balanced, normalize=zscore (max I 0.76)
  - `normalize, threshold`: normalize=zscore, threshold=0.3 (max I 0.79); normalize=zscore, threshold=0.25 (max I 0.86); normalize=zscore, threshold=0.7 (max I 2.14)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.52); lr_schedule=step, normalize=zscore (max I 1.52)
  - `normalize`: normalize=zscore (max I 1.54)
  - `lr_schedule, threshold`: lr_schedule=cosine, threshold=0.9 (max I 2.77)
  - `lr_schedule`: lr_schedule=cosine (max I 2.8)
- Equally good values: `threshold` in {0.25, 0.3}

Notes:
- configurations the target claim can't tell apart from the answer: normalize=zscore, threshold=0.3; class_weight=balanced, normalize=minmax
- equally good values within one noise band (measured): threshold in {0.25, 0.3}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `threshold=0.3`, `normalize=zscore` | 5 | +0.0% | +4.9% | 2.4% |
| `normalize=minmax`, `class_weight=balanced` | 5 | +1.6% | +4.3% | 3.0% |
| `threshold=0.25`, `normalize=zscore` | 5 | -5.5% | +0.6% | 3.1% |
| `class_weight=balanced`, `normalize=zscore` | 5 | +3.3% | +5.0% | 4.2% |
| `normalize=zscore` | 6 | +9.3% | +8.4% | 8.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `median_over_7_runs`, `SCALES`, `WEIGHTS`, `PYTHON_VERSION`, `OS`

## Provenance
- GapFinder commit: `e9c31fd1405f5c8aae4bd880eadcdc8d491fad02` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0668, sandbox reported $0.0000 (total $0.0668; this search; ledger extraction is included only if it shared the search's router)
