# Gap Report: test-v11-09

Artifact `mlbench` · generated 2026-10-15 19:48 · 164 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -29.3% | -0.6% | ±6.6% | `normalize=minmax`, `lr=2.5` |

## C1: test_accuracy (paper 0.7542)
**Fits but unsupported** · gap -29.3% → -0.6% · 61 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0053`, `B0086`, `B0133`, `B0134`, `B0135` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `lr` naive `0.05`, changed to `2.5`
- Command:

  Replay: fork checkpoint `199a16f2-0b9d-49ae-a003-8d807cd20921` and run
  ```
  RUN_TAG=de0d590e2ef8 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 2.5 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.8125, 0.825, 0.65, 0.75, 0.7167; gap after -0.6%; result checkpoint `99e51eb3-bd9a-4fc8-98d7-e9f3c63cd79a`
- Effect: candidate 0.75 minus naive 0.5333 = +0.2167, 95% bootstrap interval [+0.16, +0.3067] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.754 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7542 (headline claim)

### What did we measure?
- Naive median 0.5333 over 5 runs; repeats: 0.4667, 0.5375, 0.5583, 0.4875, 0.5333
- Spread: range 0.4667 to 0.5583, noise band ±0.05 (2 x MAD), CV 7.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -29.3% (noise band ±6.6% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -35.4% (it comes back)
- PASS · Counterfactual (reversal test): without `lr` the gap is -21.0% (it comes back)
- PASS · Held-out claim: C2: -25.4% to +3.9% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- FAIL · Evidence: `lr=2.5`: no evidence mentions '2.5'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2167 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (2.92 noise units, gap +9.9%); `lr_schedule=cosine` (1.75 noise units, gap -17.7%)
- Near alternatives (closest across all claims):
  - `lr=0.0005`, `normalize=zscore`: this claim -0.6%, mean |gap| 0.3% (5 runs)
  - `lr=0.5`, `normalize=minmax`: this claim +3.3%, mean |gap| 3.0% (5 runs)
  - `lr=2.5`, `normalize=zscore`: this claim +4.4%, mean |gap| 5.5% (5 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `lr=2.5, normalize=minmax` (reported)
- `lr=0.0005, normalize=zscore`
- `lr=2.5, normalize=zscore`

### History matching (every measured configuration, all claims together)
- 23 of 61 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr, normalize`: lr=2.5, normalize=minmax (max I 0.08); lr=0.0005, normalize=zscore (max I 0.28); lr=0.5, normalize=minmax (max I 0.59); lr=2.5, normalize=zscore (max I 0.81); +4 more
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 1.4); class_weight=balanced, normalize=zscore (max I 1.44)
- Equally good values: `normalize` in {minmax, zscore}; `lr` in {0.5, 2.5}

Notes:
- configurations the target claim can't tell apart from the answer: lr=2.5, normalize=minmax; lr=0.0005, normalize=zscore; lr=2.5, normalize=zscore
- equally good values within one noise band (measured): normalize in {minmax, zscore}; lr in {0.5, 2.5}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr=0.0005`, `normalize=zscore` | 5 | -0.6% | -0.0% | 0.3% |
| `lr=2.5`, `normalize=minmax` | 5 | -0.6% | +3.9% | 2.2% |
| `lr=0.5`, `normalize=minmax` | 5 | +3.3% | +2.7% | 3.0% |
| `lr=2.5`, `normalize=zscore` | 5 | +4.4% | +6.7% | 5.5% |
| `class_weight=balanced`, `normalize=minmax` | 5 | +3.3% | +8.5% | 5.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
