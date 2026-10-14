# Gap Report: test-v11-03

Artifact `mlbench` · generated 2026-10-14 12:30 · 151 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -31.4% | +0.5% | ±2.1% | `normalize=minmax`, `batch_size=3` |

## C1: test_accuracy (paper 0.7833)
**Fits but unsupported** · gap -31.4% → +0.5% · 61 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0076`, `B0126`, `B0127` (3 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `batch_size` naive `32`, changed to `3`
- Command:

  Replay: fork checkpoint `79047770-4462-40db-8300-2ba05654e71b` and run
  ```
  RUN_TAG=5cf3241fd15e "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 3 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7917, 0.7875, 0.7875; gap after +0.5%; result checkpoint `bc3eb43d-c262-4d9f-82d1-1a4a2e715b0f`
- Effect: candidate 0.7875 minus naive 0.5375 = +0.25, 95% bootstrap interval [+0.2417, +0.2931] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.783 test accuracy and 0.752 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7833 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5375, 0.5458, 0.5375, 0.4833, 0.5458
- Spread: range 0.4833 to 0.5458, noise band ±0.0166 (2 x MAD), CV 5.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -31.4% (noise band ±2.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -26.9% (it comes back)
- PASS · Counterfactual (reversal test): without `batch_size` the gap is -23.9% (it comes back)
- PASS · Held-out claim: C2: -27.9% to +1.1% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- FAIL · Evidence: `batch_size=3`: no evidence mentions '3'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.25 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `aggregation_method`, `num_runs`, `shuffling_seed_method`, `SCALES`, `WEIGHTS`, `weight_init_scale`, `bias_init`, `logit_intercept_formula`, `label_noise_mechanism`, `sigmoid_clip_range`, `random_module`, `hardware_cpu`, `os_python_version`, `batch_gradient_aggregation`, `class_weight_balanced_formula`, `floating_point_precision`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (12.04 noise units, gap +5.9%); `lr_schedule=cosine` (6.52 noise units, gap -17.6%); `positive_rate=0.7` (1.51 noise units, gap -28.2%); `label_noise=0.005` (1.25 noise units, gap -28.7%)
- Near alternatives (closest across all claims):
  - `batch_size=3`, `normalize=zscore`: this claim +4.8%, mean |gap| 5.9% (3 runs)
  - `batch_size=320`, `normalize=zscore`: this claim +5.9%, mean |gap| 6.7% (3 runs)
  - `normalize=zscore`: this claim +5.9%, mean |gap| 6.8% (4 runs)

### History matching (every measured configuration, all claims together)
- 10 of 60 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `batch_size, normalize`: batch_size=3, normalize=minmax (max I 0.14); batch_size=3, normalize=zscore (max I 1.25); batch_size=320, normalize=zscore (max I 1.25); batch_size=64, normalize=zscore (max I 1.34)
  - `normalize`: normalize=zscore (max I 1.34)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.34); lr_schedule=step, normalize=zscore (max I 1.34)
  - `normalize, positive_rate`: normalize=zscore, positive_rate=0.7 (max I 1.44)
  - `batch_size, lr_schedule`: batch_size=3, lr_schedule=cosine (max I 2.09)
  - `lr_schedule, positive_rate`: lr_schedule=cosine, positive_rate=0.7 (max I 2.95)
- 3 separate islands (no single-knob move joins them): batch_size=3, normalize=minmax; batch_size=3, normalize=zscore; batch_size=320, normalize=zscore | batch_size=3, lr_schedule=cosine | lr_schedule=cosine, positive_rate=0.7

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `batch_size=3`, `normalize=minmax` | 3 | +0.5% | +1.1% | 0.8% |
| `batch_size=3`, `normalize=zscore` | 3 | +4.8% | +7.0% | 5.9% |
| `batch_size=320`, `normalize=zscore` | 3 | +5.9% | +7.5% | 6.7% |
| `normalize=zscore` | 4 | +5.9% | +7.8% | 6.8% |
| `normalize=zscore`, `lr_schedule=cosine` | 3 | +5.9% | +7.8% | 6.8% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: invalid_value, Setting positive_rate to 0.0 causes a math domain error when computing log(p/(1-p)) because log(0) is undefined. A valid positive_rate must be strictly between 0 and 1; a small value like 0.001 preserves the intent of a low positive rate while avoiding the error; retried as `positive_rate=0.001`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `aggregation_method`, `num_runs`, `shuffling_seed_method`, `SCALES`, `WEIGHTS`, `weight_init_scale`, `bias_init`, `logit_intercept_formula`, `label_noise_mechanism`, `sigmoid_clip_range`, `random_module`, `hardware_cpu`, `os_python_version`, `batch_gradient_aggregation`, `class_weight_balanced_formula`, `floating_point_precision`

## Provenance
- GapFinder commit: `b05f7288e1a4df8af69bb0b5e7633827b4cb46c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0668, sandbox reported $0.0000 (total $0.0668; this search; ledger extraction is included only if it shared the search's router)
