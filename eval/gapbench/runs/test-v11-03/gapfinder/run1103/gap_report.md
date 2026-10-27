# Gap Report: test-v11-03

Artifact `mlbench` · generated 2026-10-15 00:34 · 199 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -31.4% | +0.0% | ±1.1% | `normalize=zscore`, `label_noise=0.905` |

## C1: test_accuracy (paper 0.7833)
**Fits but unsupported** · gap -31.4% → +0.0% · 99 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0097`, `B0168`, `B0169` (3 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Config: `label_noise` naive `0.05`, changed to `0.905`
- Command:

  Replay: fork checkpoint `271b22b7-9897-47cb-98d8-7b8a46f0bd9c` and run
  ```
  RUN_TAG=768ea7d38404 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.905 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7833, 0.7875, 0.7833; gap after +0.0%; result checkpoint `ad2e31c1-adec-4c2d-ba89-bebdb3933fd9`
- Effect: candidate 0.7833 minus naive 0.5375 = +0.2458, 95% bootstrap interval [+0.2214, +0.2517] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.783 test accuracy and 0.752 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7833 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5333, 0.5667, 0.5375, 0.5583, 0.5375
- Spread: range 0.5333 to 0.5667, noise band ±0.0084 (2 x MAD), CV 2.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -31.4% (noise band ±1.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -30.3% (it comes back)
- PASS · Counterfactual (reversal test): without `label_noise` the gap is +5.6% (it comes back)
- PASS · Held-out claim: C2: -27.9% to +1.5% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- FAIL · Evidence: `label_noise=0.905`: no evidence mentions '0.905'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2458 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `aggregation_method`, `num_runs`, `shuffling_seed_method`, `SCALES`, `WEIGHTS`, `weight_init_scale`, `bias_init`, `logit_intercept_formula`, `label_noise_mechanism`, `sigmoid_clip_range`, `random_module`, `hardware_cpu`, `os_python_version`, `batch_gradient_aggregation`, `class_weight_balanced_formula`, `floating_point_precision`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (10.92 noise units, gap -19.7%); `normalize=minmax` (6.94 noise units, gap -23.9%); `batch_size=1` (4.46 noise units, gap -26.6%); `label_noise=0.81` (3.48 noise units, gap -27.7%); `positive_rate=0.7` (2.48 noise units, gap -28.7%) (and 2 more in the JSON)
- Near alternatives (closest across all claims):
  - `normalize=zscore`, `batch_size=1`: this claim +1.6%, mean |gap| 2.6% (3 runs)
  - `normalize=minmax`, `batch_size=1`: this claim +2.7%, mean |gap| 4.4% (3 runs)
  - `normalize=zscore`, `batch_size=16`: this claim +5.3%, mean |gap| 6.3% (3 runs)

### History matching (every measured configuration, all claims together)
- 29 of 97 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `label_noise, normalize`: label_noise=0.905, normalize=zscore (max I 0.35); label_noise=0.1, normalize=zscore (max I 1.04); label_noise=0.981, normalize=zscore (max I 1.36)
  - `batch_size, normalize`: batch_size=1, normalize=zscore (max I 0.48); batch_size=1600, normalize=zscore (max I 1.13); batch_size=3200, normalize=zscore (max I 1.16); batch_size=1, normalize=minmax (max I 1.19); +1 more
  - `normalize, positive_rate`: normalize=zscore, positive_rate=0.5 (max I 0.8); normalize=zscore, positive_rate=0.86 (max I 1.1)
- 2 separate islands (no single-knob move joins them): label_noise=0.905, normalize=zscore; batch_size=1, normalize=zscore; normalize=zscore, positive_rate=0.5 | batch_size=1, lr_schedule=cosine

Notes:
- stopped early: run budget of 200 reached (wanted 2 more run(s) of {'label_noise': '0.81', 'positive_rate': '0.7'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore`, `label_noise=0.905` | 3 | +0.0% | +1.5% | 0.8% |
| `normalize=zscore`, `batch_size=1` | 3 | +1.6% | +3.6% | 2.6% |
| `normalize=minmax`, `batch_size=1` | 3 | +2.7% | +6.1% | 4.4% |
| `normalize=zscore`, `batch_size=16` | 3 | +5.3% | +7.3% | 6.3% |
| `normalize=zscore`, `positive_rate=0.65` | 3 | +5.3% | +7.8% | 6.6% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `aggregation_method`, `num_runs`, `shuffling_seed_method`, `SCALES`, `WEIGHTS`, `weight_init_scale`, `bias_init`, `logit_intercept_formula`, `label_noise_mechanism`, `sigmoid_clip_range`, `random_module`, `hardware_cpu`, `os_python_version`, `batch_gradient_aggregation`, `class_weight_balanced_formula`, `floating_point_precision`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
