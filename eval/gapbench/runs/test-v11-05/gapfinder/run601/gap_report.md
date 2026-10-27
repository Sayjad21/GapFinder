# Gap Report: test-v11-05

Artifact `mlbench` · generated 2026-10-14 22:35 · 158 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -25.2% | -12.3% | ±2.3% | `epochs=750` |

## C1: test_accuracy (paper 0.7292)
**Fits but unsupported** · gap -25.2% → -12.3% · 54 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0015`, `B0048`, `B0049`, `B0050` (4 run(s) of the same config)
- Config: `epochs` naive `15`, changed to `750`
- Command:

  Replay: fork checkpoint `f55a2453-8672-4ab2-8155-578e57def1ad` and run
  ```
  RUN_TAG=3216810c909e "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize none --epochs 750 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.55, 0.7458, 0.6167, 0.6625; gap after -12.3%; result checkpoint `30c5cc20-7d3f-442a-973c-e922256062a2`
- Effect: candidate 0.6396 minus naive 0.5458 = +0.0938, 95% bootstrap interval [+0.0659, +0.2067] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.729 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7292 (headline claim)

### What did we measure?
- Naive median 0.5458 over 5 runs; repeats: 0.5458, 0.5333, 0.5583, 0.5458, 0.5375
- Spread: range 0.5333 to 0.5583, noise band ±0.0166 (2 x MAD), CV 1.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -25.2% (noise band ±2.3% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `epochs` the gap is -25.2% (it comes back)
- PASS · Held-out claim: C2: -18.7% to -8.1% (not worse beyond noise)
- FAIL · Evidence: `epochs=750`: no evidence mentions '750'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.0938 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (5.28 noise units, gap +13.1%); `lr_schedule=cosine` (3.77 noise units, gap -16.6%); `normalize=minmax` (3.01 noise units, gap -18.3%); `epochs=150` (2.26 noise units, gap -20.0%)
- Near alternatives (closest across all claims):
  - `epochs=150`, `lr_schedule=cosine`: this claim -1.7%, mean |gap| 2.4% (3 runs)
  - `epochs=750`, `lr_schedule=step`: this claim -8.6%, mean |gap| 6.7% (3 runs)
  - `epochs=150`, `normalize=minmax`: this claim +6.3%, mean |gap| 8.1% (3 runs)

### Equally good configurations
The target claim can't tell these 4 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `epochs=750` (reported)
- `epochs=150, lr_schedule=cosine`
- `epochs=750, lr_schedule=step`
- `class_weight=balanced, normalize=minmax`

### History matching (every measured configuration, all claims together)
- 7 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 7 configurations
  - `epochs, lr_schedule`: epochs=150, lr_schedule=cosine (max I 0.62); epochs=750, lr_schedule=step (max I 1.23); epochs=750, lr_schedule=cosine (max I 2.61); epochs=30, lr_schedule=cosine (max I 2.62)
  - `epochs, normalize`: epochs=150, normalize=minmax (max I 2.04)
  - `epochs`: epochs=750 (max I 2.31)
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 2.86)
- 3 separate islands (no single-knob move joins them): epochs=150, lr_schedule=cosine; epochs=750, lr_schedule=step; epochs=750 | epochs=150, normalize=minmax | class_weight=balanced, normalize=minmax

Notes:
- configurations the target claim can't tell apart from the answer: epochs=750; epochs=150, lr_schedule=cosine; epochs=750, lr_schedule=step; class_weight=balanced, normalize=minmax

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `epochs=150`, `lr_schedule=cosine` | 3 | -1.7% | +3.1% | 2.4% |
| `epochs=750`, `lr_schedule=step` | 3 | -8.6% | -4.8% | 6.7% |
| `epochs=150`, `normalize=minmax` | 3 | +6.3% | +9.9% | 8.1% |
| `class_weight=balanced`, `normalize=minmax` | 3 | +5.1% | +14.5% | 9.8% |
| `epochs=30`, `lr_schedule=cosine` | 3 | -13.2% | -6.5% | 9.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`

## Provenance
- GapFinder commit: `e0f13d101585ad1609a15fbf67b70128f4cfffc8` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
