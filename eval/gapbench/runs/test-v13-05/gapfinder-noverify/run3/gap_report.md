# Gap Report: test-v13-05

Artifact `mlbench` · generated 2026-10-16 00:44 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Explained | -39.0% | +0.5% | ±2.1% | `normalize=zscore`, `class_weight=balanced` |

## C1: test_accuracy (paper 0.7792)
**Explained** · gap -39.0% → +0.5% · 49 hypotheses tested
> Interacting factors: these changes close the gap only together, and every check passes

### Which experiment changed it?
- Branch: `B0131`, `B0152`, `B0177`, `B0178`, `B0179` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Config: `class_weight` naive `none`, changed to `balanced`
- Command:

  Replay: fork checkpoint `1dd6ca8b-742a-4e07-b008-255b06d48ff7` and run
  ```
  RUN_TAG=542c58215edf "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight balanced --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7875, 0.7875, 0.7833, 0.7833, 0.7833; gap after +0.5%; result checkpoint `1fc9ce34-591b-4367-ad81-9ca4452414e5`
- Effect: candidate 0.7833 minus naive 0.475 = +0.3083, 95% bootstrap interval [+0.2625, +0.3191] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.779 test accuracy and 0.750 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7792 (headline claim)

### What did we measure?
- Naive median 0.475 over 5 runs; repeats: 0.5333, 0.4833, 0.475, 0.4667, 0.4667
- Spread: range 0.4667 to 0.5333, noise band ±0.0166 (2 x MAD), CV 5.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -39.0% (noise band ±2.1% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is +0.3083 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (8.54 noise units, gap -20.9%); `epochs=75` (7.78 noise units, gap -22.5%); `normalize=minmax` (7.28 noise units, gap -23.5%); `epochs=150` (6.28 noise units, gap -25.7%); `epochs=2` (4.52 noise units, gap -29.4%) (and 7 more in the JSON)
- Near alternatives (closest across all claims):
  - `normalize=minmax`, `epochs=150`: this claim -0.5%, mean |gap| 0.9% (5 runs)
  - `normalize=minmax`, `class_weight=balanced`: this claim -1.6%, mean |gap| 2.6% (5 runs)
  - `normalize=zscore`, `epochs=150`: this claim +5.3%, mean |gap| 6.1% (5 runs)

### History matching (every measured configuration, all claims together)
- 14 of 49 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `epochs, normalize`: epochs=150, normalize=minmax (max I 0.28); epochs=150, normalize=zscore (max I 1.22); epochs=75, normalize=zscore (max I 1.27)
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 0.61); class_weight=balanced, normalize=zscore (max I 0.85)
  - `epochs, lr_schedule`: epochs=150, lr_schedule=cosine (max I 1.33)
  - `normalize`: normalize=zscore (max I 1.35)
  - `label_noise, normalize`: label_noise=0.025, normalize=zscore (max I 1.38)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.4); lr_schedule=step, normalize=zscore (max I 1.4)
- 2 separate islands (no single-knob move joins them): epochs=150, normalize=minmax; class_weight=balanced, normalize=minmax; class_weight=balanced, normalize=zscore | epochs=150, lr_schedule=cosine; epochs=75, lr_schedule=cosine; epochs=75, lr_schedule=step

Notes:
- stopped early: run budget of 200 reached (wanted 3 more run(s) of {'lr_schedule': 'cosine', 'epochs': '150'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax`, `epochs=150` | 5 | -0.5% | -1.3% | 0.9% |
| `normalize=zscore`, `class_weight=balanced` | 5 | +0.5% | +4.7% | 2.6% |
| `normalize=minmax`, `class_weight=balanced` | 5 | -1.6% | +3.7% | 2.6% |
| `normalize=zscore`, `epochs=150` | 5 | +5.3% | +6.9% | 6.1% |
| `normalize=zscore` | 6 | +5.9% | +7.6% | 6.7% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `out`

## Provenance
- GapFinder commit: `e9c31fd1405f5c8aae4bd880eadcdc8d491fad02` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
