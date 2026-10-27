# Gap Report: test-v11-05

Artifact `mlbench` · generated 2026-10-16 01:54 · 148 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -33.1% | -1.2% | ±0.7% | `epochs=750`, `lr_schedule=step` |

## C1: test_accuracy (paper 0.7292)
**Fits but unsupported** · gap -33.1% → -1.2% · 57 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0082`, `B0091`, `B0129` (3 run(s) of the same config)
- Config: `epochs` naive `15`, changed to `750`
- Config: `lr_schedule` naive `const`, changed to `step`
- Command:

  Replay: fork checkpoint `3364c58d-0b29-4837-bc2a-eff7b21d6b53` and run
  ```
  RUN_TAG=12f0bc8589df "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize none --epochs 750 --batch_size 32 --lr 0.05 --lr_schedule step --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7208, 0.7833, 0.7125; gap after -1.2%; result checkpoint `e2fef5e3-fb6d-4c58-bae6-b3fa8b01b997`
- Effect: candidate 0.7208 minus naive 0.4875 = +0.2333, 95% bootstrap interval [+0.1967, +0.3008] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.729 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7292 (headline claim)

### What did we measure?
- Naive median 0.4875 over 5 runs; repeats: 0.5333, 0.4875, 0.475, 0.4875, 0.4875
- Spread: range 0.475 to 0.5333, noise band ±0.004875 (2 x MAD), CV 4.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -33.1% (noise band ±0.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `epochs` the gap is -34.3% (it comes back)
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is -24.3% (it comes back)
- PASS · Held-out claim: C2: -28.1% to +3.1% (not worse beyond noise)
- FAIL · Evidence: `epochs=750`: no evidence mentions '750'; it fits, but nothing says the authors used it
- FAIL · Evidence: `lr_schedule=step`: no evidence mentions 'step'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2333 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `epochs=150` (31.63 noise units, gap -12.0%); `normalize=zscore` (29.07 noise units, gap +13.7%); `lr_schedule=cosine` (28.21 noise units, gap -14.3%); `normalize=minmax` (22.22 noise units, gap -18.3%); `epochs=20` (18.81 noise units, gap -20.6%) (and 4 more in the JSON)
- Near alternatives (closest across all claims):
  - `epochs=150`, `lr_schedule=cosine`: this claim -1.2%, mean |gap| 2.4% (3 runs)
  - `normalize=minmax`, `epochs=150`: this claim +6.3%, mean |gap| 8.1% (3 runs)
  - `lr_schedule=cosine`, `epochs=30`: this claim -13.2%, mean |gap| 9.7% (3 runs)

### Equally good configurations
The target claim can't tell these 2 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `epochs=750, lr_schedule=step` (reported)
- `epochs=150, lr_schedule=cosine`

### History matching (every measured configuration, all claims together)
- 10 of 57 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `epochs, lr_schedule`: epochs=150, lr_schedule=cosine (max I 0.66); epochs=750, lr_schedule=step (max I 0.89); epochs=750, lr_schedule=cosine (max I 2.23); epochs=30, lr_schedule=cosine (max I 2.42); +2 more
  - `epochs, normalize`: epochs=150, normalize=minmax (max I 1.72)
  - `lr_schedule`: lr_schedule=cosine (max I 2.73)
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 2.81); class_weight=balanced, normalize=zscore (max I 2.91)
- 3 separate islands (no single-knob move joins them): epochs=150, lr_schedule=cosine; epochs=750, lr_schedule=step; epochs=750, lr_schedule=cosine | class_weight=balanced, normalize=minmax; class_weight=balanced, normalize=zscore | epochs=150, normalize=minmax

Notes:
- configurations the target claim can't tell apart from the answer: epochs=750, lr_schedule=step; epochs=150, lr_schedule=cosine

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `epochs=750`, `lr_schedule=step` | 3 | -1.2% | +3.1% | 2.2% |
| `epochs=150`, `lr_schedule=cosine` | 3 | -1.2% | +3.7% | 2.4% |
| `normalize=minmax`, `epochs=150` | 3 | +6.3% | +9.9% | 8.1% |
| `lr_schedule=cosine`, `epochs=30` | 3 | -13.2% | -6.3% | 9.7% |
| `epochs=750`, `lr_schedule=cosine` | 3 | +8.6% | +12.7% | 10.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
