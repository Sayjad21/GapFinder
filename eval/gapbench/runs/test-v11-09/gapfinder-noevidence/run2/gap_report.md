# Gap Report: test-v11-09

Artifact `mlbench` · generated 2026-10-14 12:06 · 198 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -35.9% | +1.7% | ±2.2% | `class_weight=balanced`, `normalize=minmax` |

## C1: test_accuracy (paper 0.7542)
**Fits but unsupported** · gap -35.9% → +1.7% · 49 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0081`, `B0179`, `B0180`, `B0181`, `B0182` (5 run(s) of the same config)
- Config: `class_weight` naive `none`, changed to `balanced`
- Config: `normalize` naive `none`, changed to `minmax`
- Command:

  Replay: fork checkpoint `a1a1db72-5d48-4efe-a40d-fb60bda9b9cd` and run
  ```
  RUN_TAG=f5ae7acc7fc0 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight balanced --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7583, 0.7667, 0.7667, 0.775, 0.7708; gap after +1.7%; result checkpoint `c7b1fa9d-df5c-4dae-a63b-abfe49fb73de`
- Effect: candidate 0.7667 minus naive 0.4833 = +0.2834, 95% bootstrap interval [+0.2008, +0.2917] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.754 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7542 (headline claim)

### What did we measure?
- Naive median 0.4833 over 5 runs; repeats: 0.5708, 0.4833, 0.475, 0.4833, 0.5625
- Spread: range 0.475 to 0.5708, noise band ±0.0166 (2 x MAD), CV 9.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -35.9% (noise band ±2.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `class_weight` the gap is -21.0% (it comes back)
- PASS · Counterfactual (reversal test): without `normalize` the gap is -31.2% (it comes back)
- PASS · Held-out claim: C2: -33.7% to +7.9% (not worse beyond noise)
- FAIL · Evidence: `class_weight=balanced`: evidence gate off: no evidence was looked for
- FAIL · Evidence: `normalize=minmax`: evidence gate off: no evidence was looked for
- PASS · Effect vs noise: candidate minus naive is +0.2834 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (11.8 noise units, gap +9.9%); `lr_schedule=cosine` (8.54 noise units, gap -17.1%); `lr_schedule=step` (5.02 noise units, gap -24.9%); `lr=0.905` (4.77 noise units, gap -25.4%); `lr=0.1` (3.27 noise units, gap -28.7%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr=0.905`, `normalize=minmax`: this claim +5.0%, mean |gap| 5.4% (5 runs)
  - `normalize=zscore`, `class_weight=balanced`: this claim +3.9%, mean |gap| 6.3% (5 runs)
  - `normalize=zscore`, `lr=0.905`: this claim +7.7%, mean |gap| 8.9% (5 runs)

### History matching (every measured configuration, all claims together)
- 17 of 49 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr, normalize`: lr=0.905, normalize=minmax (max I 0.8); lr=0.905, normalize=zscore (max I 1.56); lr=0.005, normalize=zscore (max I 1.69); lr=0.1, normalize=zscore (max I 1.76); +2 more
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 1.24); class_weight=balanced, normalize=zscore (max I 1.33)
  - `lr_schedule, normalize`: lr_schedule=step, normalize=zscore (max I 1.8); lr_schedule=cosine, normalize=zscore (max I 1.82)

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'lr_schedule': 'step', 'lr': '0.01'} for 'confirm-combo')
- evidence gate off: no evidence was checked, so this cannot be labelled Explained
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `class_weight=balanced`, `normalize=minmax` | 5 | +1.7% | +7.9% | 4.8% |
| `lr=0.905`, `normalize=minmax` | 5 | +5.0% | +5.8% | 5.4% |
| `normalize=zscore`, `class_weight=balanced` | 5 | +3.9% | +8.7% | 6.3% |
| `normalize=zscore`, `lr=0.905` | 5 | +7.7% | +10.0% | 8.9% |
| `normalize=zscore`, `lr=0.005` | 5 | +9.4% | +11.4% | 10.4% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `b05f7288e1a4df8af69bb0b5e7633827b4cb46c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
