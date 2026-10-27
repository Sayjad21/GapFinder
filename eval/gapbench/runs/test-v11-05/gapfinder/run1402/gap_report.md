# Gap Report: test-v11-05

Artifact `mlbench` · generated 2026-10-15 18:58 · 189 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -26.9% | +0.0% | ±3.4% | `epochs=75`, `normalize=minmax` |

## C1: test_accuracy (paper 0.7292)
**Fits but unsupported** · gap -26.9% → +0.0% · 61 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0073`, `B0092`, `B0129`, `B0130`, `B0131` (5 run(s) of the same config)
- Config: `epochs` naive `15`, changed to `75`
- Config: `normalize` naive `none`, changed to `minmax`
- Command:

  Replay: fork checkpoint `d55023d4-dc71-49ad-9013-bdc79363168c` and run
  ```
  RUN_TAG=c361ae2ca64c "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 75 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7333, 0.7458, 0.7292, 0.7292, 0.7083; gap after +0.0%; result checkpoint `40869016-f5f7-44df-914c-4ae493e90f1a`
- Effect: candidate 0.7292 minus naive 0.5333 = +0.1959, 95% bootstrap interval [+0.1759, +0.2525] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.729 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7292 (headline claim)

### What did we measure?
- Naive median 0.5333 over 5 runs; repeats: 0.4667, 0.5458, 0.4875, 0.5333, 0.5458
- Spread: range 0.4667 to 0.5458, noise band ±0.025 (2 x MAD), CV 7.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -26.9% (noise band ±3.4% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `epochs` the gap is -18.3% (it comes back)
- PASS · Counterfactual (reversal test): without `normalize` the gap is -30.9% (it comes back)
- PASS · Held-out claim: C2: -20.0% to +0.0% (not worse beyond noise)
- FAIL · Evidence: `epochs=75`: no evidence mentions '75'; it fits, but nothing says the authors used it
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.1959 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `epochs=750` (7.17 noise units, gap +2.3%); `normalize=zscore` (4 noise units, gap +13.1%); `lr_schedule=step` (3 noise units, gap -16.6%); `lr_schedule=cosine` (3 noise units, gap -16.6%)
- Near alternatives (closest across all claims):
  - `epochs=150`, `lr_schedule=cosine`: this claim -1.7%, mean |gap| 2.4% (5 runs)
  - `lr_schedule=cosine`, `epochs=75`: this claim -8.6%, mean |gap| 5.5% (5 runs)
  - `lr_schedule=step`, `epochs=750`: this claim +4.0%, mean |gap| 5.8% (5 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `epochs=75, normalize=minmax` (reported)
- `epochs=150, lr_schedule=cosine`
- `epochs=750, lr_schedule=step`

### History matching (every measured configuration, all claims together)
- 17 of 61 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `epochs, normalize`: epochs=75, normalize=minmax (max I 0)
  - `epochs, lr_schedule`: epochs=150, lr_schedule=cosine (max I 0.48); epochs=750, lr_schedule=step (max I 1.22); epochs=75, lr_schedule=cosine (max I 1.36); epochs=750, lr_schedule=cosine (max I 2.08); +2 more
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 2.45); class_weight=balanced, normalize=zscore (max I 2.65)
  - `class_weight, lr_schedule`: class_weight=balanced, lr_schedule=cosine (max I 2.53)
- 4 separate islands (no single-knob move joins them): epochs=150, lr_schedule=cosine; epochs=750, lr_schedule=step; epochs=75, lr_schedule=cosine | epochs=8, normalize=zscore; epochs=10, normalize=zscore; epochs=3, normalize=zscore | class_weight=balanced, normalize=minmax; class_weight=balanced, normalize=zscore | epochs=75, normalize=minmax

Notes:
- configurations the target claim can't tell apart from the answer: epochs=75, normalize=minmax; epochs=150, lr_schedule=cosine; epochs=750, lr_schedule=step

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `epochs=75`, `normalize=minmax` | 5 | +0.0% | +0.0% | 0.0% |
| `epochs=150`, `lr_schedule=cosine` | 5 | -1.7% | +3.1% | 2.4% |
| `lr_schedule=cosine`, `epochs=75` | 5 | -8.6% | -2.4% | 5.5% |
| `lr_schedule=step`, `epochs=750` | 5 | +4.0% | +7.6% | 5.8% |
| `epochs=20`, `lr_schedule=cosine` | 5 | -13.7% | -6.8% | 10.3% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
