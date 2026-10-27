# Gap Report: test-v11-09

Artifact `mlbench` · generated 2026-10-16 01:25 · 199 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -31.5% | +1.7% | ±5.5% | `normalize=minmax`, `class_weight=balanced` |

## C1: test_accuracy (paper 0.7542)
**Fits but unsupported** · gap -31.5% → +1.7% · 61 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0114`, `B0137`, `B0173`, `B0174`, `B0175` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `class_weight` naive `none`, changed to `balanced`
- Command:

  Replay: fork checkpoint `040cbc4f-0a32-45f4-845e-694eae02dc9e` and run
  ```
  RUN_TAG=d59680bbc677 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight balanced --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7667, 0.7667, 0.7625, 0.7667, 0.7667; gap after +1.7%; result checkpoint `85c1757a-2bd3-47d5-8e5d-c684ef318fe4`
- Effect: candidate 0.7667 minus naive 0.5167 = +0.25, 95% bootstrap interval [+0.2275, +0.2917] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.754 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7542 (headline claim)

### What did we measure?
- Naive median 0.5167 over 5 runs; repeats: 0.5375, 0.5167, 0.4667, 0.4833, 0.5375
- Spread: range 0.4667 to 0.5375, noise band ±0.0416 (2 x MAD), CV 6.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -31.5% (noise band ±5.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -34.3% (it comes back)
- PASS · Counterfactual (reversal test): without `class_weight` the gap is -21.0% (it comes back)
- PASS · Held-out claim: C2: -29.2% to +8.3% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- FAIL · Evidence: `class_weight=balanced`: no evidence mentions 'balanced'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.25 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `PYTHONHASHSEED`, `PYTHON_VERSION`, `OMP_NUM_THREADS`, `CPU_MODEL`, `OS_TYPE`, `MEMORY_GB`, `FLOAT_DETERMINISM`, `DISK_TYPE`, `--out`, `NETWORK_LATENCY`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (3.91 noise units, gap +9.9%); `lr_schedule=cosine` (2.5 noise units, gap -17.7%); `lr=0.005` (1.1 noise units, gap -25.4%); `lr=0.025` (1 noise units, gap -26.0%)
- Near alternatives (closest across all claims):
  - `lr=0.0005`, `normalize=zscore`: this claim +4.4%, mean |gap| 5.5% (5 runs)
  - `normalize=minmax`, `lr=0.5`: this claim +5.0%, mean |gap| 5.6% (5 runs)
  - `lr=2.5`, `normalize=zscore`: this claim +5.0%, mean |gap| 5.7% (5 runs)

### History matching (every measured configuration, all claims together)
- 22 of 61 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr, normalize`: lr=0.5, normalize=minmax (max I 0.88); lr=0.0005, normalize=zscore (max I 0.99); lr=2.5, normalize=zscore (max I 1.19); lr=0.001, normalize=zscore (max I 1.64); +2 more
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 1.38); class_weight=balanced, normalize=zscore (max I 1.45)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.84); lr_schedule=step, normalize=zscore (max I 1.84)
- 2 separate islands (no single-knob move joins them): lr=0.5, normalize=minmax; lr=0.0005, normalize=zscore; lr=2.5, normalize=zscore | lr=0.25, lr_schedule=cosine; lr=0.1, lr_schedule=cosine; lr=0.025, lr_schedule=cosine

Notes:
- stopped early: run budget of 200 reached (wanted 3 more run(s) of {'normalize': 'zscore', 'lr': '0.1'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax`, `class_weight=balanced` | 5 | +1.7% | +8.3% | 5.0% |
| `lr=0.0005`, `normalize=zscore` | 5 | +4.4% | +6.6% | 5.5% |
| `normalize=minmax`, `lr=0.5` | 5 | +5.0% | +6.2% | 5.6% |
| `lr=2.5`, `normalize=zscore` | 5 | +5.0% | +6.4% | 5.7% |
| `normalize=zscore`, `class_weight=balanced` | 5 | +3.9% | +8.7% | 6.3% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `PYTHONHASHSEED`, `PYTHON_VERSION`, `OMP_NUM_THREADS`, `CPU_MODEL`, `OS_TYPE`, `MEMORY_GB`, `FLOAT_DETERMINISM`, `DISK_TYPE`, `--out`, `NETWORK_LATENCY`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
