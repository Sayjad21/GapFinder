# Gap Report: test-v11-05

Artifact `mlbench` · generated 2026-10-14 23:33 · 141 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -26.3% | +5.7% | ±10.3% | `normalize=minmax`, `class_weight=balanced` |

## C1: test_accuracy (paper 0.7292)
**Fits but unsupported** · gap -26.3% → +5.7% · 53 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0059`, `B0134`, `B0135`, `B0136`, `B0137` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `class_weight` naive `none`, changed to `balanced`
- Command:

  Replay: fork checkpoint `d02b077e-e24d-47f6-9afd-a9b64478f60a` and run
  ```
  RUN_TAG=0af82e15913b "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight balanced --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7708, 0.7333, 0.7917, 0.775, 0.7458; gap after +5.7%; result checkpoint `4fa504e8-a448-44f7-9141-90a70d6f35d8`
- Effect: candidate 0.7708 minus naive 0.5375 = +0.2333, 95% bootstrap interval [+0.1991, +0.295] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.729 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7292 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.575, 0.5375, 0.5375, 0.4667, 0.475
- Spread: range 0.4667 to 0.575, noise band ±0.075 (2 x MAD), CV 8.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -26.3% (noise band ±10.3% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -33.1% (it comes back)
- PASS · Counterfactual (reversal test): without `class_weight` the gap is -18.3% (it comes back)
- PASS · Held-out claim: C2: -19.5% to +15.0% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- FAIL · Evidence: `class_weight=balanced`: no evidence mentions 'balanced'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2333 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (1.28 noise units, gap +13.1%); `lr_schedule=cosine` (1.17 noise units, gap -14.3%)
- Near alternatives (closest across all claims):
  - `normalize=minmax`, `epochs=75`: this claim +2.3%, mean |gap| 2.7% (5 runs)
  - `lr_schedule=cosine`, `epochs=75`: this claim -7.4%, mean |gap| 4.5% (5 runs)
  - `epochs=30`, `lr_schedule=cosine`: this claim -13.2%, mean |gap| 9.8% (5 runs)

### Equally good configurations
The target claim can't tell these 2 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `class_weight=balanced, normalize=minmax` (reported)
- `epochs=75, normalize=minmax`

### History matching (every measured configuration, all claims together)
- 35 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `epochs, normalize`: epochs=75, normalize=minmax (max I 0.27)
  - `epochs, lr_schedule`: epochs=75, lr_schedule=cosine (max I 1.24); epochs=30, lr_schedule=cosine (max I 2); epochs=75, lr_schedule=step (max I 2); epochs=20, lr_schedule=cosine (max I 2.17); +2 more
  - `lr_schedule`: lr_schedule=cosine (max I 2.23)
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 2.26)
  - `epochs`: epochs=75 (max I 2.39)
- 2 separate islands (no single-knob move joins them): epochs=75, normalize=minmax; epochs=75, lr_schedule=cosine; epochs=30, lr_schedule=cosine | class_weight=balanced, epochs=30; class_weight=balanced, epochs=20; class_weight=balanced, epochs=1
- Equally good values: `normalize` in {minmax, zscore}

Notes:
- configurations the target claim can't tell apart from the answer: class_weight=balanced, normalize=minmax; epochs=75, normalize=minmax
- equally good values within one noise band (measured): normalize in {minmax, zscore}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax`, `epochs=75` | 5 | +2.3% | +3.1% | 2.7% |
| `lr_schedule=cosine`, `epochs=75` | 5 | -7.4% | -1.6% | 4.5% |
| `epochs=30`, `lr_schedule=cosine` | 5 | -13.2% | -6.5% | 9.8% |
| `normalize=minmax`, `class_weight=balanced` | 5 | +5.7% | +15.0% | 10.4% |
| `epochs=20`, `lr_schedule=cosine` | 5 | -13.7% | -7.3% | 10.5% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `efb2f63a257a40b9982099a274f2e882f272b80c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
