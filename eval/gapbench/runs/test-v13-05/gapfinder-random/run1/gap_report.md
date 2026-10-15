# Gap Report: test-v13-05

Artifact `mlbench` · generated 2026-10-15 23:43 · 162 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -31.0% | +0.5% | ±0.7% | `normalize=zscore`, `class_weight=balanced` |

## C1: test_accuracy (paper 0.7792)
**Fits but unsupported** · gap -31.0% → +0.5% · 73 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0060`, `B0103`, `B0143` (3 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Config: `class_weight` naive `none`, changed to `balanced`
- Command:

  Replay: fork checkpoint `354f1933-692b-4e8b-9d0f-47a772a0e9f1` and run
  ```
  RUN_TAG=a36e9bee0599 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight balanced --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7875, 0.7833, 0.7833; gap after +0.5%; result checkpoint `1812e46c-a4f2-4a0e-925b-b889f3d472d4`
- Effect: candidate 0.7833 minus naive 0.5375 = +0.2458, 95% bootstrap interval [+0.2458, +0.2691] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.779 test accuracy and 0.750 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7792 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5125, 0.5208, 0.5375, 0.5375, 0.5375
- Spread: range 0.5125 to 0.5375, noise band ±0.005375 (2 x MAD), CV 2.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -31.0% (noise band ±0.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -31.6% (it comes back)
- PASS · Counterfactual (reversal test): without `class_weight` the gap is +6.4% (it comes back)
- PASS · Held-out claim: C2: -27.7% to +4.7% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- PASS · Evidence: `class_weight=balanced`: code evidence at train.py:75: 'cw = {1: 0.5 / pos, 0: 0.5 / (1 - pos)} if a.class_weight == "balanced" else {1: 1.0, 0: 1.0}'
- PASS · Effect vs noise: candidate minus naive is +0.2458 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `number_of_runs`, `aggregation_method`, `SCALES`, `WEIGHTS`, `shuffling_seed_generation`, `out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (15.5 noise units, gap -20.3%); `normalize=minmax` (10.85 noise units, gap -23.5%); `epochs=2` (5.43 noise units, gap -27.3%); `label_noise=0.905` (4.65 noise units, gap -27.8%); `epochs=75` (4.65 noise units, gap -27.8%) (and 3 more in the JSON)
- Near alternatives (closest across all claims):
  - `normalize=zscore`, `label_noise=0.905`: this claim +0.5%, mean |gap| 1.2% (3 runs)
  - `normalize=minmax`, `class_weight=balanced`: this claim -1.1%, mean |gap| 2.7% (3 runs)
  - `epochs=1`, `normalize=zscore`: this claim +4.3%, mean |gap| 4.9% (3 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `class_weight=balanced, normalize=zscore` (reported)
- `label_noise=0.905, normalize=zscore`
- `class_weight=balanced, normalize=minmax`

### History matching (every measured configuration, all claims together)
- 26 of 73 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `label_noise, normalize`: label_noise=0.905, normalize=zscore (max I 0.34); label_noise=0.1, normalize=zscore (max I 1.04); label_noise=0.981, normalize=zscore (max I 1.27)
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 0.81); class_weight=balanced, normalize=zscore (max I 0.91)
  - `epochs, normalize`: epochs=1, normalize=zscore (max I 1.08); epochs=750, normalize=zscore (max I 1.38); epochs=20, normalize=zscore (max I 1.41); epochs=75, normalize=zscore (max I 1.43); +1 more
- 2 separate islands (no single-knob move joins them): label_noise=0.905, normalize=zscore; class_weight=balanced, normalize=minmax; class_weight=balanced, normalize=zscore | epochs=75, lr_schedule=cosine
- Equally good values: `normalize` in {minmax, zscore}

Notes:
- configurations the target claim can't tell apart from the answer: class_weight=balanced, normalize=zscore; label_noise=0.905, normalize=zscore; class_weight=balanced, normalize=minmax
- equally good values within one noise band (measured): normalize in {minmax, zscore}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore`, `label_noise=0.905` | 3 | +0.5% | +1.8% | 1.2% |
| `normalize=zscore`, `class_weight=balanced` | 3 | +0.5% | +4.7% | 2.6% |
| `normalize=minmax`, `class_weight=balanced` | 3 | -1.1% | +4.4% | 2.7% |
| `epochs=1`, `normalize=zscore` | 3 | +4.3% | +5.5% | 4.9% |
| `normalize=zscore`, `label_noise=0.1` | 3 | +4.3% | +5.7% | 5.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `number_of_runs`, `aggregation_method`, `SCALES`, `WEIGHTS`, `shuffling_seed_generation`, `out`

## Provenance
- GapFinder commit: `e9c31fd1405f5c8aae4bd880eadcdc8d491fad02` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
