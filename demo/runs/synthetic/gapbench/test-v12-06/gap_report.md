# Gap Report: test-v12-06

Artifact `mlbench` · generated 2026-10-23 17:59 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -35.7% | +0.3% | ±3.2% | `class_weight=balanced`, `normalize=minmax` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Held-out claims outside noise:**
  - C2 (`balanced_accuracy`): paper 0.7447, measured 0.4907 (-34.1%, band ±3.2%)
- **The paper states these, and this harness can't vary them** (they are part of what the number means):
  - `NUM_RUNS`: "Numbers are medians over 7 runs with different shuffling seeds." (p.1)
  - `AGGREGATION`: "Numbers are medians over 7 runs with different shuffling seeds." (p.1)

## C1: test_accuracy (paper 0.7708)
**Fits but unsupported** · gap -35.7% → +0.3% · 60 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0135`, `B0138`, `B0139`, `B0140`, `B0141`, `B0142` (6 run(s) of the same config)
- Config: `class_weight` naive `none`, changed to `balanced`
- Config: `normalize` naive `none`, changed to `minmax`
- Command:

  Replay: fork checkpoint `0b0ae032-cf12-4cb6-9dbb-1efd6e9b562a` and run
  ```
  RUN_TAG=95ad4c122928 export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight balanced --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.75, 0.7708, 0.7833, 0.7667, 0.7917, 0.775; gap after +0.3%; result checkpoint `1029baeb-2fd2-4c4e-baaa-33b8ac6cb4f0`
- Effect: candidate 0.7729 minus naive 0.4958 = +0.2771, 95% bootstrap interval [+0.2132, +0.2941] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.771 test accuracy and 0.745 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7708 (headline claim)

### What did we measure?
- Naive median 0.4958 over 5 runs; repeats: 0.5625, 0.5417, 0.4875, 0.4958, 0.4833
- Spread: range 0.4833 to 0.5625, noise band ±0.025 (2 x MAD), CV 6.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -35.7% (noise band ±3.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `class_weight` the gap is -22.7% (it comes back)
- PASS · Counterfactual (reversal test): without `normalize` the gap is -30.3% (it comes back)
- PASS · Held-out claim: C2: -34.1% to +4.6% (not worse beyond noise)
- FAIL · Evidence: `class_weight=balanced`: no evidence mentions 'balanced'; it fits, but nothing says the authors used it
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2771 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `NUM_RUNS`, `AGGREGATION`, `PYTHON_VERSION`, `OS`, `CPU_ARCH`, `CPU_CORES`, `MEMORY_SIZE`, `DISK_TYPE`, `NETWORK`, `PYTHONHASHSEED`, `OMP_NUM_THREADS`, `MKL_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `NUMEXPR_NUM_THREADS`, `RANDOM_SEED`, `PYTHON_RANDOM_MODULE`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (8.66 noise units, gap +7.6%); `lr_schedule=cosine` (5.17 noise units, gap -18.9%); `positive_rate=0.7` (3.5 noise units, gap -24.3%); `positive_rate=0.15` (3.17 noise units, gap -25.4%); `weight_decay=1e-4` (2 noise units, gap -29.2%) (and 4 more in the JSON)
- Near alternatives (closest across all claims):
  - `positive_rate=0.5`, `normalize=minmax`: this claim +1.4%, mean |gap| 3.1% (6 runs)
  - `positive_rate=0.5`, `normalize=zscore`: this claim +1.9%, mean |gap| 3.7% (6 runs)
  - `class_weight=balanced`, `normalize=zscore`: this claim +1.9%, mean |gap| 3.8% (6 runs)

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting class_weight=balanced, normalize=minmax | settings | 43% | 0.8 sigma (fits every claim) | run with class_weight=balanced, normalize=minmax |
| 2 | the setting normalize=minmax, positive_rate=0.5 | settings | 14% | 0.8 sigma (fits every claim) | run with normalize=minmax, positive_rate=0.5 |
| 3 | the setting normalize=zscore, positive_rate=0.5 | settings | 12% | 0.9 sigma (fits every claim) | run with normalize=zscore, positive_rate=0.5 |

### History matching (every measured configuration, all claims together)
- 16 of 58 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 0.8); class_weight=balanced, normalize=zscore (max I 0.95)
  - `normalize, positive_rate`: normalize=minmax, positive_rate=0.5 (max I 0.83); normalize=zscore, positive_rate=0.86 (max I 0.85); normalize=zscore, positive_rate=0.5 (max I 0.92); normalize=zscore, positive_rate=0.65 (max I 1.33); +1 more
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.33); lr_schedule=step, normalize=zscore (max I 1.33)
  - `normalize`: normalize=zscore (max I 1.45)
- 2 separate islands (no single-knob move joins them): class_weight=balanced, normalize=minmax; normalize=minmax, positive_rate=0.5; normalize=zscore, positive_rate=0.86 | lr_schedule=cosine, positive_rate=0.7; lr_schedule=cosine, positive_rate=0.93; lr_schedule=cosine, positive_rate=0.15

Notes:
- stopped early: run budget of 200 reached (wanted 3 more run(s) of {'normalize': 'zscore', 'positive_rate': '0.86'} for 'confirm-combo')
- verified from runs already made, after the budget ran out
- spec knobs no ledger assumption names (batch_size, data_seed, epochs, label_noise, lr, n, split, threshold) were screened too; no better answer
- value interval stopped early: run budget of 200 reached (wanted 1 more run(s) of {'class_weight': 'none', 'normalize': 'minmax'} for 'interval class_weight=none')
- the paper states class_weight = none ("no class weighting"), but none leaves the gap at -35.7% (beyond noise); balanced closes it: the stated value is likely not the one behind the paper's numbers

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `class_weight=balanced`, `normalize=minmax` | 6 | +0.3% | +4.6% | 2.4% |
| `positive_rate=0.5`, `normalize=minmax` | 6 | +1.4% | +4.9% | 3.1% |
| `positive_rate=0.5`, `normalize=zscore` | 6 | +1.9% | +5.5% | 3.7% |
| `class_weight=balanced`, `normalize=zscore` | 6 | +1.9% | +5.6% | 3.8% |
| `normalize=zscore`, `positive_rate=0.15` | 6 | +1.1% | -8.7% | 4.9% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Runtime trace (one dry run)
1 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `NUM_RUNS`, `AGGREGATION`, `PYTHON_VERSION`, `OS`, `CPU_ARCH`, `CPU_CORES`, `MEMORY_SIZE`, `DISK_TYPE`, `NETWORK`, `PYTHONHASHSEED`, `OMP_NUM_THREADS`, `MKL_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `NUMEXPR_NUM_THREADS`, `RANDOM_SEED`, `PYTHON_RANDOM_MODULE`

## Provenance
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `a5ee8e94932cc1397dd02c920427dbe9702911f36a6fbfee753b818e8d60994f`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
