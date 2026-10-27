# Gap Report: test-v11-03

Artifact `mlbench` · generated 2026-10-14 23:32 · 197 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -37.8% | +0.0% | ±5.3% | `normalize=zscore`, `class_weight=balanced` |

## C1: test_accuracy (paper 0.7833)
**Fits but unsupported** · gap -37.8% → +0.0% · 75 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0140`, `B0186`, `B0187`, `B0188`, `B0189` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Config: `class_weight` naive `none`, changed to `balanced`
- Command:

  Replay: fork checkpoint `0156bf02-1ff4-4c36-bb47-21605dcddd72` and run
  ```
  RUN_TAG=6d15f25c31bb "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight balanced --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7875, 0.7875, 0.7833, 0.7833, 0.7833; gap after +0.0%; result checkpoint `00fabe4d-324d-4feb-b771-9e09bd185da8`
- Effect: candidate 0.7833 minus naive 0.4875 = +0.2958, 95% bootstrap interval [+0.2458, +0.3191] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.783 test accuracy and 0.752 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7833 (headline claim)

### What did we measure?
- Naive median 0.4875 over 5 runs; repeats: 0.4667, 0.4875, 0.4667, 0.5375, 0.5375
- Spread: range 0.4667 to 0.5375, noise band ±0.0416 (2 x MAD), CV 7.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -37.8% (noise band ±5.3% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -29.3% (it comes back)
- PASS · Counterfactual (reversal test): without `class_weight` the gap is +5.3% (it comes back)
- PASS · Held-out claim: C2: -35.9% to +4.4% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- FAIL · Evidence: `class_weight=balanced`: no evidence mentions 'balanced'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2958 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `aggregation_method`, `num_runs`, `shuffling_seed_method`, `SCALES`, `WEIGHTS`, `weight_init_scale`, `bias_init`, `logit_intercept_formula`, `label_noise_mechanism`, `sigmoid_clip_range`, `random_module`, `hardware_cpu`, `os_python_version`, `batch_gradient_aggregation`, `class_weight_balanced_formula`, `floating_point_precision`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (3.31 noise units, gap -20.2%); `normalize=minmax` (2.6 noise units, gap -23.9%); `label_noise=0.005` (2 noise units, gap -27.1%); `positive_rate=0.5` (1.4 noise units, gap -30.3%); `positive_rate=0.65` (1.4 noise units, gap -30.3%) (and 12 more in the JSON)
- Near alternatives (closest across all claims):
  - `positive_rate=0.5`, `normalize=zscore`: this claim +0.5%, mean |gap| 2.6% (5 runs)
  - `positive_rate=0.65`, `normalize=zscore`: this claim +4.8%, mean |gap| 6.1% (5 runs)
  - `normalize=zscore`: this claim +5.3%, mean |gap| 6.3% (6 runs)

### History matching (every measured configuration, all claims together)
- 15 of 74 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `label_noise, normalize`: label_noise=0.905, normalize=zscore (max I 0.2)
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 0.37); class_weight=balanced, normalize=zscore (max I 0.75)
  - `normalize, positive_rate`: normalize=minmax, positive_rate=0.5 (max I 0.59); normalize=zscore, positive_rate=0.5 (max I 0.75); normalize=zscore, positive_rate=0.65 (max I 1.19)
  - `batch_size, normalize`: batch_size=16, normalize=zscore (max I 0.9); batch_size=64, normalize=zscore (max I 0.98)
  - `lr_schedule, normalize`: lr_schedule=step, normalize=zscore (max I 0.98)
  - `normalize`: normalize=zscore (max I 1.21)
- 4 separate islands (no single-knob move joins them): label_noise=0.905, normalize=zscore; class_weight=balanced, normalize=minmax; normalize=minmax, positive_rate=0.5 | label_noise=0.005, lr_schedule=cosine | lr_schedule=cosine, positive_rate=0.65 | batch_size=16, lr_schedule=cosine

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'normalize': 'zscore', 'label_noise': '0.905'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore`, `class_weight=balanced` | 5 | +0.0% | +4.4% | 2.2% |
| `positive_rate=0.5`, `normalize=zscore` | 5 | +0.5% | +4.7% | 2.6% |
| `positive_rate=0.65`, `normalize=zscore` | 5 | +4.8% | +7.3% | 6.1% |
| `normalize=zscore` | 6 | +5.3% | +7.3% | 6.3% |
| `normalize=zscore`, `lr_schedule=cosine` | 5 | +5.9% | +7.8% | 6.8% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `aggregation_method`, `num_runs`, `shuffling_seed_method`, `SCALES`, `WEIGHTS`, `weight_init_scale`, `bias_init`, `logit_intercept_formula`, `label_noise_mechanism`, `sigmoid_clip_range`, `random_module`, `hardware_cpu`, `os_python_version`, `batch_gradient_aggregation`, `class_weight_balanced_formula`, `floating_point_precision`

## Provenance
- GapFinder commit: `efb2f63a257a40b9982099a274f2e882f272b80c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
