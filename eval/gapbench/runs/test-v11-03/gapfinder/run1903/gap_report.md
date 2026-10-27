# Gap Report: test-v11-03

Artifact `mlbench` · generated 2026-10-15 19:45 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -31.4% | +5.3% | ±0.7% | `normalize=zscore` |

## C1: test_accuracy (paper 0.7833)
**Fits but unsupported** · gap -31.4% → +5.3% · 99 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0036`, `B0065`, `B0066`, `B0071`, `B0072`, `B0073` (6 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Command:

  Replay: fork checkpoint `2729ae80-e120-4705-a196-4f1fe5ecaea2` and run
  ```
  RUN_TAG=7a3d326de07e "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.8292, 0.825, 0.825, 0.825, 0.825, 0.8292; gap after +5.3%; result checkpoint `9bc4b655-9930-42ed-a917-d8c66b1a4940`
- Effect: candidate 0.825 minus naive 0.5375 = +0.2875, 95% bootstrap interval [+0.2575, +0.345] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.783 test accuracy and 0.752 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7833 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.4667, 0.5375, 0.5375, 0.5375, 0.575
- Spread: range 0.4667 to 0.575, noise band ±0.005375 (2 x MAD), CV 7.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -31.4% (noise band ±0.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -31.4% (it comes back)
- PASS · Held-out claim: C2: -27.9% to +7.3% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2875 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `aggregation_method`, `num_runs`, `shuffling_seed_method`, `SCALES`, `WEIGHTS`, `weight_init_scale`, `bias_init`, `logit_intercept_formula`, `label_noise_mechanism`, `sigmoid_clip_range`, `random_module`, `hardware_cpu`, `os_python_version`, `batch_gradient_aggregation`, `class_weight_balanced_formula`, `floating_point_precision`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (15.5 noise units, gap -20.7%); `normalize=minmax` (10.85 noise units, gap -23.9%); `batch_size=3` (6.98 noise units, gap -26.6%); `label_noise=0.01` (2.33 noise units, gap -29.8%); `label_noise=0.905` (1.54 noise units, gap -30.3%)
- Near alternatives (closest across all claims):
  - `normalize=minmax`, `batch_size=3`: this claim -0.3%, mean |gap| 0.3% (2 runs)
  - `normalize=zscore`, `label_noise=0.905`: this claim +0.0%, mean |gap| 0.8% (2 runs)
  - `batch_size=1`, `normalize=zscore`: this claim +0.8%, mean |gap| 1.6% (2 runs)

### History matching (every measured configuration, all claims together)
- 33 of 97 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `batch_size, normalize`: batch_size=3, normalize=minmax (max I 0.04); batch_size=1, normalize=zscore (max I 0.36); batch_size=1600, normalize=zscore (max I 0.71); batch_size=3200, normalize=zscore (max I 0.84); +1 more
  - `label_noise, normalize`: label_noise=0.905, normalize=zscore (max I 0.22); label_noise=0.1, normalize=zscore (max I 0.78); label_noise=0.981, normalize=zscore (max I 0.94)
  - `normalize, positive_rate`: normalize=zscore, positive_rate=0.5 (max I 0.69); normalize=zscore, positive_rate=0.86 (max I 0.84)
- 4 separate islands (no single-knob move joins them): batch_size=3, normalize=minmax; label_noise=0.905, normalize=zscore; batch_size=1, normalize=zscore | batch_size=3, lr_schedule=cosine; batch_size=64, lr_schedule=cosine | lr_schedule=cosine, positive_rate=0.86 | label_noise=0.01, lr_schedule=cosine

Notes:
- stopped early: run budget of 200 reached (wanted 1 more run(s) of {'normalize': 'minmax', 'positive_rate': '0.06'} for 'confirm-combo (race)')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax`, `batch_size=3` | 2 | -0.3% | -0.2% | 0.3% |
| `normalize=zscore`, `label_noise=0.905` | 2 | +0.0% | +1.5% | 0.8% |
| `batch_size=1`, `normalize=zscore` | 2 | +0.8% | +2.5% | 1.6% |
| `positive_rate=0.5`, `normalize=zscore` | 2 | +0.5% | +4.7% | 2.6% |
| `normalize=zscore`, `batch_size=1600` | 2 | +2.7% | +4.9% | 3.8% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `aggregation_method`, `num_runs`, `shuffling_seed_method`, `SCALES`, `WEIGHTS`, `weight_init_scale`, `bias_init`, `logit_intercept_formula`, `label_noise_mechanism`, `sigmoid_clip_range`, `random_module`, `hardware_cpu`, `os_python_version`, `batch_gradient_aggregation`, `class_weight_balanced_formula`, `floating_point_precision`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
