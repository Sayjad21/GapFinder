# Gap Report: test-v11-05

Artifact `mlbench` · generated 2026-10-14 23:49 · 198 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -22.3% | -2.3% | ±2.3% | `lr_schedule=cosine`, `epochs=150` |

## C1: test_accuracy (paper 0.7292)
**Fits but unsupported** · gap -22.3% → -2.3% · 53 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0084`, `B0143`, `B0144`, `B0145`, `B0146` (5 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `cosine`
- Config: `epochs` naive `15`, changed to `150`
- Command:

  Replay: fork checkpoint `a70bc1de-8b8b-4943-9600-cb5fc711da92` and run
  ```
  RUN_TAG=cdbf813d70e4 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize none --epochs 150 --batch_size 32 --lr 0.05 --lr_schedule cosine --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7125, 0.7167, 0.725, 0.7125, 0.7042; gap after -2.3%; result checkpoint `a205fe1b-225a-4364-88b2-06310837acad`
- Effect: candidate 0.7125 minus naive 0.5667 = +0.1458, 95% bootstrap interval [+0.1375, +0.2184] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.729 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7292 (headline claim)

### What did we measure?
- Naive median 0.5667 over 5 runs; repeats: 0.5667, 0.4833, 0.55, 0.5667, 0.575
- Spread: range 0.4833 to 0.575, noise band ±0.0166 (2 x MAD), CV 6.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -22.3% (noise band ±2.3% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is -23.1% (it comes back)
- PASS · Counterfactual (reversal test): without `epochs` the gap is -14.9% (it comes back)
- PASS · Held-out claim: C2: -16.3% to +2.9% (not worse beyond noise)
- FAIL · Evidence: `lr_schedule=cosine`: no evidence mentions 'cosine'; it fits, but nothing says the authors used it
- FAIL · Evidence: `epochs=150`: no evidence mentions '150'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.1458 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (3.77 noise units, gap +13.7%); `normalize=minmax` (1.75 noise units, gap -18.3%)
- Near alternatives (closest across all claims):
  - `normalize=minmax`, `epochs=150`: this claim +6.3%, mean |gap| 7.8% (5 runs)
  - `lr_schedule=cosine`, `epochs=30`: this claim -12.6%, mean |gap| 9.0% (5 runs)
  - `lr_schedule=cosine`, `epochs=750`: this claim +8.6%, mean |gap| 10.6% (5 runs)

### History matching (every measured configuration, all claims together)
- 16 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `epochs, lr_schedule`: epochs=150, lr_schedule=cosine (max I 0.48); epochs=750, lr_schedule=step (max I 1.08); epochs=750, lr_schedule=cosine (max I 2.08); epochs=30, lr_schedule=cosine (max I 2.11); +1 more
  - `epochs, normalize`: epochs=150, normalize=minmax (max I 1.62); epochs=750, normalize=minmax (max I 2.42)
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 1.76)
  - `lr_schedule`: lr_schedule=cosine (max I 2.39)
  - `class_weight, epochs`: class_weight=balanced, epochs=30 (max I 2.57)
- 4 separate islands (no single-knob move joins them): epochs=150, lr_schedule=cosine; epochs=750, lr_schedule=step; epochs=750, lr_schedule=cosine | epochs=150, normalize=minmax; epochs=750, normalize=minmax | class_weight=balanced, normalize=minmax; class_weight=balanced, normalize=zscore | class_weight=balanced, epochs=30; class_weight=balanced, epochs=750

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'normalize': 'minmax', 'epochs': '750'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=cosine`, `epochs=150` | 5 | -2.3% | +2.9% | 2.6% |
| `normalize=minmax`, `epochs=150` | 5 | +6.3% | +9.4% | 7.8% |
| `lr_schedule=cosine`, `epochs=30` | 5 | -12.6% | -5.5% | 9.0% |
| `lr_schedule=cosine`, `epochs=750` | 5 | +8.6% | +12.7% | 10.6% |
| `lr_schedule=cosine` | 3 | -14.9% | -8.3% | 11.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`

## Provenance
- GapFinder commit: `efb2f63a257a40b9982099a274f2e882f272b80c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
