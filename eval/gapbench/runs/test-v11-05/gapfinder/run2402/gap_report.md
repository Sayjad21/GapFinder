# Gap Report: test-v11-05

Artifact `mlbench` · generated 2026-10-16 01:24 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -26.3% | +0.0% | ±0.7% | `epochs=75`, `normalize=minmax` |

## C1: test_accuracy (paper 0.7292)
**Fits but unsupported** · gap -26.3% → +0.0% · 61 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0069`, `B0103`, `B0144`, `B0145`, `B0146` (5 run(s) of the same config)
- Config: `epochs` naive `15`, changed to `75`
- Config: `normalize` naive `none`, changed to `minmax`
- Command:

  Replay: fork checkpoint `f689b803-7335-474e-8f45-a924f83a72c2` and run
  ```
  RUN_TAG=80a168f3c9d4 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 75 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7292, 0.7375, 0.7167, 0.7167, 0.7333; gap after +0.0%; result checkpoint `ef75f635-1d28-4b03-85af-3b6fdab64e65`
- Effect: candidate 0.7292 minus naive 0.5375 = +0.1917, 95% bootstrap interval [+0.1742, +0.2466] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.729 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7292 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.55, 0.5375, 0.5375, 0.4667, 0.5375
- Spread: range 0.4667 to 0.55, noise band ±0.005375 (2 x MAD), CV 6.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -26.3% (noise band ±0.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `epochs` the gap is -18.3% (it comes back)
- PASS · Counterfactual (reversal test): without `normalize` the gap is -29.7% (it comes back)
- PASS · Held-out claim: C2: -19.5% to +0.0% (not worse beyond noise)
- FAIL · Evidence: `epochs=75`: no evidence mentions '75'; it fits, but nothing says the authors used it
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.1917 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (17.84 noise units, gap +13.1%); `lr_schedule=cosine` (13.17 noise units, gap -16.6%); `epochs=750` (9.3 noise units, gap -19.4%); `epochs=2` (3.87 noise units, gap -23.4%); `epochs=3` (3.11 noise units, gap -24.0%) (and 2 more in the JSON)
- Near alternatives (closest across all claims):
  - `epochs=75`, `lr_schedule=cosine`: this claim -8.0%, mean |gap| 5.1% (5 runs)
  - `epochs=750`, `lr_schedule=step`: this claim +5.7%, mean |gap| 7.5% (5 runs)
  - `normalize=minmax`, `epochs=150`: this claim +6.9%, mean |gap| 8.8% (5 runs)

### History matching (every measured configuration, all claims together)
- 12 of 61 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `epochs, normalize`: epochs=75, normalize=minmax (max I 0.07); epochs=150, normalize=minmax (max I 1.78)
  - `epochs, lr_schedule`: epochs=750, lr_schedule=step (max I 0.71); epochs=75, lr_schedule=cosine (max I 1.36); epochs=750, lr_schedule=cosine (max I 2.12); epochs=20, lr_schedule=cosine (max I 2.34); +1 more
  - `lr_schedule`: lr_schedule=cosine (max I 2.55)
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 2.56)
  - `class_weight, lr_schedule`: class_weight=balanced, lr_schedule=cosine (max I 2.66)
- 4 separate islands (no single-knob move joins them): epochs=750, lr_schedule=step; epochs=75, lr_schedule=cosine; epochs=750, lr_schedule=cosine | epochs=75, normalize=minmax; epochs=150, normalize=minmax | class_weight=balanced, normalize=minmax; class_weight=balanced, normalize=zscore | epochs=10, normalize=zscore

Notes:
- stopped early: run budget of 200 reached (wanted 3 more run(s) of {'normalize': 'zscore', 'epochs': '10'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `epochs=75`, `normalize=minmax` | 5 | +0.0% | +0.0% | 0.0% |
| `epochs=75`, `lr_schedule=cosine` | 5 | -8.0% | -2.1% | 5.1% |
| `epochs=750`, `lr_schedule=step` | 5 | +5.7% | +9.4% | 7.5% |
| `normalize=minmax`, `epochs=150` | 5 | +6.9% | +10.7% | 8.8% |
| `normalize=minmax`, `class_weight=balanced` | 5 | +5.7% | +15.8% | 10.7% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
