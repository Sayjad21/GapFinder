# Gap Report: test-v11-05

Artifact `mlbench` · generated 2026-10-15 19:46 · 131 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -24.0% | -0.6% | ±3.4% | `normalize=minmax`, `epochs=75` |

## C1: test_accuracy (paper 0.7292)
**Fits but unsupported** · gap -24.0% → -0.6% · 61 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0056`, `B0076`, `B0109` (3 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `epochs` naive `15`, changed to `75`
- Command:

  Replay: fork checkpoint `fdd9f52b-7fed-4b61-a067-a5fbb91a7cd1` and run
  ```
  RUN_TAG=f64579277dcd "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 75 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7333, 0.725, 0.7167; gap after -0.6%; result checkpoint `67341752-9148-4d14-bace-7de3c3cd87ec`
- Effect: candidate 0.725 minus naive 0.5542 = +0.1708, 95% bootstrap interval [+0.1586, +0.1908] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.729 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7292 (headline claim)

### What did we measure?
- Naive median 0.5542 over 5 runs; repeats: 0.5333, 0.5417, 0.5542, 0.5667, 0.5583
- Spread: range 0.5333 to 0.5667, noise band ±0.025 (2 x MAD), CV 2.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -24.0% (noise band ±3.4% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -33.1% (it comes back)
- PASS · Counterfactual (reversal test): without `epochs` the gap is -18.3% (it comes back)
- PASS · Held-out claim: C2: -18.1% to -0.8% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- FAIL · Evidence: `epochs=75`: no evidence mentions '75'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.1708 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (3 noise units, gap +13.7%); `lr_schedule=cosine` (2.5 noise units, gap -15.4%)
- Near alternatives (closest across all claims):
  - `epochs=150`, `lr_schedule=cosine`: this claim -2.3%, mean |gap| 2.5% (3 runs)
  - `lr_schedule=step`, `epochs=750`: this claim +4.0%, mean |gap| 5.9% (3 runs)
  - `epochs=75`, `lr_schedule=cosine`: this claim -9.1%, mean |gap| 6.1% (3 runs)

### Equally good configurations
The target claim can't tell these 2 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `epochs=75, normalize=minmax` (reported)
- `epochs=750, lr_schedule=step`

### History matching (every measured configuration, all claims together)
- 11 of 61 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `epochs, normalize`: epochs=75, normalize=minmax (max I 0.14); epochs=150, normalize=minmax (max I 1.99)
  - `epochs, lr_schedule`: epochs=150, lr_schedule=cosine (max I 0.55); epochs=750, lr_schedule=step (max I 1.34); epochs=75, lr_schedule=cosine (max I 1.77); epochs=30, lr_schedule=cosine (max I 2.39); +3 more
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 2.94)
- 3 separate islands (no single-knob move joins them): epochs=150, lr_schedule=cosine; epochs=750, lr_schedule=step; epochs=75, lr_schedule=cosine | epochs=75, normalize=minmax; epochs=150, normalize=minmax | class_weight=balanced, normalize=minmax

Notes:
- configurations the target claim can't tell apart from the answer: epochs=75, normalize=minmax; epochs=750, lr_schedule=step

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax`, `epochs=75` | 3 | -0.6% | -0.8% | 0.7% |
| `epochs=150`, `lr_schedule=cosine` | 3 | -2.3% | +2.6% | 2.5% |
| `lr_schedule=step`, `epochs=750` | 3 | +4.0% | +7.8% | 5.9% |
| `epochs=75`, `lr_schedule=cosine` | 3 | -9.1% | -3.1% | 6.1% |
| `normalize=minmax`, `epochs=150` | 3 | +6.9% | +10.7% | 8.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
