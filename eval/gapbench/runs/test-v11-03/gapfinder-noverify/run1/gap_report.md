# Gap Report: test-v11-03

Artifact `mlbench` · generated 2026-10-14 11:11 · 190 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Explained | -31.9% | +0.0% | ±2.1% | `normalize=minmax`, `positive_rate=0.1` |

## C1: test_accuracy (paper 0.7833)
**Explained** · gap -31.9% → +0.0% · 65 hypotheses tested
> Interacting factors: these changes close the gap only together, and every check passes

### Which experiment changed it?
- Branch: `B0111`, `B0167`, `B0168` (3 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `positive_rate` naive `0.3`, changed to `0.1`
- Command:

  Replay: fork checkpoint `fa87e8d5-6799-4949-9ed6-36ae8f95fdf5` and run
  ```
  RUN_TAG=6fd2a2a58e21 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.1 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7833, 0.7833, 0.7833; gap after +0.0%; result checkpoint `6ea02e41-1cf1-405c-9754-cef0e0f9d638`
- Effect: candidate 0.7833 minus naive 0.5333 = +0.25, 95% bootstrap interval [+0.2433, +0.2875] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.783 test accuracy and 0.752 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7833 (headline claim)

### What did we measure?
- Naive median 0.5333 over 5 runs; repeats: 0.4875, 0.5417, 0.5083, 0.5333, 0.5333
- Spread: range 0.4875 to 0.5417, noise band ±0.0168 (2 x MAD), CV 4.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -31.9% (noise band ±2.1% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is +0.25 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `NUM_RUNS`, `AGGREGATION_METHOD`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (12.4 noise units, gap +5.3%); `lr_schedule=cosine` (5.46 noise units, gap -20.2%); `batch_size=1` (2.48 noise units, gap -26.6%); `class_weight=balanced` (1.74 noise units, gap -28.2%)
- Near alternatives (closest across all claims):
  - `label_noise=0.905`, `normalize=zscore`: this claim +0.0%, mean |gap| 0.8% (3 runs)
  - `batch_size=3`, `normalize=minmax`: this claim +0.5%, mean |gap| 1.0% (3 runs)
  - `normalize=zscore`, `batch_size=1`: this claim +0.5%, mean |gap| 1.4% (3 runs)

### History matching (every measured configuration, all claims together)
- 13 of 64 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `batch_size, normalize`: batch_size=3, normalize=minmax (max I 0.17); batch_size=1, normalize=zscore (max I 0.34); batch_size=1, normalize=minmax (max I 0.93); batch_size=3, normalize=zscore (max I 1.04)
  - `label_noise, normalize`: label_noise=0.905, normalize=zscore (max I 0.27); label_noise=0.0, normalize=zscore (max I 1.4)
  - `batch_size, class_weight, lr_schedule, normalize`: batch_size=1, class_weight=balanced, lr_schedule=cosine, normalize=zscore (max I 1)
  - `normalize`: normalize=zscore (max I 1.34)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.36); lr_schedule=step, normalize=zscore (max I 1.36)
- 3 separate islands (no single-knob move joins them): batch_size=3, normalize=minmax; label_noise=0.905, normalize=zscore; batch_size=1, normalize=zscore | batch_size=1, lr_schedule=cosine; batch_size=3, lr_schedule=cosine | batch_size=1, class_weight=balanced, lr_schedule=cosine, normalize=zscore

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `label_noise=0.905`, `normalize=zscore` | 3 | +0.0% | +1.5% | 0.8% |
| `batch_size=3`, `normalize=minmax` | 3 | +0.5% | +1.6% | 1.0% |
| `normalize=zscore`, `batch_size=1` | 3 | +0.5% | +2.3% | 1.4% |
| `class_weight=balanced`, `normalize=zscore`, `batch_size=1`, `lr_schedule=cosine` | 3 | +1.6% | +5.8% | 3.7% |
| `batch_size=1`, `normalize=minmax` | 3 | +3.7% | +5.4% | 4.5% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: invalid_value, The code computes math.log(positive_rate / (1 - positive_rate)). With positive_rate = 0.0, the argument becomes 0, causing a math domain error because log is undefined for non-positive values; retried as `positive_rate=0.001`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `NUM_RUNS`, `AGGREGATION_METHOD`

## Provenance
- GapFinder commit: `b05f7288e1a4df8af69bb0b5e7633827b4cb46c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0006, sandbox reported $0.0000 (total $0.0006; this search; ledger extraction is included only if it shared the search's router)
