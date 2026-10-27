# Gap Report: test-gen-06

Artifact `mlbench` · generated 2026-10-15 01:09 · 155 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -27.5% | +0.0% | ±0.7% | `normalize=zscore`, `n=600` |

## C1: test_accuracy (paper 0.7417)
**Fits but unsupported** · gap -27.5% → +0.0% · 61 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0047`, `B0100`, `B0101` (3 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Config: `n` naive `1200`, changed to `600`
- Command:

  Replay: fork checkpoint `775d7012-ad8f-487b-aced-63ba5dc820f3` and run
  ```
  RUN_TAG=05d10a9a15d8 "${PYTHON:-python3}" train.py --n 600 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7417, 0.7417, 0.7417; gap after +0.0%; result checkpoint `fdeede97-0bcf-4f76-a30e-e195739cdc0a`
- Effect: candidate 0.7417 minus naive 0.5375 = +0.2042, 95% bootstrap interval [+0.1742, +0.2042] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.742 test accuracy and 0.700 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7417 accuracy (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5375, 0.5375, 0.5375, 0.575, 0.5375
- Spread: range 0.5375 to 0.575, noise band ±0.005375 (2 x MAD), CV 3.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -27.5% (noise band ±0.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -25.3% (it comes back)
- PASS · Counterfactual (reversal test): without `n` the gap is +11.8% (it comes back)
- PASS · Held-out claim: C2: -22.6% to +0.0% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- FAIL · Evidence: `n=600`: no evidence mentions '600'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2042 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `NUM_RUNS`, `CPU_MODEL`, `PYTHON_VERSION`, `LIBM_VERSION`, `OS_VERSION`, `ROUNDING_PRECISION`, `MEMORY_SIZE`, `STORAGE_DEVICE`, `CPU_CORES`, `ULIMIT_SETTINGS`, `FILESYSTEM`, `PYTHONHASHSEED`, `RANDOM_MODULE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (16.28 noise units, gap -15.7%); `normalize=minmax` (10.85 noise units, gap -19.7%); `n=120` (8.52 noise units, gap -21.4%); `n=12000` (7.98 noise units, gap -21.7%); `n=6000` (6.51 noise units, gap -22.8%)
- Near alternatives (closest across all claims):
  - `n=6000`, `normalize=zscore`: this claim +1.1%, mean |gap| 1.9% (3 runs)
  - `n=2400`, `normalize=zscore`: this claim -4.2%, mean |gap| 2.5% (3 runs)
  - `n=120`, `normalize=zscore`: this claim -4.5%, mean |gap| 2.9% (3 runs)

### Equally good configurations
The target claim can't tell these 5 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `n=600, normalize=zscore` (reported)
- `n=6000, normalize=zscore`
- `class_weight=balanced, normalize=minmax`
- `n=120, normalize=zscore`
- `n=12000, normalize=zscore`

### History matching (every measured configuration, all claims together)
- 17 of 58 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `n, normalize`: n=600, normalize=zscore (max I 0); n=6000, normalize=zscore (max I 0.51); n=120, normalize=zscore (max I 0.6); n=12000, normalize=zscore (max I 0.8); +5 more
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 1.82)
- 2 separate islands (no single-knob move joins them): n=600, normalize=zscore; n=6000, normalize=zscore; n=120, normalize=zscore | lr_schedule=cosine, n=12000

Notes:
- configurations the target claim can't tell apart from the answer: n=600, normalize=zscore; n=6000, normalize=zscore; class_weight=balanced, normalize=minmax; n=120, normalize=zscore; n=12000, normalize=zscore

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `n=600`, `normalize=zscore` | 3 | +0.0% | +0.0% | 0.0% |
| `n=6000`, `normalize=zscore` | 3 | +1.1% | +2.6% | 1.9% |
| `n=2400`, `normalize=zscore` | 3 | -4.2% | -0.7% | 2.5% |
| `n=120`, `normalize=zscore` | 3 | -4.5% | +1.3% | 2.9% |
| `n=12000`, `normalize=zscore` | 3 | +2.1% | +4.2% | 3.2% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `n=1`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `NUM_RUNS`, `CPU_MODEL`, `PYTHON_VERSION`, `LIBM_VERSION`, `OS_VERSION`, `ROUNDING_PRECISION`, `MEMORY_SIZE`, `STORAGE_DEVICE`, `CPU_CORES`, `ULIMIT_SETTINGS`, `FILESYSTEM`, `PYTHONHASHSEED`, `RANDOM_MODULE`, `--out`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
