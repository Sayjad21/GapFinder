# Gap Report: dev-ml-normalize

Artifact `mlbench` · generated 2026-10-15 19:32 · 64 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -40.7% | +0.0% | ±4.0% | `normalize=zscore` |

## C1: test_accuracy (paper 0.8292)
**Fits but unsupported** · gap -40.7% → +0.0% · 14 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0006`, `B0011`, `B0012`, `B0021`, `B0022`, `B0023` (6 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Command:

  Replay: fork checkpoint `ed570e2d-13b8-4496-8647-2173c10638ca` and run
  ```
  RUN_TAG=52cc4e7b7971 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.825, 0.8292, 0.8292, 0.8292, 0.825, 0.8292; gap after +0.0%; result checkpoint `5b838e16-151d-4f51-972d-8d470bc7eba1`
- Effect: candidate 0.8292 minus naive 0.4917 = +0.3375, 95% bootstrap interval [+0.2859, +0.3492] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic credit-screening dataset and show it reaches 0.829 test accuracy, competitive with far larger models.

- p. 1; value used: `test_accuracy` = 0.8292 accuracy (headline claim)

### What did we measure?
- Naive median 0.4917 over 5 runs; repeats: 0.5375, 0.4875, 0.4917, 0.55, 0.475
- Spread: range 0.475 to 0.55, noise band ±0.0334 (2 x MAD), CV 6.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -40.7% (noise band ±4.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -40.7% (it comes back)
- PASS · Held-out claim: C2: -39.9% to +0.0% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.3375 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `median aggregation over runs`, `shuffling seed per run`, `SCALES`, `WEIGHTS`, `hardware`, `OS`, `Python version`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (3.87 noise units, gap -25.1%); `normalize=minmax` (3.12 noise units, gap -28.1%); `class_weight=balanced` (1.62 noise units, gap -34.2%); `lr_schedule=step` (1.5 noise units, gap -34.7%)
- Near alternatives (closest across all claims):
  - `normalize=zscore`, `lr_schedule=cosine`: this claim +0.0%, mean |gap| 0.0% (5 runs)
  - `normalize=zscore`, `lr_schedule=step`: this claim +0.0%, mean |gap| 0.0% (5 runs)
  - `normalize=zscore`, `class_weight=balanced`, `lr_schedule=cosine`: this claim -5.0%, mean |gap| 3.6% (5 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `normalize=zscore` (reported)
- `lr_schedule=cosine, normalize=zscore`
- `lr_schedule=step, normalize=zscore`

### History matching (every measured configuration, all claims together)
- 6 of 14 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 6 configurations
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 0); lr_schedule=step, normalize=zscore (max I 0)
  - `normalize`: normalize=zscore (max I 0.03)
  - `class_weight, lr_schedule, normalize`: class_weight=balanced, lr_schedule=cosine, normalize=zscore (max I 0.89)
  - `class_weight, normalize`: class_weight=balanced, normalize=zscore (max I 1); class_weight=balanced, normalize=minmax (max I 1.25)

Notes:
- configurations the target claim can't tell apart from the answer: normalize=zscore; lr_schedule=cosine, normalize=zscore; lr_schedule=step, normalize=zscore

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore` | 6 | +0.0% | +0.0% | 0.0% |
| `normalize=zscore`, `lr_schedule=cosine` | 5 | +0.0% | +0.0% | 0.0% |
| `normalize=zscore`, `lr_schedule=step` | 5 | +0.0% | +0.0% | 0.0% |
| `normalize=zscore`, `class_weight=balanced`, `lr_schedule=cosine` | 5 | -5.0% | -2.3% | 3.6% |
| `normalize=zscore`, `class_weight=balanced` | 5 | -5.5% | -3.1% | 4.3% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `median aggregation over runs`, `shuffling seed per run`, `SCALES`, `WEIGHTS`, `hardware`, `OS`, `Python version`, `--out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
