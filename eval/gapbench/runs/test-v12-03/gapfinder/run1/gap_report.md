# Gap Report: test-v12-03

Artifact `mlbench` · generated 2026-10-15 07:19 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -29.8% | +0.0% | ±4.8% | `normalize=minmax`, `positive_rate=0.15` |

## C1: test_accuracy (paper 0.7)
**Fits but unsupported** · gap -29.8% → +0.0% · 59 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0091`, `B0143`, `B0144`, `B0145`, `B0146` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `positive_rate` naive `0.3`, changed to `0.15`
- Command:

  Replay: fork checkpoint `cffcf4b1-fdb8-4ca2-8b23-ef0b660c92b3` and run
  ```
  RUN_TAG=2b695f246713 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.15 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7, 0.7, 0.7, 0.7, 0.7; gap after +0.0%; result checkpoint `e0388669-7030-485c-baff-7a6548a50c63`
- Effect: candidate 0.7 minus naive 0.4917 = +0.2083, 95% bootstrap interval [+0.1475, +0.2217] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.700 test accuracy and 0.500 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7 (headline claim)

### What did we measure?
- Naive median 0.4917 over 5 runs; repeats: 0.5375, 0.475, 0.4833, 0.5625, 0.4917
- Spread: range 0.475 to 0.5625, noise band ±0.0334 (2 x MAD), CV 7.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -29.8% (noise band ±4.8% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -24.1% (it comes back)
- PASS · Counterfactual (reversal test): without `positive_rate` the gap is -14.9% (it comes back)
- PASS · Held-out claim: C2: -2.6% to +0.0% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- FAIL · Evidence: `positive_rate=0.15`: no evidence mentions '0.15'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2083 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (3.87 noise units, gap -11.3%); `normalize=zscore` (2.49 noise units, gap +17.9%); `positive_rate=0.5` (1.5 noise units, gap -22.6%); `class_weight=balanced` (1.5 noise units, gap -22.6%); `lr_schedule=step` (1.37 noise units, gap -23.2%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `normalize=minmax`: this claim -14.9%, mean |gap| 7.4% (5 runs)
  - `normalize=minmax`, `lr_schedule=cosine`: this claim -14.9%, mean |gap| 7.4% (5 runs)
  - `lr_schedule=step`, `normalize=minmax`: this claim -14.9%, mean |gap| 7.4% (5 runs)

### History matching (every measured configuration, all claims together)
- 18 of 57 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `normalize, positive_rate`: normalize=minmax, positive_rate=0.15 (max I 0); normalize=minmax, positive_rate=0.1 (max I 1.52); normalize=zscore, positive_rate=0.1 (max I 2.28); normalize=zscore, positive_rate=0.93 (max I 2.59)
  - `lr_schedule, positive_rate`: lr_schedule=cosine, positive_rate=0.06 (max I 1.68); lr_schedule=cosine, positive_rate=0.86 (max I 2.14); lr_schedule=step, positive_rate=0.5 (max I 2.28)
  - `normalize`: normalize=minmax (max I 2.43)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=minmax (max I 2.43); lr_schedule=step, normalize=minmax (max I 2.43)
- 4 separate islands (no single-knob move joins them): normalize=minmax, positive_rate=0.15; normalize=minmax, positive_rate=0.1; normalize=zscore, positive_rate=0.1 | lr_schedule=cosine, positive_rate=0.06; lr_schedule=cosine, positive_rate=0.86; lr_schedule=step, positive_rate=0.5 | class_weight=balanced, lr_schedule=step | class_weight=balanced, positive_rate=0.1

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'lr_schedule': 'step', 'normalize': 'zscore'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax`, `positive_rate=0.15` | 5 | +0.0% | +0.0% | 0.0% |
| `normalize=minmax` | 5 | -14.9% | +0.0% | 7.4% |
| `normalize=minmax`, `lr_schedule=cosine` | 5 | -14.9% | +0.0% | 7.4% |
| `lr_schedule=step`, `normalize=minmax` | 5 | -14.9% | +0.0% | 7.4% |
| `normalize=minmax`, `positive_rate=0.93` | 5 | +17.9% | +0.0% | 8.9% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: invalid_value, The code computes log(positive_rate/(1-positive_rate)), which is undefined for positive_rate=0 (log(0)). A small positive value like 0.001 preserves the intent of a low positive rate while keeping the expression defined; retried as `positive_rate=0.001`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `f01fe3d9a0095f98d6304ad0543b917ca8e529eb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0426, sandbox reported $0.0000 (total $0.0426; this search; ledger extraction is included only if it shared the search's router)
