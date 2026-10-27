# Gap Report: test-gen-06

Artifact `mlbench` · generated 2026-10-15 00:49 · 165 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -28.1% | +0.0% | ±1.1% | `n=600`, `normalize=zscore` |

## C1: test_accuracy (paper 0.7417)
**Fits but unsupported** · gap -28.1% → +0.0% · 61 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0060`, `B0118`, `B0119` (3 run(s) of the same config)
- Config: `n` naive `1200`, changed to `600`
- Config: `normalize` naive `none`, changed to `zscore`
- Command:

  Replay: fork checkpoint `aa166248-e2bf-404b-801d-b049c54c38ac` and run
  ```
  RUN_TAG=be6a50c194b3 "${PYTHON:-python3}" train.py --n 600 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7417, 0.7417, 0.7417; gap after +0.0%; result checkpoint `46c70762-a76b-4814-a923-348f75ddc799`
- Effect: candidate 0.7417 minus naive 0.5333 = +0.2084, 95% bootstrap interval [+0.185, +0.2217] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.742 test accuracy and 0.700 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7417 accuracy (headline claim)

### What did we measure?
- Naive median 0.5333 over 5 runs; repeats: 0.5333, 0.5625, 0.5333, 0.5375, 0.5167
- Spread: range 0.5167 to 0.5625, noise band ±0.0084 (2 x MAD), CV 3.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -28.1% (noise band ±1.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `n` the gap is +11.8% (it comes back)
- PASS · Counterfactual (reversal test): without `normalize` the gap is -29.2% (it comes back)
- PASS · Held-out claim: C2: -23.1% to +0.0% (not worse beyond noise)
- FAIL · Evidence: `n=600`: no evidence mentions '600'; it fits, but nothing says the authors used it
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2084 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `NUM_RUNS`, `CPU_MODEL`, `PYTHON_VERSION`, `LIBM_VERSION`, `OS_VERSION`, `ROUNDING_PRECISION`, `MEMORY_SIZE`, `STORAGE_DEVICE`, `CPU_CORES`, `ULIMIT_SETTINGS`, `FILESYSTEM`, `PYTHONHASHSEED`, `RANDOM_MODULE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `n=24` (17.87 noise units, gap +7.9%); `n=240` (10.92 noise units, gap -15.7%); `lr_schedule=cosine` (9.43 noise units, gap -17.4%); `normalize=minmax` (7.44 noise units, gap -19.7%); `n=6000` (5.06 noise units, gap -22.4%) (and 3 more in the JSON)
- Near alternatives (closest across all claims):
  - `normalize=minmax`, `n=12000`: this claim -0.2%, mean |gap| 0.8% (3 runs)
  - `n=6000`, `normalize=zscore`: this claim +0.8%, mean |gap| 1.6% (3 runs)
  - `n=2400`, `normalize=zscore`: this claim -3.9%, mean |gap| 2.2% (3 runs)

### Equally good configurations
The target claim can't tell these 5 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `n=600, normalize=zscore` (reported)
- `n=12000, normalize=minmax`
- `n=6000, normalize=zscore`
- `n=120, normalize=zscore`
- `n=12000, normalize=zscore`

### History matching (every measured configuration, all claims together)
- 18 of 58 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `n, normalize`: n=600, normalize=zscore (max I 0); n=12000, normalize=minmax (max I 0.35); n=6000, normalize=zscore (max I 0.46); n=2400, normalize=zscore (max I 0.75); +5 more
  - `lr_schedule, n`: lr_schedule=cosine, n=12000 (max I 1.86)
- 3 separate islands (no single-knob move joins them): n=600, normalize=zscore; n=12000, normalize=minmax; n=6000, normalize=zscore | lr_schedule=cosine, n=12000; lr_schedule=step, n=12000 | n=24
- Equally good values: `n` in {120, 600, 6000}

Notes:
- configurations the target claim can't tell apart from the answer: n=600, normalize=zscore; n=12000, normalize=minmax; n=6000, normalize=zscore; n=120, normalize=zscore; n=12000, normalize=zscore
- equally good values within one noise band (measured): n in {120, 600, 6000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `n=600`, `normalize=zscore` | 3 | +0.0% | +0.0% | 0.0% |
| `normalize=minmax`, `n=12000` | 3 | -0.2% | -1.4% | 0.8% |
| `n=6000`, `normalize=zscore` | 3 | +0.8% | +2.5% | 1.6% |
| `n=2400`, `normalize=zscore` | 3 | -3.9% | -0.4% | 2.2% |
| `normalize=zscore`, `n=12000` | 3 | +2.1% | +4.2% | 3.1% |

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
