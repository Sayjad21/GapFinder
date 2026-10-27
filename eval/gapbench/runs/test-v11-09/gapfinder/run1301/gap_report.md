# Gap Report: test-v11-09

Artifact `mlbench` · generated 2026-10-15 01:16 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -28.7% | +9.9% | ±6.6% | `normalize=zscore` |

## C1: test_accuracy (paper 0.7542)
**Fits but unsupported** · gap -28.7% → +9.9% · 61 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0018`, `B0045`, `B0046`, `B0055`, `B0056`, `B0057` (6 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Command:

  Replay: fork checkpoint `a3e444af-bbb1-44a8-b3d0-30d9cd3ebcb2` and run
  ```
  RUN_TAG=01ebe3a67690 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.8292, 0.8292, 0.8292, 0.825, 0.8292, 0.8292; gap after +9.9%; result checkpoint `cbf92fbf-5502-48ff-99de-ee74221da7b0`
- Effect: candidate 0.8292 minus naive 0.5375 = +0.2917, 95% bootstrap interval [+0.2692, +0.3542] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.754 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7542 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5375, 0.4667, 0.4875, 0.5625, 0.5458
- Spread: range 0.4667 to 0.5625, noise band ±0.05 (2 x MAD), CV 7.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -28.7% (noise band ±6.6% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -28.7% (it comes back)
- PASS · Held-out claim: C2: -24.9% to +12.2% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2917 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `PYTHONHASHSEED`, `PYTHON_VERSION`, `OMP_NUM_THREADS`, `CPU_MODEL`, `OS_TYPE`, `MEMORY_GB`, `FLOAT_DETERMINISM`, `DISK_TYPE`, `--out`, `NETWORK_LATENCY`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (1.75 noise units, gap -17.1%); `normalize=minmax` (1.17 noise units, gap -21.0%)
- Near alternatives (closest across all claims):
  - `normalize=zscore`, `class_weight=balanced`: this claim +3.9%, mean |gap| 6.3% (5 runs)
  - `normalize=zscore`, `lr=0.5`: this claim +8.3%, mean |gap| 9.4% (5 runs)
  - `normalize=zscore`, `lr=0.005`: this claim +8.8%, mean |gap| 9.9% (5 runs)

### History matching (every measured configuration, all claims together)
- 25 of 61 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr, normalize`: lr=0.0005, normalize=zscore (max I 0.64); lr=0.5, normalize=minmax (max I 1.04); lr=2.5, normalize=zscore (max I 1.08); lr=0.25, normalize=zscore (max I 1.36); +4 more
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 1.02); class_weight=balanced, normalize=zscore (max I 1.35)

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'normalize': 'minmax', 'lr': '0.01'} for 'confirm-combo')
- class_weight dropped: with repeats, {'normalize': 'zscore', 'class_weight': 'balanced'} fits {'normalize': 'zscore'}'s gap by less than one noise band, so it is not needed
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore`, `class_weight=balanced` | 5 | +3.9% | +8.7% | 6.3% |
| `normalize=zscore`, `lr=0.5` | 5 | +8.3% | +10.5% | 9.4% |
| `normalize=zscore`, `lr=0.005` | 5 | +8.8% | +11.0% | 9.9% |
| `normalize=zscore`, `lr=0.1` | 5 | +9.4% | +11.7% | 10.5% |
| `normalize=zscore`, `lr=0.01` | 5 | +9.9% | +11.9% | 10.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `PYTHONHASHSEED`, `PYTHON_VERSION`, `OMP_NUM_THREADS`, `CPU_MODEL`, `OS_TYPE`, `MEMORY_GB`, `FLOAT_DETERMINISM`, `DISK_TYPE`, `--out`, `NETWORK_LATENCY`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
