# Gap Report: test-v13-06

Artifact `mlbench` · generated 2026-10-16 01:37 · 172 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -34.9% | -0.1% | ±6.6% | `n=12000`, `normalize=zscore` |

## C1: test_accuracy (paper 0.7558)
**Fits but unsupported** · gap -34.9% → -0.1% · 53 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0069`, `B0094`, `B0124`, `B0125`, `B0126` (5 run(s) of the same config)
- Config: `n` naive `1200`, changed to `12000`
- Config: `normalize` naive `none`, changed to `zscore`
- Command:

  Replay: fork checkpoint `2ba688e3-ed84-4a68-885c-3dd408201107` and run
  ```
  RUN_TAG=276f79af37c6 "${PYTHON:-python3}" train.py --n 12000 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7554, 0.7604, 0.7538, 0.7571, 0.755; gap after -0.1%; result checkpoint `a495017b-bf45-4516-bfa5-4187cf2faa07`
- Effect: candidate 0.7554 minus naive 0.4917 = +0.2637, 95% bootstrap interval [+0.1921, +0.2907] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.756 test accuracy and 0.728 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7558 (headline claim)

### What did we measure?
- Naive median 0.4917 over 5 runs; repeats: 0.4917, 0.4667, 0.5375, 0.5708, 0.4667
- Spread: range 0.4667 to 0.5708, noise band ±0.05 (2 x MAD), CV 9.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -34.9% (noise band ±6.6% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `n` the gap is +9.7% (it comes back)
- PASS · Counterfactual (reversal test): without `normalize` the gap is -26.9% (it comes back)
- PASS · Held-out claim: C2: -33.0% to -0.1% (not worse beyond noise)
- FAIL · Evidence: `n=12000`: no evidence mentions '12000'; it fits, but nothing says the authors used it
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2637 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `PYTHON_VERSION`, `OS`, `CPU_ARCH`, `MATH_LIBRARY`, `FLOATING_POINT_ROUNDING`, `RANDOM_MODULE_IMPLEMENTATION`, `MEMORY_SIZE`, `STORAGE_TYPE`, `PYTHONHASHSEED`, `PYTHONOPTIMIZE`, `OPENBLAS_THREADS`, `MKL_NUM_THREADS`, `NUMEXPR_MAX_THREADS`, `PYTHONMALLOC`, `PYTHONFAULTHANDLER`, `out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `n=24` (4.4 noise units, gap +5.8%); `n=120` (3.5 noise units, gap -11.8%); `lr_schedule=cosine` (2.75 noise units, gap -16.8%); `normalize=minmax` (2.08 noise units, gap -21.2%); `n=5000` (1.65 noise units, gap -24.1%) (and 4 more in the JSON)
- Near alternatives (closest across all claims):
  - `n=5000`, `normalize=zscore`: this claim -0.4%, mean |gap| 0.4% (5 runs)
  - `n=6000`, `normalize=zscore`: this claim -0.9%, mean |gap| 1.1% (5 runs)
  - `n=12000`, `normalize=minmax`: this claim -2.3%, mean |gap| 4.1% (5 runs)

### Equally good configurations
The target claim can't tell these 4 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `n=12000, normalize=zscore` (reported)
- `n=5000, normalize=zscore`
- `n=6000, normalize=zscore`
- `class_weight=balanced, normalize=minmax`

### History matching (every measured configuration, all claims together)
- 20 of 52 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `n, normalize`: n=12000, normalize=zscore (max I 0.02); n=5000, normalize=zscore (max I 0.09); n=6000, normalize=zscore (max I 0.2); n=120, normalize=zscore (max I 0.64); +2 more
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 1.09); class_weight=balanced, normalize=zscore (max I 1.21)
  - `normalize`: normalize=zscore (max I 1.7)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.72)
- Equally good values: `n` in {120, 5000, 6000, 12000}; `normalize` in {minmax, zscore}

Notes:
- configurations the target claim can't tell apart from the answer: n=12000, normalize=zscore; n=5000, normalize=zscore; n=6000, normalize=zscore; class_weight=balanced, normalize=minmax
- equally good values within one noise band (measured): n in {120, 5000, 6000, 12000}; normalize in {minmax, zscore}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `n=12000`, `normalize=zscore` | 5 | -0.1% | -0.1% | 0.1% |
| `n=5000`, `normalize=zscore` | 5 | -0.4% | +0.5% | 0.4% |
| `n=6000`, `normalize=zscore` | 5 | -0.9% | -1.3% | 1.1% |
| `n=12000`, `normalize=minmax` | 5 | -2.3% | -5.8% | 4.1% |
| `n=120`, `normalize=zscore` | 5 | -6.3% | -2.5% | 4.4% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `n=1`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `PYTHON_VERSION`, `OS`, `CPU_ARCH`, `MATH_LIBRARY`, `FLOATING_POINT_ROUNDING`, `RANDOM_MODULE_IMPLEMENTATION`, `MEMORY_SIZE`, `STORAGE_TYPE`, `PYTHONHASHSEED`, `PYTHONOPTIMIZE`, `OPENBLAS_THREADS`, `MKL_NUM_THREADS`, `NUMEXPR_MAX_THREADS`, `PYTHONMALLOC`, `PYTHONFAULTHANDLER`, `out`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
