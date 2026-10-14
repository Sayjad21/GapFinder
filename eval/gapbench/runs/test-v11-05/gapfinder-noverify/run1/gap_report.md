# Gap Report: test-v11-05

Artifact `mlbench` · generated 2026-10-14 11:17 · 197 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Partially explained | -32.6% | -1.2% | ±1.2% | `epochs=150`, `lr_schedule=cosine` |

## C1: test_accuracy (paper 0.7292)
**Partially explained** · gap -32.6% → -1.2% · 49 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0091`, `B0186`, `B0187`, `B0188`, `B0189` (5 run(s) of the same config)
- Config: `epochs` naive `15`, changed to `150`
- Config: `lr_schedule` naive `const`, changed to `cosine`
- Command:

  Replay: fork checkpoint `493d6eac-0c09-49e6-b4b5-d507a8deafb6` and run
  ```
  RUN_TAG=0e67cb92fc00 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize none --epochs 150 --batch_size 32 --lr 0.05 --lr_schedule cosine --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7208, 0.7167, 0.7167, 0.7292, 0.7208; gap after -1.2%; result checkpoint `87c54c03-6dd1-450c-a12a-f0ced3e0d3c2`
- Effect: candidate 0.7208 minus naive 0.4917 = +0.2291, 95% bootstrap interval [+0.18, +0.2367] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.729 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7292 (headline claim)

### What did we measure?
- Naive median 0.4917 over 5 runs; repeats: 0.4917, 0.4875, 0.4917, 0.4875, 0.55
- Spread: range 0.4875 to 0.55, noise band ±0.0084 (2 x MAD), CV 5.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -32.6% (noise band ±1.2% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is +0.2291 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (16.37 noise units, gap +13.7%); `normalize=minmax` (12.39 noise units, gap -18.3%); `epochs=10` (8.93 noise units, gap -22.3%); `epochs=20` (8.43 noise units, gap -22.9%); `epochs=2` (5.45 noise units, gap -26.3%) (and 3 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=cosine`: this claim -13.7%, mean |gap| 10.4% (6 runs)
  - `class_weight=balanced`, `normalize=minmax`: this claim +5.7%, mean |gap| 10.7% (5 runs)
  - `lr_schedule=cosine`, `epochs=20`: this claim -14.3%, mean |gap| 10.9% (5 runs)

### History matching (every measured configuration, all claims together)
- 9 of 49 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 9 configurations
  - `epochs, lr_schedule`: epochs=150, lr_schedule=cosine (max I 0.65); epochs=150, lr_schedule=step (max I 1.68); epochs=20, lr_schedule=step (max I 2.38); epochs=20, lr_schedule=cosine (max I 2.51)
  - `epochs, normalize`: epochs=150, normalize=minmax (max I 1.45); epochs=8, normalize=zscore (max I 2.97)
  - `lr_schedule`: lr_schedule=cosine (max I 2.56)
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 2.73); class_weight=balanced, normalize=zscore (max I 2.95)
- 4 separate islands (no single-knob move joins them): epochs=150, lr_schedule=cosine; epochs=150, lr_schedule=step; epochs=20, lr_schedule=step | class_weight=balanced, normalize=minmax; class_weight=balanced, normalize=zscore | epochs=150, normalize=minmax | epochs=8, normalize=zscore

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'normalize': 'zscore', 'epochs': '8'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `epochs=150`, `lr_schedule=cosine` | 5 | -1.2% | +3.7% | 2.4% |
| `lr_schedule=cosine` | 6 | -13.7% | -7.2% | 10.4% |
| `class_weight=balanced`, `normalize=minmax` | 5 | +5.7% | +15.8% | 10.7% |
| `lr_schedule=cosine`, `epochs=20` | 5 | -14.3% | -7.6% | 10.9% |
| `class_weight=balanced`, `normalize=zscore` | 5 | +7.4% | +16.6% | 12.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`

## Provenance
- GapFinder commit: `b05f7288e1a4df8af69bb0b5e7633827b4cb46c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
