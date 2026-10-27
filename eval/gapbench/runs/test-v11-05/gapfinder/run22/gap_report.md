# Gap Report: test-v11-05

Artifact `mlbench` · generated 2026-10-14 21:13 · 197 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -26.3% | -0.6% | ±0.7% | `epochs=75`, `normalize=minmax` |

## C1: test_accuracy (paper 0.7292)
**Fits but unsupported** · gap -26.3% → -0.6% · 54 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0077`, `B0194`, `B0195`, `B0196`, `B0197` (5 run(s) of the same config)
- Config: `epochs` naive `15`, changed to `75`
- Config: `normalize` naive `none`, changed to `minmax`
- Command:

  Replay: fork checkpoint `d9bb8179-1c04-4921-be2a-6774071c9fd2` and run
  ```
  RUN_TAG=4ea3ec30db1d "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 75 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7125, 0.725, 0.7333, 0.7333, 0.7125; gap after -0.6%; result checkpoint `abe957ce-d57e-4e78-998a-c9f7c1ad0875`
- Effect: candidate 0.725 minus naive 0.5375 = +0.1875, 95% bootstrap interval [+0.1792, +0.2483] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.729 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7292 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5375, 0.5375, 0.5375, 0.475, 0.475
- Spread: range 0.475 to 0.5375, noise band ±0.005375 (2 x MAD), CV 6.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -26.3% (noise band ±0.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `epochs` the gap is -18.3% (it comes back)
- PASS · Counterfactual (reversal test): without `normalize` the gap is -31.4% (it comes back)
- PASS · Held-out claim: C2: -19.5% to -0.8% (not worse beyond noise)
- FAIL · Evidence: `epochs=75`: no evidence mentions '75'; it fits, but nothing says the authors used it
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.1875 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `epochs=750` (22.47 noise units, gap -9.7%); `normalize=zscore` (17.06 noise units, gap +13.7%); `lr_schedule=cosine` (13.95 noise units, gap -16.0%); `epochs=20` (6.2 noise units, gap -21.7%); `epochs=8` (1.54 noise units, gap -25.2%)
- Near alternatives (closest across all claims):
  - `epochs=75`, `lr_schedule=cosine`: this claim -6.9%, mean |gap| 3.8% (5 runs)
  - `lr_schedule=step`, `epochs=750`: this claim +4.0%, mean |gap| 6.0% (5 runs)
  - `class_weight=balanced`, `normalize=minmax`: this claim +2.3%, mean |gap| 8.3% (5 runs)

### History matching (every measured configuration, all claims together)
- 14 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `epochs, normalize`: epochs=75, normalize=minmax (max I 0.17)
  - `epochs, lr_schedule`: epochs=750, lr_schedule=step (max I 0.83); epochs=75, lr_schedule=cosine (max I 1.21); epochs=750, lr_schedule=cosine (max I 2.13); epochs=20, lr_schedule=cosine (max I 2.46); +1 more
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 2.18); class_weight=balanced, normalize=zscore (max I 2.67)
  - `epochs`: epochs=750 (max I 2.35)
  - `lr_schedule`: lr_schedule=cosine (max I 2.45)
- 4 separate islands (no single-knob move joins them): epochs=750, lr_schedule=step; epochs=75, lr_schedule=cosine; epochs=750, lr_schedule=cosine | class_weight=balanced, normalize=minmax; class_weight=balanced, normalize=zscore | epochs=75, normalize=minmax | epochs=1, normalize=zscore

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'normalize': 'minmax', 'lr_schedule': 'step'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `epochs=75`, `normalize=minmax` | 5 | -0.6% | -0.8% | 0.7% |
| `epochs=75`, `lr_schedule=cosine` | 5 | -6.9% | -0.8% | 3.8% |
| `lr_schedule=step`, `epochs=750` | 5 | +4.0% | +8.1% | 6.0% |
| `class_weight=balanced`, `normalize=minmax` | 5 | +2.3% | +14.4% | 8.3% |
| `lr_schedule=cosine` | 6 | -14.0% | -6.9% | 10.5% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `958fafed572bbbf30aedd8af86ba04a1fefc05c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
