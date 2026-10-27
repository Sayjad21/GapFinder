# Gap Report: test-gen-04

Artifact `mlbench` · generated 2026-10-15 19:37 · 52 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Paper-artifact inconsistency | -34.8% | +0.5% | ±6.1% | `normalize=zscore` |

## C1: test_accuracy (paper 0.825)
**Paper-artifact inconsistency** · gap -34.8% → +0.5% · 13 hypotheses tested
> Confirmed cause: reverting it brings the gap back, held-out claims hold, and the value has evidence

### Which experiment changed it?
- Branch: `B0006`, `B0011`, `B0012`, `B0013`, `B0014`, `B0015` (6 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Command:

  Replay: fork checkpoint `a8af48e5-23aa-4b15-bbea-74420bd10dc3` and run
  ```
  RUN_TAG=3f660670acf8 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.8292, 0.8292, 0.825, 0.8292, 0.8292, 0.8292; gap after +0.5%; result checkpoint `26ffdd39-26f6-47b7-ac97-52938ce41893`
- Effect: candidate 0.8292 minus naive 0.5375 = +0.2917, 95% bootstrap interval [+0.2759, +0.34] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.825 test accuracy and 0.807 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.825 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5375, 0.5375, 0.4875, 0.5625, 0.4875
- Spread: range 0.4875 to 0.5625, noise band ±0.05 (2 x MAD), CV 6.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -34.8% (noise band ±6.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -34.8% (it comes back)
- PASS · Held-out claim: C2: -32.8% to +0.4% (not worse beyond noise)
- PASS · Evidence: `normalize=zscore`: paper states 'zscore'
- PASS · Effect vs noise: candidate minus naive is +0.2917 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (1.42 noise units, gap -26.3%); `normalize=minmax` (1.17 noise units, gap -27.8%)
- Near alternatives (closest across all claims):
  - `lr_schedule=cosine`, `normalize=zscore`: this claim +0.5%, mean |gap| 0.5% (5 runs)
  - `lr_schedule=step`, `normalize=zscore`: this claim +0.5%, mean |gap| 0.5% (5 runs)
  - `class_weight=balanced`, `normalize=zscore`: this claim -5.1%, mean |gap| 3.9% (5 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `normalize=zscore` (reported)
- `lr_schedule=cosine, normalize=zscore`
- `lr_schedule=step, normalize=zscore`

### History matching (every measured configuration, all claims together)
- 5 of 13 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 5 configurations
  - `normalize`: normalize=zscore (max I 0.08)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 0.09); lr_schedule=step, normalize=zscore (max I 0.09)
  - `class_weight, normalize`: class_weight=balanced, normalize=zscore (max I 0.88); class_weight=balanced, normalize=minmax (max I 1.18)

Notes:
- configurations the target claim can't tell apart from the answer: normalize=zscore; lr_schedule=cosine, normalize=zscore; lr_schedule=step, normalize=zscore

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore` | 6 | +0.5% | +0.4% | 0.5% |
| `lr_schedule=cosine`, `normalize=zscore` | 5 | +0.5% | +0.4% | 0.5% |
| `lr_schedule=step`, `normalize=zscore` | 5 | +0.5% | +0.4% | 0.5% |
| `class_weight=balanced`, `normalize=zscore` | 5 | -5.1% | -2.7% | 3.9% |
| `normalize=minmax`, `class_weight=balanced` | 5 | -6.6% | -3.2% | 4.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
