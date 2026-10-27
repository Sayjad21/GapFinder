# Gap Report: test-v11-09

Artifact `mlbench` · generated 2026-10-15 19:24 · 199 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -35.4% | -2.8% | ±5.5% | `normalize=minmax`, `lr=0.25` |

## C1: test_accuracy (paper 0.7542)
**Fits but unsupported** · gap -35.4% → -2.8% · 61 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0113`, `B0143`, `B0185`, `B0186`, `B0187` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `lr` naive `0.05`, changed to `0.25`
- Command:

  Replay: fork checkpoint `a7e43a7f-3732-4d6a-ad21-2acdd89a8c69` and run
  ```
  RUN_TAG=e1b924991b90 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.25 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7333, 0.7667, 0.725, 0.7167, 0.7667; gap after -2.8%; result checkpoint `b697e9b9-9c92-4ac1-8340-18db4281712d`
- Effect: candidate 0.7333 minus naive 0.4875 = +0.2458, 95% bootstrap interval [+0.1942, +0.2817] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.754 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7542 (headline claim)

### What did we measure?
- Naive median 0.4875 over 5 runs; repeats: 0.4875, 0.5375, 0.5375, 0.4667, 0.4875
- Spread: range 0.4667 to 0.5375, noise band ±0.0416 (2 x MAD), CV 6.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -35.4% (noise band ±5.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -32.3% (it comes back)
- PASS · Counterfactual (reversal test): without `lr` the gap is -21.0% (it comes back)
- PASS · Held-out claim: C2: -33.0% to -6.1% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- FAIL · Evidence: `lr=0.25`: no evidence mentions '0.25'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2458 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `PYTHONHASHSEED`, `PYTHON_VERSION`, `OMP_NUM_THREADS`, `CPU_MODEL`, `OS_TYPE`, `MEMORY_GB`, `FLOAT_DETERMINISM`, `DISK_TYPE`, `--out`, `NETWORK_LATENCY`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (4.61 noise units, gap +9.9%); `lr_schedule=cosine` (3.31 noise units, gap -17.1%); `lr_schedule=step` (1.7 noise units, gap -26.0%); `lr=0.1` (1.5 noise units, gap -27.1%); `lr=0.01` (1.3 noise units, gap -28.2%) (and 2 more in the JSON)
- Near alternatives (closest across all claims):
  - `normalize=minmax`, `lr=2.5`: this claim +5.5%, mean |gap| 5.3% (5 runs)
  - `class_weight=balanced`, `normalize=minmax`: this claim +2.2%, mean |gap| 5.5% (5 runs)
  - `lr=0.001`, `normalize=zscore`: this claim +5.2%, mean |gap| 6.1% (2 runs)

### History matching (every measured configuration, all claims together)
- 22 of 61 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr, normalize`: lr=2.5, normalize=minmax (max I 0.22); lr=0.25, normalize=minmax (max I 0.72); lr=0.001, normalize=zscore (max I 1.05); lr=0.0005, normalize=zscore (max I 1.34); +4 more
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 1.45); class_weight=balanced, normalize=zscore (max I 1.47)
- 3 separate islands (no single-knob move joins them): lr=2.5, normalize=minmax; lr=0.25, normalize=minmax; lr=0.001, normalize=zscore | lr=0.25, lr_schedule=cosine; lr=2.5, lr_schedule=cosine; lr=0.5, lr_schedule=cosine | class_weight=balanced, lr_schedule=cosine

Notes:
- stopped early: run budget of 200 reached (wanted 3 more run(s) of {'normalize': 'zscore', 'lr': '0.001'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax`, `lr=0.25` | 5 | -2.8% | -6.1% | 4.4% |
| `normalize=minmax`, `lr=2.5` | 5 | +5.5% | +5.1% | 5.3% |
| `class_weight=balanced`, `normalize=minmax` | 5 | +2.2% | +8.8% | 5.5% |
| `lr=0.001`, `normalize=zscore` | 2 | +5.2% | +7.0% | 6.1% |
| `normalize=zscore`, `lr=2.5` | 5 | +5.0% | +7.3% | 6.2% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `PYTHONHASHSEED`, `PYTHON_VERSION`, `OMP_NUM_THREADS`, `CPU_MODEL`, `OS_TYPE`, `MEMORY_GB`, `FLOAT_DETERMINISM`, `DISK_TYPE`, `--out`, `NETWORK_LATENCY`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
