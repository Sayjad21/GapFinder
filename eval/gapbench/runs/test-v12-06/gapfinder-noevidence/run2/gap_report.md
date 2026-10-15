# Gap Report: test-v12-06

Artifact `mlbench` · generated 2026-10-15 08:15 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -30.3% | -0.5% | ±2.2% | `class_weight=balanced`, `normalize=minmax` |

## C1: test_accuracy (paper 0.7708)
**Fits but unsupported** · gap -30.3% → -0.5% · 61 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0104`, `B0189`, `B0190`, `B0191`, `B0192` (5 run(s) of the same config)
- Config: `class_weight` naive `none`, changed to `balanced`
- Config: `normalize` naive `none`, changed to `minmax`
- Command:

  Replay: fork checkpoint `2cc2891b-7fd9-4ad5-82bb-f3d2dee9507e` and run
  ```
  RUN_TAG=067d7708fcda "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight balanced --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7667, 0.7708, 0.7625, 0.7458, 0.7792; gap after -0.5%; result checkpoint `01d0c450-f401-4d3b-be07-43b56dc0a3a8`
- Effect: candidate 0.7667 minus naive 0.5375 = +0.2292, 95% bootstrap interval [+0.2008, +0.2709] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.771 test accuracy and 0.745 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7708 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5458, 0.5333, 0.4833, 0.5375, 0.5625
- Spread: range 0.4833 to 0.5625, noise band ±0.0166 (2 x MAD), CV 5.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -30.3% (noise band ±2.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `class_weight` the gap is -22.7% (it comes back)
- PASS · Counterfactual (reversal test): without `normalize` the gap is -29.2% (it comes back)
- PASS · Held-out claim: C2: -27.7% to +4.4% (not worse beyond noise)
- FAIL · Evidence: `class_weight=balanced`: evidence gate off: no evidence was looked for
- FAIL · Evidence: `normalize=minmax`: evidence gate off: no evidence was looked for
- PASS · Effect vs noise: candidate minus naive is +0.2292 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `SCALES`, `WEIGHTS`, `RUN_TAG`, `num_runs`, `aggregation_method`, `python_version`, `os`, `cpu_arch`, `memory_size`, `storage_type`, `out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (10.54 noise units, gap +7.6%); `lr_schedule=cosine` (4.77 noise units, gap -20.0%); `lr_schedule=step` (3.51 noise units, gap -22.7%); `positive_rate=0.15` (2.26 noise units, gap -25.4%)
- Near alternatives (closest across all claims):
  - `positive_rate=0.5`, `normalize=zscore`: this claim +2.2%, mean |gap| 4.0% (5 runs)
  - `class_weight=balanced`, `normalize=zscore`: this claim +2.2%, mean |gap| 4.0% (5 runs)
  - `positive_rate=0.15`, `normalize=zscore`: this claim +1.1%, mean |gap| 4.9% (5 runs)

### History matching (every measured configuration, all claims together)
- 13 of 59 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 0.74); class_weight=balanced, normalize=zscore (max I 1)
  - `normalize, positive_rate`: normalize=minmax, positive_rate=0.5 (max I 0.84); normalize=zscore, positive_rate=0.86 (max I 0.97); normalize=zscore, positive_rate=0.5 (max I 0.99); normalize=zscore, positive_rate=0.65 (max I 1.23); +1 more
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.55); lr_schedule=step, normalize=zscore (max I 1.55)
  - `normalize`: normalize=zscore (max I 1.56)
- 2 separate islands (no single-knob move joins them): class_weight=balanced, normalize=minmax; normalize=minmax, positive_rate=0.5; normalize=zscore, positive_rate=0.86 | lr_schedule=cosine, positive_rate=0.93; lr_schedule=cosine, positive_rate=0.1; lr_schedule=cosine, positive_rate=0.5

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'lr_schedule': 'cosine', 'positive_rate': '0.5'} for 'confirm-combo')
- evidence gate off: no evidence was checked, so this cannot be labelled Explained
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `class_weight=balanced`, `normalize=minmax` | 5 | -0.5% | +4.4% | 2.5% |
| `positive_rate=0.5`, `normalize=zscore` | 5 | +2.2% | +5.7% | 4.0% |
| `class_weight=balanced`, `normalize=zscore` | 5 | +2.2% | +5.9% | 4.0% |
| `positive_rate=0.15`, `normalize=zscore` | 5 | +1.1% | -8.7% | 4.9% |
| `positive_rate=0.86`, `normalize=zscore` | 5 | +5.4% | -4.9% | 5.1% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: invalid_value, The code computes math.log(positive_rate / (1 - positive_rate)). With positive_rate = 0.0 the argument becomes 0, causing a math domain error. A small positive value like 0.01 preserves the intent of a low positive rate while keeping the logarithm defined; retried as `positive_rate=0.01`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `SCALES`, `WEIGHTS`, `RUN_TAG`, `num_runs`, `aggregation_method`, `python_version`, `os`, `cpu_arch`, `memory_size`, `storage_type`, `out`

## Provenance
- GapFinder commit: `f01fe3d9a0095f98d6304ad0543b917ca8e529eb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0006, sandbox reported $0.0000 (total $0.0006; this search; ledger extraction is included only if it shared the search's router)
