# Gap Report: test-v11-08

Artifact `mlbench` · generated 2026-10-15 19:23 · 49 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -18.2% | +0.0% | ±4.2% | `normalize=minmax` |

## C1: test_accuracy (paper 0.5958)
**Fits but unsupported** · gap -18.2% → +0.0% · 13 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0007`, `B0011`, `B0012`, `B0013`, `B0014`, `B0015` (6 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Command:

  Replay: fork checkpoint `ac3751eb-0c0e-418f-857f-ae4c9a419cdf` and run
  ```
  RUN_TAG=e09bd6e35ff9 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.5958, 0.5958, 0.5958, 0.5958, 0.5958, 0.5958; gap after +0.0%; result checkpoint `90ad1b41-e8c2-4b2c-99c6-b5a5f551e8c3`
- Effect: candidate 0.5958 minus naive 0.4875 = +0.1083, 95% bootstrap interval [+0.07746, +0.1241] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.596 test accuracy and 0.500 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.5958 (headline claim)

### What did we measure?
- Naive median 0.4875 over 5 runs; repeats: 0.4917, 0.4667, 0.5375, 0.475, 0.4875
- Spread: range 0.4667 to 0.5375, noise band ±0.025 (2 x MAD), CV 5.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -18.2% (noise band ±4.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -18.2% (it comes back)
- PASS · Held-out claim: C2: -3.3% to +0.0% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.1083 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (3.5 noise units, gap +3.5%); `lr_schedule=step` (3.17 noise units, gap -4.9%)
- Near alternatives (closest across all claims):
  - `normalize=minmax`, `lr_schedule=step`: this claim +0.0%, mean |gap| 0.0% (5 runs)
  - `lr_schedule=cosine`, `normalize=minmax`: this claim +0.0%, mean |gap| 0.0% (5 runs)
  - `lr_schedule=step`: this claim -4.2%, mean |gap| 9.0% (6 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `normalize=minmax` (reported)
- `lr_schedule=cosine, normalize=minmax`
- `lr_schedule=step, normalize=minmax`

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 6 configurations
  - `normalize`: normalize=minmax (max I 0)
  - `lr_schedule, normalize`: lr_schedule=step, normalize=minmax (max I 0); lr_schedule=cosine, normalize=minmax (max I 0)
  - `class_weight, lr_schedule`: class_weight=balanced, lr_schedule=step (max I 2.01)
  - `lr_schedule`: lr_schedule=step (max I 2.24)
  - `class_weight`: class_weight=balanced (max I 2.74)

Notes:
- configurations the target claim can't tell apart from the answer: normalize=minmax; lr_schedule=cosine, normalize=minmax; lr_schedule=step, normalize=minmax

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax` | 6 | +0.0% | +0.0% | 0.0% |
| `normalize=minmax`, `lr_schedule=step` | 5 | +0.0% | +0.0% | 0.0% |
| `lr_schedule=cosine`, `normalize=minmax` | 5 | +0.0% | +0.0% | 0.0% |
| `lr_schedule=step` | 6 | -4.2% | +13.9% | 9.0% |
| `lr_schedule=step`, `class_weight=balanced` | 5 | -9.1% | +9.1% | 9.1% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
