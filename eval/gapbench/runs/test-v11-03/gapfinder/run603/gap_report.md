# Gap Report: test-v11-03

Artifact `mlbench` · generated 2026-10-14 22:33 · 197 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -30.3% | -0.5% | ±2.1% | `normalize=zscore`, `positive_rate=0.15` |

## C1: test_accuracy (paper 0.7833)
**Fits but unsupported** · gap -30.3% → -0.5% · 75 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0129`, `B0178`, `B0179`, `B0180`, `B0181` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Config: `positive_rate` naive `0.3`, changed to `0.15`
- Command:

  Replay: fork checkpoint `65e876d7-d59e-4173-8d4e-e4dc802ee0b2` and run
  ```
  RUN_TAG=fd3d2754df22 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.15 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7792, 0.775, 0.7708, 0.7792, 0.7792; gap after -0.5%; result checkpoint `9621f8d2-5c18-4a7d-a0e2-646c4ecf2ae2`
- Effect: candidate 0.7792 minus naive 0.5458 = +0.2334, 95% bootstrap interval [+0.2167, +0.2826] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.783 test accuracy and 0.752 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7833 (headline claim)

### What did we measure?
- Naive median 0.5458 over 5 runs; repeats: 0.5625, 0.5375, 0.5458, 0.4833, 0.5458
- Spread: range 0.4833 to 0.5625, noise band ±0.0166 (2 x MAD), CV 5.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -30.3% (noise band ±2.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -35.1% (it comes back)
- PASS · Counterfactual (reversal test): without `positive_rate` the gap is +5.9% (it comes back)
- PASS · Held-out claim: C2: -27.2% to -9.6% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- FAIL · Evidence: `positive_rate=0.15`: no evidence mentions '0.15'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2334 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `aggregation_method`, `num_runs`, `shuffling_seed_method`, `SCALES`, `WEIGHTS`, `weight_init_scale`, `bias_init`, `logit_intercept_formula`, `label_noise_mechanism`, `sigmoid_clip_range`, `random_module`, `hardware_cpu`, `os_python_version`, `batch_gradient_aggregation`, `class_weight_balanced_formula`, `floating_point_precision`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (4.02 noise units, gap -21.8%); `batch_size=6` (3.01 noise units, gap -23.9%); `normalize=minmax` (3.01 noise units, gap -23.9%); `label_noise=0.1` (1.76 noise units, gap -26.6%); `batch_size=16` (1.01 noise units, gap -28.2%) (and 2 more in the JSON)
- Near alternatives (closest across all claims):
  - `normalize=zscore`, `label_noise=0.1`: this claim +3.2%, mean |gap| 4.0% (5 runs)
  - `normalize=zscore`, `batch_size=6`: this claim +4.8%, mean |gap| 5.8% (5 runs)
  - `normalize=zscore`, `label_noise=0.001`: this claim +5.9%, mean |gap| 6.8% (5 runs)

### History matching (every measured configuration, all claims together)
- 14 of 74 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `label_noise, normalize`: label_noise=0.1, normalize=zscore (max I 0.88); label_noise=0.001, normalize=zscore (max I 1.39)
  - `batch_size, normalize`: batch_size=6, normalize=minmax (max I 0.88); batch_size=6, normalize=zscore (max I 1.19); batch_size=16, normalize=zscore (max I 1.33)
  - `lr_schedule, normalize`: lr_schedule=step, normalize=zscore (max I 1.33); lr_schedule=cosine, normalize=zscore (max I 1.35)
  - `normalize`: normalize=zscore (max I 1.36)
  - `normalize, positive_rate`: normalize=zscore, positive_rate=0.15 (max I 1.77)
  - `batch_size, lr_schedule`: batch_size=6, lr_schedule=cosine (max I 2.26)
- 4 separate islands (no single-knob move joins them): label_noise=0.1, normalize=zscore; batch_size=6, normalize=minmax; batch_size=6, normalize=zscore | batch_size=6, lr_schedule=cosine; batch_size=16, lr_schedule=cosine | lr_schedule=cosine, positive_rate=0.93; lr_schedule=cosine, positive_rate=0.15 | label_noise=0.001, lr_schedule=cosine

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'normalize': 'minmax', 'lr_schedule': 'cosine'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore`, `label_noise=0.1` | 5 | +3.2% | +4.8% | 4.0% |
| `normalize=zscore`, `positive_rate=0.15` | 5 | -0.5% | -9.6% | 5.1% |
| `normalize=zscore`, `batch_size=6` | 5 | +4.8% | +6.8% | 5.8% |
| `normalize=zscore`, `label_noise=0.001` | 5 | +5.9% | +7.7% | 6.8% |
| `normalize=zscore` | 6 | +5.9% | +7.8% | 6.8% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `aggregation_method`, `num_runs`, `shuffling_seed_method`, `SCALES`, `WEIGHTS`, `weight_init_scale`, `bias_init`, `logit_intercept_formula`, `label_noise_mechanism`, `sigmoid_clip_range`, `random_module`, `hardware_cpu`, `os_python_version`, `batch_gradient_aggregation`, `class_weight_balanced_formula`, `floating_point_precision`

## Provenance
- GapFinder commit: `e0f13d101585ad1609a15fbf67b70128f4cfffc8` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
