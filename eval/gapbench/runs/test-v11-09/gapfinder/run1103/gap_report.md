# Gap Report: test-v11-09

Artifact `mlbench` · generated 2026-10-15 00:37 · 176 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -28.7% | +0.5% | ±1.1% | `normalize=minmax`, `class_weight=balanced` |

## C1: test_accuracy (paper 0.7542)
**Fits but unsupported** · gap -28.7% → +0.5% · 61 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0079`, `B0141`, `B0142` (3 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `class_weight` naive `none`, changed to `balanced`
- Command:

  Replay: fork checkpoint `0f05c16a-ca1c-46de-8d0d-18af12b68982` and run
  ```
  RUN_TAG=d979660f68cf "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight balanced --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7708, 0.75, 0.7583; gap after +0.5%; result checkpoint `809b2546-43cd-4c40-8c00-409cbd2709be`
- Effect: candidate 0.7583 minus naive 0.5375 = +0.2208, 95% bootstrap interval [+0.1825, +0.2358] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.754 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7542 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.575, 0.5625, 0.5333, 0.5333, 0.5375
- Spread: range 0.5333 to 0.575, noise band ±0.0084 (2 x MAD), CV 3.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -28.7% (noise band ±1.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -27.6% (it comes back)
- PASS · Counterfactual (reversal test): without `class_weight` the gap is -21.0% (it comes back)
- PASS · Held-out claim: C2: -24.9% to +7.4% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- FAIL · Evidence: `class_weight=balanced`: no evidence mentions 'balanced'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2208 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `aggregation`, `CPU`, `memory`, `OS`, `Python_version`, `random_module`, `floating_point`, `num_features`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (16.87 noise units, gap +9.9%); `lr_schedule=cosine` (8.93 noise units, gap -18.8%)
- Near alternatives (closest across all claims):
  - `lr=2.5`, `normalize=zscore`: this claim +0.5%, mean |gap| 0.6% (3 runs)
  - `normalize=minmax`, `lr=0.25`: this claim +1.7%, mean |gap| 1.1% (3 runs)
  - `normalize=minmax`, `lr=0.5`: this claim +4.4%, mean |gap| 5.1% (3 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `class_weight=balanced, normalize=minmax` (reported)
- `lr=2.5, normalize=zscore`
- `lr=0.25, normalize=minmax`

### History matching (every measured configuration, all claims together)
- 16 of 61 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr, normalize`: lr=0.25, normalize=minmax (max I 0.57); lr=0.5, normalize=minmax (max I 0.9); lr=2.5, normalize=zscore (max I 0.92); lr=0.0005, normalize=zscore (max I 1.42); +4 more
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 1.46); class_weight=balanced, normalize=zscore (max I 1.73)

Notes:
- configurations the target claim can't tell apart from the answer: class_weight=balanced, normalize=minmax; lr=2.5, normalize=zscore; lr=0.25, normalize=minmax

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr=2.5`, `normalize=zscore` | 3 | +0.5% | +0.7% | 0.6% |
| `normalize=minmax`, `lr=0.25` | 3 | +1.7% | +0.5% | 1.1% |
| `normalize=minmax`, `class_weight=balanced` | 3 | +0.5% | +7.4% | 4.0% |
| `normalize=minmax`, `lr=0.5` | 3 | +4.4% | +5.7% | 5.1% |
| `lr=0.0005`, `normalize=zscore` | 3 | +4.4% | +7.1% | 5.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `aggregation`, `CPU`, `memory`, `OS`, `Python_version`, `random_module`, `floating_point`, `num_features`, `--out`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
