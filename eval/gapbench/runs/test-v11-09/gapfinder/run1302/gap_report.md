# Gap Report: test-v11-09

Artifact `mlbench` · generated 2026-10-15 01:16 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -37.0% | +2.2% | ±2.2% | `lr=2.5`, `normalize=zscore` |

## C1: test_accuracy (paper 0.7542)
**Fits but unsupported** · gap -37.0% → +2.2% · 57 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0068`, `B0125`, `B0126`, `B0127`, `B0128` (5 run(s) of the same config)
- Config: `lr` naive `0.05`, changed to `2.5`
- Config: `normalize` naive `none`, changed to `zscore`
- Command:

  Replay: fork checkpoint `f643ab77-49da-4c01-ba46-a0efd15a9a70` and run
  ```
  RUN_TAG=5f4ce38cb28d "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 2.5 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7708, 0.7708, 0.7792, 0.7625, 0.8083; gap after +2.2%; result checkpoint `0b1006fc-a767-4e23-a62c-34ad52e1af85`
- Effect: candidate 0.7708 minus naive 0.475 = +0.2958, 95% bootstrap interval [+0.2542, +0.3283] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.754 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7542 (headline claim)

### What did we measure?
- Naive median 0.475 over 5 runs; repeats: 0.5333, 0.475, 0.4667, 0.4667, 0.475
- Spread: range 0.4667 to 0.5333, noise band ±0.0166 (2 x MAD), CV 5.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -37.0% (noise band ±2.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr` the gap is +9.4% (it comes back)
- PASS · Counterfactual (reversal test): without `normalize` the gap is -28.2% (it comes back)
- PASS · Held-out claim: C2: -35.0% to +3.8% (not worse beyond noise)
- FAIL · Evidence: `lr=2.5`: no evidence mentions '2.5'; it fits, but nothing says the authors used it
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2958 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (8.78 noise units, gap -17.7%); `normalize=minmax` (7.28 noise units, gap -21.0%); `lr=0.01` (5.52 noise units, gap -24.9%); `lr=0.001` (5.27 noise units, gap -25.4%); `lr=0.0005` (5.02 noise units, gap -26.0%) (and 5 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr=2.5`, `normalize=minmax`: this claim +3.9%, mean |gap| 3.2% (5 runs)
  - `normalize=zscore`, `class_weight=balanced`: this claim +3.9%, mean |gap| 6.3% (5 runs)
  - `lr=0.0005`, `normalize=zscore`: this claim +5.5%, mean |gap| 6.4% (5 runs)

### History matching (every measured configuration, all claims together)
- 16 of 57 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr, normalize`: lr=2.5, normalize=minmax (max I 0.4); lr=2.5, normalize=zscore (max I 0.81); lr=0.0005, normalize=zscore (max I 1.36); lr=0.005, normalize=zscore (max I 1.54); +4 more
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 1.24); class_weight=balanced, normalize=zscore (max I 1.49)

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'normalize': 'minmax', 'class_weight': 'balanced'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr=2.5`, `normalize=zscore` | 5 | +2.2% | +3.8% | 3.0% |
| `lr=2.5`, `normalize=minmax` | 5 | +3.9% | +2.5% | 3.2% |
| `normalize=zscore`, `class_weight=balanced` | 5 | +3.9% | +8.7% | 6.3% |
| `lr=0.0005`, `normalize=zscore` | 5 | +5.5% | +7.4% | 6.4% |
| `lr=0.25`, `normalize=minmax` | 5 | -7.2% | -11.8% | 9.5% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
