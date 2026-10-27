# Gap Report: test-v11-05

Artifact `mlbench` · generated 2026-10-15 19:47 · 144 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -26.3% | +1.1% | ±0.7% | `normalize=minmax`, `epochs=75` |

## C1: test_accuracy (paper 0.7292)
**Fits but unsupported** · gap -26.3% → +1.1% · 53 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0076`, `B0101`, `B0129` (3 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `epochs` naive `15`, changed to `75`
- Command:

  Replay: fork checkpoint `0a1aeef7-264f-448c-98f9-fe75f00573d1` and run
  ```
  RUN_TAG=a572f724da38 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 75 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7167, 0.7417, 0.7375; gap after +1.1%; result checkpoint `1ca5f6dd-ccd3-482e-9332-b6a9a503c533`
- Effect: candidate 0.7375 minus naive 0.5375 = +0.2, 95% bootstrap interval [+0.1759, +0.2414] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.729 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7292 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5375, 0.5458, 0.4875, 0.5375, 0.5375
- Spread: range 0.4875 to 0.5458, noise band ±0.005375 (2 x MAD), CV 4.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -26.3% (noise band ±0.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -27.7% (it comes back)
- PASS · Counterfactual (reversal test): without `epochs` the gap is -18.3% (it comes back)
- PASS · Held-out claim: C2: -19.5% to +1.5% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- FAIL · Evidence: `epochs=75`: no evidence mentions '75'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `os`, `evaluation_metric`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (17.84 noise units, gap +13.1%); `lr_schedule=cosine` (14.73 noise units, gap -15.4%); `lr_schedule=step` (8.52 noise units, gap -20.0%); `epochs=750` (6.2 noise units, gap -21.7%); `epochs=3` (3.87 noise units, gap -23.4%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=step`, `epochs=750`: this claim -1.2%, mean |gap| 1.7% (3 runs)
  - `epochs=150`, `lr_schedule=cosine`: this claim -1.7%, mean |gap| 2.5% (3 runs)
  - `epochs=75`, `lr_schedule=cosine`: this claim -7.4%, mean |gap| 4.4% (3 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `epochs=75, normalize=minmax` (reported)
- `epochs=150, lr_schedule=cosine`
- `epochs=750, lr_schedule=step`

### History matching (every measured configuration, all claims together)
- 12 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `epochs, normalize`: epochs=75, normalize=minmax (max I 0.09); epochs=150, normalize=minmax (max I 1.88)
  - `epochs, lr_schedule`: epochs=150, lr_schedule=cosine (max I 0.58); epochs=750, lr_schedule=step (max I 0.69); epochs=75, lr_schedule=cosine (max I 1.44); epochs=750, lr_schedule=cosine (max I 2.24); +2 more
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 2.51)
  - `lr_schedule`: lr_schedule=cosine (max I 2.81)
- 3 separate islands (no single-knob move joins them): epochs=150, lr_schedule=cosine; epochs=750, lr_schedule=step; epochs=75, lr_schedule=cosine | epochs=75, normalize=minmax; epochs=150, normalize=minmax | class_weight=balanced, normalize=minmax; class_weight=balanced, normalize=zscore

Notes:
- configurations the target claim can't tell apart from the answer: epochs=75, normalize=minmax; epochs=150, lr_schedule=cosine; epochs=750, lr_schedule=step

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax`, `epochs=75` | 3 | +1.1% | +1.5% | 1.3% |
| `lr_schedule=step`, `epochs=750` | 3 | -1.2% | +2.2% | 1.7% |
| `epochs=150`, `lr_schedule=cosine` | 3 | -1.7% | +3.4% | 2.5% |
| `epochs=75`, `lr_schedule=cosine` | 3 | -7.4% | -1.3% | 4.4% |
| `epochs=150`, `normalize=minmax` | 3 | +6.9% | +10.7% | 8.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `os`, `evaluation_metric`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
