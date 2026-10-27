# Gap Report: test-v12-03

Artifact `mlbench` · generated 2026-10-16 01:28 · 142 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -19.6% | -8.3% | ±4.8% | `normalize=minmax`, `positive_rate=0.2` |

## C1: test_accuracy (paper 0.7)
**Fits but unsupported** · gap -19.6% → -8.3% · 53 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0089`, `B0107`, `B0123`, `B0124`, `B0125` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `positive_rate` naive `0.3`, changed to `0.2`
- Command:

  Replay: fork checkpoint `736dacb2-4c16-458c-b387-d13338da9727` and run
  ```
  RUN_TAG=83ac0accf762 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.2 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.6417, 0.6417, 0.6417, 0.6417, 0.6417; gap after -8.3%; result checkpoint `ad749a87-ebf4-4920-9141-99e113c5139e`
- Effect: candidate 0.6417 minus naive 0.5625 = +0.0792, 95% bootstrap interval [+0.065, +0.1258] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.700 test accuracy and 0.500 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7 (headline claim)

### What did we measure?
- Naive median 0.5625 over 5 runs; repeats: 0.5667, 0.5792, 0.5625, 0.5042, 0.5375
- Spread: range 0.5042 to 0.5792, noise band ±0.0334 (2 x MAD), CV 5.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -19.6% (noise band ±4.8% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -27.1% (it comes back)
- PASS · Counterfactual (reversal test): without `positive_rate` the gap is -14.9% (it comes back)
- PASS · Held-out claim: C2: +12.3% to +0.0% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- FAIL · Evidence: `positive_rate=0.2`: no evidence mentions '0.2'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.0792 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `training_loop_bugs`, `RUN_TAG`, `aggregation_method`, `num_runs`, `SCALES`, `WEIGHTS`, `weight_init_scale`, `sigmoid_clamp`, `python_random_module`, `logit_bias_term`, `feature_generation_gaussian`, `balanced_accuracy_formula`, `label_noise_application`, `python_version`, `hardware_cpu`, `os_settings`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (1.62 noise units, gap -11.9%)
- Near alternatives (closest across all claims):
  - `positive_rate=0.1`, `normalize=minmax`: this claim +11.9%, mean |gap| 6.0% (2 runs)
  - `positive_rate=0.4`, `normalize=minmax`: this claim -15.5%, mean |gap| 12.9% (2 runs)
  - `positive_rate=0.06`: this claim -27.7%, mean |gap| 14.2% (6 runs)

### History matching (every measured configuration, all claims together)
- 12 of 52 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `normalize, positive_rate`: normalize=minmax, positive_rate=0.2 (max I 1.46); normalize=minmax, positive_rate=0.1 (max I 1.93); normalize=minmax, positive_rate=0.65 (max I 2.34); normalize=minmax, positive_rate=0.4 (max I 2.51); +1 more
  - `normalize`: normalize=minmax (max I 2.17)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=minmax (max I 2.17); lr_schedule=step, normalize=minmax (max I 2.17)
  - `lr_schedule, positive_rate`: lr_schedule=step, positive_rate=0.65 (max I 2.46); lr_schedule=cosine, positive_rate=0.03 (max I 2.78)
- 4 separate islands (no single-knob move joins them): normalize=minmax, positive_rate=0.2; normalize=minmax, positive_rate=0.1; normalize=minmax | class_weight=balanced, positive_rate=0.65; class_weight=balanced, positive_rate=0.2 | lr_schedule=step, positive_rate=0.65 | lr_schedule=cosine, positive_rate=0.03
- Equally good values: `positive_rate` in {0.1, 0.2}

Notes:
- equally good values within one noise band (measured): positive_rate in {0.1, 0.2}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `positive_rate=0.2`, `normalize=minmax` | 5 | -8.3% | +0.0% | 4.2% |
| `positive_rate=0.1`, `normalize=minmax` | 2 | +11.9% | +0.0% | 6.0% |
| `positive_rate=0.4`, `normalize=minmax` | 2 | -15.5% | +10.3% | 12.9% |
| `positive_rate=0.06` | 6 | -27.7% | +0.7% | 14.2% |
| `positive_rate=0.2` | 6 | -27.1% | +1.9% | 14.5% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `training_loop_bugs`, `RUN_TAG`, `aggregation_method`, `num_runs`, `SCALES`, `WEIGHTS`, `weight_init_scale`, `sigmoid_clamp`, `python_random_module`, `logit_bias_term`, `feature_generation_gaussian`, `balanced_accuracy_formula`, `label_noise_application`, `python_version`, `hardware_cpu`, `os_settings`, `--out`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
