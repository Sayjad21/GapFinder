# Gap Report: test-v11-05

Artifact `mlbench` · generated 2026-10-14 23:33 · 199 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -33.7% | +5.1% | ±1.2% | `normalize=minmax`, `class_weight=balanced` |

## C1: test_accuracy (paper 0.7292)
**Fits but unsupported** · gap -33.7% → +5.1% · 53 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0094`, `B0168`, `B0169`, `B0170`, `B0171` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `class_weight` naive `none`, changed to `balanced`
- Command:

  Replay: fork checkpoint `7f01c5aa-306f-4a9f-803c-2353451db1ad` and run
  ```
  RUN_TAG=56637b408ed1 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight balanced --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7708, 0.7333, 0.7667, 0.7625, 0.775; gap after +5.1%; result checkpoint `4b48eeec-f637-4b73-b23a-ad2cdd110527`
- Effect: candidate 0.7667 minus naive 0.4833 = +0.2834, 95% bootstrap interval [+0.2167, +0.2983] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.729 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7292 (headline claim)

### What did we measure?
- Naive median 0.4833 over 5 runs; repeats: 0.5583, 0.4833, 0.4667, 0.4833, 0.4875
- Spread: range 0.4667 to 0.5583, noise band ±0.0084 (2 x MAD), CV 7.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -33.7% (noise band ±1.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -26.6% (it comes back)
- PASS · Counterfactual (reversal test): without `class_weight` the gap is -18.3% (it comes back)
- PASS · Held-out claim: C2: -28.9% to +15.6% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- FAIL · Evidence: `class_weight=balanced`: no evidence mentions 'balanced'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2834 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (17.87 noise units, gap +13.1%); `lr_schedule=cosine` (14.39 noise units, gap -17.1%); `epochs=750` (10.92 noise units, gap -21.1%); `epochs=3` (7.94 noise units, gap -24.6%); `epochs=2` (6.45 noise units, gap -26.3%) (and 4 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=cosine`, `epochs=30`: this claim -13.2%, mean |gap| 9.8% (5 runs)
  - `lr_schedule=cosine`, `epochs=750`: this claim +8.6%, mean |gap| 10.6% (5 runs)
  - `epochs=20`, `lr_schedule=cosine`: this claim -14.3%, mean |gap| 10.9% (5 runs)

### History matching (every measured configuration, all claims together)
- 11 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `epochs, lr_schedule`: epochs=750, lr_schedule=step (max I 0.25); epochs=30, lr_schedule=cosine (max I 2.12); epochs=750, lr_schedule=cosine (max I 2.13); epochs=20, lr_schedule=cosine (max I 2.39); +1 more
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 2.47); class_weight=balanced, normalize=zscore (max I 2.73)
  - `lr_schedule`: lr_schedule=cosine (max I 2.52)
  - `lr_schedule, normalize`: lr_schedule=step, normalize=zscore (max I 2.61)
  - `epochs, normalize`: epochs=30, normalize=minmax (max I 2.87)
- 4 separate islands (no single-knob move joins them): epochs=750, lr_schedule=step; epochs=30, lr_schedule=cosine; epochs=750, lr_schedule=cosine | class_weight=balanced, normalize=minmax; class_weight=balanced, normalize=zscore | lr_schedule=step, normalize=zscore | epochs=30, normalize=minmax

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'normalize': 'minmax', 'epochs': '2'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=cosine`, `epochs=30` | 5 | -13.2% | -6.5% | 9.8% |
| `normalize=minmax`, `class_weight=balanced` | 5 | +5.1% | +15.6% | 10.4% |
| `lr_schedule=cosine`, `epochs=750` | 5 | +8.6% | +12.7% | 10.6% |
| `epochs=20`, `lr_schedule=cosine` | 5 | -14.3% | -7.6% | 10.9% |
| `normalize=zscore`, `class_weight=balanced` | 5 | +7.4% | +16.6% | 12.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`

## Provenance
- GapFinder commit: `efb2f63a257a40b9982099a274f2e882f272b80c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
