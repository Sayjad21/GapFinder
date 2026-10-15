# Gap Report: test-v12-04

Artifact `mlbench` · generated 2026-10-15 07:22 · 48 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Paper-artifact inconsistency | -35.7% | -0.3% | ±9.0% | `normalize=zscore` |

## C1: test_accuracy (paper 0.8292)
**Paper-artifact inconsistency** · gap -35.7% → -0.3% · 13 hypotheses tested
> Confirmed cause: reverting it brings the gap back, held-out claims hold, and the value has evidence

### Which experiment changed it?
- Branch: `B0006`, `B0011`, `B0012`, `B0013`, `B0014`, `B0015` (6 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Command:

  Replay: fork checkpoint `6ff55184-43a2-4f32-bdf8-a338beb9c04a` and run
  ```
  RUN_TAG=9f5111b2dc49 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.825, 0.8292, 0.8292, 0.825, 0.8292, 0.825; gap after -0.3%; result checkpoint `1b0265c4-fe9a-44ff-bc12-1ba3f2952372`
- Effect: candidate 0.8271 minus naive 0.5333 = +0.2938, 95% bootstrap interval [+0.275, +0.3483] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.829 test accuracy and 0.810 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.8292 (headline claim)

### What did we measure?
- Naive median 0.5333 over 5 runs; repeats: 0.5333, 0.4917, 0.5708, 0.5375, 0.4625
- Spread: range 0.4625 to 0.5708, noise band ±0.075 (2 x MAD), CV 8.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -35.7% (noise band ±9.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -35.7% (it comes back)
- PASS · Held-out claim: C2: -33.5% to -0.3% (not worse beyond noise)
- PASS · Evidence: `normalize=zscore`: paper states 'zscore'
- PASS · Effect vs noise: candidate minus naive is +0.2938 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `NUM_RUNS`, `DATA_RNG_SOURCE`, `PYTHON_VERSION`, `OS`, `CPU_ARCH`, `MEMORY_GB`, `DISK_TYPE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (1.06 noise units, gap -26.1%)
- Near alternatives (closest across all claims):
  - `normalize=zscore`, `lr_schedule=cosine`: this claim +0.0%, mean |gap| 0.0% (5 runs)
  - `normalize=zscore`, `lr_schedule=step`: this claim +0.0%, mean |gap| 0.0% (5 runs)
  - `normalize=zscore`, `class_weight=balanced`: this claim -5.5%, mean |gap| 4.3% (5 runs)

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
  - `class_weight, normalize`: class_weight=balanced, normalize=zscore (max I 0.89); class_weight=balanced, normalize=minmax (max I 1.19)

Notes:
- configurations the target claim can't tell apart from the answer: normalize=zscore; lr_schedule=cosine, normalize=zscore; lr_schedule=step, normalize=zscore

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore`, `lr_schedule=cosine` | 5 | +0.0% | +0.0% | 0.0% |
| `normalize=zscore`, `lr_schedule=step` | 5 | +0.0% | +0.0% | 0.0% |
| `normalize=zscore` | 6 | -0.3% | -0.3% | 0.3% |
| `normalize=zscore`, `class_weight=balanced` | 5 | -5.5% | -3.1% | 4.3% |
| `normalize=minmax`, `class_weight=balanced` | 5 | -7.5% | -4.0% | 5.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `NUM_RUNS`, `DATA_RNG_SOURCE`, `PYTHON_VERSION`, `OS`, `CPU_ARCH`, `MEMORY_GB`, `DISK_TYPE`, `--out`

## Provenance
- GapFinder commit: `f01fe3d9a0095f98d6304ad0543b917ca8e529eb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
