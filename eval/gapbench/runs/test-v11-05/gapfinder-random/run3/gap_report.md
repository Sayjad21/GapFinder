# Gap Report: test-v11-05

Artifact `mlbench` · generated 2026-10-14 12:38 · 121 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -26.3% | -1.2% | ±2.3% | `lr_schedule=cosine`, `epochs=150` |

## C1: test_accuracy (paper 0.7292)
**Fits but unsupported** · gap -26.3% → -1.2% · 49 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0046`, `B0104`, `B0105` (3 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `cosine`
- Config: `epochs` naive `15`, changed to `150`
- Command:

  Replay: fork checkpoint `c56e3b4b-9b9a-406b-84ee-f611979472fd` and run
  ```
  RUN_TAG=4a4ad1574d1c "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize none --epochs 150 --batch_size 32 --lr 0.05 --lr_schedule cosine --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.725, 0.7167, 0.7208; gap after -1.2%; result checkpoint `a696f880-7105-4a25-8aa1-c4accf647383`
- Effect: candidate 0.7208 minus naive 0.5375 = +0.1833, 95% bootstrap interval [+0.1739, +0.2203] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.729 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7292 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.4833, 0.5333, 0.5458, 0.5458, 0.5375
- Spread: range 0.4833 to 0.5458, noise band ±0.0166 (2 x MAD), CV 4.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -26.3% (noise band ±2.3% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is -30.9% (it comes back)
- PASS · Counterfactual (reversal test): without `epochs` the gap is -15.7% (it comes back)
- PASS · Held-out claim: C2: -19.5% to +3.7% (not worse beyond noise)
- FAIL · Evidence: `lr_schedule=cosine`: no evidence mentions 'cosine'; it fits, but nothing says the authors used it
- FAIL · Evidence: `epochs=150`: no evidence mentions '150'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.1833 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `os`, `evaluation_metric`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (5.52 noise units, gap +13.7%); `normalize=minmax` (3.51 noise units, gap -18.3%)
- Near alternatives (closest across all claims):
  - `normalize=minmax`, `epochs=150`: this claim +6.3%, mean |gap| 8.1% (3 runs)
  - `epochs=30`, `lr_schedule=cosine`: this claim -13.2%, mean |gap| 9.8% (3 runs)
  - `normalize=minmax`, `class_weight=balanced`: this claim +5.7%, mean |gap| 10.9% (3 runs)

### History matching (every measured configuration, all claims together)
- 8 of 49 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 8 configurations
  - `epochs, lr_schedule`: epochs=150, lr_schedule=cosine (max I 0.62); epochs=30, lr_schedule=cosine (max I 2.42); epochs=20, lr_schedule=cosine (max I 2.55); epochs=10, lr_schedule=cosine (max I 2.82)
  - `epochs, normalize`: epochs=150, normalize=minmax (max I 1.67)
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 2.7); class_weight=balanced, normalize=zscore (max I 2.75)
  - `lr_schedule`: lr_schedule=cosine (max I 2.84)
- 3 separate islands (no single-knob move joins them): epochs=150, lr_schedule=cosine; epochs=30, lr_schedule=cosine; epochs=20, lr_schedule=cosine | class_weight=balanced, normalize=minmax; class_weight=balanced, normalize=zscore | epochs=150, normalize=minmax

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=cosine`, `epochs=150` | 3 | -1.2% | +3.7% | 2.4% |
| `normalize=minmax`, `epochs=150` | 3 | +6.3% | +9.9% | 8.1% |
| `epochs=30`, `lr_schedule=cosine` | 3 | -13.2% | -6.5% | 9.8% |
| `normalize=minmax`, `class_weight=balanced` | 3 | +5.7% | +16.0% | 10.9% |
| `normalize=zscore`, `class_weight=balanced` | 3 | +7.4% | +16.6% | 12.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `os`, `evaluation_metric`

## Provenance
- GapFinder commit: `b05f7288e1a4df8af69bb0b5e7633827b4cb46c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
