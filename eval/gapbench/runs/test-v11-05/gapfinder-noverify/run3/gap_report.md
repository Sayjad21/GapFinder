# Gap Report: test-v11-05

Artifact `mlbench` · generated 2026-10-14 12:38 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Partially explained | -32.6% | -2.3% | ±6.9% | `lr_schedule=cosine`, `epochs=150` |

## C1: test_accuracy (paper 0.7292)
**Partially explained** · gap -32.6% → -2.3% · 50 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0067`, `B0121`, `B0122`, `B0123`, `B0124` (5 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `cosine`
- Config: `epochs` naive `15`, changed to `150`
- Command:

  Replay: fork checkpoint `4bc0ace4-f79f-48af-9566-2e3f1257756d` and run
  ```
  RUN_TAG=ca8584ea23cb "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize none --epochs 150 --batch_size 32 --lr 0.05 --lr_schedule cosine --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7125, 0.7125, 0.7125, 0.7125, 0.7042; gap after -2.3%; result checkpoint `c4160ecf-fac0-48de-898d-d87e0f0a9faf`
- Effect: candidate 0.7125 minus naive 0.4917 = +0.2208, 95% bootstrap interval [+0.1684, +0.2375] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.729 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7292 (headline claim)

### What did we measure?
- Naive median 0.4917 over 5 runs; repeats: 0.4917, 0.5375, 0.5458, 0.4667, 0.4875
- Spread: range 0.4667 to 0.5458, noise band ±0.05 (2 x MAD), CV 6.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -32.6% (noise band ±6.9% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is +0.2208 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `os`, `evaluation_metric`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (2.75 noise units, gap +13.7%); `normalize=minmax` (2.08 noise units, gap -18.3%); `epochs=2` (1.17 noise units, gap -24.6%)
- Near alternatives (closest across all claims):
  - `normalize=minmax`, `epochs=150`: this claim +6.3%, mean |gap| 8.1% (5 runs)
  - `lr_schedule=cosine`, `epochs=30`: this claim -13.2%, mean |gap| 9.8% (5 runs)
  - `lr_schedule=cosine`: this claim -14.0%, mean |gap| 10.6% (6 runs)

### History matching (every measured configuration, all claims together)
- 12 of 50 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `epochs, lr_schedule`: epochs=150, lr_schedule=cosine (max I 0.43); epochs=20, lr_schedule=step (max I 2.07); epochs=30, lr_schedule=cosine (max I 2.3); epochs=20, lr_schedule=cosine (max I 2.54); +2 more
  - `epochs, normalize`: epochs=150, normalize=minmax (max I 1.72)
  - `lr_schedule`: lr_schedule=cosine (max I 2.45)
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 2.58); class_weight=balanced, normalize=zscore (max I 2.67)
- 4 separate islands (no single-knob move joins them): epochs=150, lr_schedule=cosine; epochs=20, lr_schedule=step; epochs=30, lr_schedule=cosine | class_weight=balanced, normalize=minmax; class_weight=balanced, normalize=zscore | epochs=150, normalize=minmax | epochs=1, lr_schedule=cosine, normalize=zscore

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'epochs': '150', 'class_weight': 'balanced'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=cosine`, `epochs=150` | 5 | -2.3% | +2.6% | 2.5% |
| `normalize=minmax`, `epochs=150` | 5 | +6.3% | +9.9% | 8.1% |
| `lr_schedule=cosine`, `epochs=30` | 5 | -13.2% | -6.5% | 9.8% |
| `lr_schedule=cosine` | 6 | -14.0% | -7.2% | 10.6% |
| `normalize=minmax`, `class_weight=balanced` | 5 | +5.7% | +16.0% | 10.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `os`, `evaluation_metric`

## Provenance
- GapFinder commit: `b05f7288e1a4df8af69bb0b5e7633827b4cb46c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
