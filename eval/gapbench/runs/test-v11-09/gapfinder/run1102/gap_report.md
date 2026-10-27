# Gap Report: test-v11-09

Artifact `mlbench` · generated 2026-10-15 00:37 · 145 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -28.7% | +0.0% | ±0.7% | `normalize=minmax`, `lr=0.25` |

## C1: test_accuracy (paper 0.7542)
**Fits but unsupported** · gap -28.7% → +0.0% · 61 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0049`, `B0110`, `B0111` (3 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `lr` naive `0.05`, changed to `0.25`
- Command:

  Replay: fork checkpoint `1407c1c1-7b3d-40b8-888d-8e2123b0269c` and run
  ```
  RUN_TAG=e6efe2f1560e "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.25 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7083, 0.7542, 0.7833; gap after +0.0%; result checkpoint `02ed39e2-b2bd-43eb-8c11-6fb7bcca41aa`
- Effect: candidate 0.7542 minus naive 0.5375 = +0.2167, 95% bootstrap interval [+0.1575, +0.2475] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.754 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7542 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5375, 0.5375, 0.5292, 0.5375, 0.575
- Spread: range 0.5292 to 0.575, noise band ±0.005375 (2 x MAD), CV 3.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -28.7% (noise band ±0.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -29.3% (it comes back)
- PASS · Counterfactual (reversal test): without `lr` the gap is -21.0% (it comes back)
- PASS · Held-out claim: C2: -24.9% to -2.3% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- FAIL · Evidence: `lr=0.25`: no evidence mentions '0.25'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2167 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (27.14 noise units, gap +9.4%); `lr_schedule=cosine` (16.28 noise units, gap -17.1%)
- Near alternatives (closest across all claims):
  - `lr=0.5`, `normalize=minmax`: this claim +3.9%, mean |gap| 4.1% (3 runs)
  - `lr=0.0005`, `normalize=zscore`: this claim +3.9%, mean |gap| 4.4% (3 runs)
  - `class_weight=balanced`, `normalize=minmax`: this claim +1.7%, mean |gap| 4.8% (3 runs)

### Equally good configurations
The target claim can't tell these 5 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `lr=0.25, normalize=minmax` (reported)
- `class_weight=balanced, normalize=minmax`
- `lr=0.0005, normalize=zscore`
- `lr=2.5, normalize=zscore`
- `lr=0.5, normalize=minmax`

### History matching (every measured configuration, all claims together)
- 16 of 61 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr, normalize`: lr=0.25, normalize=minmax (max I 0.54); lr=0.0005, normalize=zscore (max I 0.91); lr=0.5, normalize=minmax (max I 1.05); lr=2.5, normalize=zscore (max I 1.36); +4 more
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 1.5); class_weight=balanced, normalize=zscore (max I 1.7)

Notes:
- configurations the target claim can't tell apart from the answer: lr=0.25, normalize=minmax; class_weight=balanced, normalize=minmax; lr=0.0005, normalize=zscore; lr=2.5, normalize=zscore; lr=0.5, normalize=minmax

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr=0.25`, `normalize=minmax` | 3 | +0.0% | -2.3% | 1.1% |
| `lr=0.5`, `normalize=minmax` | 3 | +3.9% | +4.3% | 4.1% |
| `lr=0.0005`, `normalize=zscore` | 3 | +3.9% | +5.0% | 4.4% |
| `class_weight=balanced`, `normalize=minmax` | 3 | +1.7% | +7.8% | 4.8% |
| `lr=2.5`, `normalize=zscore` | 3 | +4.4% | +8.0% | 6.2% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
