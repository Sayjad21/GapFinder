# Gap Report: test-v12-06

Artifact `mlbench` · generated 2026-10-15 09:00 · 198 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -30.3% | -0.5% | ±0.7% | `class_weight=balanced`, `normalize=minmax` |

## C1: test_accuracy (paper 0.7708)
**Fits but unsupported** · gap -30.3% → -0.5% · 73 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0064`, `B0179`, `B0180`, `B0181`, `B0182` (5 run(s) of the same config)
- Config: `class_weight` naive `none`, changed to `balanced`
- Config: `normalize` naive `none`, changed to `minmax`
- Command:

  Replay: fork checkpoint `2eebd926-785f-499c-ad7f-8904070bd67c` and run
  ```
  RUN_TAG=a29b6ab4e927 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight balanced --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7667, 0.7667, 0.7042, 0.7792, 0.7708; gap after -0.5%; result checkpoint `db200c3b-e55e-4242-8b8b-895594afb094`
- Effect: candidate 0.7667 minus naive 0.5375 = +0.2292, 95% bootstrap interval [+0.1942, +0.2892] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.771 test accuracy and 0.745 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7708 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5375, 0.5375, 0.5375, 0.4833, 0.4667
- Spread: range 0.4667 to 0.5375, noise band ±0.005375 (2 x MAD), CV 6.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -30.3% (noise band ±0.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `class_weight` the gap is -22.7% (it comes back)
- PASS · Counterfactual (reversal test): without `normalize` the gap is -36.8% (it comes back)
- PASS · Held-out claim: C2: -27.2% to +4.6% (not worse beyond noise)
- FAIL · Evidence: `class_weight=balanced`: no evidence mentions 'balanced'; it fits, but nothing says the authors used it
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2292 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `SCALES[0]`, `SCALES[1]`, `SCALES[2]`, `SCALES[3]`, `SCALES[4]`, `SCALES[5]`, `SCALES[6]`, `SCALES[7]`, `WEIGHTS[0]`, `WEIGHTS[1]`, `WEIGHTS[2]`, `WEIGHTS[3]`, `WEIGHTS[4]`, `WEIGHTS[5]`, `WEIGHTS[6]`, `WEIGHTS[7]`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (33.32 noise units, gap +7.0%); `lr_schedule=cosine` (13.17 noise units, gap -21.1%); `positive_rate=0.65` (6.2 noise units, gap -25.9%)
- Near alternatives (closest across all claims):
  - `class_weight=balanced`, `normalize=zscore`: this claim +1.6%, mean |gap| 3.5% (5 runs)
  - `positive_rate=0.65`, `normalize=zscore`: this claim +6.5%, mean |gap| 7.4% (5 runs)
  - `weight_decay=1e-4`, `normalize=zscore`: this claim +7.0%, mean |gap| 7.7% (5 runs)

### History matching (every measured configuration, all claims together)
- 17 of 70 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 0.62); class_weight=balanced, normalize=zscore (max I 0.91)
  - `normalize, positive_rate`: normalize=zscore, positive_rate=0.5 (max I 0.74); normalize=zscore, positive_rate=0.86 (max I 0.77); normalize=zscore, positive_rate=0.15 (max I 1.13); normalize=zscore, positive_rate=0.65 (max I 1.4)
  - `normalize, weight_decay`: normalize=zscore, weight_decay=1e-4 (max I 1.39); normalize=zscore, weight_decay=1e-3 (max I 1.41)
  - `normalize`: normalize=zscore (max I 1.44)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.45)
- 2 separate islands (no single-knob move joins them): class_weight=balanced, normalize=minmax; normalize=zscore, positive_rate=0.5; normalize=zscore, positive_rate=0.86 | lr_schedule=cosine, positive_rate=0.15; lr_schedule=cosine, positive_rate=0.86; lr_schedule=cosine, positive_rate=0.93

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'lr_schedule': 'step', 'positive_rate': '0.93'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `class_weight=balanced`, `normalize=minmax` | 5 | -0.5% | +4.6% | 2.6% |
| `class_weight=balanced`, `normalize=zscore` | 5 | +1.6% | +5.4% | 3.5% |
| `positive_rate=0.65`, `normalize=zscore` | 5 | +6.5% | +8.4% | 7.4% |
| `weight_decay=1e-4`, `normalize=zscore` | 5 | +7.0% | +8.3% | 7.7% |
| `normalize=zscore` | 6 | +7.6% | +8.8% | 8.2% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: invalid_value, The code computes log(positive_rate / (1 - positive_rate)), which requires positive_rate > 0 and < 1. Setting it to 0.0 causes a math domain error because log(0) is undefined; retried as `positive_rate=0.001`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `SCALES[0]`, `SCALES[1]`, `SCALES[2]`, `SCALES[3]`, `SCALES[4]`, `SCALES[5]`, `SCALES[6]`, `SCALES[7]`, `WEIGHTS[0]`, `WEIGHTS[1]`, `WEIGHTS[2]`, `WEIGHTS[3]`, `WEIGHTS[4]`, `WEIGHTS[5]`, `WEIGHTS[6]`, `WEIGHTS[7]`

## Provenance
- GapFinder commit: `f01fe3d9a0095f98d6304ad0543b917ca8e529eb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0006, sandbox reported $0.0000 (total $0.0006; this search; ledger extraction is included only if it shared the search's router)
