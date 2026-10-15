# Gap Report: test-v12-03

Artifact `mlbench` · generated 2026-10-15 08:07 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Explained | -30.4% | +6.5% | ±0.7% | `positive_rate=0.1`, `lr_schedule=cosine` |

## C1: test_accuracy (paper 0.7)
**Explained** · gap -30.4% → +6.5% · 59 hypotheses tested
> Interacting factors: these changes close the gap only together, and every check passes

### Which experiment changed it?
- Branch: `B0088`, `B0137`, `B0138`, `B0139`, `B0140` (5 run(s) of the same config)
- Config: `positive_rate` naive `0.3`, changed to `0.1`
- Config: `lr_schedule` naive `const`, changed to `cosine`
- Command:

  Replay: fork checkpoint `08157580-8ba9-4e4c-86fc-3960793f1ce5` and run
  ```
  RUN_TAG=34290b28e344 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.1 --label_noise 0.05 --split 0.8 --normalize none --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule cosine --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7958, 0.7042, 0.7708, 0.7458, 0.7417; gap after +6.5%; result checkpoint `cd4e13b9-6dd7-4ef9-bb10-6397db88f4e4`
- Effect: candidate 0.7458 minus naive 0.4875 = +0.2583, 95% bootstrap interval [+0.1959, +0.2891] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.700 test accuracy and 0.500 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7 (headline claim)

### What did we measure?
- Naive median 0.4875 over 5 runs; repeats: 0.4875, 0.4875, 0.5333, 0.5375, 0.4875
- Spread: range 0.4875 to 0.5375, noise band ±0.004875 (2 x MAD), CV 5.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -30.4% (noise band ±0.7% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is +0.2583 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `training_loop_bugs`, `RUN_TAG`, `aggregation_method`, `num_runs`, `SCALES`, `WEIGHTS`, `weight_init_scale`, `sigmoid_clamp`, `python_random_module`, `logit_bias_term`, `feature_generation_gaussian`, `balanced_accuracy_formula`, `label_noise_application`, `python_version`, `hardware_cpu`, `os_settings`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=minmax` (22.22 noise units, gap -14.9%); `normalize=zscore` (17.09 noise units, gap +18.5%); `positive_rate=0.65` (11.96 noise units, gap -22.0%); `positive_rate=0.06` (10.26 noise units, gap -23.2%); `class_weight=balanced` (10.26 noise units, gap -23.2%) (and 4 more in the JSON)
- Near alternatives (closest across all claims):
  - `normalize=minmax`, `positive_rate=0.1`: this claim +11.9%, mean |gap| 6.0% (5 runs)
  - `normalize=minmax`: this claim -14.9%, mean |gap| 7.4% (3 runs)
  - `normalize=minmax`, `lr_schedule=cosine`: this claim -14.9%, mean |gap| 7.4% (5 runs)

### History matching (every measured configuration, all claims together)
- 9 of 57 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 9 configurations
  - `lr_schedule, positive_rate`: lr_schedule=cosine, positive_rate=0.03 (max I 1.47); lr_schedule=step, positive_rate=0.006 (max I 1.69); lr_schedule=cosine, positive_rate=0.15 (max I 2.45); lr_schedule=step, positive_rate=0.65 (max I 2.57)
  - `normalize, positive_rate`: normalize=minmax, positive_rate=0.1 (max I 2.14); normalize=minmax, positive_rate=0.65 (max I 2.89)
  - `lr_schedule, normalize`: lr_schedule=step, normalize=minmax (max I 2.29); lr_schedule=cosine, normalize=minmax (max I 2.68)
  - `normalize`: normalize=minmax (max I 2.6)
- 3 separate islands (no single-knob move joins them): normalize=minmax, positive_rate=0.1; lr_schedule=step, normalize=minmax; normalize=minmax | lr_schedule=cosine, positive_rate=0.03; lr_schedule=cosine, positive_rate=0.15 | lr_schedule=step, positive_rate=0.006; lr_schedule=step, positive_rate=0.65

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'normalize': 'zscore', 'class_weight': 'balanced'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax`, `positive_rate=0.1` | 5 | +11.9% | +0.0% | 6.0% |
| `normalize=minmax` | 3 | -14.9% | +0.0% | 7.4% |
| `normalize=minmax`, `lr_schedule=cosine` | 5 | -14.9% | +0.0% | 7.4% |
| `normalize=minmax`, `positive_rate=0.65` | 5 | -16.1% | +0.0% | 8.0% |
| `normalize=minmax`, `positive_rate=0.93` | 5 | +17.9% | +0.0% | 8.9% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: invalid_value, Setting positive_rate to 0.0 causes a math domain error in log(p/(1-p)) because log(0) is undefined. A small positive value like 0.001 preserves the intent of a near‑zero positive rate while keeping the argument of log positive; retried as `positive_rate=0.001`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `training_loop_bugs`, `RUN_TAG`, `aggregation_method`, `num_runs`, `SCALES`, `WEIGHTS`, `weight_init_scale`, `sigmoid_clamp`, `python_random_module`, `logit_bias_term`, `feature_generation_gaussian`, `balanced_accuracy_formula`, `label_noise_application`, `python_version`, `hardware_cpu`, `os_settings`, `--out`

## Provenance
- GapFinder commit: `f01fe3d9a0095f98d6304ad0543b917ca8e529eb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0007, sandbox reported $0.0000 (total $0.0007; this search; ledger extraction is included only if it shared the search's router)
