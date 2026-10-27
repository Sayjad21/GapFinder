# Gap Report: test-v11-05

Artifact `mlbench` · generated 2026-10-15 18:58 · 138 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -25.2% | -0.6% | ±1.2% | `lr_schedule=step`, `epochs=750` |

## C1: test_accuracy (paper 0.7292)
**Fits but unsupported** · gap -25.2% → -0.6% · 53 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0088`, `B0097`, `B0128` (3 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `step`
- Config: `epochs` naive `15`, changed to `750`
- Command:

  Replay: fork checkpoint `87ad20e4-4ecf-4c83-b555-17baaf2b6aed` and run
  ```
  RUN_TAG=baa27b13839c "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize none --epochs 750 --batch_size 32 --lr 0.05 --lr_schedule step --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.725, 0.6292, 0.7875; gap after -0.6%; result checkpoint `3dc4945b-77a4-47fe-9f97-f952175ad616`
- Effect: candidate 0.725 minus naive 0.5458 = +0.1792, 95% bootstrap interval [+0.08172, +0.2709] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.729 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7292 (headline claim)

### What did we measure?
- Naive median 0.5458 over 5 runs; repeats: 0.5375, 0.5458, 0.55, 0.4958, 0.5458
- Spread: range 0.4958 to 0.55, noise band ±0.0084 (2 x MAD), CV 4.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -25.2% (noise band ±1.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is -28.0% (it comes back)
- PASS · Counterfactual (reversal test): without `epochs` the gap is -21.1% (it comes back)
- PASS · Held-out claim: C2: -19.5% to +2.4% (not worse beyond noise)
- FAIL · Evidence: `lr_schedule=step`: no evidence mentions 'step'; it fits, but nothing says the authors used it
- FAIL · Evidence: `epochs=750`: no evidence mentions '750'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.1792 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `os`, `evaluation_metric`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (10.43 noise units, gap +13.1%); `lr_schedule=cosine` (9.93 noise units, gap -13.7%); `normalize=minmax` (5.95 noise units, gap -18.3%)
- Near alternatives (closest across all claims):
  - `lr_schedule=cosine`, `epochs=150`: this claim -1.7%, mean |gap| 2.4% (3 runs)
  - `normalize=minmax`, `epochs=150`: this claim +5.7%, mean |gap| 7.4% (3 runs)
  - `lr_schedule=cosine`: this claim -13.7%, mean |gap| 10.4% (3 runs)

### Equally good configurations
The target claim can't tell these 2 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `epochs=750, lr_schedule=step` (reported)
- `epochs=150, lr_schedule=cosine`

### History matching (every measured configuration, all claims together)
- 8 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 8 configurations
  - `epochs, lr_schedule`: epochs=750, lr_schedule=step (max I 0.38); epochs=150, lr_schedule=cosine (max I 0.52); epochs=750, lr_schedule=cosine (max I 2.29); epochs=20, lr_schedule=cosine (max I 2.48)
  - `epochs, normalize`: epochs=150, normalize=minmax (max I 1.63)
  - `lr_schedule`: lr_schedule=cosine (max I 2.46)
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 2.78); class_weight=balanced, normalize=zscore (max I 2.96)
- 3 separate islands (no single-knob move joins them): epochs=750, lr_schedule=step; epochs=150, lr_schedule=cosine; epochs=750, lr_schedule=cosine | class_weight=balanced, normalize=minmax; class_weight=balanced, normalize=zscore | epochs=150, normalize=minmax

Notes:
- configurations the target claim can't tell apart from the answer: epochs=750, lr_schedule=step; epochs=150, lr_schedule=cosine

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `epochs=750`, `lr_schedule=step` | 3 | -0.6% | +2.4% | 1.5% |
| `lr_schedule=cosine`, `epochs=150` | 3 | -1.7% | +3.1% | 2.4% |
| `normalize=minmax`, `epochs=150` | 3 | +5.7% | +9.1% | 7.4% |
| `lr_schedule=cosine` | 3 | -13.7% | -7.1% | 10.4% |
| `lr_schedule=cosine`, `epochs=20` | 2 | -14.0% | -6.9% | 10.5% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `os`, `evaluation_metric`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
