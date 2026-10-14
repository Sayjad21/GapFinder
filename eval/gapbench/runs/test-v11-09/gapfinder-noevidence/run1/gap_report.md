# Gap Report: test-v11-09

Artifact `mlbench` · generated 2026-10-14 11:27 · 192 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -29.3% | +1.7% | ±7.7% | `normalize=minmax`, `class_weight=balanced` |

## C1: test_accuracy (paper 0.7542)
**Fits but unsupported** · gap -29.3% → +1.7% · 49 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0084`, `B0165`, `B0166`, `B0167`, `B0168` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `class_weight` naive `none`, changed to `balanced`
- Command:

  Replay: fork checkpoint `c39a1d41-fbd1-4c23-b1e4-161216d08914` and run
  ```
  RUN_TAG=7282979ed09c "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight balanced --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7708, 0.7458, 0.7667, 0.7583, 0.7667; gap after +1.7%; result checkpoint `fb70a306-2599-45aa-9d6f-0601a0e03eff`
- Effect: candidate 0.7667 minus naive 0.5333 = +0.2334, 95% bootstrap interval [+0.1983, +0.28] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.754 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7542 (headline claim)

### What did we measure?
- Naive median 0.5333 over 5 runs; repeats: 0.55, 0.4833, 0.5333, 0.4875, 0.5625
- Spread: range 0.4833 to 0.5625, noise band ±0.0584 (2 x MAD), CV 6.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -29.3% (noise band ±7.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -28.7% (it comes back)
- PASS · Counterfactual (reversal test): without `class_weight` the gap is -21.0% (it comes back)
- PASS · Held-out claim: C2: -25.4% to +7.4% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: evidence gate off: no evidence was looked for
- FAIL · Evidence: `class_weight=balanced`: evidence gate off: no evidence was looked for
- PASS · Effect vs noise: candidate minus naive is +0.2334 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `PYTHONHASHSEED`, `PYTHON_VERSION`, `OMP_NUM_THREADS`, `CPU_MODEL`, `OS_TYPE`, `MEMORY_GB`, `FLOAT_DETERMINISM`, `DISK_TYPE`, `--out`, `NETWORK_LATENCY`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (2.5 noise units, gap +9.9%); `lr_schedule=cosine` (1.57 noise units, gap -17.1%)
- Near alternatives (closest across all claims):
  - `normalize=minmax`, `lr=0.905`: this claim +5.0%, mean |gap| 5.5% (5 runs)
  - `class_weight=balanced`, `normalize=zscore`: this claim +4.4%, mean |gap| 6.8% (5 runs)
  - `lr=0.905`, `normalize=zscore`: this claim +7.7%, mean |gap| 8.7% (5 runs)

### History matching (every measured configuration, all claims together)
- 12 of 49 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr, normalize`: lr=0.905, normalize=minmax (max I 1.06); lr=0.905, normalize=zscore (max I 1.76); lr=0.01, normalize=zscore (max I 1.94); lr=0.1, normalize=zscore (max I 1.95); +1 more
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 1.24); class_weight=balanced, normalize=zscore (max I 1.5)
  - `normalize`: normalize=zscore (max I 2.02)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 2.03); lr_schedule=step, normalize=zscore (max I 2.03)
- 2 separate islands (no single-knob move joins them): lr=0.905, normalize=minmax; class_weight=balanced, normalize=minmax; class_weight=balanced, normalize=zscore | lr=0.1, lr_schedule=cosine
- Equally good values: `normalize` in {minmax, zscore}

Notes:
- evidence gate off: no evidence was checked, so this cannot be labelled Explained
- equally good values within one noise band (measured): normalize in {minmax, zscore}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax`, `class_weight=balanced` | 5 | +1.7% | +7.4% | 4.5% |
| `normalize=minmax`, `lr=0.905` | 5 | +5.0% | +6.0% | 5.5% |
| `class_weight=balanced`, `normalize=zscore` | 5 | +4.4% | +9.2% | 6.8% |
| `lr=0.905`, `normalize=zscore` | 5 | +7.7% | +9.8% | 8.7% |
| `lr=0.01`, `normalize=zscore` | 5 | +9.4% | +11.4% | 10.4% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `PYTHONHASHSEED`, `PYTHON_VERSION`, `OMP_NUM_THREADS`, `CPU_MODEL`, `OS_TYPE`, `MEMORY_GB`, `FLOAT_DETERMINISM`, `DISK_TYPE`, `--out`, `NETWORK_LATENCY`

## Provenance
- GapFinder commit: `b05f7288e1a4df8af69bb0b5e7633827b4cb46c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
