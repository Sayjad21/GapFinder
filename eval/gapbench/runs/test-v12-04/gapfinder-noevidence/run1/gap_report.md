# Gap Report: test-v12-04

Artifact `mlbench` · generated 2026-10-15 07:22 · 70 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -41.2% | +0.0% | ±3.0% | `normalize=zscore` |

## C1: test_accuracy (paper 0.8292)
**Fits but unsupported** · gap -41.2% → +0.0% · 13 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0006`, `B0011`, `B0012`, `B0013`, `B0014`, `B0015` (6 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Command:

  Replay: fork checkpoint `59cd5b73-a19e-4bc4-bc4c-2730f1a35fe6` and run
  ```
  RUN_TAG=b22df07fd2c8 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.8292, 0.825, 0.8292, 0.8292, 0.8292, 0.8292; gap after +0.0%; result checkpoint `48c041ca-7ec3-4a38-a847-1420bea1b851`
- Effect: candidate 0.8292 minus naive 0.4875 = +0.3417, 95% bootstrap interval [+0.3042, +0.3583] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.829 test accuracy and 0.810 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.8292 (headline claim)

### What did we measure?
- Naive median 0.4875 over 5 runs; repeats: 0.475, 0.4917, 0.4875, 0.5375, 0.4667
- Spread: range 0.4667 to 0.5375, noise band ±0.025 (2 x MAD), CV 5.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -41.2% (noise band ±3.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -41.2% (it comes back)
- PASS · Held-out claim: C2: -40.3% to +0.0% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: evidence gate off: no evidence was looked for
- PASS · Effect vs noise: candidate minus naive is +0.3417 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `NUM_RUNS`, `DATA_RNG_SOURCE`, `PYTHON_VERSION`, `OS`, `CPU_ARCH`, `MEMORY_GB`, `DISK_TYPE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (5 noise units, gap -26.1%); `normalize=minmax` (4.33 noise units, gap -28.1%); `lr_schedule=step` (2.17 noise units, gap -34.7%)
- Near alternatives (closest across all claims):
  - `lr_schedule=cosine`, `normalize=zscore`: this claim +0.0%, mean |gap| 0.0% (5 runs)
  - `lr_schedule=step`, `normalize=zscore`: this claim +0.0%, mean |gap| 0.0% (5 runs)
  - `class_weight=balanced`, `normalize=zscore`: this claim -5.5%, mean |gap| 4.3% (5 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `normalize=zscore` (reported)
- `lr_schedule=cosine, normalize=zscore`
- `lr_schedule=step, normalize=zscore`

### History matching (every measured configuration, all claims together)
- 5 of 13 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 5 configurations
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 0); lr_schedule=step, normalize=zscore (max I 0)
  - `normalize`: normalize=zscore (max I 0.02)
  - `class_weight, normalize`: class_weight=balanced, normalize=zscore (max I 0.98); class_weight=balanced, normalize=minmax (max I 1.31)

Notes:
- evidence gate off: no evidence was checked, so this cannot be labelled Explained
- configurations the target claim can't tell apart from the answer: normalize=zscore; lr_schedule=cosine, normalize=zscore; lr_schedule=step, normalize=zscore

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore` | 6 | +0.0% | +0.0% | 0.0% |
| `lr_schedule=cosine`, `normalize=zscore` | 5 | +0.0% | +0.0% | 0.0% |
| `lr_schedule=step`, `normalize=zscore` | 5 | +0.0% | +0.0% | 0.0% |
| `class_weight=balanced`, `normalize=zscore` | 5 | -5.5% | -3.1% | 4.3% |
| `normalize=minmax`, `class_weight=balanced` | 5 | -7.0% | -3.4% | 5.2% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `NUM_RUNS`, `DATA_RNG_SOURCE`, `PYTHON_VERSION`, `OS`, `CPU_ARCH`, `MEMORY_GB`, `DISK_TYPE`, `--out`

## Provenance
- GapFinder commit: `f01fe3d9a0095f98d6304ad0543b917ca8e529eb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
