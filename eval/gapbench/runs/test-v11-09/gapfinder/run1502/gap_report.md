# Gap Report: test-v11-09

Artifact `mlbench` · generated 2026-10-15 19:24 · 128 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -27.6% | +3.9% | ±2.2% | `normalize=minmax`, `lr=2.5` |

## C1: test_accuracy (paper 0.7542)
**Fits but unsupported** · gap -27.6% → +3.9% · 61 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0045`, `B0085`, `B0114` (3 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `lr` naive `0.05`, changed to `2.5`
- Command:

  Replay: fork checkpoint `a3bf027d-c746-46f5-8117-46897ccfeac7` and run
  ```
  RUN_TAG=aa729972574a "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 2.5 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.8167, 0.7458, 0.7833; gap after +3.9%; result checkpoint `074b61a6-1493-47f3-bec1-a630bae73126`
- Effect: candidate 0.7833 minus naive 0.5458 = +0.2375, 95% bootstrap interval [+0.1992, +0.2842] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.754 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7542 (headline claim)

### What did we measure?
- Naive median 0.5458 over 5 runs; repeats: 0.5375, 0.5458, 0.5458, 0.5583, 0.5125
- Spread: range 0.5125 to 0.5583, noise band ±0.0166 (2 x MAD), CV 3.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -27.6% (noise band ±2.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -28.5% (it comes back)
- PASS · Counterfactual (reversal test): without `lr` the gap is -21.0% (it comes back)
- PASS · Held-out claim: C2: -24.4% to +9.6% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- FAIL · Evidence: `lr=2.5`: no evidence mentions '2.5'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2375 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (8.29 noise units, gap +9.4%); `lr_schedule=cosine` (4.77 noise units, gap -17.1%)
- Near alternatives (closest across all claims):
  - `lr=2.5`, `normalize=zscore`: this claim +3.9%, mean |gap| 4.1% (3 runs)
  - `lr=0.0005`, `normalize=zscore`: this claim +3.3%, mean |gap| 4.7% (3 runs)
  - `normalize=minmax`, `class_weight=balanced`: this claim +2.2%, mean |gap| 5.1% (3 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `lr=2.5, normalize=minmax` (reported)
- `lr=2.5, normalize=zscore`
- `class_weight=balanced, normalize=minmax`

### History matching (every measured configuration, all claims together)
- 15 of 61 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr, normalize`: lr=2.5, normalize=zscore (max I 0.67); lr=0.0005, normalize=zscore (max I 1.04); lr=2.5, normalize=minmax (max I 1.08); lr=0.001, normalize=zscore (max I 1.99); +3 more
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 1.52); class_weight=balanced, normalize=zscore (max I 1.69)
  - `normalize`: normalize=zscore (max I 2.2)
- Equally good values: `normalize` in {minmax, zscore}

Notes:
- configurations the target claim can't tell apart from the answer: lr=2.5, normalize=minmax; lr=2.5, normalize=zscore; class_weight=balanced, normalize=minmax
- equally good values within one noise band (measured): normalize in {minmax, zscore}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr=2.5`, `normalize=zscore` | 3 | +3.9% | +4.3% | 4.1% |
| `lr=0.0005`, `normalize=zscore` | 3 | +3.3% | +6.1% | 4.7% |
| `normalize=minmax`, `class_weight=balanced` | 3 | +2.2% | +7.9% | 5.1% |
| `lr=2.5`, `normalize=minmax` | 3 | +3.9% | +9.6% | 6.7% |
| `normalize=zscore`, `class_weight=balanced` | 3 | +4.4% | +9.2% | 6.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
