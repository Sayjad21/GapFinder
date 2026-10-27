# Gap Report: test-v11-09

Artifact `mlbench` · generated 2026-10-15 21:05 · 161 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -27.6% | +1.7% | ±2.2% | `normalize=minmax`, `class_weight=balanced` |

## C1: test_accuracy (paper 0.7542)
**Fits but unsupported** · gap -27.6% → +1.7% · 61 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0078`, `B0113`, `B0146` (3 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `class_weight` naive `none`, changed to `balanced`
- Command:

  Replay: fork checkpoint `18b7b83b-63df-49a2-a69f-a339fd2c74d5` and run
  ```
  RUN_TAG=4bf64efd94ed "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight balanced --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7708, 0.7667, 0.7625; gap after +1.7%; result checkpoint `5942d3ca-e937-4364-b472-da4a88b0e993`
- Effect: candidate 0.7667 minus naive 0.5458 = +0.2209, 95% bootstrap interval [+0.2014, +0.2316] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.754 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7542 (headline claim)

### What did we measure?
- Naive median 0.5458 over 5 runs; repeats: 0.5625, 0.5458, 0.5375, 0.5375, 0.5625
- Spread: range 0.5375 to 0.5625, noise band ±0.0166 (2 x MAD), CV 2.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -27.6% (noise band ±2.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -32.3% (it comes back)
- PASS · Counterfactual (reversal test): without `class_weight` the gap is -21.0% (it comes back)
- PASS · Held-out claim: C2: -24.0% to +7.4% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- FAIL · Evidence: `class_weight=balanced`: no evidence mentions 'balanced'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2209 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `aggregation`, `CPU`, `memory`, `OS`, `Python_version`, `random_module`, `floating_point`, `num_features`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (8.04 noise units, gap +9.9%); `lr_schedule=cosine` (4.27 noise units, gap -18.2%); `lr=0.0` (1.26 noise units, gap -24.9%)
- Near alternatives (closest across all claims):
  - `normalize=zscore`, `lr=2.5`: this claim +1.7%, mean |gap| 1.9% (3 runs)
  - `lr=2.5`, `normalize=minmax`: this claim +4.4%, mean |gap| 3.9% (3 runs)
  - `normalize=zscore`, `class_weight=balanced`: this claim +3.9%, mean |gap| 6.3% (3 runs)

### Equally good configurations
The target claim can't tell these 5 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `class_weight=balanced, normalize=minmax` (reported)
- `lr=2.5, normalize=zscore`
- `lr=2.5, normalize=minmax`
- `lr=0.25, normalize=minmax`
- `lr=0.0005, normalize=zscore`

### History matching (every measured configuration, all claims together)
- 16 of 61 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr, normalize`: lr=2.5, normalize=zscore (max I 0.6); lr=2.5, normalize=minmax (max I 0.61); lr=0.0005, normalize=zscore (max I 1.35); lr=0.25, normalize=minmax (max I 1.43); +4 more
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 1.52); class_weight=balanced, normalize=zscore (max I 1.65)
- Equally good values: `normalize` in {minmax, zscore}

Notes:
- configurations the target claim can't tell apart from the answer: class_weight=balanced, normalize=minmax; lr=2.5, normalize=zscore; lr=2.5, normalize=minmax; lr=0.25, normalize=minmax; lr=0.0005, normalize=zscore
- equally good values within one noise band (measured): normalize in {minmax, zscore}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore`, `lr=2.5` | 3 | +1.7% | +2.1% | 1.9% |
| `lr=2.5`, `normalize=minmax` | 3 | +4.4% | +3.4% | 3.9% |
| `class_weight=balanced`, `normalize=minmax` | 3 | +1.7% | +7.4% | 4.6% |
| `normalize=zscore`, `class_weight=balanced` | 3 | +3.9% | +8.7% | 6.3% |
| `normalize=zscore`, `lr=0.0005` | 3 | +6.6% | +8.4% | 7.5% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `aggregation`, `CPU`, `memory`, `OS`, `Python_version`, `random_module`, `floating_point`, `num_features`, `--out`

## Provenance
- GapFinder commit: `cd8c8af2b9d079dd9a57443ed501c0dd8a467d34` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
