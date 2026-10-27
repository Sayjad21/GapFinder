# Gap Report: test-v12-06

Artifact `mlbench` · generated 2026-10-15 19:29 · 199 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -30.8% | +0.0% | ±1.1% | `class_weight=balanced`, `normalize=minmax` |

## C1: test_accuracy (paper 0.7708)
**Fits but unsupported** · gap -30.8% → +0.0% · 64 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0124`, `B0155`, `B0194`, `B0195`, `B0196` (5 run(s) of the same config)
- Config: `class_weight` naive `none`, changed to `balanced`
- Config: `normalize` naive `none`, changed to `minmax`
- Command:

  Replay: fork checkpoint `2b66752d-07ea-4e73-8608-4499de16f316` and run
  ```
  RUN_TAG=ba953d128751 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight balanced --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7667, 0.7417, 0.7708, 0.7708, 0.775; gap after +0.0%; result checkpoint `f34646fd-fb31-489c-a00a-d11e660b3318`
- Effect: candidate 0.7708 minus naive 0.5333 = +0.2375, 95% bootstrap interval [+0.2159, +0.2983] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.771 test accuracy and 0.745 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7708 (headline claim)

### What did we measure?
- Naive median 0.5333 over 5 runs; repeats: 0.5333, 0.4667, 0.4792, 0.5375, 0.5375
- Spread: range 0.4667 to 0.5375, noise band ±0.0084 (2 x MAD), CV 6.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -30.8% (noise band ±1.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `class_weight` the gap is -22.7% (it comes back)
- PASS · Counterfactual (reversal test): without `normalize` the gap is -32.7% (it comes back)
- PASS · Held-out claim: C2: -27.7% to +4.9% (not worse beyond noise)
- FAIL · Evidence: `class_weight=balanced`: no evidence mentions 'balanced'; it fits, but nothing says the authors used it
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2375 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `NUM_RUNS`, `AGGREGATION`, `PYTHON_VERSION`, `OS`, `CPU_ARCH`, `CPU_CORES`, `MEMORY_SIZE`, `DISK_TYPE`, `NETWORK`, `PYTHONHASHSEED`, `OMP_NUM_THREADS`, `MKL_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `NUMEXPR_NUM_THREADS`, `RANDOM_SEED`, `PYTHON_RANDOM_MODULE`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (21.32 noise units, gap +7.6%); `lr_schedule=cosine` (11.42 noise units, gap -18.4%); `lr_schedule=step` (4.46 noise units, gap -25.9%); `positive_rate=0.7` (2.49 noise units, gap -28.1%); `positive_rate=0.15` (1.49 noise units, gap -29.2%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `class_weight=balanced`, `normalize=zscore`: this claim +1.6%, mean |gap| 3.5% (5 runs)
  - `normalize=zscore`, `positive_rate=0.5`: this claim +2.2%, mean |gap| 4.0% (5 runs)
  - `normalize=zscore`, `positive_rate=0.15`: this claim +1.1%, mean |gap| 4.9% (5 runs)

### History matching (every measured configuration, all claims together)
- 17 of 61 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 0.75); class_weight=balanced, normalize=zscore (max I 0.92)
  - `normalize, positive_rate`: normalize=zscore, positive_rate=0.86 (max I 0.86); normalize=zscore, positive_rate=0.5 (max I 0.94); normalize=zscore, positive_rate=0.65 (max I 1.23); normalize=zscore, positive_rate=0.7 (max I 1.39); +1 more
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.3); lr_schedule=step, normalize=zscore (max I 1.3)
  - `normalize`: normalize=zscore (max I 1.41)
- 2 separate islands (no single-knob move joins them): class_weight=balanced, normalize=minmax; normalize=zscore, positive_rate=0.86; class_weight=balanced, normalize=zscore | lr_schedule=cosine, positive_rate=0.7; lr_schedule=cosine, positive_rate=0.65; lr_schedule=cosine, positive_rate=0.15

Notes:
- stopped early: run budget of 200 reached (wanted 3 more run(s) of {'lr_schedule': 'cosine', 'positive_rate': '0.03'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `class_weight=balanced`, `normalize=minmax` | 5 | +0.0% | +4.9% | 2.5% |
| `class_weight=balanced`, `normalize=zscore` | 5 | +1.6% | +5.4% | 3.5% |
| `normalize=zscore`, `positive_rate=0.5` | 5 | +2.2% | +5.8% | 4.0% |
| `normalize=zscore`, `positive_rate=0.15` | 5 | +1.1% | -8.7% | 4.9% |
| `positive_rate=0.86`, `normalize=zscore` | 2 | +5.4% | -4.9% | 5.1% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `NUM_RUNS`, `AGGREGATION`, `PYTHON_VERSION`, `OS`, `CPU_ARCH`, `CPU_CORES`, `MEMORY_SIZE`, `DISK_TYPE`, `NETWORK`, `PYTHONHASHSEED`, `OMP_NUM_THREADS`, `MKL_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `NUMEXPR_NUM_THREADS`, `RANDOM_SEED`, `PYTHON_RANDOM_MODULE`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
