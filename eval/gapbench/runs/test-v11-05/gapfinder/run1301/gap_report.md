# Gap Report: test-v11-05

Artifact `mlbench` · generated 2026-10-15 01:14 · 188 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -26.3% | +2.9% | ±9.1% | `lr_schedule=step`, `epochs=750` |

## C1: test_accuracy (paper 0.7292)
**Fits but unsupported** · gap -26.3% → +2.9% · 53 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0100`, `B0177`, `B0178`, `B0179`, `B0180` (5 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `step`
- Config: `epochs` naive `15`, changed to `750`
- Command:

  Replay: fork checkpoint `875891bd-f987-4a3b-8d49-2a4d931834ee` and run
  ```
  RUN_TAG=c39e79a9a700 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize none --epochs 750 --batch_size 32 --lr 0.05 --lr_schedule step --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7583, 0.6667, 0.75, 0.7042, 0.7875; gap after +2.9%; result checkpoint `9535c11f-0cba-41fe-80d6-e6bb02ad4953`
- Effect: candidate 0.75 minus naive 0.5375 = +0.2125, 95% bootstrap interval [+0.1267, +0.2542] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.729 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7292 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5375, 0.5708, 0.5333, 0.4875, 0.5708
- Spread: range 0.4875 to 0.5708, noise band ±0.0666 (2 x MAD), CV 6.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -26.3% (noise band ±9.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is -24.6% (it comes back)
- PASS · Counterfactual (reversal test): without `epochs` the gap is -25.7% (it comes back)
- PASS · Held-out claim: C2: -19.5% to +6.8% (not worse beyond noise)
- FAIL · Evidence: `lr_schedule=step`: no evidence mentions 'step'; it fits, but nothing says the authors used it
- FAIL · Evidence: `epochs=750`: no evidence mentions '750'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2125 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (1.44 noise units, gap +13.1%); `lr_schedule=cosine` (1.31 noise units, gap -14.3%)
- Near alternatives (closest across all claims):
  - `normalize=minmax`, `epochs=75`: this claim -1.7%, mean |gap| 2.0% (5 runs)
  - `epochs=150`, `lr_schedule=cosine`: this claim -2.3%, mean |gap| 2.5% (5 runs)
  - `epochs=75`, `lr_schedule=cosine`: this claim -8.6%, mean |gap| 5.6% (5 runs)

### Equally good configurations
The target claim can't tell these 4 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `epochs=750, lr_schedule=step` (reported)
- `epochs=75, normalize=minmax`
- `epochs=150, lr_schedule=cosine`
- `class_weight=balanced, normalize=minmax`

### History matching (every measured configuration, all claims together)
- 13 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `epochs, normalize`: epochs=75, normalize=minmax (max I 0.28); epochs=150, normalize=minmax (max I 1.61)
  - `epochs, lr_schedule`: epochs=150, lr_schedule=cosine (max I 0.47); epochs=750, lr_schedule=step (max I 0.74); epochs=75, lr_schedule=cosine (max I 1.33); epochs=750, lr_schedule=cosine (max I 2.14); +1 more
  - `lr_schedule`: lr_schedule=cosine (max I 2.37)
  - `class_weight, lr_schedule`: class_weight=balanced, lr_schedule=cosine (max I 2.46)
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 2.49)
- 3 separate islands (no single-knob move joins them): epochs=150, lr_schedule=cosine; epochs=750, lr_schedule=step; epochs=75, lr_schedule=cosine | epochs=75, normalize=minmax; epochs=150, normalize=minmax | class_weight=balanced, normalize=minmax; class_weight=balanced, normalize=zscore
- Equally good values: `lr_schedule` in {cosine, step}

Notes:
- configurations the target claim can't tell apart from the answer: epochs=750, lr_schedule=step; epochs=75, normalize=minmax; epochs=150, lr_schedule=cosine; class_weight=balanced, normalize=minmax
- equally good values within one noise band (measured): lr_schedule in {cosine, step}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax`, `epochs=75` | 5 | -1.7% | -2.3% | 2.0% |
| `epochs=150`, `lr_schedule=cosine` | 5 | -2.3% | +2.6% | 2.5% |
| `lr_schedule=step`, `epochs=750` | 5 | +2.9% | +6.8% | 4.8% |
| `epochs=75`, `lr_schedule=cosine` | 5 | -8.6% | -2.6% | 5.6% |
| `normalize=minmax`, `epochs=150` | 5 | +6.3% | +9.4% | 7.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
