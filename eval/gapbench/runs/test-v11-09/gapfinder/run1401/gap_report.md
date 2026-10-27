# Gap Report: test-v11-09

Artifact `mlbench` · generated 2026-10-15 19:00 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -35.4% | -0.6% | ±3.3% | `class_weight=balanced`, `normalize=minmax` |

## C1: test_accuracy (paper 0.7542)
**Fits but unsupported** · gap -35.4% → -0.6% · 61 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0117`, `B0139`, `B0180`, `B0181`, `B0182` (5 run(s) of the same config)
- Config: `class_weight` naive `none`, changed to `balanced`
- Config: `normalize` naive `none`, changed to `minmax`
- Command:

  Replay: fork checkpoint `2f407ed4-5028-4fd2-9b87-1aed51148bee` and run
  ```
  RUN_TAG=557dc02a7f83 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight balanced --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.75, 0.7667, 0.7417, 0.75, 0.7583; gap after -0.6%; result checkpoint `a8d7682d-5dea-4fb3-b2ab-e7d906d51b95`
- Effect: candidate 0.75 minus naive 0.4875 = +0.2625, 95% bootstrap interval [+0.1992, +0.2792] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.754 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7542 (headline claim)

### What did we measure?
- Naive median 0.4875 over 5 runs; repeats: 0.5375, 0.475, 0.4875, 0.5625, 0.4875
- Spread: range 0.475 to 0.5625, noise band ±0.025 (2 x MAD), CV 7.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -35.4% (noise band ±3.3% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `class_weight` the gap is -21.0% (it comes back)
- PASS · Counterfactual (reversal test): without `normalize` the gap is -28.7% (it comes back)
- PASS · Held-out claim: C2: -33.0% to +7.1% (not worse beyond noise)
- FAIL · Evidence: `class_weight=balanced`: no evidence mentions 'balanced'; it fits, but nothing says the authors used it
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2625 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `PYTHONHASHSEED`, `PYTHON_VERSION`, `OMP_NUM_THREADS`, `CPU_MODEL`, `OS_TYPE`, `MEMORY_GB`, `FLOAT_DETERMINISM`, `DISK_TYPE`, `--out`, `NETWORK_LATENCY`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (7.67 noise units, gap +9.9%); `lr_schedule=cosine` (4.83 noise units, gap -19.3%); `lr=0.005` (2.33 noise units, gap -27.6%); `lr=0.5` (2.33 noise units, gap -27.6%); `lr=0.0005` (2.17 noise units, gap -28.2%) (and 5 more in the JSON)
- Near alternatives (closest across all claims):
  - `normalize=zscore`, `lr=2.5`: this claim +0.0%, mean |gap| 1.5% (5 runs)
  - `lr=0.5`, `normalize=minmax`: this claim +3.3%, mean |gap| 2.9% (5 runs)
  - `normalize=zscore`, `lr=0.0005`: this claim +3.3%, mean |gap| 3.9% (5 runs)

### History matching (every measured configuration, all claims together)
- 25 of 61 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr, normalize`: lr=0.5, normalize=minmax (max I 0.3); lr=0.0005, normalize=zscore (max I 0.49); lr=2.5, normalize=zscore (max I 0.59); lr=0.001, normalize=zscore (max I 1.2); +4 more
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 1.12); class_weight=balanced, normalize=zscore (max I 1.41)

Notes:
- stopped early: run budget of 200 reached (wanted 3 more run(s) of {'normalize': 'zscore', 'lr': '0.005'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore`, `lr=2.5` | 5 | +0.0% | +3.1% | 1.5% |
| `lr=0.5`, `normalize=minmax` | 5 | +3.3% | +2.5% | 2.9% |
| `class_weight=balanced`, `normalize=minmax` | 5 | -0.6% | +7.1% | 3.8% |
| `normalize=zscore`, `lr=0.0005` | 5 | +3.3% | +4.5% | 3.9% |
| `normalize=zscore`, `class_weight=balanced` | 5 | +3.9% | +8.7% | 6.3% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `PYTHONHASHSEED`, `PYTHON_VERSION`, `OMP_NUM_THREADS`, `CPU_MODEL`, `OS_TYPE`, `MEMORY_GB`, `FLOAT_DETERMINISM`, `DISK_TYPE`, `--out`, `NETWORK_LATENCY`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
