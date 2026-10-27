# Gap Report: test-v11-09

Artifact `mlbench` · generated 2026-10-14 23:50 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -28.2% | +3.9% | ±5.5% | `class_weight=balanced`, `normalize=zscore` |

## C1: test_accuracy (paper 0.7542)
**Fits but unsupported** · gap -28.2% → +3.9% · 53 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0100`, `B0165`, `B0166`, `B0167`, `B0168` (5 run(s) of the same config)
- Config: `class_weight` naive `none`, changed to `balanced`
- Config: `normalize` naive `none`, changed to `zscore`
- Command:

  Replay: fork checkpoint `407d3456-9915-4cf3-b59e-daf85e70102d` and run
  ```
  RUN_TAG=38b9530a9921 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight balanced --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7833, 0.7833, 0.7833, 0.7875, 0.7833; gap after +3.9%; result checkpoint `ae3c15b5-4903-4f97-a8c3-24198cb68d10`
- Effect: candidate 0.7833 minus naive 0.5417 = +0.2416, 95% bootstrap interval [+0.225, +0.3183] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.754 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7542 (headline claim)

### What did we measure?
- Naive median 0.5417 over 5 runs; repeats: 0.5458, 0.5625, 0.4667, 0.5417, 0.4667
- Spread: range 0.4667 to 0.5625, noise band ±0.0416 (2 x MAD), CV 9.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -28.2% (noise band ±5.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `class_weight` the gap is +9.9% (it comes back)
- PASS · Counterfactual (reversal test): without `normalize` the gap is -29.3% (it comes back)
- PASS · Held-out claim: C2: -24.7% to +8.7% (not worse beyond noise)
- FAIL · Evidence: `class_weight=balanced`: no evidence mentions 'balanced'; it fits, but nothing says the authors used it
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2416 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `aggregation`, `CPU`, `memory`, `OS`, `Python_version`, `random_module`, `floating_point`, `num_features`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (2.1 noise units, gap -16.6%); `normalize=minmax` (1.3 noise units, gap -21.0%)
- Near alternatives (closest across all claims):
  - `normalize=zscore`, `lr=0.001`: this claim +6.6%, mean |gap| 7.6% (5 runs)
  - `normalize=zscore`, `lr=0.5`: this claim +8.8%, mean |gap| 9.9% (5 runs)
  - `lr=0.1`, `normalize=zscore`: this claim +9.4%, mean |gap| 10.4% (5 runs)

### History matching (every measured configuration, all claims together)
- 20 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 0.84); class_weight=balanced, normalize=zscore (max I 1.29)
  - `lr, normalize`: lr=0.5, normalize=minmax (max I 0.88); lr=0.001, normalize=zscore (max I 1.22); lr=0.5, normalize=zscore (max I 1.6); lr=0.005, normalize=zscore (max I 1.7); +2 more
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.81); lr_schedule=step, normalize=zscore (max I 1.81)

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'normalize': 'minmax', 'lr': '0.001'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `class_weight=balanced`, `normalize=zscore` | 5 | +3.9% | +8.7% | 6.3% |
| `normalize=zscore`, `lr=0.001` | 5 | +6.6% | +8.6% | 7.6% |
| `normalize=zscore`, `lr=0.5` | 5 | +8.8% | +11.0% | 9.9% |
| `lr=0.1`, `normalize=zscore` | 5 | +9.4% | +11.4% | 10.4% |
| `normalize=zscore`, `lr=0.005` | 5 | +9.4% | +11.4% | 10.4% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `aggregation`, `CPU`, `memory`, `OS`, `Python_version`, `random_module`, `floating_point`, `num_features`, `--out`

## Provenance
- GapFinder commit: `efb2f63a257a40b9982099a274f2e882f272b80c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
