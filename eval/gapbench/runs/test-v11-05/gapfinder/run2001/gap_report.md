# Gap Report: test-v11-05

Artifact `mlbench` · generated 2026-10-15 21:02 · 199 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -32.0% | +4.0% | ±3.4% | `lr_schedule=step`, `epochs=750` |

## C1: test_accuracy (paper 0.7292)
**Fits but unsupported** · gap -32.0% → +4.0% · 53 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0092`, `B0123`, `B0161`, `B0162`, `B0163` (5 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `step`
- Config: `epochs` naive `15`, changed to `750`
- Command:

  Replay: fork checkpoint `1261402c-98eb-4265-9091-bfb0fc497ba1` and run
  ```
  RUN_TAG=e0dbca911547 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize none --epochs 750 --batch_size 32 --lr 0.05 --lr_schedule step --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7625, 0.775, 0.7583, 0.7208, 0.6625; gap after +4.0%; result checkpoint `ac6bdab5-ec3c-476a-accd-9b38661fff5b`
- Effect: candidate 0.7583 minus naive 0.4958 = +0.2625, 95% bootstrap interval [+0.1625, +0.275] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.729 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7292 (headline claim)

### What did we measure?
- Naive median 0.4958 over 5 runs; repeats: 0.4833, 0.4917, 0.4958, 0.5375, 0.5375
- Spread: range 0.4833 to 0.5375, noise band ±0.025 (2 x MAD), CV 5.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -32.0% (noise band ±3.4% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is -22.6% (it comes back)
- PASS · Counterfactual (reversal test): without `epochs` the gap is -26.3% (it comes back)
- PASS · Held-out claim: C2: -26.9% to +7.6% (not worse beyond noise)
- FAIL · Evidence: `lr_schedule=step`: no evidence mentions 'step'; it fits, but nothing says the authors used it
- FAIL · Evidence: `epochs=750`: no evidence mentions '750'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2625 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (5.34 noise units, gap +13.7%); `lr_schedule=cosine` (5.17 noise units, gap -14.3%); `normalize=minmax` (4 noise units, gap -18.3%); `epochs=150` (3.5 noise units, gap -20.0%); `class_weight=balanced` (2.17 noise units, gap -24.6%) (and 6 more in the JSON)
- Near alternatives (closest across all claims):
  - `epochs=150`, `lr_schedule=cosine`: this claim -2.3%, mean |gap| 2.5% (5 runs)
  - `epochs=150`, `normalize=minmax`: this claim +6.3%, mean |gap| 8.1% (5 runs)
  - `class_weight=balanced`, `normalize=minmax`: this claim +5.7%, mean |gap| 11.0% (5 runs)

### History matching (every measured configuration, all claims together)
- 9 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 9 configurations
  - `epochs, lr_schedule`: epochs=150, lr_schedule=cosine (max I 0.5); epochs=750, lr_schedule=step (max I 0.83); epochs=750, lr_schedule=cosine (max I 2.29); epochs=20, lr_schedule=cosine (max I 2.58); +1 more
  - `epochs, normalize`: epochs=150, normalize=minmax (max I 1.83)
  - `lr_schedule`: lr_schedule=cosine (max I 2.62)
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 2.75); class_weight=balanced, normalize=zscore (max I 2.9)
- 3 separate islands (no single-knob move joins them): epochs=150, lr_schedule=cosine; epochs=750, lr_schedule=step; epochs=750, lr_schedule=cosine | class_weight=balanced, normalize=minmax; class_weight=balanced, normalize=zscore | epochs=150, normalize=minmax

Notes:
- stopped early: run budget of 200 reached (wanted 3 more run(s) of {'normalize': 'zscore', 'lr_schedule': 'step'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `epochs=150`, `lr_schedule=cosine` | 5 | -2.3% | +2.6% | 2.5% |
| `lr_schedule=step`, `epochs=750` | 5 | +4.0% | +7.6% | 5.8% |
| `epochs=150`, `normalize=minmax` | 5 | +6.3% | +9.9% | 8.1% |
| `class_weight=balanced`, `normalize=minmax` | 5 | +5.7% | +16.3% | 11.0% |
| `lr_schedule=cosine`, `epochs=750` | 5 | +9.1% | +13.5% | 11.3% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`

## Provenance
- GapFinder commit: `cd8c8af2b9d079dd9a57443ed501c0dd8a467d34` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
