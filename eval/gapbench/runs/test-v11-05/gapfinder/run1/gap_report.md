# Gap Report: test-v11-05

Artifact `mlbench` · generated 2026-10-14 11:16 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -26.9% | -1.2% | ±1.2% | `lr_schedule=cosine`, `epochs=150` |

## C1: test_accuracy (paper 0.7292)
**Fits but unsupported** · gap -26.9% → -1.2% · 49 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0091`, `B0197`, `B0198`, `B0199`, `B0200` (5 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `cosine`
- Config: `epochs` naive `15`, changed to `150`
- Command:

  Replay: fork checkpoint `c230b3ba-2917-4f6c-95bd-4b986be7bc81` and run
  ```
  RUN_TAG=e60498029d35 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize none --epochs 150 --batch_size 32 --lr 0.05 --lr_schedule cosine --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7208, 0.7083, 0.7208, 0.725, 0.7167; gap after -1.2%; result checkpoint `96c93a61-1ea0-4e0a-b9c3-220ad4f4a4f6`
- Effect: candidate 0.7208 minus naive 0.5333 = +0.1875, 95% bootstrap interval [+0.1775, +0.2358] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.729 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7292 (headline claim)

### What did we measure?
- Naive median 0.5333 over 5 runs; repeats: 0.4875, 0.4833, 0.5375, 0.5375, 0.5333
- Spread: range 0.4833 to 0.5375, noise band ±0.0084 (2 x MAD), CV 5.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -26.9% (noise band ±1.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is -26.6% (it comes back)
- PASS · Counterfactual (reversal test): without `epochs` the gap is -14.6% (it comes back)
- PASS · Held-out claim: C2: -20.0% to +3.7% (not worse beyond noise)
- FAIL · Evidence: `lr_schedule=cosine`: no evidence mentions 'cosine'; it fits, but nothing says the authors used it
- FAIL · Evidence: `epochs=150`: no evidence mentions '150'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.1875 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (11.42 noise units, gap +13.7%); `normalize=minmax` (7.44 noise units, gap -18.3%); `epochs=2` (2.98 noise units, gap -23.4%); `epochs=8` (1.49 noise units, gap -25.2%); `epochs=20` (1 noise units, gap -25.7%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `normalize=minmax`, `class_weight=balanced`: this claim +5.1%, mean |gap| 10.5% (5 runs)
  - `lr_schedule=cosine`, `epochs=20`: this claim -14.3%, mean |gap| 10.9% (5 runs)
  - `lr_schedule=cosine`: this claim -14.6%, mean |gap| 11.3% (6 runs)

### History matching (every measured configuration, all claims together)
- 8 of 49 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 8 configurations
  - `epochs, lr_schedule`: epochs=150, lr_schedule=step (max I 0.48); epochs=150, lr_schedule=cosine (max I 0.58); epochs=20, lr_schedule=cosine (max I 2.6)
  - `epochs, normalize`: epochs=150, normalize=minmax (max I 1.44)
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 2.64); class_weight=balanced, normalize=zscore (max I 2.85)
  - `lr_schedule`: lr_schedule=cosine (max I 2.65)
  - `class_weight, lr_schedule`: class_weight=balanced, lr_schedule=cosine (max I 2.89)
- 3 separate islands (no single-knob move joins them): epochs=150, lr_schedule=step; epochs=150, lr_schedule=cosine; epochs=20, lr_schedule=cosine | class_weight=balanced, normalize=minmax; class_weight=balanced, normalize=zscore | epochs=150, normalize=minmax

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'lr_schedule': 'step', 'epochs': '20'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=cosine`, `epochs=150` | 5 | -1.2% | +3.7% | 2.4% |
| `normalize=minmax`, `class_weight=balanced` | 5 | +5.1% | +15.8% | 10.5% |
| `lr_schedule=cosine`, `epochs=20` | 5 | -14.3% | -7.6% | 10.9% |
| `lr_schedule=cosine` | 6 | -14.6% | -7.9% | 11.3% |
| `normalize=zscore`, `class_weight=balanced` | 5 | +7.4% | +16.6% | 12.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`

## Provenance
- GapFinder commit: `b05f7288e1a4df8af69bb0b5e7633827b4cb46c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0464, sandbox reported $0.0000 (total $0.0464; this search; ledger extraction is included only if it shared the search's router)
