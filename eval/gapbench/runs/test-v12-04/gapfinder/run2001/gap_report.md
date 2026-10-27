# Gap Report: test-v12-04

Artifact `mlbench` · generated 2026-10-15 21:07 · 38 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Paper-artifact inconsistency | -34.7% | -0.3% | ±1.0% | `normalize=zscore` |

## C1: test_accuracy (paper 0.8292)
**Paper-artifact inconsistency** · gap -34.7% → -0.3% · 13 hypotheses tested
> Confirmed cause: reverting it brings the gap back, held-out claims hold, and the value has evidence

### Which experiment changed it?
- Branch: `B0006`, `B0011`, `B0012`, `B0013` (4 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Command:

  Replay: fork checkpoint `53df623f-174a-4137-a61a-bb3452599b7d` and run
  ```
  RUN_TAG=d6ecc05ac0e3 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.8292, 0.825, 0.825, 0.8292; gap after -0.3%; result checkpoint `e81dd0a5-fbb4-4eed-a653-000387ba36d2`
- Effect: candidate 0.8271 minus naive 0.5417 = +0.2854, 95% bootstrap interval [+0.2689, +0.2895] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.829 test accuracy and 0.810 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.8292 (headline claim)

### What did we measure?
- Naive median 0.5417 over 5 runs; repeats: 0.5625, 0.55, 0.5375, 0.5375, 0.5417
- Spread: range 0.5375 to 0.5625, noise band ±0.0084 (2 x MAD), CV 1.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -34.7% (noise band ±1.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -34.7% (it comes back)
- PASS · Held-out claim: C2: -33.1% to -0.2% (not worse beyond noise)
- PASS · Evidence: `normalize=zscore`: paper states 'zscore'
- PASS · Effect vs noise: candidate minus naive is +0.2854 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `NUM_RUNS`, `DATA_RNG_SOURCE`, `PYTHON_VERSION`, `OS`, `CPU_ARCH`, `MEMORY_GB`, `DISK_TYPE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (14.38 noise units, gap -20.1%); `normalize=minmax` (6.44 noise units, gap -28.1%)
- Near alternatives (closest across all claims):
  - `lr_schedule=cosine`, `normalize=zscore`: this claim +0.0%, mean |gap| 0.0% (3 runs)
  - `normalize=zscore`, `lr_schedule=step`: this claim +0.0%, mean |gap| 0.0% (3 runs)
  - `normalize=minmax`, `class_weight=balanced`: this claim -4.5%, mean |gap| 3.7% (3 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `normalize=zscore` (reported)
- `lr_schedule=cosine, normalize=zscore`
- `lr_schedule=step, normalize=zscore`

### History matching (every measured configuration, all claims together)
- 5 of 13 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 5 configurations
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 0); lr_schedule=step, normalize=zscore (max I 0)
  - `normalize`: normalize=zscore (max I 0.05)
  - `class_weight, normalize`: class_weight=balanced, normalize=zscore (max I 1.05); class_weight=balanced, normalize=minmax (max I 1.22)

Notes:
- configurations the target claim can't tell apart from the answer: normalize=zscore; lr_schedule=cosine, normalize=zscore; lr_schedule=step, normalize=zscore

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=cosine`, `normalize=zscore` | 3 | +0.0% | +0.0% | 0.0% |
| `normalize=zscore`, `lr_schedule=step` | 3 | +0.0% | +0.0% | 0.0% |
| `normalize=zscore` | 4 | -0.3% | -0.2% | 0.2% |
| `normalize=minmax`, `class_weight=balanced` | 3 | -4.5% | -2.9% | 3.7% |
| `normalize=zscore`, `class_weight=balanced` | 3 | -5.5% | -3.1% | 4.3% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `NUM_RUNS`, `DATA_RNG_SOURCE`, `PYTHON_VERSION`, `OS`, `CPU_ARCH`, `MEMORY_GB`, `DISK_TYPE`, `--out`

## Provenance
- GapFinder commit: `cd8c8af2b9d079dd9a57443ed501c0dd8a467d34` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
