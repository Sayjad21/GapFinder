# Gap Report: test-v11-05

Artifact `mlbench` · generated 2026-10-15 00:55 · 198 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -30.3% | +0.0% | ±9.1% | `normalize=minmax`, `epochs=75` |

## C1: test_accuracy (paper 0.7292)
**Fits but unsupported** · gap -30.3% → +0.0% · 61 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0054`, `B0139`, `B0140`, `B0141`, `B0142` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `epochs` naive `15`, changed to `75`
- Command:

  Replay: fork checkpoint `b7638bc7-52f3-47b7-9317-1d7cd1edc5d6` and run
  ```
  RUN_TAG=f5ba0e037ca9 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 75 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7125, 0.7542, 0.7208, 0.7292, 0.7333; gap after +0.0%; result checkpoint `3350dac7-e4fb-495b-9a8c-8dd7546edb29`
- Effect: candidate 0.7292 minus naive 0.5083 = +0.2209, 95% bootstrap interval [+0.1858, +0.2583] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.729 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7292 (headline claim)

### What did we measure?
- Naive median 0.5083 over 5 runs; repeats: 0.5458, 0.475, 0.5375, 0.5083, 0.475
- Spread: range 0.475 to 0.5458, noise band ±0.0666 (2 x MAD), CV 6.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -30.3% (noise band ±9.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -21.7% (it comes back)
- PASS · Counterfactual (reversal test): without `epochs` the gap is -18.3% (it comes back)
- PASS · Held-out claim: C2: -25.1% to +0.0% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- FAIL · Evidence: `epochs=75`: no evidence mentions '75'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2209 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (1.82 noise units, gap +13.7%); `epochs=750` (1.69 noise units, gap -14.9%); `lr_schedule=cosine` (1.5 noise units, gap -16.6%)
- Near alternatives (closest across all claims):
  - `lr_schedule=step`, `epochs=750`: this claim +2.9%, mean |gap| 4.6% (5 runs)
  - `epochs=75`, `lr_schedule=cosine`: this claim -9.1%, mean |gap| 6.1% (5 runs)
  - `epochs=20`, `lr_schedule=cosine`: this claim -12.0%, mean |gap| 8.5% (5 runs)

### History matching (every measured configuration, all claims together)
- 14 of 61 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `epochs, normalize`: epochs=75, normalize=minmax (max I 0.03); epochs=150, normalize=zscore (max I 2.52)
  - `epochs, lr_schedule`: epochs=150, lr_schedule=cosine (max I 0.48); epochs=750, lr_schedule=step (max I 0.94); epochs=75, lr_schedule=cosine (max I 1.39); epochs=30, lr_schedule=cosine (max I 1.93); +2 more
  - `lr_schedule`: lr_schedule=cosine (max I 2.61)
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 2.65)
- 4 separate islands (no single-knob move joins them): epochs=150, lr_schedule=cosine; epochs=750, lr_schedule=step; epochs=75, lr_schedule=cosine | epochs=150, normalize=zscore; epochs=3, normalize=zscore | class_weight=balanced, normalize=minmax; class_weight=balanced, normalize=zscore | epochs=75, normalize=minmax

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'normalize': 'zscore', 'epochs': '150'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax`, `epochs=75` | 5 | +0.0% | +0.0% | 0.0% |
| `lr_schedule=step`, `epochs=750` | 5 | +2.9% | +6.3% | 4.6% |
| `epochs=75`, `lr_schedule=cosine` | 5 | -9.1% | -3.1% | 6.1% |
| `epochs=20`, `lr_schedule=cosine` | 5 | -12.0% | -5.0% | 8.5% |
| `class_weight=balanced`, `normalize=minmax` | 5 | +5.1% | +16.0% | 10.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
