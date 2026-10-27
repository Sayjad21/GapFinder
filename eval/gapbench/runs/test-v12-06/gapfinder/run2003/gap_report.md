# Gap Report: test-v12-06

Artifact `mlbench` · generated 2026-10-15 21:08 · 99 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -36.8% | -0.5% | ±5.4% | `normalize=minmax`, `class_weight=balanced` |

## C1: test_accuracy (paper 0.7708)
**Fits but unsupported** · gap -36.8% → -0.5% · 29 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0052`, `B0059`, `B0074`, `B0075`, `B0076` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `class_weight` naive `none`, changed to `balanced`
- Command:

  Replay: fork checkpoint `0af1ec66-de30-4010-9127-51dc496f14e2` and run
  ```
  RUN_TAG=7c00ed71c09b "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight balanced --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7625, 0.7917, 0.7792, 0.7625, 0.7667; gap after -0.5%; result checkpoint `d13b39f8-9c54-4173-aaf5-4280bb1ca44f`
- Effect: candidate 0.7667 minus naive 0.4875 = +0.2792, 95% bootstrap interval [+0.2, +0.3092] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.771 test accuracy and 0.745 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7708 (headline claim)

### What did we measure?
- Naive median 0.4875 over 5 runs; repeats: 0.4667, 0.4875, 0.5375, 0.4667, 0.5875
- Spread: range 0.4667 to 0.5875, noise band ±0.0416 (2 x MAD), CV 10.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -36.8% (noise band ±5.4% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -30.5% (it comes back)
- PASS · Counterfactual (reversal test): without `class_weight` the gap is -22.7% (it comes back)
- PASS · Held-out claim: C2: -35.0% to +5.1% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- FAIL · Evidence: `class_weight=balanced`: no evidence mentions 'balanced'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2792 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `SCALES[0]`, `SCALES[1]`, `SCALES[2]`, `SCALES[3]`, `SCALES[4]`, `SCALES[5]`, `SCALES[6]`, `SCALES[7]`, `WEIGHTS[0]`, `WEIGHTS[1]`, `WEIGHTS[2]`, `WEIGHTS[3]`, `WEIGHTS[4]`, `WEIGHTS[5]`, `WEIGHTS[6]`, `WEIGHTS[7]`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (5.51 noise units, gap +7.0%); `lr_schedule=cosine` (3.31 noise units, gap -18.9%); `weight_decay=1e-3` (1.9 noise units, gap -26.5%); `weight_decay=1e-4` (1.2 noise units, gap -30.3%)
- Near alternatives (closest across all claims):
  - `normalize=zscore`, `class_weight=balanced`: this claim +1.6%, mean |gap| 3.5% (5 runs)
  - `normalize=zscore`, `weight_decay=1e-3`: this claim +7.0%, mean |gap| 7.7% (5 runs)
  - `normalize=zscore`, `weight_decay=1e-4`: this claim +7.0%, mean |gap| 7.7% (5 runs)

### Equally good configurations
The target claim can't tell these 2 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `class_weight=balanced, normalize=minmax` (reported)
- `class_weight=balanced, normalize=zscore`

### History matching (every measured configuration, all claims together)
- 10 of 29 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 0.76); class_weight=balanced, normalize=zscore (max I 0.81)
  - `normalize, weight_decay`: normalize=zscore, weight_decay=1e-3 (max I 1.23); normalize=zscore, weight_decay=1e-4 (max I 1.25)
  - `normalize`: normalize=zscore (max I 1.29)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.3); lr_schedule=step, normalize=zscore (max I 1.3)
  - `lr_schedule`: lr_schedule=cosine (max I 2.76)
  - `lr_schedule, weight_decay`: lr_schedule=cosine, weight_decay=1e-3 (max I 2.9)
  - `class_weight, lr_schedule`: class_weight=balanced, lr_schedule=cosine (max I 2.9)
- Equally good values: `normalize` in {minmax, zscore}

Notes:
- configurations the target claim can't tell apart from the answer: class_weight=balanced, normalize=minmax; class_weight=balanced, normalize=zscore
- equally good values within one noise band (measured): normalize in {minmax, zscore}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `class_weight=balanced`, `normalize=minmax` | 5 | -0.5% | +5.1% | 2.8% |
| `normalize=zscore`, `class_weight=balanced` | 5 | +1.6% | +5.4% | 3.5% |
| `normalize=zscore`, `weight_decay=1e-3` | 5 | +7.0% | +8.3% | 7.7% |
| `normalize=zscore`, `weight_decay=1e-4` | 5 | +7.0% | +8.3% | 7.7% |
| `normalize=zscore` | 6 | +7.3% | +8.6% | 7.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `SCALES[0]`, `SCALES[1]`, `SCALES[2]`, `SCALES[3]`, `SCALES[4]`, `SCALES[5]`, `SCALES[6]`, `SCALES[7]`, `WEIGHTS[0]`, `WEIGHTS[1]`, `WEIGHTS[2]`, `WEIGHTS[3]`, `WEIGHTS[4]`, `WEIGHTS[5]`, `WEIGHTS[6]`, `WEIGHTS[7]`

## Provenance
- GapFinder commit: `cd8c8af2b9d079dd9a57443ed501c0dd8a467d34` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
