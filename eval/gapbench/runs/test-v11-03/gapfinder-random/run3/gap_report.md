# Gap Report: test-v11-03

Artifact `mlbench` · generated 2026-10-14 12:31 · 131 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -32.4% | +0.0% | ±3.2% | `normalize=zscore`, `class_weight=balanced` |

## C1: test_accuracy (paper 0.7833)
**Fits but unsupported** · gap -32.4% → +0.0% · 56 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0060`, `B0098`, `B0099` (3 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Config: `class_weight` naive `none`, changed to `balanced`
- Command:

  Replay: fork checkpoint `c069d127-b061-45e6-98b4-075e770efd07` and run
  ```
  RUN_TAG=a0a5fe868ff8 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight balanced --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7875, 0.7833, 0.7833; gap after +0.0%; result checkpoint `a6417337-ecdd-4ffd-ac79-530b7c9f6c83`
- Effect: candidate 0.7833 minus naive 0.5292 = +0.2541, 95% bootstrap interval [+0.2441, +0.2961] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.783 test accuracy and 0.752 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7833 (headline claim)

### What did we measure?
- Naive median 0.5292 over 5 runs; repeats: 0.5292, 0.5375, 0.5417, 0.4833, 0.5
- Spread: range 0.4833 to 0.5417, noise band ±0.025 (2 x MAD), CV 4.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -32.4% (noise band ±3.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -31.4% (it comes back)
- PASS · Counterfactual (reversal test): without `class_weight` the gap is +5.6% (it comes back)
- PASS · Held-out claim: C2: -31.2% to +4.4% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- FAIL · Evidence: `class_weight=balanced`: no evidence mentions 'balanced'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2541 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `aggregation_method`, `num_runs`, `shuffling_seed_method`, `SCALES`, `WEIGHTS`, `weight_init_scale`, `bias_init`, `logit_intercept_formula`, `label_noise_mechanism`, `sigmoid_clip_range`, `random_module`, `hardware_cpu`, `os_python_version`, `batch_gradient_aggregation`, `class_weight_balanced_formula`, `floating_point_precision`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (3 noise units, gap -22.9%); `normalize=minmax` (2.66 noise units, gap -23.9%); `batch_size=3` (2.16 noise units, gap -25.5%); `batch_size=128` (1.16 noise units, gap -28.7%); `lr_schedule=step` (1 noise units, gap -29.2%) (and 2 more in the JSON)
- Near alternatives (closest across all claims):
  - `normalize=zscore`, `label_noise=0.905`: this claim +0.0%, mean |gap| 0.8% (3 runs)
  - `normalize=minmax`, `batch_size=3`: this claim -1.1%, mean |gap| 1.3% (3 runs)
  - `normalize=minmax`, `class_weight=balanced`: this claim -2.1%, mean |gap| 2.9% (3 runs)

### History matching (every measured configuration, all claims together)
- 11 of 55 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `batch_size, normalize`: batch_size=3, normalize=minmax (max I 0.06); batch_size=128, normalize=zscore (max I 1.29); batch_size=3, normalize=zscore (max I 1.31)
  - `label_noise, normalize`: label_noise=0.905, normalize=zscore (max I 0.27); label_noise=0.01, normalize=zscore (max I 1.44)
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 0.59); class_weight=balanced, normalize=zscore (max I 0.79)
  - `normalize`: normalize=zscore (max I 1.32)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.34); lr_schedule=step, normalize=zscore (max I 1.34)
- 2 separate islands (no single-knob move joins them): batch_size=3, normalize=minmax; label_noise=0.905, normalize=zscore; class_weight=balanced, normalize=minmax | batch_size=3, lr_schedule=cosine
- Equally good values: `normalize` in {minmax, zscore}

Notes:
- equally good values within one noise band (measured): normalize in {minmax, zscore}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore`, `label_noise=0.905` | 3 | +0.0% | +1.5% | 0.8% |
| `normalize=minmax`, `batch_size=3` | 3 | -1.1% | -1.6% | 1.3% |
| `normalize=zscore`, `class_weight=balanced` | 3 | +0.0% | +4.4% | 2.2% |
| `normalize=minmax`, `class_weight=balanced` | 3 | -2.1% | +3.6% | 2.9% |
| `normalize=zscore` | 4 | +5.6% | +7.5% | 6.6% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: invalid_value, The value 0.0 leads to math.log(0) which is undefined; positive_rate must be strictly between 0 and 1 to compute the log-odds term; retried as `positive_rate=0.001`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `aggregation_method`, `num_runs`, `shuffling_seed_method`, `SCALES`, `WEIGHTS`, `weight_init_scale`, `bias_init`, `logit_intercept_formula`, `label_noise_mechanism`, `sigmoid_clip_range`, `random_module`, `hardware_cpu`, `os_python_version`, `batch_gradient_aggregation`, `class_weight_balanced_formula`, `floating_point_precision`

## Provenance
- GapFinder commit: `b05f7288e1a4df8af69bb0b5e7633827b4cb46c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0006, sandbox reported $0.0000 (total $0.0006; this search; ledger extraction is included only if it shared the search's router)
