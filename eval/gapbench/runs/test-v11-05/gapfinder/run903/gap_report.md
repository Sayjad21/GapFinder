# Gap Report: test-v11-05

Artifact `mlbench` · generated 2026-10-14 23:49 · 196 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -26.3% | +0.6% | ±9.1% | `epochs=75`, `normalize=minmax` |

## C1: test_accuracy (paper 0.7292)
**Fits but unsupported** · gap -26.3% → +0.6% · 53 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0090`, `B0157`, `B0158`, `B0159`, `B0160` (5 run(s) of the same config)
- Config: `epochs` naive `15`, changed to `75`
- Config: `normalize` naive `none`, changed to `minmax`
- Command:

  Replay: fork checkpoint `de31ced5-c11c-407c-a124-cd461b0bfb97` and run
  ```
  RUN_TAG=110246f2d5a6 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 75 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7125, 0.7542, 0.7167, 0.7583, 0.7333; gap after +0.6%; result checkpoint `24ee509a-966d-4672-9b4f-89e8a85faf16`
- Effect: candidate 0.7333 minus naive 0.5375 = +0.1958, 95% bootstrap interval [+0.1584, +0.2567] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.729 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7292 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5625, 0.475, 0.4875, 0.5375, 0.5708
- Spread: range 0.475 to 0.5708, noise band ±0.0666 (2 x MAD), CV 8.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -26.3% (noise band ±9.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `epochs` the gap is -18.3% (it comes back)
- PASS · Counterfactual (reversal test): without `normalize` the gap is -29.1% (it comes back)
- PASS · Held-out claim: C2: -19.5% to +0.8% (not worse beyond noise)
- FAIL · Evidence: `epochs=75`: no evidence mentions '75'; it fits, but nothing says the authors used it
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.1958 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `os`, `evaluation_metric`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `epochs=750` (2.44 noise units, gap -4.0%); `normalize=zscore` (1.44 noise units, gap +13.1%); `lr_schedule=cosine` (1.19 noise units, gap -15.4%)
- Near alternatives (closest across all claims):
  - `lr_schedule=step`, `epochs=750`: this claim -1.2%, mean |gap| 1.5% (5 runs)
  - `lr_schedule=cosine`, `epochs=150`: this claim -1.2%, mean |gap| 2.4% (5 runs)
  - `lr_schedule=cosine`, `epochs=75`: this claim -8.6%, mean |gap| 5.6% (5 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `epochs=75, normalize=minmax` (reported)
- `epochs=150, lr_schedule=cosine`
- `epochs=750, lr_schedule=step`

### History matching (every measured configuration, all claims together)
- 32 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `epochs, normalize`: epochs=75, normalize=minmax (max I 0.16); epochs=150, normalize=minmax (max I 1.52)
  - `epochs, lr_schedule`: epochs=750, lr_schedule=step (max I 0.4); epochs=150, lr_schedule=cosine (max I 0.59); epochs=75, lr_schedule=cosine (max I 1.36); epochs=750, lr_schedule=cosine (max I 1.93); +1 more
  - `class_weight, lr_schedule`: class_weight=balanced, lr_schedule=cosine (max I 2.14)
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 2.35)
  - `lr_schedule`: lr_schedule=cosine (max I 2.42)
- Equally good values: `epochs` in {75, 150}

Notes:
- configurations the target claim can't tell apart from the answer: epochs=75, normalize=minmax; epochs=150, lr_schedule=cosine; epochs=750, lr_schedule=step
- equally good values within one noise band (measured): epochs in {75, 150}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `epochs=75`, `normalize=minmax` | 5 | +0.6% | +0.8% | 0.7% |
| `lr_schedule=step`, `epochs=750` | 5 | -1.2% | +1.9% | 1.5% |
| `lr_schedule=cosine`, `epochs=150` | 5 | -1.2% | +3.7% | 2.4% |
| `lr_schedule=cosine`, `epochs=75` | 5 | -8.6% | -2.6% | 5.6% |
| `epochs=150`, `normalize=minmax` | 5 | +6.3% | +9.9% | 8.1% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `os`, `evaluation_metric`

## Provenance
- GapFinder commit: `efb2f63a257a40b9982099a274f2e882f272b80c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
