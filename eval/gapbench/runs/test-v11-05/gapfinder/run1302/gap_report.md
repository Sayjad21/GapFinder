# Gap Report: test-v11-05

Artifact `mlbench` · generated 2026-10-15 01:14 · 197 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -32.0% | -1.2% | ±4.6% | `epochs=150`, `lr_schedule=cosine` |

## C1: test_accuracy (paper 0.7292)
**Fits but unsupported** · gap -32.0% → -1.2% · 61 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0076`, `B0158`, `B0159`, `B0160`, `B0161` (5 run(s) of the same config)
- Config: `epochs` naive `15`, changed to `150`
- Config: `lr_schedule` naive `const`, changed to `cosine`
- Command:

  Replay: fork checkpoint `f55b4be3-ec1e-4d59-8731-383909f89a79` and run
  ```
  RUN_TAG=6273f5963d4e "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize none --epochs 150 --batch_size 32 --lr 0.05 --lr_schedule cosine --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.725, 0.7208, 0.7167, 0.7208, 0.7167; gap after -1.2%; result checkpoint `7d6fb8cb-a37d-40bd-a193-108e11e499c3`
- Effect: candidate 0.7208 minus naive 0.4958 = +0.225, 95% bootstrap interval [+0.1692, +0.24] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.729 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7292 (headline claim)

### What did we measure?
- Naive median 0.4958 over 5 runs; repeats: 0.5375, 0.4833, 0.5625, 0.4958, 0.4792
- Spread: range 0.4792 to 0.5625, noise band ±0.0332 (2 x MAD), CV 7.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -32.0% (noise band ±4.6% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `epochs` the gap is -13.7% (it comes back)
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is -26.0% (it comes back)
- PASS · Held-out claim: C2: -27.1% to +3.7% (not worse beyond noise)
- FAIL · Evidence: `epochs=150`: no evidence mentions '150'; it fits, but nothing says the authors used it
- FAIL · Evidence: `lr_schedule=cosine`: no evidence mentions 'cosine'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.225 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (4.14 noise units, gap +13.1%); `normalize=minmax` (3.01 noise units, gap -18.3%); `class_weight=balanced` (1.88 noise units, gap -23.4%); `lr_schedule=step` (1.76 noise units, gap -24.0%); `epochs=30` (1.26 noise units, gap -26.3%) (and 4 more in the JSON)
- Near alternatives (closest across all claims):
  - `epochs=150`, `normalize=minmax`: this claim +6.3%, mean |gap| 8.0% (5 runs)
  - `epochs=30`, `lr_schedule=cosine`: this claim -13.2%, mean |gap| 9.8% (5 runs)
  - `lr_schedule=cosine`: this claim -13.7%, mean |gap| 10.4% (3 runs)

### History matching (every measured configuration, all claims together)
- 16 of 61 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `epochs, normalize`: epochs=75, normalize=minmax (max I 0.38); epochs=150, normalize=minmax (max I 1.62); epochs=750, normalize=minmax (max I 2.4); epochs=750, normalize=zscore (max I 2.46); +1 more
  - `epochs, lr_schedule`: epochs=150, lr_schedule=cosine (max I 0.58); epochs=150, lr_schedule=step (max I 1.76); epochs=30, lr_schedule=cosine (max I 2.2)
  - `lr_schedule`: lr_schedule=cosine (max I 2.23)
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 2.47)
- 3 separate islands (no single-knob move joins them): epochs=75, normalize=minmax; epochs=150, normalize=minmax; epochs=750, normalize=minmax | epochs=150, lr_schedule=cosine; epochs=150, lr_schedule=step; epochs=30, lr_schedule=cosine | class_weight=balanced, normalize=minmax; class_weight=balanced, normalize=zscore

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'normalize': 'minmax', 'epochs': '10'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `epochs=150`, `lr_schedule=cosine` | 5 | -1.2% | +3.7% | 2.4% |
| `epochs=150`, `normalize=minmax` | 5 | +6.3% | +9.7% | 8.0% |
| `epochs=30`, `lr_schedule=cosine` | 5 | -13.2% | -6.5% | 9.8% |
| `lr_schedule=cosine` | 3 | -13.7% | -7.0% | 10.4% |
| `normalize=minmax`, `class_weight=balanced` | 5 | +5.7% | +15.6% | 10.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
