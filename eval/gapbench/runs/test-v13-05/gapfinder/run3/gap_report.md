# Gap Report: test-v13-05

Artifact `mlbench` · generated 2026-10-16 00:43 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -31.0% | -0.5% | ±1.1% | `class_weight=balanced`, `normalize=minmax` |

## C1: test_accuracy (paper 0.7792)
**Fits but unsupported** · gap -31.0% → -0.5% · 66 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0131`, `B0153`, `B0187`, `B0188`, `B0189` (5 run(s) of the same config)
- Config: `class_weight` naive `none`, changed to `balanced`
- Config: `normalize` naive `none`, changed to `minmax`
- Command:

  Replay: fork checkpoint `e87df6bd-c2d4-46de-a669-593febdb8bce` and run
  ```
  RUN_TAG=2e7df0ff76dc "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight balanced --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.8, 0.775, 0.7625, 0.7708, 0.775; gap after -0.5%; result checkpoint `37ad52d9-59a3-4846-a995-b3c9935edf72`
- Effect: candidate 0.775 minus naive 0.5375 = +0.2375, 95% bootstrap interval [+0.215, +0.2991] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.779 test accuracy and 0.750 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7792 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.4667, 0.5333, 0.5625, 0.5375, 0.5375
- Spread: range 0.4667 to 0.5625, noise band ±0.0084 (2 x MAD), CV 6.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -31.0% (noise band ±1.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `class_weight` the gap is -23.5% (it comes back)
- PASS · Counterfactual (reversal test): without `normalize` the gap is -32.9% (it comes back)
- PASS · Held-out claim: C2: -27.7% to +5.3% (not worse beyond noise)
- PASS · Evidence: `class_weight=balanced`: paper evidence at p.1: 'A plain logistic-regression baseline reaches 0.779 test accuracy and 0.750 balanced accuracy on a synthetic screening ta'
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2375 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (22.82 noise units, gap +6.4%); `epochs=750` (17.86 noise units, gap -11.8%); `lr_schedule=cosine` (9.92 noise units, gap -20.3%); `epochs=75` (2.48 noise units, gap -28.3%); `epochs=2` (1.99 noise units, gap -28.9%)
- Near alternatives (closest across all claims):
  - `epochs=750`, `lr_schedule=cosine`: this claim +2.1%, mean |gap| 2.0% (5 runs)
  - `class_weight=balanced`, `normalize=zscore`: this claim +1.1%, mean |gap| 3.1% (5 runs)
  - `normalize=zscore`, `epochs=1`: this claim +4.3%, mean |gap| 5.0% (5 runs)

### History matching (every measured configuration, all claims together)
- 23 of 66 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `epochs, lr_schedule`: epochs=750, lr_schedule=cosine (max I 0.33); epochs=750, lr_schedule=step (max I 0.97)
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 0.8); class_weight=balanced, normalize=zscore (max I 0.82)
  - `epochs, normalize`: epochs=1, normalize=zscore (max I 1.03); epochs=750, normalize=minmax (max I 1.07); epochs=750, normalize=zscore (max I 1.08); epochs=150, normalize=zscore (max I 1.08); +2 more
- 2 separate islands (no single-knob move joins them): class_weight=balanced, normalize=minmax; class_weight=balanced, normalize=zscore; epochs=1, normalize=zscore | epochs=750, lr_schedule=cosine; epochs=750, lr_schedule=step; epochs=75, lr_schedule=cosine

Notes:
- stopped early: run budget of 200 reached (wanted 3 more run(s) of {'normalize': 'zscore', 'epochs': '150'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `epochs=750`, `lr_schedule=cosine` | 5 | +2.1% | +1.9% | 2.0% |
| `class_weight=balanced`, `normalize=minmax` | 5 | -0.5% | +5.3% | 2.9% |
| `class_weight=balanced`, `normalize=zscore` | 5 | +1.1% | +5.1% | 3.1% |
| `normalize=zscore`, `epochs=1` | 5 | +4.3% | +5.7% | 5.0% |
| `epochs=750`, `lr_schedule=step` | 2 | -6.2% | -6.4% | 6.3% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `out`

## Provenance
- GapFinder commit: `e9c31fd1405f5c8aae4bd880eadcdc8d491fad02` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0381, sandbox reported $0.0000 (total $0.0381; this search; ledger extraction is included only if it shared the search's router)
