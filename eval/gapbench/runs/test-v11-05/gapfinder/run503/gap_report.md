# Gap Report: test-v11-05

Artifact `mlbench` · generated 2026-10-14 22:19 · 199 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -26.3% | +6.3% | ±2.3% | `class_weight=balanced`, `normalize=minmax` |

## C1: test_accuracy (paper 0.7292)
**Fits but unsupported** · gap -26.3% → +6.3% · 53 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0097`, `B0168`, `B0169`, `B0170`, `B0171` (5 run(s) of the same config)
- Config: `class_weight` naive `none`, changed to `balanced`
- Config: `normalize` naive `none`, changed to `minmax`
- Command:

  Replay: fork checkpoint `fdae3ea7-6c8d-40fa-9113-b33847087d24` and run
  ```
  RUN_TAG=79332aaae169 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight balanced --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7833, 0.7833, 0.775, 0.775, 0.7667; gap after +6.3%; result checkpoint `159eebb3-8819-4e1e-95c2-2debb7eab190`
- Effect: candidate 0.775 minus naive 0.5375 = +0.2375, 95% bootstrap interval [+0.2175, +0.295] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.729 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7292 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5625, 0.4667, 0.5333, 0.5458, 0.5375
- Spread: range 0.4667 to 0.5625, noise band ±0.0166 (2 x MAD), CV 6.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -26.3% (noise band ±2.3% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `class_weight` the gap is -18.3% (it comes back)
- PASS · Counterfactual (reversal test): without `normalize` the gap is -36.0% (it comes back)
- PASS · Held-out claim: C2: -19.5% to +16.3% (not worse beyond noise)
- FAIL · Evidence: `class_weight=balanced`: no evidence mentions 'balanced'; it fits, but nothing says the authors used it
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2375 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `os`, `evaluation_metric`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (5.78 noise units, gap +13.1%); `lr_schedule=cosine` (4.77 noise units, gap -15.4%); `epochs=75` (2.01 noise units, gap -21.7%); `epochs=8` (1.25 noise units, gap -23.4%)
- Near alternatives (closest across all claims):
  - `lr_schedule=cosine`, `epochs=30`: this claim -12.6%, mean |gap| 9.2% (5 runs)
  - `lr_schedule=cosine`, `epochs=750`: this claim +8.6%, mean |gap| 10.6% (5 runs)
  - `normalize=zscore`, `class_weight=balanced`: this claim +7.4%, mean |gap| 12.0% (5 runs)

### History matching (every measured configuration, all claims together)
- 11 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `epochs, lr_schedule`: epochs=750, lr_schedule=step (max I 1.24); epochs=750, lr_schedule=cosine (max I 2.05); epochs=30, lr_schedule=cosine (max I 2.18); epochs=2, lr_schedule=cosine (max I 2.75); +1 more
  - `epochs, normalize`: epochs=750, normalize=minmax (max I 2.36)
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 2.58); class_weight=balanced, normalize=zscore (max I 2.64)
  - `lr_schedule`: lr_schedule=cosine (max I 2.61)
  - `class_weight, lr_schedule`: class_weight=balanced, lr_schedule=cosine (max I 2.83)
- 3 separate islands (no single-knob move joins them): epochs=750, lr_schedule=step; epochs=750, lr_schedule=cosine; epochs=30, lr_schedule=cosine | epochs=750, normalize=minmax; epochs=30, normalize=minmax | class_weight=balanced, normalize=minmax; class_weight=balanced, normalize=zscore

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'lr_schedule': 'cosine', 'epochs': '2'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=cosine`, `epochs=30` | 5 | -12.6% | -5.7% | 9.2% |
| `lr_schedule=cosine`, `epochs=750` | 5 | +8.6% | +12.7% | 10.6% |
| `class_weight=balanced`, `normalize=minmax` | 5 | +6.3% | +16.3% | 11.3% |
| `normalize=zscore`, `class_weight=balanced` | 5 | +7.4% | +16.6% | 12.0% |
| `lr_schedule=cosine` | 6 | -15.7% | -8.6% | 12.2% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `os`, `evaluation_metric`

## Provenance
- GapFinder commit: `e0f13d101585ad1609a15fbf67b70128f4cfffc8` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
