# Gap Report: test-v13-05

Artifact `mlbench` · generated 2026-10-16 01:36 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -37.4% | +0.5% | ±1.1% | `class_weight=balanced`, `normalize=zscore` |

## C1: test_accuracy (paper 0.7792)
**Fits but unsupported** · gap -37.4% → +0.5% · 48 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0135`, `B0152`, `B0175`, `B0176`, `B0177` (5 run(s) of the same config)
- Config: `class_weight` naive `none`, changed to `balanced`
- Config: `normalize` naive `none`, changed to `zscore`
- Command:

  Replay: fork checkpoint `d71327fc-f070-4201-a127-9dba602c3b01` and run
  ```
  RUN_TAG=fe1404f53001 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight balanced --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7833, 0.7833, 0.7833, 0.7875, 0.7833; gap after +0.5%; result checkpoint `65d591ef-dc18-4228-b916-ffe76194410d`
- Effect: candidate 0.7833 minus naive 0.4875 = +0.2958, 95% bootstrap interval [+0.2492, +0.3141] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.779 test accuracy and 0.750 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7792 (headline claim)

### What did we measure?
- Naive median 0.4875 over 5 runs; repeats: 0.4875, 0.5458, 0.4875, 0.4667, 0.4833
- Spread: range 0.4667 to 0.5458, noise band ±0.0084 (2 x MAD), CV 6.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -37.4% (noise band ±1.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `class_weight` the gap is +6.4% (it comes back)
- PASS · Counterfactual (reversal test): without `normalize` the gap is -31.0% (it comes back)
- PASS · Held-out claim: C2: -35.5% to +4.7% (not worse beyond noise)
- PASS · Evidence: `class_weight=balanced`: code evidence at train.py:75: 'cw = {1: 0.5 / pos, 0: 0.5 / (1 - pos)} if a.class_weight == "balanced" else {1: 1.0, 0: 1.0}'
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2958 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `number_of_runs`, `aggregation_method`, `SCALES`, `WEIGHTS`, `shuffling_seed_generation`, `out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (16.87 noise units, gap -19.3%); `normalize=minmax` (12.89 noise units, gap -23.5%); `label_noise=0.005` (8.43 noise units, gap -28.3%); `epochs=10` (7.94 noise units, gap -28.9%); `epochs=750` (7.44 noise units, gap -29.4%) (and 15 more in the JSON)
- Near alternatives (closest across all claims):
  - `label_noise=0.905`, `normalize=zscore`: this claim +0.5%, mean |gap| 1.2% (5 runs)
  - `lr_schedule=cosine`, `epochs=750`: this claim +1.6%, mean |gap| 1.4% (5 runs)
  - `normalize=minmax`, `class_weight=balanced`: this claim -3.2%, mean |gap| 3.1% (5 runs)

### History matching (every measured configuration, all claims together)
- 13 of 48 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `label_noise, normalize`: label_noise=0.905, normalize=zscore (max I 0.31); label_noise=0.981, normalize=zscore (max I 1.21); label_noise=0.005, normalize=zscore (max I 1.34)
  - `epochs, lr_schedule`: epochs=750, lr_schedule=cosine (max I 0.32)
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 0.59); class_weight=balanced, normalize=zscore (max I 0.82)
  - `epochs, normalize`: epochs=750, normalize=minmax (max I 1.23); epochs=750, normalize=zscore (max I 1.31)
  - `lr_schedule, normalize`: lr_schedule=step, normalize=zscore (max I 1.28)
  - `normalize`: normalize=zscore (max I 1.37)
- 3 separate islands (no single-knob move joins them): label_noise=0.905, normalize=zscore; class_weight=balanced, normalize=minmax; class_weight=balanced, normalize=zscore | epochs=750, lr_schedule=cosine | label_noise=0.005, lr_schedule=cosine

Notes:
- stopped early: run budget of 200 reached (wanted 3 more run(s) of {'normalize': 'zscore', 'lr_schedule': 'step'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `label_noise=0.905`, `normalize=zscore` | 5 | +0.5% | +1.8% | 1.2% |
| `lr_schedule=cosine`, `epochs=750` | 5 | +1.6% | +1.2% | 1.4% |
| `class_weight=balanced`, `normalize=zscore` | 5 | +0.5% | +4.7% | 2.6% |
| `normalize=minmax`, `class_weight=balanced` | 5 | -3.2% | +3.0% | 3.1% |
| `label_noise=0.981`, `normalize=zscore` | 5 | +5.3% | +6.7% | 6.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `number_of_runs`, `aggregation_method`, `SCALES`, `WEIGHTS`, `shuffling_seed_generation`, `out`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
