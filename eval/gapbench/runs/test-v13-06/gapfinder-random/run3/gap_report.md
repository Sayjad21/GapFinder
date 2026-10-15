# Gap Report: test-v13-06

Artifact `mlbench` · generated 2026-10-16 00:52 · 183 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -28.9% | -0.2% | ±0.7% | `normalize=zscore`, `n=5000` |

## C1: test_accuracy (paper 0.7558)
**Fits but unsupported** · gap -28.9% → -0.2% · 59 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0058`, `B0099`, `B0131`, `B0132`, `B0133` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Config: `n` naive `1200`, changed to `5000`
- Command:

  Replay: fork checkpoint `d5bdbb67-10a4-450d-883e-e0b379a393d0` and run
  ```
  RUN_TAG=c76a9230a9f9 "${PYTHON:-python3}" train.py --n 5000 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.757, 0.755, 0.753, 0.752, 0.754; gap after -0.2%; result checkpoint `d5f1bd63-f4fd-420a-8ab5-c25fe2338f85`
- Effect: candidate 0.754 minus naive 0.5375 = +0.2165, 95% bootstrap interval [+0.2155, +0.2698] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.756 test accuracy and 0.728 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7558 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.4792, 0.5375, 0.5375, 0.5375, 0.4917
- Spread: range 0.4792 to 0.5375, noise band ±0.005375 (2 x MAD), CV 5.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -28.9% (noise band ±0.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -23.5% (it comes back)
- PASS · Counterfactual (reversal test): without `n` the gap is +9.4% (it comes back)
- PASS · Held-out claim: C2: -25.5% to +0.7% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- FAIL · Evidence: `n=5000`: no evidence mentions '5000'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2165 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `PYTHON_VERSION`, `OS`, `CPU_ARCH`, `MATH_LIBRARY`, `FLOATING_POINT_ROUNDING`, `RANDOM_MODULE_IMPLEMENTATION`, `MEMORY_SIZE`, `STORAGE_TYPE`, `PYTHONHASHSEED`, `PYTHONOPTIMIZE`, `OPENBLAS_THREADS`, `MKL_NUM_THREADS`, `NUMEXPR_MAX_THREADS`, `PYTHONMALLOC`, `PYTHONFAULTHANDLER`, `out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (16.28 noise units, gap -17.3%); `normalize=minmax` (10.85 noise units, gap -21.2%); `n=120` (8.52 noise units, gap -22.8%); `n=240` (8.52 noise units, gap -22.8%); `n=2400` (5.43 noise units, gap -25.0%) (and 2 more in the JSON)
- Near alternatives (closest across all claims):
  - `n=12000`, `normalize=zscore`: this claim +0.3%, mean |gap| 0.3% (5 runs)
  - `n=6000`, `normalize=zscore`: this claim -0.9%, mean |gap| 1.1% (5 runs)
  - `normalize=zscore`, `n=2000`: this claim +1.2%, mean |gap| 1.8% (5 runs)

### Equally good configurations
The target claim can't tell these 6 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `n=5000, normalize=zscore` (reported)
- `n=12000, normalize=zscore`
- `n=6000, normalize=zscore`
- `n=2000, normalize=zscore`
- `class_weight=balanced, normalize=minmax`
- `n=600, normalize=zscore`

### History matching (every measured configuration, all claims together)
- 18 of 57 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `n, normalize`: n=12000, normalize=zscore (max I 0.05); n=5000, normalize=zscore (max I 0.12); n=6000, normalize=zscore (max I 0.23); n=2000, normalize=zscore (max I 0.42); +4 more
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 1.2); class_weight=balanced, normalize=zscore (max I 1.35)
- 2 separate islands (no single-knob move joins them): n=12000, normalize=zscore; n=5000, normalize=zscore; n=6000, normalize=zscore | lr_schedule=cosine, n=12000; lr_schedule=cosine, n=120; lr_schedule=cosine, n=5000
- Equally good values: `n` in {5000, 6000, 12000}

Notes:
- configurations the target claim can't tell apart from the answer: n=5000, normalize=zscore; n=12000, normalize=zscore; n=6000, normalize=zscore; n=2000, normalize=zscore; class_weight=balanced, normalize=minmax; n=600, normalize=zscore
- equally good values within one noise band (measured): n in {5000, 6000, 12000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `n=12000`, `normalize=zscore` | 5 | +0.3% | +0.4% | 0.3% |
| `n=5000`, `normalize=zscore` | 5 | -0.2% | +0.7% | 0.5% |
| `n=6000`, `normalize=zscore` | 5 | -0.9% | -1.3% | 1.1% |
| `normalize=zscore`, `n=2000` | 5 | +1.2% | +2.3% | 1.8% |
| `n=600`, `normalize=zscore` | 5 | -1.9% | -3.8% | 2.8% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `n=1`: invalid_value, Setting n=1 results in an empty training subset, causing an IndexError when the code tries to access Xtr[0]. A small but valid value like n=2 retains the intent of a low n while ensuring the training data is non‑empty; retried as `n=2`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `PYTHON_VERSION`, `OS`, `CPU_ARCH`, `MATH_LIBRARY`, `FLOATING_POINT_ROUNDING`, `RANDOM_MODULE_IMPLEMENTATION`, `MEMORY_SIZE`, `STORAGE_TYPE`, `PYTHONHASHSEED`, `PYTHONOPTIMIZE`, `OPENBLAS_THREADS`, `MKL_NUM_THREADS`, `NUMEXPR_MAX_THREADS`, `PYTHONMALLOC`, `PYTHONFAULTHANDLER`, `out`

## Provenance
- GapFinder commit: `e9c31fd1405f5c8aae4bd880eadcdc8d491fad02` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0006, sandbox reported $0.0000 (total $0.0006; this search; ledger extraction is included only if it shared the search's router)
