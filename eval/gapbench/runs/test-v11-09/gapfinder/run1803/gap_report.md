# Gap Report: test-v11-09

Artifact `mlbench` · generated 2026-10-15 19:48 · 199 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -34.8% | -5.0% | ±6.6% | `lr=0.25`, `normalize=minmax` |

## C1: test_accuracy (paper 0.7542)
**Fits but unsupported** · gap -34.8% → -5.0% · 61 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0113`, `B0141`, `B0188`, `B0189`, `B0190` (5 run(s) of the same config)
- Config: `lr` naive `0.05`, changed to `0.25`
- Config: `normalize` naive `none`, changed to `minmax`
- Command:

  Replay: fork checkpoint `92065570-00b1-45a5-8c6d-91ce12545040` and run
  ```
  RUN_TAG=d1b8a5a53cc3 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.25 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7167, 0.7167, 0.7458, 0.6833, 0.7542; gap after -5.0%; result checkpoint `7ad8d853-9f5f-4df1-aea2-88468a72e9b5`
- Effect: candidate 0.7167 minus naive 0.4917 = +0.225, 95% bootstrap interval [+0.1716, +0.2733] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.754 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7542 (headline claim)

### What did we measure?
- Naive median 0.4917 over 5 runs; repeats: 0.5333, 0.5375, 0.4667, 0.4667, 0.4917
- Spread: range 0.4667 to 0.5375, noise band ±0.05 (2 x MAD), CV 6.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -34.8% (noise band ±6.6% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr` the gap is -21.0% (it comes back)
- PASS · Counterfactual (reversal test): without `normalize` the gap is -28.7% (it comes back)
- PASS · Held-out claim: C2: -32.6% to -8.9% (not worse beyond noise)
- FAIL · Evidence: `lr=0.25`: no evidence mentions '0.25'; it fits, but nothing says the authors used it
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.225 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `aggregation`, `CPU`, `memory`, `OS`, `Python_version`, `random_module`, `floating_point`, `num_features`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (3.75 noise units, gap +9.9%); `lr_schedule=cosine` (2.33 noise units, gap -19.3%); `lr=0.5` (1.08 noise units, gap -27.6%); `lr=0.0005` (1.08 noise units, gap -27.6%); `lr_schedule=step` (1 noise units, gap -28.2%)
- Near alternatives (closest across all claims):
  - `lr=0.0005`, `normalize=zscore`: this claim +1.1%, mean |gap| 1.7% (5 runs)
  - `lr=0.5`, `normalize=minmax`: this claim +3.3%, mean |gap| 2.9% (5 runs)
  - `class_weight=balanced`, `normalize=minmax`: this claim +2.2%, mean |gap| 4.7% (5 runs)

### History matching (every measured configuration, all claims together)
- 21 of 61 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr, normalize`: lr=0.5, normalize=minmax (max I 0.36); lr=0.0005, normalize=zscore (max I 0.41); lr=2.5, normalize=zscore (max I 0.93); lr=0.25, normalize=minmax (max I 1.27); +4 more
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 1.22); class_weight=balanced, normalize=zscore (max I 1.42)
- 2 separate islands (no single-knob move joins them): lr=0.5, normalize=minmax; lr=0.0005, normalize=zscore; lr=2.5, normalize=zscore | lr=2.5, lr_schedule=cosine; lr=0.5, lr_schedule=cosine; lr=0.01, lr_schedule=cosine

Notes:
- stopped early: run budget of 200 reached (wanted 3 more run(s) of {'normalize': 'zscore', 'lr': '0.25'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr=0.0005`, `normalize=zscore` | 5 | +1.1% | +2.3% | 1.7% |
| `lr=0.5`, `normalize=minmax` | 5 | +3.3% | +2.5% | 2.9% |
| `class_weight=balanced`, `normalize=minmax` | 5 | +2.2% | +7.2% | 4.7% |
| `class_weight=balanced`, `normalize=zscore` | 5 | +3.9% | +8.7% | 6.3% |
| `lr=0.25`, `normalize=minmax` | 5 | -5.0% | -8.9% | 7.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `aggregation`, `CPU`, `memory`, `OS`, `Python_version`, `random_module`, `floating_point`, `num_features`, `--out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
