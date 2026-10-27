# Gap Report: test-v12-06

Artifact `mlbench` · generated 2026-10-16 01:29 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -36.8% | +0.5% | ±1.1% | `normalize=minmax`, `positive_rate=0.5` |

## C1: test_accuracy (paper 0.7708)
**Fits but unsupported** · gap -36.8% → +0.5% · 68 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0123`, `B0153`, `B0195`, `B0196`, `B0197` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `positive_rate` naive `0.3`, changed to `0.5`
- Command:

  Replay: fork checkpoint `2707297a-bd8e-4bbd-89c1-b63c13f236bf` and run
  ```
  RUN_TAG=dbcd25939b30 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.5 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7875, 0.775, 0.775, 0.7875, 0.775; gap after +0.5%; result checkpoint `ab267156-7797-4907-b8df-4c344221df02`
- Effect: candidate 0.775 minus naive 0.4875 = +0.2875, 95% bootstrap interval [+0.2425, +0.2992] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.771 test accuracy and 0.745 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7708 (headline claim)

### What did we measure?
- Naive median 0.4875 over 5 runs; repeats: 0.5375, 0.4875, 0.4875, 0.5333, 0.4833
- Spread: range 0.4833 to 0.5375, noise band ±0.0084 (2 x MAD), CV 5.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -36.8% (noise band ±1.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -31.9% (it comes back)
- PASS · Counterfactual (reversal test): without `positive_rate` the gap is -22.7% (it comes back)
- PASS · Held-out claim: C2: -35.0% to +4.2% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- FAIL · Evidence: `positive_rate=0.5`: no evidence mentions '0.5'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2875 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `NUM_RUNS`, `AGGREGATION`, `PYTHON_VERSION`, `OS`, `CPU_ARCH`, `CPU_CORES`, `MEMORY_SIZE`, `DISK_TYPE`, `NETWORK`, `PYTHONHASHSEED`, `OMP_NUM_THREADS`, `MKL_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `NUMEXPR_NUM_THREADS`, `RANDOM_SEED`, `PYTHON_RANDOM_MODULE`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (27.27 noise units, gap +7.0%); `lr_schedule=cosine` (14.38 noise units, gap -21.1%); `positive_rate=0.65` (6.94 noise units, gap -29.2%); `lr_schedule=step` (6.45 noise units, gap -29.7%); `weight_decay=1e-4` (5.95 noise units, gap -30.3%) (and 6 more in the JSON)
- Near alternatives (closest across all claims):
  - `normalize=zscore`, `positive_rate=0.2`: this claim +3.2%, mean |gap| 1.7% (2 runs)
  - `normalize=zscore`, `positive_rate=0.5`: this claim +2.2%, mean |gap| 4.0% (5 runs)
  - `normalize=zscore`, `positive_rate=0.15`: this claim +1.1%, mean |gap| 4.9% (5 runs)

### History matching (every measured configuration, all claims together)
- 15 of 66 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `normalize, positive_rate`: normalize=zscore, positive_rate=0.2 (max I 0.56); normalize=minmax, positive_rate=0.5 (max I 0.82); normalize=zscore, positive_rate=0.5 (max I 0.98); normalize=zscore, positive_rate=0.4 (max I 1.32); +1 more
  - `normalize, weight_decay`: normalize=zscore, weight_decay=1e-3 (max I 1.31); normalize=zscore, weight_decay=1e-4 (max I 1.36); normalize=zscore, weight_decay=0.01 (max I 1.38)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.42); lr_schedule=step, normalize=zscore (max I 1.42)
- 2 separate islands (no single-knob move joins them): normalize=zscore, positive_rate=0.2; normalize=minmax, positive_rate=0.5; normalize=zscore, positive_rate=0.5 | lr_schedule=cosine, positive_rate=0.2

Notes:
- stopped early: run budget of 200 reached (wanted 3 more run(s) of {'normalize': 'zscore', 'positive_rate': '0.2'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore`, `positive_rate=0.2` | 2 | +3.2% | -0.2% | 1.7% |
| `normalize=minmax`, `positive_rate=0.5` | 5 | +0.5% | +4.2% | 2.4% |
| `normalize=zscore`, `positive_rate=0.5` | 5 | +2.2% | +5.7% | 4.0% |
| `normalize=zscore`, `positive_rate=0.15` | 5 | +1.1% | -8.7% | 4.9% |
| `normalize=zscore`, `positive_rate=0.4` | 2 | +5.1% | +8.2% | 6.7% |

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
