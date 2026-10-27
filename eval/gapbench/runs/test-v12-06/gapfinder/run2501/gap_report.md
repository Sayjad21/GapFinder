# Gap Report: test-v12-06

Artifact `mlbench` · generated 2026-10-16 01:59 · 199 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -37.3% | -0.5% | ±1.1% | `positive_rate=0.1`, `lr_schedule=cosine` |

## C1: test_accuracy (paper 0.7708)
**Fits but unsupported** · gap -37.3% → -0.5% · 65 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0149`, `B0151`, `B0197`, `B0198`, `B0199` (5 run(s) of the same config)
- Config: `positive_rate` naive `0.3`, changed to `0.1`
- Config: `lr_schedule` naive `const`, changed to `cosine`
- Command:

  Replay: fork checkpoint `94e0e71b-353e-42ea-8366-7a01851c371f` and run
  ```
  RUN_TAG=290ee9932ea2 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.1 --label_noise 0.05 --split 0.8 --normalize none --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule cosine --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7667, 0.7458, 0.8083, 0.7458, 0.7667; gap after -0.5%; result checkpoint `54e913a4-1001-420f-a9fc-866371f74c6c`
- Effect: candidate 0.7667 minus naive 0.4833 = +0.2834, 95% bootstrap interval [+0.2342, +0.3133] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.771 test accuracy and 0.745 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7708 (headline claim)

### What did we measure?
- Naive median 0.4833 over 5 runs; repeats: 0.475, 0.5375, 0.4792, 0.4833, 0.4833
- Spread: range 0.475 to 0.5375, noise band ±0.0082 (2 x MAD), CV 5.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -37.3% (noise band ±1.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `positive_rate` the gap is -18.6% (it comes back)
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is -34.1% (it comes back)
- PASS · Held-out claim: C2: -35.7% to -19.3% (not worse beyond noise)
- FAIL · Evidence: `positive_rate=0.1`: no evidence mentions '0.1'; it fits, but nothing says the authors used it
- FAIL · Evidence: `lr_schedule=cosine`: no evidence mentions 'cosine'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2834 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `NUM_RUNS`, `AGGREGATION`, `PYTHON_VERSION`, `OS`, `CPU_ARCH`, `CPU_CORES`, `MEMORY_SIZE`, `DISK_TYPE`, `NETWORK`, `PYTHONHASHSEED`, `OMP_NUM_THREADS`, `MKL_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `NUMEXPR_NUM_THREADS`, `RANDOM_SEED`, `PYTHON_RANDOM_MODULE`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (28.45 noise units, gap +7.0%); `normalize=minmax` (13.72 noise units, gap -22.7%); `weight_decay=1e-4` (9.66 noise units, gap -27.0%); `positive_rate=0.4` (9.66 noise units, gap -27.0%); `positive_rate=0.7` (9.15 noise units, gap -27.6%) (and 5 more in the JSON)
- Near alternatives (closest across all claims):
  - `normalize=zscore`, `positive_rate=0.2`: this claim +3.2%, mean |gap| 1.7% (2 runs)
  - `normalize=zscore`, `positive_rate=0.5`: this claim +2.2%, mean |gap| 4.0% (2 runs)
  - `normalize=zscore`, `positive_rate=0.15`: this claim +1.1%, mean |gap| 4.9% (5 runs)

### History matching (every measured configuration, all claims together)
- 16 of 63 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `normalize, positive_rate`: normalize=zscore, positive_rate=0.2 (max I 0.56); normalize=zscore, positive_rate=0.5 (max I 0.95); normalize=zscore, positive_rate=0.4 (max I 1.3); normalize=zscore, positive_rate=0.65 (max I 1.45)
  - `normalize, weight_decay`: normalize=zscore, weight_decay=0.01 (max I 1.39); normalize=zscore, weight_decay=1e-4 (max I 1.45); normalize=zscore, weight_decay=1e-3 (max I 1.45)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.45); lr_schedule=step, normalize=zscore (max I 1.45)
  - `normalize`: normalize=zscore (max I 1.54)
- 2 separate islands (no single-knob move joins them): normalize=zscore, positive_rate=0.2; normalize=zscore, positive_rate=0.5; normalize=zscore, positive_rate=0.4 | lr_schedule=cosine, positive_rate=0.7; lr_schedule=cosine, positive_rate=0.2; lr_schedule=cosine, positive_rate=0.93

Notes:
- stopped early: run budget of 200 reached (wanted 3 more run(s) of {'normalize': 'zscore', 'positive_rate': '0.5'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore`, `positive_rate=0.2` | 2 | +3.2% | -0.2% | 1.7% |
| `normalize=zscore`, `positive_rate=0.5` | 2 | +2.2% | +5.8% | 4.0% |
| `normalize=zscore`, `positive_rate=0.15` | 5 | +1.1% | -8.7% | 4.9% |
| `normalize=zscore`, `positive_rate=0.4` | 2 | +4.9% | +7.9% | 6.4% |
| `normalize=zscore`, `positive_rate=0.65` | 2 | +7.0% | +8.8% | 7.9% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `NUM_RUNS`, `AGGREGATION`, `PYTHON_VERSION`, `OS`, `CPU_ARCH`, `CPU_CORES`, `MEMORY_SIZE`, `DISK_TYPE`, `NETWORK`, `PYTHONHASHSEED`, `OMP_NUM_THREADS`, `MKL_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `NUMEXPR_NUM_THREADS`, `RANDOM_SEED`, `PYTHON_RANDOM_MODULE`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
