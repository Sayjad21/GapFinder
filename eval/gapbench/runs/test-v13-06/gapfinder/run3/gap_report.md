# Gap Report: test-v13-06

Artifact `mlbench` · generated 2026-10-16 00:51 · 190 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -37.2% | -0.2% | ±2.2% | `n=5000`, `normalize=zscore` |

## C1: test_accuracy (paper 0.7558)
**Fits but unsupported** · gap -37.2% → -0.2% · 54 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0070`, `B0100`, `B0135`, `B0136`, `B0137` (5 run(s) of the same config)
- Config: `n` naive `1200`, changed to `5000`
- Config: `normalize` naive `none`, changed to `zscore`
- Command:

  Replay: fork checkpoint `b321462d-1af8-4c5b-a521-fa752c0e9841` and run
  ```
  RUN_TAG=f973fc93c20c "${PYTHON:-python3}" train.py --n 5000 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.753, 0.754, 0.757, 0.754, 0.751; gap after -0.2%; result checkpoint `dbb53953-d3ef-4728-bfd3-3bed46649c48`
- Effect: candidate 0.754 minus naive 0.475 = +0.279, 95% bootstrap interval [+0.208, +0.2879] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.756 test accuracy and 0.728 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7558 (headline claim)

### What did we measure?
- Naive median 0.475 over 5 runs; repeats: 0.4792, 0.4667, 0.4667, 0.475, 0.5625
- Spread: range 0.4667 to 0.5625, noise band ±0.0166 (2 x MAD), CV 8.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -37.2% (noise band ±2.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `n` the gap is +9.7% (it comes back)
- PASS · Counterfactual (reversal test): without `normalize` the gap is -25.5% (it comes back)
- PASS · Held-out claim: C2: -35.4% to +0.7% (not worse beyond noise)
- FAIL · Evidence: `n=5000`: no evidence mentions '5000'; it fits, but nothing says the authors used it
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.279 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `PYTHON_VERSION`, `OS`, `CPU_ARCH`, `MATH_LIBRARY`, `FLOATING_POINT_ROUNDING`, `RANDOM_MODULE_IMPLEMENTATION`, `MEMORY_SIZE`, `STORAGE_TYPE`, `PYTHONHASHSEED`, `PYTHONOPTIMIZE`, `OPENBLAS_THREADS`, `MKL_NUM_THREADS`, `NUMEXPR_MAX_THREADS`, `PYTHONMALLOC`, `PYTHONFAULTHANDLER`, `out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `n=24` (14.25 noise units, gap +5.8%); `lr_schedule=cosine` (8.28 noise units, gap -19.0%); `normalize=minmax` (7.28 noise units, gap -21.2%); `n=120` (6.52 noise units, gap -22.8%); `lr_schedule=step` (5.52 noise units, gap -25.0%) (and 4 more in the JSON)
- Near alternatives (closest across all claims):
  - `n=120`, `normalize=zscore`: this claim -0.8%, mean |gap| 1.8% (5 runs)
  - `normalize=zscore`, `n=600`: this claim -1.9%, mean |gap| 2.8% (5 runs)
  - `class_weight=balanced`, `normalize=minmax`: this claim +2.5%, mean |gap| 4.8% (5 runs)

### Equally good configurations
The target claim can't tell these 4 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `n=5000, normalize=zscore` (reported)
- `n=120, normalize=zscore`
- `n=600, normalize=zscore`
- `class_weight=balanced, normalize=minmax`

### History matching (every measured configuration, all claims together)
- 14 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `n, normalize`: n=5000, normalize=zscore (max I 0.1); n=120, normalize=zscore (max I 0.31); n=600, normalize=zscore (max I 0.6); n=2400, normalize=zscore (max I 0.96); +1 more
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 1.14); class_weight=balanced, normalize=zscore (max I 1.28)
  - `normalize`: normalize=zscore (max I 1.77)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.8); lr_schedule=step, normalize=zscore (max I 1.8)
- Equally good values: `n` in {120, 600, 5000}

Notes:
- configurations the target claim can't tell apart from the answer: n=5000, normalize=zscore; n=120, normalize=zscore; n=600, normalize=zscore; class_weight=balanced, normalize=minmax
- equally good values within one noise band (measured): n in {120, 600, 5000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore`, `n=5000` | 5 | -0.2% | +0.7% | 0.5% |
| `n=120`, `normalize=zscore` | 5 | -0.8% | +2.8% | 1.8% |
| `normalize=zscore`, `n=600` | 5 | -1.9% | -3.8% | 2.8% |
| `class_weight=balanced`, `normalize=minmax` | 5 | +2.5% | +7.1% | 4.8% |
| `normalize=zscore`, `n=2400` | 5 | -6.0% | -4.5% | 5.2% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `n=1`: invalid_value, Setting n=1 results in insufficient data leading to an empty training subset, causing an IndexError when accessing Xtr[0]; retried as `n=2`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `PYTHON_VERSION`, `OS`, `CPU_ARCH`, `MATH_LIBRARY`, `FLOATING_POINT_ROUNDING`, `RANDOM_MODULE_IMPLEMENTATION`, `MEMORY_SIZE`, `STORAGE_TYPE`, `PYTHONHASHSEED`, `PYTHONOPTIMIZE`, `OPENBLAS_THREADS`, `MKL_NUM_THREADS`, `NUMEXPR_MAX_THREADS`, `PYTHONMALLOC`, `PYTHONFAULTHANDLER`, `out`

## Provenance
- GapFinder commit: `e9c31fd1405f5c8aae4bd880eadcdc8d491fad02` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0725, sandbox reported $0.0000 (total $0.0725; this search; ledger extraction is included only if it shared the search's router)
