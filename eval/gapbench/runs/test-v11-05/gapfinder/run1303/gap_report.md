# Gap Report: test-v11-05

Artifact `mlbench` · generated 2026-10-15 01:15 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -33.1% | +0.0% | ±5.7% | `epochs=75`, `normalize=minmax` |

## C1: test_accuracy (paper 0.7292)
**Fits but unsupported** · gap -33.1% → +0.0% · 53 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0089`, `B0163`, `B0164`, `B0165`, `B0166` (5 run(s) of the same config)
- Config: `epochs` naive `15`, changed to `75`
- Config: `normalize` naive `none`, changed to `minmax`
- Command:

  Replay: fork checkpoint `da8d6b70-ab64-4faf-8cc6-1fad1b7b6838` and run
  ```
  RUN_TAG=5ede13a58a57 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 75 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7333, 0.75, 0.7292, 0.7292, 0.7167; gap after +0.0%; result checkpoint `9cddb5fc-30c2-4fc7-8b65-8ff9dced8579`
- Effect: candidate 0.7292 minus naive 0.4875 = +0.2417, 95% bootstrap interval [+0.175, +0.2625] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.729 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7292 (headline claim)

### What did we measure?
- Naive median 0.4875 over 5 runs; repeats: 0.4667, 0.4875, 0.5625, 0.5375, 0.4875
- Spread: range 0.4667 to 0.5625, noise band ±0.0416 (2 x MAD), CV 7.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -33.1% (noise band ±5.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `epochs` the gap is -18.3% (it comes back)
- PASS · Counterfactual (reversal test): without `normalize` the gap is -26.3% (it comes back)
- PASS · Held-out claim: C2: -28.1% to +0.0% (not worse beyond noise)
- FAIL · Evidence: `epochs=75`: no evidence mentions '75'; it fits, but nothing says the authors used it
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2417 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `os`, `evaluation_metric`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (3.51 noise units, gap +13.1%); `lr_schedule=cosine` (3.11 noise units, gap -15.4%); `epochs=750` (1.5 noise units, gap -24.6%); `epochs=150` (1.3 noise units, gap -25.7%); `epochs=20` (1.2 noise units, gap -26.3%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=cosine`, `epochs=150`: this claim -1.7%, mean |gap| 2.4% (5 runs)
  - `lr_schedule=cosine`, `epochs=75`: this claim -8.0%, mean |gap| 4.9% (5 runs)
  - `epochs=150`, `normalize=minmax`: this claim +6.3%, mean |gap| 7.8% (5 runs)

### History matching (every measured configuration, all claims together)
- 22 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `epochs, normalize`: epochs=75, normalize=minmax (max I 0.07); epochs=150, normalize=minmax (max I 1.47)
  - `epochs, lr_schedule`: epochs=150, lr_schedule=cosine (max I 0.49); epochs=750, lr_schedule=step (max I 0.73); epochs=75, lr_schedule=step (max I 1.16); epochs=75, lr_schedule=cosine (max I 1.29); +1 more
  - `class_weight, epochs`: class_weight=balanced, epochs=150 (max I 1.75)
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 1.98)
  - `class_weight, lr_schedule`: class_weight=balanced, lr_schedule=cosine (max I 2.26)
- 4 separate islands (no single-knob move joins them): epochs=150, lr_schedule=cosine; epochs=750, lr_schedule=step; epochs=75, lr_schedule=step | epochs=75, normalize=minmax; epochs=150, normalize=minmax; class_weight=balanced, normalize=minmax | class_weight=balanced, epochs=150; class_weight=balanced, epochs=750 | lr_schedule=step, normalize=minmax

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'lr_schedule': 'cosine', 'class_weight': 'balanced'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `epochs=75`, `normalize=minmax` | 5 | +0.0% | +0.0% | 0.0% |
| `lr_schedule=cosine`, `epochs=150` | 5 | -1.7% | +3.1% | 2.4% |
| `lr_schedule=cosine`, `epochs=75` | 5 | -8.0% | -1.8% | 4.9% |
| `epochs=150`, `normalize=minmax` | 5 | +6.3% | +9.4% | 7.8% |
| `lr_schedule=cosine`, `epochs=750` | 5 | +8.6% | +12.7% | 10.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `os`, `evaluation_metric`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
