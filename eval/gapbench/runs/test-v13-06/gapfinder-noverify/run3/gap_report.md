# Gap Report: test-v13-06

Artifact `mlbench` · generated 2026-10-16 00:51 · 182 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Explained | -36.1% | -0.1% | ±4.4% | `normalize=zscore`, `n=5000` |

## C1: test_accuracy (paper 0.7558)
**Explained** · gap -36.1% → -0.1% · 57 hypotheses tested
> Interacting factors: these changes close the gap only together, and every check passes

### Which experiment changed it?
- Branch: `B0056`, `B0096`, `B0130`, `B0131`, `B0132` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Config: `n` naive `1200`, changed to `5000`
- Command:

  Replay: fork checkpoint `e9e230de-662b-4542-af45-0a2d3034c3ac` and run
  ```
  RUN_TAG=df4019f79b15 "${PYTHON:-python3}" train.py --n 5000 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.755, 0.755, 0.753, 0.755, 0.751; gap after -0.1%; result checkpoint `0d138b71-b492-446d-9562-abf85539a85b`
- Effect: candidate 0.755 minus naive 0.4833 = +0.2717, 95% bootstrap interval [+0.2117, +0.2875] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.756 test accuracy and 0.728 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7558 (headline claim)

### What did we measure?
- Naive median 0.4833 over 5 runs; repeats: 0.4667, 0.5417, 0.5417, 0.4667, 0.4833
- Spread: range 0.4667 to 0.5417, noise band ±0.0332 (2 x MAD), CV 7.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -36.1% (noise band ±4.4% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is +0.2717 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `PYTHON_VERSION`, `OS`, `CPU_ARCH`, `MATH_LIBRARY`, `FLOATING_POINT_ROUNDING`, `RANDOM_MODULE_IMPLEMENTATION`, `MEMORY_SIZE`, `STORAGE_TYPE`, `PYTHONHASHSEED`, `PYTHONOPTIMIZE`, `OPENBLAS_THREADS`, `MKL_NUM_THREADS`, `NUMEXPR_MAX_THREADS`, `PYTHONMALLOC`, `PYTHONFAULTHANDLER`, `out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `n=120` (4.27 noise units, gap -17.3%); `lr_schedule=cosine` (3.64 noise units, gap -20.1%); `normalize=minmax` (3.39 noise units, gap -21.2%); `n=6000` (2.48 noise units, gap -25.1%); `n=2400` (2.39 noise units, gap -25.6%) (and 2 more in the JSON)
- Near alternatives (closest across all claims):
  - `n=12000`, `normalize=zscore`: this claim +0.3%, mean |gap| 0.3% (5 runs)
  - `n=6000`, `normalize=zscore`: this claim -0.7%, mean |gap| 0.9% (5 runs)
  - `n=2000`, `normalize=zscore`: this claim +1.2%, mean |gap| 1.8% (5 runs)

### Equally good configurations
The target claim can't tell these 6 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `n=5000, normalize=zscore` (reported)
- `n=12000, normalize=zscore`
- `n=6000, normalize=zscore`
- `n=2000, normalize=zscore`
- `class_weight=balanced, normalize=minmax`
- `n=600, normalize=zscore`

### History matching (every measured configuration, all claims together)
- 19 of 55 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `n, normalize`: n=12000, normalize=zscore (max I 0.03); n=5000, normalize=zscore (max I 0.11); n=6000, normalize=zscore (max I 0.19); n=2000, normalize=zscore (max I 0.37); +4 more
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 1.06); class_weight=balanced, normalize=zscore (max I 1.29)
- 2 separate islands (no single-knob move joins them): n=12000, normalize=zscore; n=5000, normalize=zscore; n=6000, normalize=zscore | lr_schedule=cosine, n=120; lr_schedule=cosine, n=6000; lr_schedule=cosine, n=5000
- Equally good values: `n` in {600, 2000, 5000, 6000, 12000}

Notes:
- configurations the target claim can't tell apart from the answer: n=5000, normalize=zscore; n=12000, normalize=zscore; n=6000, normalize=zscore; n=2000, normalize=zscore; class_weight=balanced, normalize=minmax; n=600, normalize=zscore
- equally good values within one noise band (measured): n in {600, 2000, 5000, 6000, 12000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `n=12000`, `normalize=zscore` | 5 | +0.3% | +0.4% | 0.3% |
| `n=5000`, `normalize=zscore` | 5 | -0.1% | +0.8% | 0.4% |
| `n=6000`, `normalize=zscore` | 5 | -0.7% | -1.2% | 0.9% |
| `n=2000`, `normalize=zscore` | 5 | +1.2% | +2.3% | 1.8% |
| `n=600`, `normalize=zscore` | 5 | -1.9% | -3.8% | 2.8% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `n=1`: crash, Setting n=1 resulted in an insufficient number of samples, causing the training data array Xtr to be empty after the train/test split, which triggered an IndexError when trying to access Xtr[0]

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `PYTHON_VERSION`, `OS`, `CPU_ARCH`, `MATH_LIBRARY`, `FLOATING_POINT_ROUNDING`, `RANDOM_MODULE_IMPLEMENTATION`, `MEMORY_SIZE`, `STORAGE_TYPE`, `PYTHONHASHSEED`, `PYTHONOPTIMIZE`, `OPENBLAS_THREADS`, `MKL_NUM_THREADS`, `NUMEXPR_MAX_THREADS`, `PYTHONMALLOC`, `PYTHONFAULTHANDLER`, `out`

## Provenance
- GapFinder commit: `e9c31fd1405f5c8aae4bd880eadcdc8d491fad02` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0006, sandbox reported $0.0000 (total $0.0006; this search; ledger extraction is included only if it shared the search's router)
