# Gap Report: test-v12-06

Artifact `mlbench` · generated 2026-10-15 08:15 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -36.8% | -1.1% | ±5.4% | `normalize=minmax`, `class_weight=balanced` |

## C1: test_accuracy (paper 0.7708)
**Fits but unsupported** · gap -36.8% → -1.1% · 65 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0066`, `B0155`, `B0156`, `B0157`, `B0158` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `class_weight` naive `none`, changed to `balanced`
- Command:

  Replay: fork checkpoint `21eda65f-4652-43db-bff6-a3cb205d887b` and run
  ```
  RUN_TAG=75d14422d673 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight balanced --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7708, 0.775, 0.7458, 0.7625, 0.7375; gap after -1.1%; result checkpoint `8d68ac13-e394-425f-b90b-e0182dccb6a1`
- Effect: candidate 0.7625 minus naive 0.4875 = +0.275, 95% bootstrap interval [+0.2141, +0.2908] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.771 test accuracy and 0.745 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7708 (headline claim)

### What did we measure?
- Naive median 0.4875 over 5 runs; repeats: 0.4875, 0.4667, 0.5375, 0.4833, 0.5375
- Spread: range 0.4667 to 0.5375, noise band ±0.0416 (2 x MAD), CV 6.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -36.8% (noise band ±5.4% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -37.0% (it comes back)
- PASS · Counterfactual (reversal test): without `class_weight` the gap is -22.7% (it comes back)
- PASS · Held-out claim: C2: -35.0% to +4.4% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- FAIL · Evidence: `class_weight=balanced`: no evidence mentions 'balanced'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.275 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `SCALES`, `WEIGHTS`, `RUN_TAG`, `num_runs`, `aggregation_method`, `python_version`, `os`, `cpu_arch`, `memory_size`, `storage_type`, `out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (5.41 noise units, gap +7.6%); `lr_schedule=cosine` (3 noise units, gap -20.5%); `lr_schedule=step` (2 noise units, gap -25.9%); `positive_rate=0.65` (1.4 noise units, gap -29.2%); `positive_rate=0.1` (1.3 noise units, gap -29.7%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `normalize=zscore`, `class_weight=balanced`: this claim +1.6%, mean |gap| 3.5% (5 runs)
  - `normalize=zscore`, `positive_rate=0.65`: this claim +6.5%, mean |gap| 7.4% (5 runs)
  - `normalize=zscore`, `weight_decay=1e-3`: this claim +7.0%, mean |gap| 7.7% (5 runs)

### History matching (every measured configuration, all claims together)
- 13 of 63 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 0.66); class_weight=balanced, normalize=zscore (max I 0.89)
  - `normalize, positive_rate`: normalize=zscore, positive_rate=0.5 (max I 0.76); normalize=zscore, positive_rate=0.86 (max I 0.79); normalize=zscore, positive_rate=0.15 (max I 1.41); normalize=zscore, positive_rate=0.65 (max I 1.42)
  - `normalize, weight_decay`: normalize=zscore, weight_decay=1e-3 (max I 1.4); normalize=zscore, weight_decay=1e-4 (max I 1.43)
  - `normalize`: normalize=zscore (max I 1.47)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.47)
- 2 separate islands (no single-knob move joins them): class_weight=balanced, normalize=minmax; normalize=zscore, positive_rate=0.5; normalize=zscore, positive_rate=0.86 | lr_schedule=cosine, positive_rate=0.93

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'positive_rate': '0.65', 'weight_decay': '1e-3'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax`, `class_weight=balanced` | 5 | -1.1% | +4.4% | 2.7% |
| `normalize=zscore`, `class_weight=balanced` | 5 | +1.6% | +5.4% | 3.5% |
| `normalize=zscore`, `positive_rate=0.65` | 5 | +6.5% | +8.4% | 7.4% |
| `normalize=zscore`, `weight_decay=1e-3` | 5 | +7.0% | +8.3% | 7.7% |
| `normalize=zscore` | 6 | +7.6% | +8.8% | 8.2% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: invalid_value, The code computes log(positive_rate / (1 - positive_rate)). With positive_rate = 0.0, the argument becomes 0, causing a math domain error because log is undefined for non-positive values. A valid positive_rate must be strictly between 0 and 1; a small value like 0.001 preserves the intent of a very low positive rate while avoiding the error; retried as `positive_rate=0.001`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `SCALES`, `WEIGHTS`, `RUN_TAG`, `num_runs`, `aggregation_method`, `python_version`, `os`, `cpu_arch`, `memory_size`, `storage_type`, `out`

## Provenance
- GapFinder commit: `f01fe3d9a0095f98d6304ad0543b917ca8e529eb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0007, sandbox reported $0.0000 (total $0.0007; this search; ledger extraction is included only if it shared the search's router)
