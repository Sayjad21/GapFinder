# Gap Report: test-gen-06

Artifact `mlbench` · generated 2026-10-15 00:18 · 199 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -34.3% | +0.9% | ±3.4% | `n=6000`, `normalize=zscore` |

## C1: test_accuracy (paper 0.7417)
**Fits but unsupported** · gap -34.3% → +0.9% · 61 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0068`, `B0128`, `B0129`, `B0130`, `B0131` (5 run(s) of the same config)
- Config: `n` naive `1200`, changed to `6000`
- Config: `normalize` naive `none`, changed to `zscore`
- Command:

  Replay: fork checkpoint `6d24d251-f574-4a0f-9fc6-436e8532921e` and run
  ```
  RUN_TAG=0ba5bb8a9c18 "${PYTHON:-python3}" train.py --n 6000 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7467, 0.7517, 0.7483, 0.7475, 0.7492; gap after +0.9%; result checkpoint `05650ea0-47c9-48d9-aa43-c23603c72388`
- Effect: candidate 0.7483 minus naive 0.4875 = +0.2608, 95% bootstrap interval [+0.2219, +0.271] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.742 test accuracy and 0.700 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7417 accuracy (headline claim)

### What did we measure?
- Naive median 0.4875 over 5 runs; repeats: 0.5375, 0.5083, 0.475, 0.4875, 0.4833
- Spread: range 0.475 to 0.5375, noise band ±0.025 (2 x MAD), CV 5.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -34.3% (noise band ±3.4% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `n` the gap is +11.2% (it comes back)
- PASS · Counterfactual (reversal test): without `normalize` the gap is -41.0% (it comes back)
- PASS · Held-out claim: C2: -31.2% to +2.4% (not worse beyond noise)
- FAIL · Evidence: `n=6000`: no evidence mentions '6000'; it fits, but nothing says the authors used it
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2608 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `NUM_RUNS`, `CPU_MODEL`, `PYTHON_VERSION`, `LIBM_VERSION`, `OS_VERSION`, `ROUNDING_PRECISION`, `MEMORY_SIZE`, `STORAGE_DEVICE`, `CPU_CORES`, `ULIMIT_SETTINGS`, `FILESYSTEM`, `PYTHONHASHSEED`, `RANDOM_MODULE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (5.83 noise units, gap -14.6%); `n=24` (4.5 noise units, gap -19.1%); `normalize=minmax` (4.33 noise units, gap -19.7%); `n=120` (3.83 noise units, gap -21.4%); `n=12000` (3.47 noise units, gap -22.6%) (and 3 more in the JSON)
- Near alternatives (closest across all claims):
  - `n=12000`, `normalize=minmax`: this claim -0.9%, mean |gap| 2.0% (5 runs)
  - `n=2400`, `normalize=zscore`: this claim -4.2%, mean |gap| 2.5% (5 runs)
  - `n=120`, `normalize=zscore`: this claim -4.5%, mean |gap| 2.9% (5 runs)

### History matching (every measured configuration, all claims together)
- 21 of 58 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `n, normalize`: n=600, normalize=zscore (max I 0); n=6000, normalize=zscore (max I 0.43); n=12000, normalize=minmax (max I 0.52); n=120, normalize=zscore (max I 0.62); +5 more
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 1.46)
- 2 separate islands (no single-knob move joins them): n=600, normalize=zscore; n=6000, normalize=zscore; n=12000, normalize=minmax | lr_schedule=step, n=24; lr_schedule=step, n=2000

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'normalize': 'zscore', 'class_weight': 'balanced'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `n=6000`, `normalize=zscore` | 5 | +0.9% | +2.4% | 1.7% |
| `n=12000`, `normalize=minmax` | 5 | -0.9% | -3.1% | 2.0% |
| `n=2400`, `normalize=zscore` | 5 | -4.2% | -0.7% | 2.5% |
| `n=120`, `normalize=zscore` | 5 | -4.5% | +1.3% | 2.9% |
| `n=12000`, `normalize=zscore` | 5 | +2.1% | +4.1% | 3.1% |

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
