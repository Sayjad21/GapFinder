# Gap Report: test-v11-09

Artifact `mlbench` · generated 2026-10-14 11:26 · 196 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -27.6% | +2.2% | ±4.4% | `normalize=minmax`, `class_weight=balanced` |

## C1: test_accuracy (paper 0.7542)
**Fits but unsupported** · gap -27.6% → +2.2% · 49 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0077`, `B0145`, `B0146`, `B0147`, `B0148` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `class_weight` naive `none`, changed to `balanced`
- Command:

  Replay: fork checkpoint `ef3e5e75-1a1f-4bbb-9f91-4efc02182cea` and run
  ```
  RUN_TAG=cb0f85f521fa "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight balanced --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7667, 0.7708, 0.775, 0.775, 0.7708; gap after +2.2%; result checkpoint `65faab48-f499-4ec0-9c4a-4a277c7df0cc`
- Effect: candidate 0.7708 minus naive 0.5458 = +0.225, 95% bootstrap interval [+0.2125, +0.295] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.754 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7542 (headline claim)

### What did we measure?
- Naive median 0.5458 over 5 runs; repeats: 0.4833, 0.475, 0.5625, 0.5458, 0.5458
- Spread: range 0.475 to 0.5625, noise band ±0.0334 (2 x MAD), CV 7.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -27.6% (noise band ±4.4% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -24.3% (it comes back)
- PASS · Counterfactual (reversal test): without `class_weight` the gap is -21.0% (it comes back)
- PASS · Held-out claim: C2: -25.6% to +8.8% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- FAIL · Evidence: `class_weight=balanced`: no evidence mentions 'balanced'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.225 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `PYTHONHASHSEED`, `PYTHON_VERSION`, `OMP_NUM_THREADS`, `CPU_MODEL`, `OS_TYPE`, `MEMORY_GB`, `FLOAT_DETERMINISM`, `DISK_TYPE`, `--out`, `NETWORK_LATENCY`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (4.12 noise units, gap +9.4%); `lr_schedule=cosine` (2.25 noise units, gap -17.7%)
- Near alternatives (closest across all claims):
  - `normalize=minmax`, `lr=0.905`: this claim +4.4%, mean |gap| 4.0% (5 runs)
  - `class_weight=balanced`, `normalize=zscore`: this claim +3.9%, mean |gap| 6.3% (5 runs)
  - `normalize=zscore`, `lr=0.905`: this claim +6.6%, mean |gap| 7.4% (5 runs)

### History matching (every measured configuration, all claims together)
- 15 of 49 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr, normalize`: lr=0.905, normalize=minmax (max I 0.38); lr=0.905, normalize=zscore (max I 1.33); lr=0.005, normalize=zscore (max I 1.75); lr=0.1, normalize=zscore (max I 1.86); +1 more
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 1.38); class_weight=balanced, normalize=zscore (max I 1.39)
  - `normalize`: normalize=zscore (max I 1.89)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.94); lr_schedule=step, normalize=zscore (max I 1.94)
- Equally good values: `normalize` in {minmax, zscore}

Notes:
- equally good values within one noise band (measured): normalize in {minmax, zscore}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax`, `lr=0.905` | 5 | +4.4% | +3.6% | 4.0% |
| `class_weight=balanced`, `normalize=minmax` | 5 | +2.2% | +8.8% | 5.5% |
| `class_weight=balanced`, `normalize=zscore` | 5 | +3.9% | +8.7% | 6.3% |
| `normalize=zscore`, `lr=0.905` | 5 | +6.6% | +8.1% | 7.4% |
| `normalize=zscore`, `lr=0.005` | 5 | +8.8% | +11.0% | 9.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `PYTHONHASHSEED`, `PYTHON_VERSION`, `OMP_NUM_THREADS`, `CPU_MODEL`, `OS_TYPE`, `MEMORY_GB`, `FLOAT_DETERMINISM`, `DISK_TYPE`, `--out`, `NETWORK_LATENCY`

## Provenance
- GapFinder commit: `b05f7288e1a4df8af69bb0b5e7633827b4cb46c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0669, sandbox reported $0.0000 (total $0.0669; this search; ledger extraction is included only if it shared the search's router)
