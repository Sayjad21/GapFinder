# Gap Report: test-gen-06

Artifact `mlbench` · generated 2026-10-14 21:43 · 194 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -27.5% | +0.0% | ±3.4% | `normalize=zscore`, `n=600` |

## C1: test_accuracy (paper 0.7417)
**Fits but unsupported** · gap -27.5% → +0.0% · 53 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0046`, `B0095`, `B0096`, `B0097`, `B0098` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Config: `n` naive `1200`, changed to `600`
- Command:

  Replay: fork checkpoint `bf808c37-d1f0-40c6-99e4-6bd636f62132` and run
  ```
  RUN_TAG=09cada6d337a "${PYTHON:-python3}" train.py --n 600 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7417, 0.7417, 0.7417, 0.7417, 0.7417; gap after +0.0%; result checkpoint `05fdcce0-0f8d-46fb-8d32-b55bcacc8d3f`
- Effect: candidate 0.7417 minus naive 0.5375 = +0.2042, 95% bootstrap interval [+0.1942, +0.26] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.742 test accuracy and 0.700 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7417 accuracy (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5417, 0.5042, 0.5375, 0.4667, 0.55
- Spread: range 0.4667 to 0.55, noise band ±0.025 (2 x MAD), CV 6.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -27.5% (noise band ±3.4% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -24.7% (it comes back)
- PASS · Counterfactual (reversal test): without `n` the gap is +11.8% (it comes back)
- PASS · Held-out claim: C2: -22.6% to +0.0% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- FAIL · Evidence: `n=600`: no evidence mentions '600'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2042 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `NUM_RUNS`, `CPU_MODEL`, `PYTHON_VERSION`, `LIBM_VERSION`, `OS_VERSION`, `ROUNDING_PRECISION`, `MEMORY_SIZE`, `STORAGE_DEVICE`, `CPU_CORES`, `ULIMIT_SETTINGS`, `FILESYSTEM`, `PYTHONHASHSEED`, `RANDOM_MODULE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (3.17 noise units, gap -16.9%); `n=24` (2.5 noise units, gap -19.1%); `normalize=minmax` (2.33 noise units, gap -19.7%)
- Near alternatives (closest across all claims):
  - `n=12000`, `normalize=minmax`: this claim -1.1%, mean |gap| 2.4% (5 runs)
  - `normalize=zscore`, `n=2400`: this claim -4.2%, mean |gap| 2.5% (5 runs)
  - `normalize=zscore`, `n=12000`: this claim +2.1%, mean |gap| 3.2% (5 runs)

### History matching (every measured configuration, all claims together)
- 14 of 52 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `n, normalize`: n=600, normalize=zscore (max I 0); n=12000, normalize=minmax (max I 0.62); n=12000, normalize=zscore (max I 0.69); n=2400, normalize=zscore (max I 0.7); +3 more
  - `lr_schedule, n`: lr_schedule=cosine, n=12000 (max I 1.68)
  - `class_weight, normalize`: class_weight=balanced, normalize=zscore (max I 1.96); class_weight=balanced, normalize=minmax (max I 2)
- Equally good values: `n` in {600, 1000, 2000, 12000}

Notes:
- equally good values within one noise band (measured): n in {600, 1000, 2000, 12000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore`, `n=600` | 5 | +0.0% | +0.0% | 0.0% |
| `n=12000`, `normalize=minmax` | 5 | -1.1% | -3.6% | 2.4% |
| `normalize=zscore`, `n=2400` | 5 | -4.2% | -0.7% | 2.5% |
| `normalize=zscore`, `n=12000` | 5 | +2.1% | +4.3% | 3.2% |
| `normalize=zscore`, `n=1000` | 5 | +3.1% | +4.9% | 4.0% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `n=1`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `NUM_RUNS`, `CPU_MODEL`, `PYTHON_VERSION`, `LIBM_VERSION`, `OS_VERSION`, `ROUNDING_PRECISION`, `MEMORY_SIZE`, `STORAGE_DEVICE`, `CPU_CORES`, `ULIMIT_SETTINGS`, `FILESYSTEM`, `PYTHONHASHSEED`, `RANDOM_MODULE`, `--out`

## Provenance
- GapFinder commit: `e0f13d101585ad1609a15fbf67b70128f4cfffc8` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
