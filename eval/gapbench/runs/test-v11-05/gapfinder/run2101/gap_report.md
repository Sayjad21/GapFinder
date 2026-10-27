# Gap Report: test-v11-05

Artifact `mlbench` · generated 2026-10-15 21:02 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -36.0% | -1.2% | ±0.6% | `normalize=minmax`, `epochs=75` |

## C1: test_accuracy (paper 0.7292)
**Fits but unsupported** · gap -36.0% → -1.2% · 57 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0112`, `B0132`, `B0174`, `B0175`, `B0176` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `epochs` naive `15`, changed to `75`
- Command:

  Replay: fork checkpoint `1acf150d-a5fb-4cfb-b3af-6eeccdf29586` and run
  ```
  RUN_TAG=fd32f21294fc "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 75 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7167, 0.7208, 0.75, 0.7125, 0.7333; gap after -1.2%; result checkpoint `2308dba3-4a37-48ae-8323-ab2ac39593a7`
- Effect: candidate 0.7208 minus naive 0.4667 = +0.2541, 95% bootstrap interval [+0.1708, +0.2725] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.729 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7292 (headline claim)

### What did we measure?
- Naive median 0.4667 over 5 runs; repeats: 0.4667, 0.5625, 0.5375, 0.4667, 0.4667
- Spread: range 0.4667 to 0.5625, noise band ±0.004667 (2 x MAD), CV 9.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -36.0% (noise band ±0.6% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -25.4% (it comes back)
- PASS · Counterfactual (reversal test): without `epochs` the gap is -18.3% (it comes back)
- PASS · Held-out claim: C2: -31.5% to -1.5% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- FAIL · Evidence: `epochs=75`: no evidence mentions '75'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2541 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (36.6 noise units, gap -12.6%); `normalize=zscore` (34.82 noise units, gap +13.7%); `epochs=150` (24.98 noise units, gap -20.0%); `lr_schedule=step` (18.75 noise units, gap -24.0%); `epochs=3` (17.85 noise units, gap -24.6%) (and 6 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=cosine`, `epochs=150`: this claim -1.7%, mean |gap| 2.4% (5 runs)
  - `epochs=750`, `lr_schedule=step`: this claim +1.1%, mean |gap| 2.8% (5 runs)
  - `epochs=75`, `lr_schedule=cosine`: this claim -9.1%, mean |gap| 6.0% (5 runs)

### History matching (every measured configuration, all claims together)
- 30 of 57 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `epochs, normalize`: epochs=75, normalize=minmax (max I 0.07); epochs=150, normalize=minmax (max I 1.45)
  - `epochs, lr_schedule`: epochs=150, lr_schedule=cosine (max I 0.44); epochs=750, lr_schedule=step (max I 0.55); epochs=75, lr_schedule=cosine (max I 1.32); epochs=750, lr_schedule=cosine (max I 1.85); +2 more
  - `lr_schedule`: lr_schedule=cosine (max I 2.39)
  - `class_weight, normalize`: class_weight=balanced, normalize=zscore (max I 2.39)
- 2 separate islands (no single-knob move joins them): epochs=75, normalize=minmax; epochs=150, lr_schedule=cosine; epochs=750, lr_schedule=step | class_weight=balanced, epochs=750

Notes:
- stopped early: run budget of 200 reached (wanted 3 more run(s) of {'normalize': 'zscore', 'epochs': '150'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax`, `epochs=75` | 5 | -1.2% | -1.5% | 1.3% |
| `lr_schedule=cosine`, `epochs=150` | 5 | -1.7% | +3.1% | 2.4% |
| `epochs=750`, `lr_schedule=step` | 5 | +1.1% | +4.5% | 2.8% |
| `epochs=75`, `lr_schedule=cosine` | 5 | -9.1% | -2.9% | 6.0% |
| `normalize=minmax`, `epochs=150` | 5 | +6.3% | +9.9% | 8.1% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`

## Provenance
- GapFinder commit: `cd8c8af2b9d079dd9a57443ed501c0dd8a467d34` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
