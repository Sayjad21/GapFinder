# Gap Report: test-v11-03

Artifact `mlbench` · generated 2026-10-16 01:22 · 176 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -31.4% | +0.0% | ±3.2% | `normalize=zscore`, `class_weight=balanced` |

## C1: test_accuracy (paper 0.7833)
**Fits but unsupported** · gap -31.4% → +0.0% · 51 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0138`, `B0152`, `B0168` (3 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Config: `class_weight` naive `none`, changed to `balanced`
- Command:

  Replay: fork checkpoint `ae3f85ad-2f43-4ae0-b1d9-8c7e6b35db13` and run
  ```
  RUN_TAG=8c433a6f11fe "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight balanced --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7875, 0.7833, 0.7833; gap after +0.0%; result checkpoint `5d6e92f1-9c41-4196-bc73-4e54f07ea395`
- Effect: candidate 0.7833 minus naive 0.5375 = +0.2458, 95% bootstrap interval [+0.2358, +0.2872] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.783 test accuracy and 0.752 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7833 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5375, 0.5375, 0.55, 0.5208, 0.4917
- Spread: range 0.4917 to 0.55, noise band ±0.025 (2 x MAD), CV 4.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -31.4% (noise band ±3.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -37.2% (it comes back)
- PASS · Counterfactual (reversal test): without `class_weight` the gap is +5.6% (it comes back)
- PASS · Held-out claim: C2: -28.0% to +4.4% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- FAIL · Evidence: `class_weight=balanced`: no evidence mentions 'balanced'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2458 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `NUM_RUNS`, `AGGREGATION_METHOD`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (3.67 noise units, gap -19.7%); `normalize=minmax` (2.33 noise units, gap -23.9%); `batch_size=1` (2 noise units, gap -25.0%); `batch_size=6` (2 noise units, gap -25.0%)
- Near alternatives (closest across all claims):
  - `normalize=zscore`, `label_noise=0.905`: this claim +0.0%, mean |gap| 0.8% (3 runs)
  - `class_weight=balanced`, `normalize=minmax`: this claim -2.1%, mean |gap| 3.1% (3 runs)
  - `normalize=zscore`, `label_noise=0.1`: this claim +3.7%, mean |gap| 4.5% (3 runs)

### Equally good configurations
The target claim can't tell these 4 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `class_weight=balanced, normalize=zscore` (reported)
- `label_noise=0.905, normalize=zscore`
- `batch_size=1, normalize=zscore`
- `class_weight=balanced, normalize=minmax`

### History matching (every measured configuration, all claims together)
- 13 of 50 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `label_noise, normalize`: label_noise=0.905, normalize=zscore (max I 0.3); label_noise=0.1, normalize=zscore (max I 0.95)
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 0.65); class_weight=balanced, normalize=zscore (max I 0.82)
  - `batch_size, normalize`: batch_size=1, normalize=zscore (max I 0.69); batch_size=1, normalize=minmax (max I 0.74); batch_size=6, normalize=zscore (max I 1.1)
  - `normalize`: normalize=zscore (max I 1.35)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.35); lr_schedule=step, normalize=zscore (max I 1.35)
- 2 separate islands (no single-knob move joins them): label_noise=0.905, normalize=zscore; class_weight=balanced, normalize=minmax; batch_size=1, normalize=zscore | batch_size=1, lr_schedule=cosine; batch_size=6, lr_schedule=cosine
- Equally good values: `normalize` in {minmax, zscore}

Notes:
- configurations the target claim can't tell apart from the answer: class_weight=balanced, normalize=zscore; label_noise=0.905, normalize=zscore; batch_size=1, normalize=zscore; class_weight=balanced, normalize=minmax
- equally good values within one noise band (measured): normalize in {minmax, zscore}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore`, `label_noise=0.905` | 3 | +0.0% | +1.5% | 0.8% |
| `normalize=zscore`, `class_weight=balanced` | 3 | +0.0% | +4.4% | 2.2% |
| `class_weight=balanced`, `normalize=minmax` | 3 | -2.1% | +4.1% | 3.1% |
| `normalize=zscore`, `label_noise=0.1` | 3 | +3.7% | +5.2% | 4.5% |
| `normalize=minmax`, `batch_size=1` | 3 | +3.7% | +6.2% | 4.9% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `NUM_RUNS`, `AGGREGATION_METHOD`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
