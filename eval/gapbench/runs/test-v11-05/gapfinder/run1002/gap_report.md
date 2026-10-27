# Gap Report: test-v11-05

Artifact `mlbench` · generated 2026-10-15 00:23 · 197 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -26.9% | -1.7% | ±9.2% | `normalize=minmax`, `epochs=75` |

## C1: test_accuracy (paper 0.7292)
**Fits but unsupported** · gap -26.9% → -1.7% · 61 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0054`, `B0134`, `B0135`, `B0136`, `B0137` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `epochs` naive `15`, changed to `75`
- Command:

  Replay: fork checkpoint `b21ddb36-4c1b-4ac7-b4b2-5df1fc4da264` and run
  ```
  RUN_TAG=03f24875aa39 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 75 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7083, 0.7167, 0.7, 0.7208, 0.7167; gap after -1.7%; result checkpoint `fc2add52-5ff1-4991-9216-31f6cd22bb45`
- Effect: candidate 0.7167 minus naive 0.5333 = +0.1834, 95% bootstrap interval [+0.155, +0.23] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.729 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7292 (headline claim)

### What did we measure?
- Naive median 0.5333 over 5 runs; repeats: 0.4708, 0.4917, 0.5375, 0.5667, 0.5333
- Spread: range 0.4708 to 0.5667, noise band ±0.0668 (2 x MAD), CV 7.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -26.9% (noise band ±9.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -25.7% (it comes back)
- PASS · Counterfactual (reversal test): without `epochs` the gap is -18.3% (it comes back)
- PASS · Held-out claim: C2: -20.0% to -2.3% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- FAIL · Evidence: `epochs=75`: no evidence mentions '75'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.1834 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (1.44 noise units, gap +13.7%); `lr_schedule=cosine` (1.06 noise units, gap -17.1%)
- Near alternatives (closest across all claims):
  - `epochs=750`, `lr_schedule=step`: this claim -1.2%, mean |gap| 2.2% (5 runs)
  - `lr_schedule=cosine`, `epochs=150`: this claim -1.7%, mean |gap| 2.4% (5 runs)
  - `lr_schedule=cosine`, `epochs=75`: this claim -8.0%, mean |gap| 4.8% (5 runs)

### Equally good configurations
The target claim can't tell these 4 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `epochs=75, normalize=minmax` (reported)
- `epochs=150, lr_schedule=cosine`
- `epochs=750, lr_schedule=step`
- `class_weight=balanced, normalize=minmax`

### History matching (every measured configuration, all claims together)
- 24 of 61 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `epochs, normalize`: epochs=75, normalize=minmax (max I 0.48); epochs=150, normalize=minmax (max I 1.62)
  - `epochs, lr_schedule`: epochs=150, lr_schedule=cosine (max I 0.5); epochs=750, lr_schedule=step (max I 0.9); epochs=75, lr_schedule=cosine (max I 1.32); epochs=750, lr_schedule=cosine (max I 2.02); +2 more
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 2.28)
  - `lr_schedule`: lr_schedule=cosine (max I 2.53)
- 3 separate islands (no single-knob move joins them): epochs=75, normalize=minmax; epochs=150, lr_schedule=cosine; epochs=750, lr_schedule=step | class_weight=balanced, normalize=minmax; class_weight=balanced, normalize=zscore | epochs=1, normalize=zscore
- Equally good values: `epochs` in {75, 150}

Notes:
- configurations the target claim can't tell apart from the answer: epochs=75, normalize=minmax; epochs=150, lr_schedule=cosine; epochs=750, lr_schedule=step; class_weight=balanced, normalize=minmax
- equally good values within one noise band (measured): epochs in {75, 150}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax`, `epochs=75` | 5 | -1.7% | -2.3% | 2.0% |
| `epochs=750`, `lr_schedule=step` | 5 | -1.2% | +3.1% | 2.2% |
| `lr_schedule=cosine`, `epochs=150` | 5 | -1.7% | +3.1% | 2.4% |
| `lr_schedule=cosine`, `epochs=75` | 5 | -8.0% | -1.6% | 4.8% |
| `normalize=minmax`, `class_weight=balanced` | 5 | +2.3% | +14.2% | 8.2% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
