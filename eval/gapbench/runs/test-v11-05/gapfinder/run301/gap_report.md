# Gap Report: test-v11-05

Artifact `mlbench` · generated 2026-10-14 21:47 · 197 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -30.3% | -1.7% | ±2.3% | `lr_schedule=cosine`, `epochs=150` |

## C1: test_accuracy (paper 0.7292)
**Fits but unsupported** · gap -30.3% → -1.7% · 54 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0101`, `B0170`, `B0171`, `B0172`, `B0173` (5 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `cosine`
- Config: `epochs` naive `15`, changed to `150`
- Command:

  Replay: fork checkpoint `4d268ebd-4136-4111-ad27-e91df219454c` and run
  ```
  RUN_TAG=c8309f2f151d "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize none --epochs 150 --batch_size 32 --lr 0.05 --lr_schedule cosine --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7167, 0.7083, 0.7208, 0.7083, 0.7208; gap after -1.7%; result checkpoint `d80a5b24-0e19-45e1-bd0e-43bcafb7f7ba`
- Effect: candidate 0.7167 minus naive 0.5083 = +0.2084, 95% bootstrap interval [+0.1825, +0.2416] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.729 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7292 (headline claim)

### What did we measure?
- Naive median 0.5083 over 5 runs; repeats: 0.5083, 0.5167, 0.5375, 0.4667, 0.5
- Spread: range 0.4667 to 0.5375, noise band ±0.0168 (2 x MAD), CV 5.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -30.3% (noise band ±2.3% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is -31.4% (it comes back)
- PASS · Counterfactual (reversal test): without `epochs` the gap is -14.9% (it comes back)
- PASS · Held-out claim: C2: -25.1% to +3.1% (not worse beyond noise)
- FAIL · Evidence: `lr_schedule=cosine`: no evidence mentions 'cosine'; it fits, but nothing says the authors used it
- FAIL · Evidence: `epochs=150`: no evidence mentions '150'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2084 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (7.2 noise units, gap +13.7%); `normalize=minmax` (5.21 noise units, gap -18.3%); `lr_schedule=step` (2.73 noise units, gap -24.0%); `epochs=1` (2.23 noise units, gap -25.2%); `epochs=8` (2.23 noise units, gap -25.2%) (and 4 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=cosine`, `epochs=75`: this claim -8.0%, mean |gap| 5.1% (5 runs)
  - `lr_schedule=cosine`, `epochs=30`: this claim -13.2%, mean |gap| 9.6% (5 runs)
  - `lr_schedule=cosine`: this claim -14.9%, mean |gap| 11.5% (6 runs)

### History matching (every measured configuration, all claims together)
- 9 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 9 configurations
  - `epochs, normalize`: epochs=75, normalize=minmax (max I 0.44); epochs=150, normalize=minmax (max I 1.77)
  - `epochs, lr_schedule`: epochs=150, lr_schedule=cosine (max I 0.51); epochs=75, lr_schedule=cosine (max I 1.58); epochs=30, lr_schedule=cosine (max I 2.3)
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 1.97); class_weight=balanced, normalize=zscore (max I 2.37)
  - `class_weight, lr_schedule`: class_weight=balanced, lr_schedule=cosine (max I 2.52)
  - `lr_schedule`: lr_schedule=cosine (max I 2.65)
- 3 separate islands (no single-knob move joins them): epochs=150, lr_schedule=cosine; epochs=75, lr_schedule=cosine; epochs=30, lr_schedule=cosine | epochs=75, normalize=minmax; epochs=150, normalize=minmax | class_weight=balanced, normalize=minmax; class_weight=balanced, normalize=zscore

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'normalize': 'minmax', 'epochs': '1'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=cosine`, `epochs=150` | 5 | -1.7% | +3.1% | 2.4% |
| `lr_schedule=cosine`, `epochs=75` | 5 | -8.0% | -2.1% | 5.1% |
| `lr_schedule=cosine`, `epochs=30` | 5 | -13.2% | -6.0% | 9.6% |
| `lr_schedule=cosine` | 6 | -14.9% | -8.1% | 11.5% |
| `epochs=1`, `normalize=zscore` | 5 | +11.4% | +18.0% | 14.7% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`

## Provenance
- GapFinder commit: `e0f13d101585ad1609a15fbf67b70128f4cfffc8` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
