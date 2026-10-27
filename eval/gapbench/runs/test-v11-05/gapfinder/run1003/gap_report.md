# Gap Report: test-v11-05

Artifact `mlbench` · generated 2026-10-15 00:23 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -25.2% | -1.2% | ±2.3% | `normalize=minmax`, `epochs=75` |

## C1: test_accuracy (paper 0.7292)
**Fits but unsupported** · gap -25.2% → -1.2% · 53 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0096`, `B0185`, `B0186`, `B0187`, `B0188` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `epochs` naive `15`, changed to `75`
- Command:

  Replay: fork checkpoint `2e097c7b-45a5-4f8d-89cd-07bc6d165647` and run
  ```
  RUN_TAG=1e2be7cf2eb6 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 75 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7125, 0.7167, 0.7333, 0.7208, 0.7208; gap after -1.2%; result checkpoint `216bd497-a69f-4bb0-aaa8-48e798660cdb`
- Effect: candidate 0.7208 minus naive 0.5458 = +0.175, 95% bootstrap interval [+0.1434, +0.2192] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.729 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7292 (headline claim)

### What did we measure?
- Naive median 0.5458 over 5 runs; repeats: 0.5375, 0.5458, 0.4875, 0.5458, 0.5833
- Spread: range 0.4875 to 0.5833, noise band ±0.0166 (2 x MAD), CV 6.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -25.2% (noise band ±2.3% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -33.4% (it comes back)
- PASS · Counterfactual (reversal test): without `epochs` the gap is -18.3% (it comes back)
- PASS · Held-out claim: C2: -18.7% to -1.5% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- FAIL · Evidence: `epochs=75`: no evidence mentions '75'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.175 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `os`, `evaluation_metric`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (5.02 noise units, gap +13.7%); `lr_schedule=cosine` (4.77 noise units, gap -14.3%); `epochs=150` (1.01 noise units, gap -22.9%); `class_weight=balanced` (1.01 noise units, gap -22.9%)
- Near alternatives (closest across all claims):
  - `epochs=150`, `lr_schedule=cosine`: this claim -1.7%, mean |gap| 2.4% (5 runs)
  - `lr_schedule=cosine`, `epochs=75`: this claim -8.0%, mean |gap| 4.9% (5 runs)
  - `normalize=minmax`, `epochs=150`: this claim +6.3%, mean |gap| 8.0% (5 runs)

### History matching (every measured configuration, all claims together)
- 13 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `epochs, normalize`: epochs=75, normalize=minmax (max I 0.26); epochs=150, normalize=minmax (max I 1.72)
  - `epochs, lr_schedule`: epochs=150, lr_schedule=cosine (max I 0.55); epochs=75, lr_schedule=cosine (max I 1.37); epochs=75, lr_schedule=step (max I 2.14); epochs=20, lr_schedule=cosine (max I 2.48); +1 more
  - `lr_schedule`: lr_schedule=cosine (max I 2.53)
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 2.6)
  - `lr_schedule, normalize`: lr_schedule=step, normalize=zscore (max I 2.73)
- 4 separate islands (no single-knob move joins them): epochs=150, lr_schedule=cosine; epochs=75, lr_schedule=cosine; epochs=75, lr_schedule=step | epochs=75, normalize=minmax; epochs=150, normalize=minmax | class_weight=balanced, normalize=minmax; class_weight=balanced, normalize=zscore | lr_schedule=step, normalize=zscore

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'normalize': 'minmax', 'epochs': '8'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax`, `epochs=75` | 5 | -1.2% | -1.5% | 1.3% |
| `epochs=150`, `lr_schedule=cosine` | 5 | -1.7% | +3.1% | 2.4% |
| `lr_schedule=cosine`, `epochs=75` | 5 | -8.0% | -1.8% | 4.9% |
| `normalize=minmax`, `epochs=150` | 5 | +6.3% | +9.7% | 8.0% |
| `normalize=minmax`, `class_weight=balanced` | 5 | +4.6% | +15.2% | 9.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `os`, `evaluation_metric`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
