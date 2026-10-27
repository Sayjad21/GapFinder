# Gap Report: test-v11-08

Artifact `mlbench` · generated 2026-10-16 01:54 · 54 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -19.6% | +0.0% | ±4.2% | `normalize=minmax` |

## C1: test_accuracy (paper 0.5958)
**Fits but unsupported** · gap -19.6% → +0.0% · 13 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0007`, `B0016`, `B0017`, `B0018`, `B0019`, `B0020` (6 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Command:

  Replay: fork checkpoint `b3ecd769-6f89-425f-9fc7-348b57832d77` and run
  ```
  RUN_TAG=9a38832bd09b "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.5958, 0.5958, 0.5958, 0.5958, 0.5958, 0.5958; gap after +0.0%; result checkpoint `b3dac082-8ca4-4a4b-b2c2-50f88c008f4b`
- Effect: candidate 0.5958 minus naive 0.4792 = +0.1166, 95% bootstrap interval [+0.02832, +0.1258] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.596 test accuracy and 0.500 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.5958 (headline claim)

### What did we measure?
- Naive median 0.4792 over 5 runs; repeats: 0.4792, 0.5625, 0.475, 0.4667, 0.5708
- Spread: range 0.4667 to 0.5708, noise band ±0.025 (2 x MAD), CV 10.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -19.6% (noise band ±4.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -19.6% (it comes back)
- PASS · Held-out claim: C2: -5.3% to +0.0% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.1166 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (3.83 noise units, gap +3.5%); `lr_schedule=step` (2.5 noise units, gap -9.1%)
- Near alternatives (closest across all claims):
  - `normalize=minmax`, `lr_schedule=cosine`: this claim +0.0%, mean |gap| 0.0% (5 runs)
  - `normalize=minmax`, `lr_schedule=step`: this claim +0.0%, mean |gap| 0.0% (5 runs)
  - `lr_schedule=step`: this claim -9.8%, mean |gap| 9.1% (6 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `normalize=minmax` (reported)
- `lr_schedule=cosine, normalize=minmax`
- `lr_schedule=step, normalize=minmax`

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 8 configurations
  - `normalize`: normalize=minmax (max I 0)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=minmax (max I 0); lr_schedule=step, normalize=minmax (max I 0)
  - `lr_schedule`: lr_schedule=step (max I 1.56); lr_schedule=cosine (max I 2.74)
  - `class_weight`: class_weight=balanced (max I 2.02)
  - `class_weight, lr_schedule`: class_weight=balanced, lr_schedule=step (max I 2.11); class_weight=balanced, lr_schedule=cosine (max I 2.57)

Notes:
- configurations the target claim can't tell apart from the answer: normalize=minmax; lr_schedule=cosine, normalize=minmax; lr_schedule=step, normalize=minmax

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax` | 6 | +0.0% | +0.0% | 0.0% |
| `normalize=minmax`, `lr_schedule=cosine` | 5 | +0.0% | +0.0% | 0.0% |
| `normalize=minmax`, `lr_schedule=step` | 5 | +0.0% | +0.0% | 0.0% |
| `lr_schedule=step` | 6 | -9.8% | +8.4% | 9.1% |
| `class_weight=balanced`, `lr_schedule=step` | 5 | -17.5% | -2.2% | 9.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
