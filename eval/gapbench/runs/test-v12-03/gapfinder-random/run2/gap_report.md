# Gap Report: test-v12-03

Artifact `mlbench` · generated 2026-10-15 08:07 · 199 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -29.8% | +7.1% | ±2.4% | `positive_rate=0.86`, `normalize=minmax` |

## C1: test_accuracy (paper 0.7)
**Fits but unsupported** · gap -29.8% → +7.1% · 64 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0054`, `B0120`, `B0121`, `B0122`, `B0123` (5 run(s) of the same config)
- Config: `positive_rate` naive `0.3`, changed to `0.86`
- Config: `normalize` naive `none`, changed to `minmax`
- Command:

  Replay: fork checkpoint `b0417487-8d84-41e1-9a2d-942e2e9597b3` and run
  ```
  RUN_TAG=f00fad208f09 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.86 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.75, 0.75, 0.75, 0.75, 0.75; gap after +7.1%; result checkpoint `55334f07-010d-4c30-8dcf-2097017b9a1e`
- Effect: candidate 0.75 minus naive 0.4917 = +0.2583, 95% bootstrap interval [+0.2075, +0.265] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.700 test accuracy and 0.500 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7 (headline claim)

### What did we measure?
- Naive median 0.4917 over 5 runs; repeats: 0.4917, 0.5375, 0.4833, 0.5458, 0.4875
- Spread: range 0.4833 to 0.5458, noise band ±0.0168 (2 x MAD), CV 5.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -29.8% (noise band ±2.4% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `positive_rate` the gap is -14.9% (it comes back)
- PASS · Counterfactual (reversal test): without `normalize` the gap is -23.8% (it comes back)
- PASS · Held-out claim: C2: -2.6% to +0.0% (not worse beyond noise)
- FAIL · Evidence: `positive_rate=0.86`: no evidence mentions '0.86'; it fits, but nothing says the authors used it
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2583 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `training_loop_bugs`, `RUN_TAG`, `aggregation_method`, `num_runs`, `SCALES`, `WEIGHTS`, `weight_init_scale`, `sigmoid_clamp`, `python_random_module`, `logit_bias_term`, `feature_generation_gaussian`, `balanced_accuracy_formula`, `label_noise_application`, `python_version`, `hardware_cpu`, `os_settings`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (7.44 noise units, gap -11.9%); `normalize=zscore` (4.71 noise units, gap +18.5%); `lr_schedule=step` (3.22 noise units, gap -22.0%); `positive_rate=0.93` (2.23 noise units, gap -24.4%); `positive_rate=0.006` (1.24 noise units, gap -26.8%)
- Near alternatives (closest across all claims):
  - `positive_rate=0.1`, `normalize=minmax`: this claim +11.9%, mean |gap| 6.0% (5 runs)
  - `normalize=minmax`: this claim -14.9%, mean |gap| 7.4% (6 runs)
  - `lr_schedule=cosine`, `normalize=minmax`: this claim -14.9%, mean |gap| 7.4% (5 runs)

### History matching (every measured configuration, all claims together)
- 13 of 61 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `normalize, positive_rate`: normalize=minmax, positive_rate=0.15 (max I 0); normalize=minmax, positive_rate=0.86 (max I 1.25); normalize=minmax, positive_rate=0.1 (max I 2.08); normalize=minmax, positive_rate=0.65 (max I 2.33)
  - `lr_schedule, positive_rate`: lr_schedule=cosine, positive_rate=0.15 (max I 2.24); lr_schedule=cosine, positive_rate=0.5 (max I 2.59); lr_schedule=cosine, positive_rate=0.06 (max I 2.68)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=minmax (max I 2.6); lr_schedule=step, normalize=minmax (max I 2.6)
  - `normalize`: normalize=minmax (max I 2.63)
- 2 separate islands (no single-knob move joins them): normalize=minmax, positive_rate=0.15; normalize=minmax, positive_rate=0.86; normalize=minmax, positive_rate=0.1 | lr_schedule=cosine, positive_rate=0.15; lr_schedule=cosine, positive_rate=0.5; lr_schedule=cosine, positive_rate=0.06

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'lr_schedule': 'step', 'class_weight': 'balanced'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `positive_rate=0.86`, `normalize=minmax` | 5 | +7.1% | +0.0% | 3.6% |
| `positive_rate=0.1`, `normalize=minmax` | 5 | +11.9% | +0.0% | 6.0% |
| `normalize=minmax` | 6 | -14.9% | +0.0% | 7.4% |
| `lr_schedule=cosine`, `normalize=minmax` | 5 | -14.9% | +0.0% | 7.4% |
| `lr_schedule=step`, `normalize=minmax` | 5 | -14.9% | +0.0% | 7.4% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: invalid_value, The value 0.0 leads to math.log(0/(1-0)) = math.log(0) which raises a ValueError; positive_rate must be strictly between 0 and 1 to keep the logit computation defined; retried as `positive_rate=0.001`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `training_loop_bugs`, `RUN_TAG`, `aggregation_method`, `num_runs`, `SCALES`, `WEIGHTS`, `weight_init_scale`, `sigmoid_clamp`, `python_random_module`, `logit_bias_term`, `feature_generation_gaussian`, `balanced_accuracy_formula`, `label_noise_application`, `python_version`, `hardware_cpu`, `os_settings`, `--out`

## Provenance
- GapFinder commit: `f01fe3d9a0095f98d6304ad0543b917ca8e529eb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0008, sandbox reported $0.0000 (total $0.0008; this search; ledger extraction is included only if it shared the search's router)
