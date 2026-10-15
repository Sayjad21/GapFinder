# Gap Report: test-v12-06

Artifact `mlbench` · generated 2026-10-15 07:28 · 197 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Unexplained | -30.3% | -30.3% | ±5.4% | — |

## C1: test_accuracy (paper 0.7708)
**Unexplained** · gap -30.3% → -30.3% · 72 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (72 hypotheses tested).

### What did the paper report?
> A plain logistic-regression baseline reaches 0.771 test accuracy and 0.745 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7708 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5375, 0.4667, 0.5708, 0.5167, 0.5417
- Spread: range 0.4667 to 0.5708, noise band ±0.0416 (2 x MAD), CV 7.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -30.3% (noise band ±5.4% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `NUM_RUNS`, `AGGREGATION`, `PYTHON_VERSION`, `OS`, `CPU_ARCH`, `CPU_CORES`, `MEMORY_SIZE`, `DISK_TYPE`, `NETWORK`, `PYTHONHASHSEED`, `OMP_NUM_THREADS`, `MKL_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `NUMEXPR_NUM_THREADS`, `RANDOM_SEED`, `PYTHON_RANDOM_MODULE`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (4.31 noise units, gap +7.0%); `lr_schedule=cosine` (1.9 noise units, gap -20.0%); `normalize=minmax` (1.4 noise units, gap -22.7%)
- Near alternatives (closest across all claims):
  - `normalize=zscore`, `positive_rate=0.86`: this claim +4.9%, mean |gap| 5.4% (5 runs)
  - `normalize=zscore`, `positive_rate=0.65`: this claim +6.5%, mean |gap| 7.4% (5 runs)
  - `normalize=zscore`, `weight_decay=0.01`: this claim +7.6%, mean |gap| 8.1% (5 runs)

### History matching (every measured configuration, all claims together)
- 22 of 69 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `normalize, positive_rate`: normalize=zscore, positive_rate=0.5 (max I 0.74); normalize=zscore, positive_rate=0.86 (max I 0.94); normalize=zscore, positive_rate=0.15 (max I 1.36); normalize=zscore, positive_rate=0.65 (max I 1.39)
  - `normalize, weight_decay`: normalize=zscore, weight_decay=0.01 (max I 1.4); normalize=zscore, weight_decay=1e-4 (max I 1.41); normalize=zscore, weight_decay=1e-3 (max I 1.41)
  - `normalize`: normalize=zscore (max I 1.43)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.44); lr_schedule=step, normalize=zscore (max I 1.44)
- 3 separate islands (no single-knob move joins them): normalize=zscore, positive_rate=0.5; normalize=zscore, positive_rate=0.86; normalize=zscore, positive_rate=0.15 | lr_schedule=cosine, positive_rate=0.7; lr_schedule=cosine, positive_rate=0.1; lr_schedule=cosine, positive_rate=0.65 | lr_schedule=cosine, weight_decay=1e-4; lr_schedule=cosine, weight_decay=1e-3; lr_schedule=cosine, weight_decay=0.01

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'lr_schedule': 'cosine', 'positive_rate': '0.7'} for 'confirm-combo')
- closest configuration not verified: {'positive_rate': '0.15', 'normalize': 'zscore'} (gap +0.0%, 1 of 5 confirmation runs); the budget ran out first, so no attribution is made
- history matching: 22 of 69 tested configurations fit every claim within 3 sigma

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore`, `positive_rate=0.86` | 5 | +4.9% | -6.0% | 5.4% |
| `normalize=zscore`, `positive_rate=0.65` | 5 | +6.5% | +8.4% | 7.4% |
| `normalize=zscore`, `weight_decay=0.01` | 5 | +7.6% | +8.6% | 8.1% |
| `normalize=zscore` | 6 | +7.6% | +8.8% | 8.2% |
| `lr_schedule=cosine`, `normalize=zscore` | 5 | +7.6% | +8.8% | 8.2% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: invalid_value, The value 0.0 causes a math domain error in log(p/(1-p)) because log(0) is undefined. A small positive value like 0.001 preserves the intent of a near‑zero positive rate while keeping the argument of the log positive; retried as `positive_rate=0.001`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `NUM_RUNS`, `AGGREGATION`, `PYTHON_VERSION`, `OS`, `CPU_ARCH`, `CPU_CORES`, `MEMORY_SIZE`, `DISK_TYPE`, `NETWORK`, `PYTHONHASHSEED`, `OMP_NUM_THREADS`, `MKL_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `NUMEXPR_NUM_THREADS`, `RANDOM_SEED`, `PYTHON_RANDOM_MODULE`

## Provenance
- GapFinder commit: `f01fe3d9a0095f98d6304ad0543b917ca8e529eb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0006, sandbox reported $0.0000 (total $0.0006; this search; ledger extraction is included only if it shared the search's router)
