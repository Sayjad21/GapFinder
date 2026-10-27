# Gap Report: test-v11-05

Artifact `mlbench` · generated 2026-10-15 18:57 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -33.1% | +5.1% | ±5.7% | `epochs=750`, `lr_schedule=step` |

## C1: test_accuracy (paper 0.7292)
**Fits but unsupported** · gap -33.1% → +5.1% · 57 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0117`, `B0131`, `B0172`, `B0173`, `B0174` (5 run(s) of the same config)
- Config: `epochs` naive `15`, changed to `750`
- Config: `lr_schedule` naive `const`, changed to `step`
- Command:

  Replay: fork checkpoint `a6fb3663-9948-4d18-9235-f2ba9e0f9778` and run
  ```
  RUN_TAG=b493590e62e1 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize none --epochs 750 --batch_size 32 --lr 0.05 --lr_schedule step --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7708, 0.7667, 0.7333, 0.6917, 0.7875; gap after +5.1%; result checkpoint `0b0bac92-aac8-4988-812a-19ec62115924`
- Effect: candidate 0.7667 minus naive 0.4875 = +0.2792, 95% bootstrap interval [+0.18, +0.2992] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.729 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7292 (headline claim)

### What did we measure?
- Naive median 0.4875 over 5 runs; repeats: 0.5458, 0.4667, 0.4875, 0.4833, 0.55
- Spread: range 0.4667 to 0.55, noise band ±0.0416 (2 x MAD), CV 7.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -33.1% (noise band ±5.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `epochs` the gap is -28.6% (it comes back)
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is -23.1% (it comes back)
- PASS · Held-out claim: C2: -28.4% to +8.6% (not worse beyond noise)
- FAIL · Evidence: `epochs=750`: no evidence mentions '750'; it fits, but nothing says the authors used it
- FAIL · Evidence: `lr_schedule=step`: no evidence mentions 'step'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2792 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (4.11 noise units, gap -9.7%); `normalize=zscore` (3.41 noise units, gap +13.7%); `normalize=minmax` (2.6 noise units, gap -18.3%); `epochs=1` (2 noise units, gap -21.7%); `epochs=30` (1.6 noise units, gap -24.0%) (and 4 more in the JSON)
- Near alternatives (closest across all claims):
  - `epochs=150`, `lr_schedule=cosine`: this claim -1.7%, mean |gap| 2.5% (5 runs)
  - `epochs=75`, `lr_schedule=cosine`: this claim -9.1%, mean |gap| 6.0% (5 runs)
  - `epochs=30`, `lr_schedule=cosine`: this claim -13.2%, mean |gap| 9.7% (5 runs)

### History matching (every measured configuration, all claims together)
- 19 of 57 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `epochs, lr_schedule`: epochs=150, lr_schedule=cosine (max I 0.51); epochs=750, lr_schedule=step (max I 1.03); epochs=75, lr_schedule=cosine (max I 1.43); epochs=750, lr_schedule=cosine (max I 2.04); +3 more
  - `lr_schedule`: lr_schedule=cosine (max I 2.37)
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 2.4)
  - `class_weight, lr_schedule`: class_weight=balanced, lr_schedule=cosine (max I 2.51)
- 4 separate islands (no single-knob move joins them): epochs=150, lr_schedule=cosine; epochs=750, lr_schedule=step; epochs=75, lr_schedule=cosine | epochs=10, normalize=zscore; epochs=8, normalize=zscore; epochs=2, normalize=zscore | class_weight=balanced, normalize=minmax; class_weight=balanced, normalize=zscore | epochs=30, normalize=minmax

Notes:
- stopped early: run budget of 200 reached (wanted 3 more run(s) of {'lr_schedule': 'cosine', 'normalize': 'zscore'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `epochs=150`, `lr_schedule=cosine` | 5 | -1.7% | +3.4% | 2.5% |
| `epochs=75`, `lr_schedule=cosine` | 5 | -9.1% | -2.9% | 6.0% |
| `epochs=750`, `lr_schedule=step` | 5 | +5.1% | +8.6% | 6.9% |
| `epochs=30`, `lr_schedule=cosine` | 5 | -13.2% | -6.3% | 9.7% |
| `class_weight=balanced`, `normalize=minmax` | 5 | +4.6% | +15.0% | 9.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
