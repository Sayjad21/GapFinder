# Gap Report: test-v11-09

Artifact `mlbench` · generated 2026-10-14 12:06 · 197 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Explained | -35.4% | +1.7% | ±5.5% | `class_weight=balanced`, `normalize=minmax` |

## C1: test_accuracy (paper 0.7542)
**Explained** · gap -35.4% → +1.7% · 49 hypotheses tested
> Interacting factors: these changes close the gap only together, and every check passes

### Which experiment changed it?
- Branch: `B0072`, `B0170`, `B0171`, `B0172`, `B0173` (5 run(s) of the same config)
- Config: `class_weight` naive `none`, changed to `balanced`
- Config: `normalize` naive `none`, changed to `minmax`
- Command:

  Replay: fork checkpoint `47110295-3940-4068-8e07-695faa92c45a` and run
  ```
  RUN_TAG=63e819ab084e "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight balanced --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7667, 0.7417, 0.7708, 0.7417, 0.7875; gap after +1.7%; result checkpoint `16876c0c-75b4-49a1-af3b-c41c567f8eda`
- Effect: candidate 0.7667 minus naive 0.4875 = +0.2792, 95% bootstrap interval [+0.2042, +0.2958] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.754 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7542 (headline claim)

### What did we measure?
- Naive median 0.4875 over 5 runs; repeats: 0.4667, 0.4875, 0.4875, 0.5375, 0.5625
- Spread: range 0.4667 to 0.5625, noise band ±0.0416 (2 x MAD), CV 7.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -35.4% (noise band ±5.5% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is +0.2792 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (4.61 noise units, gap +9.9%); `lr_schedule=cosine` (3.2 noise units, gap -17.7%); `lr=0.01` (1.2 noise units, gap -28.7%); `lr=0.005` (1.2 noise units, gap -28.7%); `lr=0.905` (1.1 noise units, gap -29.3%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `class_weight=balanced`, `normalize=zscore`: this claim +3.9%, mean |gap| 6.3% (5 runs)
  - `lr=0.905`, `normalize=minmax`: this claim +4.4%, mean |gap| 6.3% (5 runs)
  - `normalize=zscore`, `lr=0.905`: this claim +9.4%, mean |gap| 10.1% (5 runs)

### History matching (every measured configuration, all claims together)
- 13 of 49 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr, normalize`: lr=0.905, normalize=minmax (max I 1.13); lr=0.005, normalize=zscore (max I 1.73); lr=0.1, normalize=zscore (max I 1.81); lr=0.905, normalize=zscore (max I 1.83); +2 more
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 1.16); class_weight=balanced, normalize=zscore (max I 1.4)
  - `normalize`: normalize=zscore (max I 1.92)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.92)
- 2 separate islands (no single-knob move joins them): lr=0.905, normalize=minmax; class_weight=balanced, normalize=minmax; class_weight=balanced, normalize=zscore | lr=0.905, lr_schedule=cosine; lr=0.1, lr_schedule=cosine

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'lr': '0.1', 'class_weight': 'balanced'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `class_weight=balanced`, `normalize=minmax` | 5 | +1.7% | +7.2% | 4.4% |
| `class_weight=balanced`, `normalize=zscore` | 5 | +3.9% | +8.7% | 6.3% |
| `lr=0.905`, `normalize=minmax` | 5 | +4.4% | +8.2% | 6.3% |
| `normalize=zscore`, `lr=0.905` | 5 | +9.4% | +10.8% | 10.1% |
| `normalize=zscore`, `lr=0.01` | 5 | +9.4% | +11.4% | 10.4% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `b05f7288e1a4df8af69bb0b5e7633827b4cb46c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
