# Gap Report: test-v11-09

Artifact `mlbench` · generated 2026-10-14 22:20 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -35.4% | +3.9% | ±1.1% | `lr=2.5`, `normalize=minmax` |

## C1: test_accuracy (paper 0.7542)
**Fits but unsupported** · gap -35.4% → +3.9% · 53 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0107`, `B0193`, `B0194`, `B0195`, `B0196` (5 run(s) of the same config)
- Config: `lr` naive `0.05`, changed to `2.5`
- Config: `normalize` naive `none`, changed to `minmax`
- Command:

  Replay: fork checkpoint `237349c2-2ce0-42f2-9e8a-d6d1015f6afb` and run
  ```
  RUN_TAG=5b7e15bde33f "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 2.5 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.825, 0.7833, 0.7792, 0.7792, 0.8; gap after +3.9%; result checkpoint `d6d7ed30-0a12-4fbf-912b-b45cd1ee19c5`
- Effect: candidate 0.7833 minus naive 0.4875 = +0.2958, 95% bootstrap interval [+0.2467, +0.325] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.754 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7542 (headline claim)

### What did we measure?
- Naive median 0.4875 over 5 runs; repeats: 0.4833, 0.5375, 0.5375, 0.4875, 0.4833
- Spread: range 0.4833 to 0.5375, noise band ±0.0084 (2 x MAD), CV 5.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -35.4% (noise band ±1.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr` the gap is -21.0% (it comes back)
- PASS · Counterfactual (reversal test): without `normalize` the gap is -28.5% (it comes back)
- PASS · Held-out claim: C2: -33.0% to +9.8% (not worse beyond noise)
- FAIL · Evidence: `lr=2.5`: no evidence mentions '2.5'; it fits, but nothing says the authors used it
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2958 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `aggregation`, `CPU`, `memory`, `OS`, `Python_version`, `random_module`, `floating_point`, `num_features`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (22.82 noise units, gap +9.9%); `lr_schedule=cosine` (14.88 noise units, gap -18.8%); `lr_schedule=step` (6.45 noise units, gap -28.2%); `lr=0.01` (5.95 noise units, gap -28.7%); `lr=0.25` (5.95 noise units, gap -28.7%) (and 4 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr=2.5`, `normalize=zscore`: this claim +5.5%, mean |gap| 6.6% (5 runs)
  - `lr=0.0005`, `normalize=zscore`: this claim +5.5%, mean |gap| 6.6% (5 runs)
  - `class_weight=balanced`, `normalize=zscore`: this claim +4.4%, mean |gap| 6.8% (5 runs)

### History matching (every measured configuration, all claims together)
- 13 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr, normalize`: lr=2.5, normalize=zscore (max I 1.03); lr=0.0005, normalize=zscore (max I 1.09); lr=2.5, normalize=minmax (max I 1.25); lr=0.25, normalize=minmax (max I 1.44); +3 more
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 1.03); class_weight=balanced, normalize=zscore (max I 1.54)
  - `lr_schedule, normalize`: lr_schedule=step, normalize=zscore (max I 2.06)

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'normalize': 'minmax', 'lr': '0.0005'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr=2.5`, `normalize=zscore` | 5 | +5.5% | +7.6% | 6.6% |
| `lr=0.0005`, `normalize=zscore` | 5 | +5.5% | +7.6% | 6.6% |
| `class_weight=balanced`, `normalize=zscore` | 5 | +4.4% | +9.2% | 6.8% |
| `lr=2.5`, `normalize=minmax` | 5 | +3.9% | +9.8% | 6.8% |
| `lr=0.25`, `normalize=zscore` | 5 | +8.3% | +10.7% | 9.5% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `aggregation`, `CPU`, `memory`, `OS`, `Python_version`, `random_module`, `floating_point`, `num_features`, `--out`

## Provenance
- GapFinder commit: `e0f13d101585ad1609a15fbf67b70128f4cfffc8` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
