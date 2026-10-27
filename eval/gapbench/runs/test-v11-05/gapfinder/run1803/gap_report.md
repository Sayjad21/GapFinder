# Gap Report: test-v11-05

Artifact `mlbench` · generated 2026-10-15 19:46 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -33.1% | +2.3% | ±5.7% | `lr_schedule=step`, `epochs=750` |

## C1: test_accuracy (paper 0.7292)
**Fits but unsupported** · gap -33.1% → +2.3% · 53 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0102`, `B0118`, `B0154`, `B0155`, `B0156` (5 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `step`
- Config: `epochs` naive `15`, changed to `750`
- Command:

  Replay: fork checkpoint `879f880e-5726-4043-955e-b568fc3a92fc` and run
  ```
  RUN_TAG=f6e2f2f8c96a "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize none --epochs 750 --batch_size 32 --lr 0.05 --lr_schedule step --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7458, 0.6917, 0.7583, 0.7875, 0.6875; gap after +2.3%; result checkpoint `415386e0-7826-42db-b8bf-51f3ac9cb839`
- Effect: candidate 0.7458 minus naive 0.4875 = +0.2583, 95% bootstrap interval [+0.1583, +0.2941] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.729 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7292 (headline claim)

### What did we measure?
- Naive median 0.4875 over 5 runs; repeats: 0.5625, 0.475, 0.5375, 0.4875, 0.4667
- Spread: range 0.4667 to 0.5625, noise band ±0.0416 (2 x MAD), CV 8.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -33.1% (noise band ±5.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is -22.9% (it comes back)
- PASS · Counterfactual (reversal test): without `epochs` the gap is -24.0% (it comes back)
- PASS · Held-out claim: C2: -28.1% to +6.5% (not worse beyond noise)
- FAIL · Evidence: `lr_schedule=step`: no evidence mentions 'step'; it fits, but nothing says the authors used it
- FAIL · Evidence: `epochs=750`: no evidence mentions '750'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2583 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `os`, `evaluation_metric`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (3.41 noise units, gap +13.7%); `lr_schedule=cosine` (3 noise units, gap -16.0%); `normalize=minmax` (2.6 noise units, gap -18.3%); `epochs=1` (1.2 noise units, gap -26.3%); `epochs=10` (1.1 noise units, gap -26.9%) (and 2 more in the JSON)
- Near alternatives (closest across all claims):
  - `epochs=75`, `normalize=minmax`: this claim -1.2%, mean |gap| 1.3% (5 runs)
  - `lr_schedule=cosine`, `epochs=75`: this claim -8.6%, mean |gap| 5.6% (5 runs)
  - `class_weight=balanced`, `normalize=minmax`: this claim +2.9%, mean |gap| 8.9% (5 runs)

### History matching (every measured configuration, all claims together)
- 19 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `epochs, normalize`: epochs=75, normalize=minmax (max I 0.23)
  - `epochs, lr_schedule`: epochs=750, lr_schedule=step (max I 0.67); epochs=75, lr_schedule=cosine (max I 1.43); epochs=750, lr_schedule=cosine (max I 1.95); epochs=30, lr_schedule=cosine (max I 2.08); +2 more
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 2.07); class_weight=balanced, normalize=zscore (max I 2.57)
  - `lr_schedule`: lr_schedule=cosine (max I 2.4)
- 2 separate islands (no single-knob move joins them): epochs=75, normalize=minmax; class_weight=balanced, normalize=minmax; class_weight=balanced, normalize=zscore | epochs=750, lr_schedule=step; epochs=75, lr_schedule=cosine; epochs=750, lr_schedule=cosine

Notes:
- stopped early: run budget of 200 reached (wanted 3 more run(s) of {'lr_schedule': 'cosine', 'epochs': '30'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `epochs=75`, `normalize=minmax` | 5 | -1.2% | -1.5% | 1.3% |
| `lr_schedule=step`, `epochs=750` | 5 | +2.3% | +6.5% | 4.4% |
| `lr_schedule=cosine`, `epochs=75` | 5 | -8.6% | -2.6% | 5.6% |
| `class_weight=balanced`, `normalize=minmax` | 5 | +2.9% | +15.0% | 8.9% |
| `lr_schedule=cosine`, `epochs=750` | 5 | +8.6% | +12.7% | 10.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `os`, `evaluation_metric`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
