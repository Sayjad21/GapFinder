# Gap Report: test-v11-05

Artifact `mlbench` · generated 2026-10-16 01:23 · 199 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -33.7% | +0.0% | ±4.6% | `normalize=minmax`, `epochs=75` |

## C1: test_accuracy (paper 0.7292)
**Fits but unsupported** · gap -33.7% → +0.0% · 53 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0098`, `B0122`, `B0152`, `B0153`, `B0154` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `epochs` naive `15`, changed to `75`
- Command:

  Replay: fork checkpoint `7331be52-e98b-4082-8087-b394760801ec` and run
  ```
  RUN_TAG=ad250dbe7fc3 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 75 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7542, 0.7208, 0.7375, 0.7125, 0.7292; gap after +0.0%; result checkpoint `196222c8-4405-4c74-b687-f4db0ffa5764`
- Effect: candidate 0.7292 minus naive 0.4833 = +0.2459, 95% bootstrap interval [+0.19, +0.2692] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.729 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7292 (headline claim)

### What did we measure?
- Naive median 0.4833 over 5 runs; repeats: 0.5083, 0.4667, 0.475, 0.5458, 0.4833
- Spread: range 0.4667 to 0.5458, noise band ±0.0332 (2 x MAD), CV 6.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -33.7% (noise band ±4.6% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -28.3% (it comes back)
- PASS · Counterfactual (reversal test): without `epochs` the gap is -18.3% (it comes back)
- PASS · Held-out claim: C2: -28.7% to +0.0% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- FAIL · Evidence: `epochs=75`: no evidence mentions '75'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2459 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (4.64 noise units, gap -12.6%); `normalize=zscore` (4.39 noise units, gap +13.7%); `class_weight=balanced` (2.51 noise units, gap -22.3%); `epochs=8` (2.14 noise units, gap -24.0%); `epochs=3` (2.14 noise units, gap -24.0%) (and 5 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=step`, `epochs=750`: this claim -3.4%, mean |gap| 2.2% (5 runs)
  - `epochs=150`, `lr_schedule=cosine`: this claim -1.7%, mean |gap| 2.4% (5 runs)
  - `epochs=75`, `lr_schedule=cosine`: this claim -8.0%, mean |gap| 5.1% (5 runs)

### History matching (every measured configuration, all claims together)
- 11 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `epochs, normalize`: epochs=75, normalize=minmax (max I 0.06); epochs=150, normalize=minmax (max I 1.64)
  - `epochs, lr_schedule`: epochs=150, lr_schedule=cosine (max I 0.49); epochs=750, lr_schedule=step (max I 0.66); epochs=75, lr_schedule=cosine (max I 1.43); epochs=750, lr_schedule=cosine (max I 2.12); +1 more
  - `lr_schedule`: lr_schedule=cosine (max I 2.42)
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 2.52)
  - `class_weight, lr_schedule`: class_weight=balanced, lr_schedule=cosine (max I 2.7)
- 3 separate islands (no single-knob move joins them): epochs=150, lr_schedule=cosine; epochs=750, lr_schedule=step; epochs=75, lr_schedule=cosine | epochs=75, normalize=minmax; epochs=150, normalize=minmax | class_weight=balanced, normalize=minmax; class_weight=balanced, normalize=zscore

Notes:
- stopped early: run budget of 200 reached (wanted 3 more run(s) of {'normalize': 'zscore', 'epochs': '8'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax`, `epochs=75` | 5 | +0.0% | +0.0% | 0.0% |
| `lr_schedule=step`, `epochs=750` | 5 | -3.4% | +1.1% | 2.2% |
| `epochs=150`, `lr_schedule=cosine` | 5 | -1.7% | +3.1% | 2.4% |
| `epochs=75`, `lr_schedule=cosine` | 5 | -8.0% | -2.1% | 5.1% |
| `normalize=minmax`, `epochs=150` | 5 | +6.3% | +9.9% | 8.1% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
