# Gap Report: test-gen-06

Artifact `mlbench` · generated 2026-10-15 18:50 · 197 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -34.8% | +0.0% | ±4.5% | `n=600`, `normalize=zscore` |

## C1: test_accuracy (paper 0.7417)
**Fits but unsupported** · gap -34.8% → +0.0% · 61 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0075`, `B0106`, `B0142`, `B0143`, `B0144` (5 run(s) of the same config)
- Config: `n` naive `1200`, changed to `600`
- Config: `normalize` naive `none`, changed to `zscore`
- Command:

  Replay: fork checkpoint `c66553ed-b59d-4596-875d-9f9f91f9d71c` and run
  ```
  RUN_TAG=e80667740be9 "${PYTHON:-python3}" train.py --n 600 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7417, 0.7417, 0.7417, 0.7417, 0.7417; gap after +0.0%; result checkpoint `e6375fd0-9870-46c7-af59-88ef3d4561f5`
- Effect: candidate 0.7417 minus naive 0.4833 = +0.2584, 95% bootstrap interval [+0.1842, +0.2733] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.742 test accuracy and 0.700 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7417 accuracy (headline claim)

### What did we measure?
- Naive median 0.4833 over 5 runs; repeats: 0.5375, 0.5625, 0.475, 0.4833, 0.4667
- Spread: range 0.4667 to 0.5625, noise band ±0.0332 (2 x MAD), CV 8.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -34.8% (noise band ±4.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `n` the gap is +11.2% (it comes back)
- PASS · Counterfactual (reversal test): without `normalize` the gap is -29.2% (it comes back)
- PASS · Held-out claim: C2: -31.7% to +0.0% (not worse beyond noise)
- FAIL · Evidence: `n=600`: no evidence mentions '600'; it fits, but nothing says the authors used it
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2584 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `NUM_RUNS`, `CPU_MODEL`, `PYTHON_VERSION`, `LIBM_VERSION`, `OS_VERSION`, `ROUNDING_PRECISION`, `MEMORY_SIZE`, `STORAGE_DEVICE`, `CPU_CORES`, `ULIMIT_SETTINGS`, `FILESYSTEM`, `PYTHONHASHSEED`, `RANDOM_MODULE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `n=24` (6.03 noise units, gap +7.9%); `lr_schedule=cosine` (4.64 noise units, gap -14.0%); `n=2000` (3.67 noise units, gap -18.4%); `normalize=minmax` (3.39 noise units, gap -19.7%); `n=120` (3.01 noise units, gap -21.4%) (and 2 more in the JSON)
- Near alternatives (closest across all claims):
  - `n=6000`, `normalize=zscore`: this claim +1.2%, mean |gap| 2.0% (5 runs)
  - `n=12000`, `normalize=minmax`: this claim -1.0%, mean |gap| 2.2% (5 runs)
  - `n=2400`, `normalize=zscore`: this claim -4.2%, mean |gap| 2.5% (5 runs)

### Equally good configurations
The target claim can't tell these 5 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `n=600, normalize=zscore` (reported)
- `n=12000, normalize=minmax`
- `n=6000, normalize=zscore`
- `n=120, normalize=zscore`
- `n=12000, normalize=zscore`

### History matching (every measured configuration, all claims together)
- 29 of 58 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `n, normalize`: n=600, normalize=zscore (max I 0); n=6000, normalize=zscore (max I 0.43); n=12000, normalize=minmax (max I 0.46); n=12000, normalize=zscore (max I 0.6); +5 more
  - `lr_schedule, n`: lr_schedule=cosine, n=12000 (max I 1.59)
- Equally good values: `n` in {120, 600, 1000, 2000, 2400, 6000, 12000}

Notes:
- configurations the target claim can't tell apart from the answer: n=600, normalize=zscore; n=12000, normalize=minmax; n=6000, normalize=zscore; n=120, normalize=zscore; n=12000, normalize=zscore
- equally good values within one noise band (measured): n in {120, 600, 1000, 2000, 2400, 6000, 12000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `n=600`, `normalize=zscore` | 5 | +0.0% | +0.0% | 0.0% |
| `n=6000`, `normalize=zscore` | 5 | +1.2% | +2.8% | 2.0% |
| `n=12000`, `normalize=minmax` | 5 | -1.0% | -3.3% | 2.2% |
| `n=2400`, `normalize=zscore` | 5 | -4.2% | -0.7% | 2.5% |
| `n=12000`, `normalize=zscore` | 5 | +1.9% | +3.9% | 2.9% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `n=1`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `NUM_RUNS`, `CPU_MODEL`, `PYTHON_VERSION`, `LIBM_VERSION`, `OS_VERSION`, `ROUNDING_PRECISION`, `MEMORY_SIZE`, `STORAGE_DEVICE`, `CPU_CORES`, `ULIMIT_SETTINGS`, `FILESYSTEM`, `PYTHONHASHSEED`, `RANDOM_MODULE`, `--out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
