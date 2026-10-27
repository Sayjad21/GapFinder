# Gap Report: test-v11-09

Artifact `mlbench` · generated 2026-10-14 22:37 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -35.4% | +1.1% | ±5.5% | `normalize=zscore`, `lr=0.0005` |

## C1: test_accuracy (paper 0.7542)
**Fits but unsupported** · gap -35.4% → +1.1% · 54 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0076`, `B0141`, `B0142`, `B0143`, `B0144` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Config: `lr` naive `0.05`, changed to `0.0005`
- Command:

  Replay: fork checkpoint `36351f14-fc62-491c-804a-be53a2d923b5` and run
  ```
  RUN_TAG=82a92778fd32 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.0005 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.725, 0.75, 0.7625, 0.7833, 0.8; gap after +1.1%; result checkpoint `2c16b969-4d5b-49db-adcb-283f8272dfc7`
- Effect: candidate 0.7625 minus naive 0.4875 = +0.275, 95% bootstrap interval [+0.2125, +0.3133] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.754 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7542 (headline claim)

### What did we measure?
- Naive median 0.4875 over 5 runs; repeats: 0.4875, 0.4667, 0.5375, 0.4667, 0.5417
- Spread: range 0.4667 to 0.5417, noise band ±0.0416 (2 x MAD), CV 7.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -35.4% (noise band ±5.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -33.7% (it comes back)
- PASS · Counterfactual (reversal test): without `lr` the gap is +9.4% (it comes back)
- PASS · Held-out claim: C2: -33.0% to +3.0% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- FAIL · Evidence: `lr=0.0005`: no evidence mentions '0.0005'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.275 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (3.31 noise units, gap -17.1%); `normalize=minmax` (2.6 noise units, gap -21.0%); `lr_schedule=step` (1.9 noise units, gap -24.9%); `lr=0.01` (1.8 noise units, gap -25.4%); `lr=0.1` (1.5 noise units, gap -27.1%) (and 3 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr=2.5`, `normalize=zscore`: this claim +3.3%, mean |gap| 4.9% (5 runs)
  - `lr=2.5`, `normalize=minmax`: this claim +3.3%, mean |gap| 5.2% (5 runs)
  - `normalize=zscore`, `class_weight=balanced`: this claim +3.9%, mean |gap| 6.3% (5 runs)

### History matching (every measured configuration, all claims together)
- 14 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr, normalize`: lr=2.5, normalize=minmax (max I 0.38); lr=0.0005, normalize=zscore (max I 0.47); lr=2.5, normalize=zscore (max I 1.06); lr=0.005, normalize=zscore (max I 1.86); +2 more
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 1.19); class_weight=balanced, normalize=zscore (max I 1.39)
  - `normalize`: normalize=zscore (max I 1.91)
  - `lr, lr_schedule, normalize`: lr=0.1, lr_schedule=cosine, normalize=zscore (max I 1.93)

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'normalize': 'minmax', 'class_weight': 'balanced'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore`, `lr=0.0005` | 5 | +1.1% | +3.0% | 2.1% |
| `lr=2.5`, `normalize=zscore` | 5 | +3.3% | +6.6% | 4.9% |
| `lr=2.5`, `normalize=minmax` | 5 | +3.3% | +7.2% | 5.2% |
| `normalize=zscore`, `class_weight=balanced` | 5 | +3.9% | +8.7% | 6.3% |
| `normalize=zscore` | 6 | +9.4% | +11.7% | 10.5% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `e0f13d101585ad1609a15fbf67b70128f4cfffc8` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
