# Gap Report: test-v11-05

Artifact `mlbench` · generated 2026-10-16 01:24 · 148 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -26.3% | +0.0% | ±0.7% | `epochs=75`, `normalize=minmax` |

## C1: test_accuracy (paper 0.7292)
**Fits but unsupported** · gap -26.3% → +0.0% · 53 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0062`, `B0097`, `B0130` (3 run(s) of the same config)
- Config: `epochs` naive `15`, changed to `75`
- Config: `normalize` naive `none`, changed to `minmax`
- Command:

  Replay: fork checkpoint `e9e0eb97-1bd1-418e-ae53-833c05f9bd08` and run
  ```
  RUN_TAG=dcd02223d5eb "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 75 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7333, 0.725, 0.7292; gap after +0.0%; result checkpoint `e719e7aa-dad9-4528-b455-fa1fb79a1f45`
- Effect: candidate 0.7292 minus naive 0.5375 = +0.1917, 95% bootstrap interval [+0.185, +0.1978] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.729 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7292 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5375, 0.5375, 0.5375, 0.5333, 0.5417
- Spread: range 0.5333 to 0.5417, noise band ±0.005375 (2 x MAD), CV 0.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -26.3% (noise band ±0.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `epochs` the gap is -18.3% (it comes back)
- PASS · Counterfactual (reversal test): without `normalize` the gap is -22.0% (it comes back)
- PASS · Held-out claim: C2: -19.5% to +0.0% (not worse beyond noise)
- FAIL · Evidence: `epochs=75`: no evidence mentions '75'; it fits, but nothing says the authors used it
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.1917 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `os`, `evaluation_metric`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (17.06 noise units, gap +13.7%); `lr_schedule=cosine` (17.06 noise units, gap -13.7%); `epochs=750` (8.52 noise units, gap -20.0%); `class_weight=balanced` (1.54 noise units, gap -25.2%); `epochs=3` (1.54 noise units, gap -25.2%)
- Near alternatives (closest across all claims):
  - `epochs=150`, `lr_schedule=cosine`: this claim -2.3%, mean |gap| 2.5% (3 runs)
  - `lr_schedule=step`, `epochs=750`: this claim +3.4%, mean |gap| 5.0% (3 runs)
  - `epochs=75`, `lr_schedule=cosine`: this claim -8.0%, mean |gap| 5.1% (3 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `epochs=75, normalize=minmax` (reported)
- `epochs=750, lr_schedule=step`
- `epochs=150, lr_schedule=cosine`

### History matching (every measured configuration, all claims together)
- 7 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 7 configurations
  - `epochs, normalize`: epochs=75, normalize=minmax (max I 0); epochs=150, normalize=minmax (max I 2.13)
  - `epochs, lr_schedule`: epochs=150, lr_schedule=cosine (max I 0.56); epochs=750, lr_schedule=step (max I 1.36); epochs=75, lr_schedule=cosine (max I 1.48); epochs=750, lr_schedule=cosine (max I 2.59); +1 more
- 2 separate islands (no single-knob move joins them): epochs=150, lr_schedule=cosine; epochs=750, lr_schedule=step; epochs=75, lr_schedule=cosine | epochs=75, normalize=minmax; epochs=150, normalize=minmax

Notes:
- configurations the target claim can't tell apart from the answer: epochs=75, normalize=minmax; epochs=750, lr_schedule=step; epochs=150, lr_schedule=cosine

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax`, `epochs=75` | 3 | +0.0% | +0.0% | 0.0% |
| `epochs=150`, `lr_schedule=cosine` | 3 | -2.3% | +2.6% | 2.5% |
| `lr_schedule=step`, `epochs=750` | 3 | +3.4% | +6.6% | 5.0% |
| `epochs=75`, `lr_schedule=cosine` | 3 | -8.0% | -2.1% | 5.1% |
| `normalize=minmax`, `epochs=150` | 3 | +6.3% | +9.9% | 8.1% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `os`, `evaluation_metric`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
