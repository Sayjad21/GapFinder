# Gap Report: test-v11-03

Artifact `mlbench` · generated 2026-10-14 11:11 · 148 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -31.9% | +0.0% | ±1.1% | `normalize=zscore`, `class_weight=balanced` |

## C1: test_accuracy (paper 0.7833)
**Fits but unsupported** · gap -31.9% → +0.0% · 62 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0053`, `B0093`, `B0094` (3 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Config: `class_weight` naive `none`, changed to `balanced`
- Command:

  Replay: fork checkpoint `8177071c-bcc3-4063-9d8c-8c0583791022` and run
  ```
  RUN_TAG=06742ea64e56 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight balanced --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7833, 0.7833, 0.7792; gap after +0.0%; result checkpoint `a4475955-fe72-49be-bce5-3059b0282a10`
- Effect: candidate 0.7833 minus naive 0.5333 = +0.25, 95% bootstrap interval [+0.2425, +0.2895] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.783 test accuracy and 0.752 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7833 (headline claim)

### What did we measure?
- Naive median 0.5333 over 5 runs; repeats: 0.4958, 0.5375, 0.4875, 0.5375, 0.5333
- Spread: range 0.4875 to 0.5375, noise band ±0.0084 (2 x MAD), CV 4.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -31.9% (noise band ±1.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -29.8% (it comes back)
- PASS · Counterfactual (reversal test): without `class_weight` the gap is +5.9% (it comes back)
- PASS · Held-out claim: C2: -28.4% to +4.4% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- FAIL · Evidence: `class_weight=balanced`: no evidence mentions 'balanced'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.25 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `NUM_RUNS`, `AGGREGATION_METHOD`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (10.42 noise units, gap -20.7%); `normalize=minmax` (7.44 noise units, gap -23.9%); `batch_size=3` (4.96 noise units, gap -26.6%); `batch_size=64` (3.48 noise units, gap -28.2%); `batch_size=1` (3.48 noise units, gap -28.2%)
- Near alternatives (closest across all claims):
  - `batch_size=3`, `normalize=minmax`: this claim +0.0%, mean |gap| 0.7% (3 runs)
  - `class_weight=balanced`, `normalize=minmax`: this claim -2.1%, mean |gap| 2.9% (3 runs)
  - `batch_size=1`, `normalize=minmax`: this claim +4.3%, mean |gap| 5.1% (3 runs)

### History matching (every measured configuration, all claims together)
- 15 of 61 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `batch_size, normalize`: batch_size=3, normalize=minmax (max I 0.14); batch_size=1, normalize=minmax (max I 0.99); batch_size=3, normalize=zscore (max I 1.03); batch_size=1, normalize=zscore (max I 1.04); +3 more
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 0.63); class_weight=balanced, normalize=zscore (max I 0.72)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.33)
- 2 separate islands (no single-knob move joins them): batch_size=3, normalize=minmax; class_weight=balanced, normalize=minmax; class_weight=balanced, normalize=zscore | batch_size=1, lr_schedule=cosine; batch_size=3, lr_schedule=cosine

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `batch_size=3`, `normalize=minmax` | 3 | +0.0% | -1.3% | 0.7% |
| `class_weight=balanced`, `normalize=zscore` | 3 | +0.0% | +4.4% | 2.2% |
| `class_weight=balanced`, `normalize=minmax` | 3 | -2.1% | +3.7% | 2.9% |
| `batch_size=1`, `normalize=minmax` | 3 | +4.3% | +5.9% | 5.1% |
| `batch_size=3`, `normalize=zscore` | 3 | +4.3% | +5.9% | 5.1% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: invalid_value, The code computes math.log(positive_rate / (1 - positive_rate)). With positive_rate = 0.0 the argument becomes 0, causing a math domain error because log(0) is undefined. A valid positive_rate must be strictly between 0 and 1; retried as `positive_rate=0.001`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `NUM_RUNS`, `AGGREGATION_METHOD`

## Provenance
- GapFinder commit: `b05f7288e1a4df8af69bb0b5e7633827b4cb46c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0006, sandbox reported $0.0000 (total $0.0006; this search; ledger extraction is included only if it shared the search's router)
