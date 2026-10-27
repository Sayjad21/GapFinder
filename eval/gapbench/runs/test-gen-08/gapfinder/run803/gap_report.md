# Gap Report: test-gen-08

Artifact `mlbench` · generated 2026-10-14 23:29 · 119 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -8.4% | +0.0% | ±2.8% | `normalize=minmax` |

## C1: test_accuracy (paper 0.5958)
**Fits but unsupported** · gap -8.4% → +0.0% · 53 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0017`, `B0043`, `B0044`, `B0047` (4 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Command:

  Replay: fork checkpoint `33f6a5a0-80e4-40f8-a69a-59f856926126` and run
  ```
  RUN_TAG=63f5e44f049d "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.5958, 0.5958, 0.5958, 0.5958; gap after +0.0%; result checkpoint `f3b75dba-de72-449b-8340-fda2a96f56f6`
- Effect: candidate 0.5958 minus naive 0.5458 = +0.05, 95% bootstrap interval [+0.03414, +0.05662] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.596 test accuracy.

- p. 1; value used: `test_accuracy` = 0.5958 (headline claim)

### What did we measure?
- Naive median 0.5458 over 5 runs; repeats: 0.5417, 0.5583, 0.5375, 0.5458, 0.5625
- Spread: range 0.5375 to 0.5625, noise band ±0.0166 (2 x MAD), CV 2.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -8.4% (noise band ±2.8% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -8.4% (it comes back)
- PASS · Held-out claim: C2: +9.2% to +0.0% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.05 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `runs`, `aggregation`, `SCALES`, `WEIGHTS`, `python_version`, `os`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (1.75 noise units, gap +3.5%); `epochs=750` (1.51 noise units, gap -4.2%)
- Near alternatives (closest across all claims):
  - `normalize=minmax`, `lr_schedule=cosine`: this claim +0.0%, mean |gap| 0.0% (3 runs)
  - `lr_schedule=step`, `normalize=minmax`: this claim +0.0%, mean |gap| 0.0% (3 runs)
  - `epochs=10`, `normalize=minmax`: this claim +0.0%, mean |gap| 0.0% (3 runs)

### Equally good configurations
The target claim can't tell these 6 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `normalize=minmax` (reported)
- `epochs=10, normalize=minmax`
- `epochs=3, normalize=minmax`
- `epochs=2, normalize=minmax`
- `lr_schedule=cosine, normalize=minmax`
- `lr_schedule=step, normalize=minmax`

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `normalize`: normalize=minmax (max I 0)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=minmax (max I 0); lr_schedule=step, normalize=minmax (max I 0)
  - `epochs, normalize`: epochs=10, normalize=minmax (max I 0); epochs=3, normalize=minmax (max I 0); epochs=2, normalize=minmax (max I 0); epochs=30, normalize=minmax (max I 1.13)
  - `lr_schedule`: lr_schedule=step (max I 1.72)
  - `class_weight, epochs`: class_weight=balanced, epochs=750 (max I 1.78)
  - `epochs, lr_schedule`: epochs=10, lr_schedule=step (max I 1.82)

Notes:
- configurations the target claim can't tell apart from the answer: normalize=minmax; epochs=10, normalize=minmax; epochs=3, normalize=minmax; epochs=2, normalize=minmax; lr_schedule=cosine, normalize=minmax; lr_schedule=step, normalize=minmax

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax` | 4 | +0.0% | +0.0% | 0.0% |
| `normalize=minmax`, `lr_schedule=cosine` | 3 | +0.0% | +0.0% | 0.0% |
| `lr_schedule=step`, `normalize=minmax` | 3 | +0.0% | +0.0% | 0.0% |
| `epochs=10`, `normalize=minmax` | 3 | +0.0% | +0.0% | 0.0% |
| `normalize=minmax`, `epochs=3` | 3 | +0.0% | +0.0% | 0.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `runs`, `aggregation`, `SCALES`, `WEIGHTS`, `python_version`, `os`

## Provenance
- GapFinder commit: `efb2f63a257a40b9982099a274f2e882f272b80c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
