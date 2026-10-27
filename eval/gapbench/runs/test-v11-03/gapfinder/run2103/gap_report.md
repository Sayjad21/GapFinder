# Gap Report: test-v11-03

Artifact `mlbench` · generated 2026-10-15 21:01 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -31.4% | +0.5% | ±11.7% | `positive_rate=0.5`, `normalize=minmax` |

## C1: test_accuracy (paper 0.7833)
**Fits but unsupported** · gap -31.4% → +0.5% · 79 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0089`, `B0118`, `B0150`, `B0151`, `B0152` (5 run(s) of the same config)
- Config: `positive_rate` naive `0.3`, changed to `0.5`
- Config: `normalize` naive `none`, changed to `minmax`
- Command:

  Replay: fork checkpoint `be534b1d-6c0d-413e-9008-649a64dae64a` and run
  ```
  RUN_TAG=f5d31d5d744a "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.5 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7917, 0.7958, 0.7708, 0.7708, 0.7875; gap after +0.5%; result checkpoint `cd560121-8ab7-4257-a035-e7a69f5633cd`
- Effect: candidate 0.7875 minus naive 0.5375 = +0.25, 95% bootstrap interval [+0.2117, +0.2967] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.783 test accuracy and 0.752 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7833 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5417, 0.5375, 0.5833, 0.4875, 0.4875
- Spread: range 0.4875 to 0.5833, noise band ±0.0916 (2 x MAD), CV 7.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -31.4% (noise band ±11.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `positive_rate` the gap is -23.9% (it comes back)
- PASS · Counterfactual (reversal test): without `normalize` the gap is -33.0% (it comes back)
- PASS · Held-out claim: C2: -27.9% to +4.7% (not worse beyond noise)
- FAIL · Evidence: `positive_rate=0.5`: no evidence mentions '0.5'; it fits, but nothing says the authors used it
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.25 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `aggregation_method`, `num_runs`, `shuffling_seed_method`, `SCALES`, `WEIGHTS`, `weight_init_scale`, `bias_init`, `logit_intercept_formula`, `label_noise_mechanism`, `sigmoid_clip_range`, `random_module`, `hardware_cpu`, `os_python_version`, `batch_gradient_aggregation`, `class_weight_balanced_formula`, `floating_point_precision`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (2.18 noise units, gap +5.9%)
- Near alternatives (closest across all claims):
  - `batch_size=3`, `normalize=minmax`: this claim +0.5%, mean |gap| 0.6% (5 runs)
  - `normalize=zscore`, `label_noise=0.905`: this claim +0.0%, mean |gap| 0.8% (5 runs)
  - `normalize=zscore`, `positive_rate=0.5`: this claim +0.0%, mean |gap| 2.1% (5 runs)

### History matching (every measured configuration, all claims together)
- 27 of 79 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `batch_size, normalize`: batch_size=3, normalize=minmax (max I 0.04); batch_size=3, normalize=zscore (max I 1.15); batch_size=320, normalize=zscore (max I 1.17); batch_size=128, normalize=zscore (max I 1.24); +1 more
  - `label_noise, normalize`: label_noise=0.905, normalize=zscore (max I 0.27); label_noise=0.1, normalize=zscore (max I 0.8); label_noise=0.981, normalize=zscore (max I 1.11)
  - `normalize, positive_rate`: normalize=minmax, positive_rate=0.5 (max I 0.7); normalize=zscore, positive_rate=0.5 (max I 0.74)

Notes:
- stopped early: run budget of 200 reached (wanted 3 more run(s) of {'normalize': 'zscore', 'positive_rate': '0.93'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `batch_size=3`, `normalize=minmax` | 5 | +0.5% | -0.6% | 0.6% |
| `normalize=zscore`, `label_noise=0.905` | 5 | +0.0% | +1.5% | 0.8% |
| `normalize=zscore`, `positive_rate=0.5` | 5 | +0.0% | +4.2% | 2.1% |
| `positive_rate=0.5`, `normalize=minmax` | 5 | +0.5% | +4.7% | 2.6% |
| `normalize=zscore`, `label_noise=0.1` | 5 | +3.2% | +4.8% | 4.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `aggregation_method`, `num_runs`, `shuffling_seed_method`, `SCALES`, `WEIGHTS`, `weight_init_scale`, `bias_init`, `logit_intercept_formula`, `label_noise_mechanism`, `sigmoid_clip_range`, `random_module`, `hardware_cpu`, `os_python_version`, `batch_gradient_aggregation`, `class_weight_balanced_formula`, `floating_point_precision`

## Provenance
- GapFinder commit: `cd8c8af2b9d079dd9a57443ed501c0dd8a467d34` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
