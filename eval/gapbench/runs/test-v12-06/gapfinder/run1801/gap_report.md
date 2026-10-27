# Gap Report: test-v12-06

Artifact `mlbench` · generated 2026-10-15 19:51 · 198 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -36.8% | +7.6% | ±5.4% | `normalize=zscore` |

## C1: test_accuracy (paper 0.7708)
**Fits but unsupported** · gap -36.8% → +7.6% · 70 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0016`, `B0042`, `B0043`, `B0058`, `B0059`, `B0060` (6 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Command:

  Replay: fork checkpoint `aeccafd7-b4bb-44a2-a613-af77d3b8eaf3` and run
  ```
  RUN_TAG=c2387736ec48 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.825, 0.8292, 0.8292, 0.8292, 0.8292, 0.825; gap after +7.6%; result checkpoint `db65b16d-e612-40f1-bbe2-008f53cf64ae`
- Effect: candidate 0.8292 minus naive 0.4875 = +0.3417, 95% bootstrap interval [+0.2834, +0.3575] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.771 test accuracy and 0.745 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7708 (headline claim)

### What did we measure?
- Naive median 0.4875 over 5 runs; repeats: 0.5458, 0.4667, 0.4875, 0.4875, 0.5417
- Spread: range 0.4667 to 0.5458, noise band ±0.0416 (2 x MAD), CV 7.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -36.8% (noise band ±5.4% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -36.8% (it comes back)
- PASS · Held-out claim: C2: -35.0% to +8.8% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.3417 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `NUM_RUNS`, `AGGREGATION`, `PYTHON_VERSION`, `OS`, `CPU_ARCH`, `CPU_CORES`, `MEMORY_SIZE`, `DISK_TYPE`, `NETWORK`, `PYTHONHASHSEED`, `OMP_NUM_THREADS`, `MKL_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `NUMEXPR_NUM_THREADS`, `RANDOM_SEED`, `PYTHON_RANDOM_MODULE`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (3.61 noise units, gap -17.3%); `normalize=minmax` (2.6 noise units, gap -22.7%); `positive_rate=0.7` (1.6 noise units, gap -28.1%); `lr_schedule=step` (1.3 noise units, gap -29.7%); `positive_rate=0.86` (1.2 noise units, gap -30.3%) (and 2 more in the JSON)
- Near alternatives (closest across all claims):
  - `positive_rate=0.5`, `normalize=zscore`: this claim +1.6%, mean |gap| 3.4% (2 runs)
  - `class_weight=balanced`, `weight_decay=1e-3`, `lr_schedule=cosine`, `normalize=zscore`: this claim +2.2%, mean |gap| 4.2% (2 runs)
  - `normalize=zscore`, `positive_rate=0.15`: this claim +0.5%, mean |gap| 5.1% (2 runs)

### History matching (every measured configuration, all claims together)
- 17 of 67 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `normalize, positive_rate`: normalize=zscore, positive_rate=0.5 (max I 0.78); normalize=zscore, positive_rate=0.86 (max I 0.9); normalize=zscore, positive_rate=0.65 (max I 1.28); normalize=zscore, positive_rate=0.7 (max I 1.41)
  - `class_weight, lr_schedule, normalize, weight_decay`: class_weight=balanced, lr_schedule=cosine, normalize=zscore, weight_decay=1e-3 (max I 0.94)
  - `normalize, weight_decay`: normalize=zscore, weight_decay=1e-4 (max I 1.28); normalize=zscore, weight_decay=1e-3 (max I 1.31); normalize=zscore, weight_decay=0.01 (max I 1.32)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.31); lr_schedule=step, normalize=zscore (max I 1.31)
- 4 separate islands (no single-knob move joins them): normalize=zscore, positive_rate=0.5; normalize=zscore, positive_rate=0.86; normalize=zscore, weight_decay=1e-4 | lr_schedule=cosine, positive_rate=0.7; lr_schedule=cosine, positive_rate=0.86; lr_schedule=cosine, positive_rate=0.93 | class_weight=balanced, lr_schedule=cosine, normalize=zscore, weight_decay=1e-3 | lr_schedule=cosine, weight_decay=1e-3

Notes:
- stopped early: run budget of 200 reached (wanted 3 more run(s) of {'normalize': 'zscore', 'positive_rate': '0.15'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `positive_rate=0.5`, `normalize=zscore` | 2 | +1.6% | +5.2% | 3.4% |
| `class_weight=balanced`, `weight_decay=1e-3`, `lr_schedule=cosine`, `normalize=zscore` | 2 | +2.2% | +6.3% | 4.2% |
| `normalize=zscore`, `positive_rate=0.15` | 2 | +0.5% | -9.7% | 5.1% |
| `positive_rate=0.86`, `normalize=zscore` | 2 | +4.9% | -6.0% | 5.4% |
| `normalize=zscore`, `positive_rate=0.65` | 2 | +6.8% | +8.6% | 7.7% |

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
