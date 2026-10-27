# Gap Report: test-v11-09

Artifact `mlbench` · generated 2026-10-14 21:48 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -27.6% | +3.9% | ±5.5% | `normalize=zscore`, `class_weight=balanced` |

## C1: test_accuracy (paper 0.7542)
**Fits but unsupported** · gap -27.6% → +3.9% · 53 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0094`, `B0141`, `B0142`, `B0143`, `B0144` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Config: `class_weight` naive `none`, changed to `balanced`
- Command:

  Replay: fork checkpoint `0d2d3f34-9b40-46c4-af90-edb1cd8d4262` and run
  ```
  RUN_TAG=6124ffc298a4 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight balanced --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7833, 0.7875, 0.7833, 0.7875, 0.7833; gap after +3.9%; result checkpoint `1b30eb5b-64a7-482f-9fcd-3e4c56b1ea31`
- Effect: candidate 0.7833 minus naive 0.5458 = +0.2375, 95% bootstrap interval [+0.2216, +0.2983] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.754 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7542 (headline claim)

### What did we measure?
- Naive median 0.5458 over 5 runs; repeats: 0.4875, 0.5667, 0.55, 0.5458, 0.4875
- Spread: range 0.4875 to 0.5667, noise band ±0.0418 (2 x MAD), CV 7.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -27.6% (noise band ±5.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -27.6% (it comes back)
- PASS · Counterfactual (reversal test): without `class_weight` the gap is +9.9% (it comes back)
- PASS · Held-out claim: C2: -24.4% to +8.7% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- FAIL · Evidence: `class_weight=balanced`: no evidence mentions 'balanced'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2375 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `aggregation`, `CPU`, `memory`, `OS`, `Python_version`, `random_module`, `floating_point`, `num_features`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (1.6 noise units, gap -18.8%); `normalize=minmax` (1.2 noise units, gap -21.0%)
- Near alternatives (closest across all claims):
  - `lr=0.001`, `normalize=zscore`: this claim +6.6%, mean |gap| 7.6% (5 runs)
  - `normalize=zscore`, `lr=0.5`: this claim +7.2%, mean |gap| 8.2% (5 runs)
  - `normalize=zscore`, `lr=0.1`: this claim +8.8%, mean |gap| 9.9% (5 runs)

### History matching (every measured configuration, all claims together)
- 17 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr, normalize`: lr=0.25, normalize=minmax (max I 0.3); lr=0.5, normalize=minmax (max I 0.8); lr=0.001, normalize=zscore (max I 1.22); lr=0.5, normalize=zscore (max I 1.67); +3 more
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 1.01); class_weight=balanced, normalize=zscore (max I 1.46)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 2)
- 2 separate islands (no single-knob move joins them): lr=0.25, normalize=minmax; lr=0.5, normalize=minmax; class_weight=balanced, normalize=minmax | lr=0.1, lr_schedule=step

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'normalize': 'minmax', 'class_weight': 'balanced'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore`, `class_weight=balanced` | 5 | +3.9% | +8.7% | 6.3% |
| `lr=0.001`, `normalize=zscore` | 5 | +6.6% | +8.6% | 7.6% |
| `normalize=zscore`, `lr=0.5` | 5 | +7.2% | +9.3% | 8.2% |
| `normalize=zscore`, `lr=0.1` | 5 | +8.8% | +11.0% | 9.9% |
| `normalize=zscore`, `lr=0.25` | 5 | +9.4% | +11.2% | 10.3% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `aggregation`, `CPU`, `memory`, `OS`, `Python_version`, `random_module`, `floating_point`, `num_features`, `--out`

## Provenance
- GapFinder commit: `e0f13d101585ad1609a15fbf67b70128f4cfffc8` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
