# Gap Report: test-v11-05

Artifact `mlbench` · generated 2026-10-15 21:03 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -26.3% | +4.6% | ±0.7% | `lr_schedule=step`, `epochs=750` |

## C1: test_accuracy (paper 0.7292)
**Fits but unsupported** · gap -26.3% → +4.6% · 57 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0102`, `B0122`, `B0157`, `B0158`, `B0159` (5 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `step`
- Config: `epochs` naive `15`, changed to `750`
- Command:

  Replay: fork checkpoint `e05b5a79-8522-4605-b317-0d753a34662e` and run
  ```
  RUN_TAG=8ae9b762fdfd "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize none --epochs 750 --batch_size 32 --lr 0.05 --lr_schedule step --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7375, 0.6625, 0.7625, 0.7833, 0.7625; gap after +4.6%; result checkpoint `71354909-d4ba-4ec5-a332-6bdaf29f09f4`
- Effect: candidate 0.7625 minus naive 0.5375 = +0.225, 95% bootstrap interval [+0.1375, +0.2767] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.729 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7292 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5375, 0.55, 0.5375, 0.475, 0.5375
- Spread: range 0.475 to 0.55, noise band ±0.005375 (2 x MAD), CV 5.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -26.3% (noise band ±0.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is -20.3% (it comes back)
- PASS · Counterfactual (reversal test): without `epochs` the gap is -34.9% (it comes back)
- PASS · Held-out claim: C2: -19.5% to +8.1% (not worse beyond noise)
- FAIL · Evidence: `lr_schedule=step`: no evidence mentions 'step'; it fits, but nothing says the authors used it
- FAIL · Evidence: `epochs=750`: no evidence mentions '750'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.225 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `os`, `evaluation_metric`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (17.84 noise units, gap +13.1%); `lr_schedule=cosine` (14.73 noise units, gap -15.4%); `normalize=minmax` (10.85 noise units, gap -18.3%); `epochs=30` (4.65 noise units, gap -22.9%); `epochs=150` (3.87 noise units, gap -23.4%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `epochs=150`, `lr_schedule=cosine`: this claim -1.2%, mean |gap| 2.4% (5 runs)
  - `epochs=75`, `lr_schedule=cosine`: this claim -8.6%, mean |gap| 5.5% (5 runs)
  - `epochs=150`, `normalize=minmax`: this claim +6.9%, mean |gap| 8.8% (5 runs)

### History matching (every measured configuration, all claims together)
- 17 of 57 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `epochs, lr_schedule`: epochs=150, lr_schedule=cosine (max I 0.59); epochs=750, lr_schedule=step (max I 0.89); epochs=75, lr_schedule=cosine (max I 1.45); epochs=750, lr_schedule=cosine (max I 2.23); +4 more
  - `epochs, normalize`: epochs=150, normalize=minmax (max I 1.79)
  - `lr_schedule`: lr_schedule=cosine (max I 2.56)
- 4 separate islands (no single-knob move joins them): epochs=150, lr_schedule=cosine; epochs=750, lr_schedule=step; epochs=75, lr_schedule=cosine | class_weight=balanced, normalize=minmax; class_weight=balanced, normalize=zscore | epochs=150, normalize=minmax | epochs=1, normalize=zscore

Notes:
- stopped early: run budget of 200 reached (wanted 3 more run(s) of {'epochs': '10', 'normalize': 'zscore'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `epochs=150`, `lr_schedule=cosine` | 5 | -1.2% | +3.7% | 2.4% |
| `epochs=75`, `lr_schedule=cosine` | 5 | -8.6% | -2.4% | 5.5% |
| `lr_schedule=step`, `epochs=750` | 5 | +4.6% | +8.1% | 6.3% |
| `epochs=150`, `normalize=minmax` | 5 | +6.9% | +10.7% | 8.8% |
| `lr_schedule=cosine`, `epochs=30` | 5 | -13.7% | -6.8% | 10.3% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `os`, `evaluation_metric`

## Provenance
- GapFinder commit: `cd8c8af2b9d079dd9a57443ed501c0dd8a467d34` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
