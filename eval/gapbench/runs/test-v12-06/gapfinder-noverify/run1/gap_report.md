# Gap Report: test-v12-06

Artifact `mlbench` · generated 2026-10-15 07:28 · 199 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Unexplained | -37.8% | -37.8% | ±3.2% | — |

## C1: test_accuracy (paper 0.7708)
**Unexplained** · gap -37.8% → -37.8% · 71 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (71 hypotheses tested).

### What did the paper report?
> A plain logistic-regression baseline reaches 0.771 test accuracy and 0.745 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7708 (headline claim)

### What did we measure?
- Naive median 0.4792 over 5 runs; repeats: 0.4667, 0.4792, 0.4667, 0.5625, 0.4875
- Spread: range 0.4667 to 0.5625, noise band ±0.025 (2 x MAD), CV 8.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -37.8% (noise band ±3.2% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `NUM_RUNS`, `AGGREGATION`, `PYTHON_VERSION`, `OS`, `CPU_ARCH`, `CPU_CORES`, `MEMORY_SIZE`, `DISK_TYPE`, `NETWORK`, `PYTHONHASHSEED`, `OMP_NUM_THREADS`, `MKL_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `NUMEXPR_NUM_THREADS`, `RANDOM_SEED`, `PYTHON_RANDOM_MODULE`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (9.33 noise units, gap +7.6%); `lr_schedule=cosine` (5 noise units, gap -21.6%); `normalize=minmax` (4.66 noise units, gap -22.7%); `weight_decay=0.01` (3.83 noise units, gap -25.4%); `class_weight=balanced` (3.33 noise units, gap -27.0%) (and 6 more in the JSON)
- Near alternatives (closest across all claims):
  - `class_weight=balanced`, `normalize=zscore`: this claim +1.6%, mean |gap| 3.5% (5 runs)
  - `positive_rate=0.65`, `normalize=zscore`: this claim +7.0%, mean |gap| 7.9% (5 runs)
  - `weight_decay=0.01`, `normalize=zscore`: this claim +7.6%, mean |gap| 8.1% (5 runs)

### History matching (every measured configuration, all claims together)
- 26 of 68 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `normalize, positive_rate`: normalize=zscore, positive_rate=0.5 (max I 0.65); normalize=zscore, positive_rate=0.86 (max I 0.71); normalize=zscore, positive_rate=0.15 (max I 1.1); normalize=zscore, positive_rate=0.7 (max I 1.18); +1 more
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 0.76); class_weight=balanced, normalize=zscore (max I 0.9)
  - `normalize, weight_decay`: normalize=zscore, weight_decay=1e-4 (max I 1.1); normalize=zscore, weight_decay=1e-3 (max I 1.38)
  - `normalize`: normalize=zscore (max I 1.41)
- 4 separate islands (no single-knob move joins them): normalize=zscore, positive_rate=0.5; normalize=zscore, positive_rate=0.86; class_weight=balanced, normalize=minmax | lr_schedule=cosine, positive_rate=0.1; lr_schedule=cosine, positive_rate=0.7; lr_schedule=cosine, positive_rate=0.86 | lr_schedule=cosine, weight_decay=1e-3; lr_schedule=cosine, weight_decay=1e-4 | class_weight=balanced, lr_schedule=cosine

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'normalize': 'minmax', 'weight_decay': '0.01'} for 'confirm-combo')
- closest configuration not verified: {'class_weight': 'balanced', 'normalize': 'minmax'} (gap +0.5%, 1 of 5 confirmation runs); the budget ran out first, so no attribution is made
- history matching: 26 of 68 tested configurations fit every claim within 3 sigma

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `class_weight=balanced`, `normalize=zscore` | 5 | +1.6% | +5.4% | 3.5% |
| `positive_rate=0.65`, `normalize=zscore` | 5 | +7.0% | +8.8% | 7.9% |
| `weight_decay=0.01`, `normalize=zscore` | 5 | +7.6% | +8.6% | 8.1% |
| `normalize=zscore` | 6 | +7.6% | +8.8% | 8.2% |
| `lr_schedule=cosine`, `normalize=zscore` | 5 | +7.6% | +8.8% | 8.2% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: invalid_value, The code computes math.log(positive_rate / (1 - positive_rate)), which requires positive_rate strictly between 0 and 1. Setting it to 0.0 leads to log(0) and a ValueError. A small positive value like 0.001 preserves the intent of a low positive rate while staying in the valid domain; retried as `positive_rate=0.001`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `NUM_RUNS`, `AGGREGATION`, `PYTHON_VERSION`, `OS`, `CPU_ARCH`, `CPU_CORES`, `MEMORY_SIZE`, `DISK_TYPE`, `NETWORK`, `PYTHONHASHSEED`, `OMP_NUM_THREADS`, `MKL_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `NUMEXPR_NUM_THREADS`, `RANDOM_SEED`, `PYTHON_RANDOM_MODULE`

## Provenance
- GapFinder commit: `f01fe3d9a0095f98d6304ad0543b917ca8e529eb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0006, sandbox reported $0.0000 (total $0.0006; this search; ledger extraction is included only if it shared the search's router)
