# Gap Report: test-v11-09

Artifact `mlbench` · generated 2026-10-23 17:54 · 195 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -32.6% | -1.7% | ±8.8% | `normalize=minmax`, `lr=0.25` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Held-out claims outside noise:**
  - C2 (`balanced_accuracy`): paper 0.7224, measured 0.5045 (-30.2%, band ±9.6%)
- **The paper states these, and this harness can't vary them** (they are part of what the number means):
  - `RUN_TAG`: "Numbers are medians over 7 runs with different shuffling seeds." (p.1)
  - `num_runs`: "Numbers are medians over 7 runs with different shuffling seeds." (p.1)
  - `aggregation`: "Numbers are medians over 7 runs with different shuffling seeds." (p.1)

## C1: test_accuracy (paper 0.7542)
**Fits but unsupported** · gap -32.6% → -1.7% · 61 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0135`, `B0143`, `B0144`, `B0145`, `B0146`, `B0147` (6 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `lr` naive `0.05`, changed to `0.25`
- Command:

  Replay: fork checkpoint `b5653ff5-cf9e-4407-83e5-0a8b75774933` and run
  ```
  RUN_TAG=43dc5fe99d08 export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.25 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7667, 0.6958, 0.7292, 0.7, 0.7542, 0.7542; gap after -1.7%; result checkpoint `76ef5f5c-3a2d-445b-8000-a323387f0da6`
- Effect: candidate 0.7417 minus naive 0.5083 = +0.2334, 95% bootstrap interval [+0.1608, +0.2643] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.754 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7542 (headline claim)

### What did we measure?
- Naive median 0.5083 over 5 runs; repeats: 0.5542, 0.5708, 0.4875, 0.475, 0.5083
- Spread: range 0.475 to 0.5708, noise band ±0.0666 (2 x MAD), CV 8.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -32.6% (noise band ±8.8% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -32.0% (it comes back)
- PASS · Counterfactual (reversal test): without `lr` the gap is -21.0% (it comes back)
- PASS · Held-out claim: C2: -30.2% to -4.7% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- FAIL · Evidence: `lr=0.25`: no evidence mentions '0.25'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2334 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `PYTHONHASHSEED`, `PYTHON_VERSION`, `OMP_NUM_THREADS`, `CPU_MODEL`, `OS_TYPE`, `MEMORY_GB`, `FLOAT_DETERMINISM`, `DISK_TYPE`, `--out`, `NETWORK_LATENCY`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (2.57 noise units, gap +9.9%); `lr_schedule=cosine` (1.5 noise units, gap -19.3%)
- Near alternatives (closest across all claims):
  - `normalize=zscore`, `lr=2.5`: this claim +2.2%, mean |gap| 3.2% (6 runs)
  - `normalize=zscore`, `lr=0.0005`: this claim +2.5%, mean |gap| 3.6% (6 runs)
  - `normalize=minmax`, `class_weight=balanced`: this claim +1.9%, mean |gap| 5.0% (6 runs)

### Equally good configurations
The target claim can't tell these 4 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `lr=0.25, normalize=minmax` (reported)
- `lr=0.0005, normalize=zscore`
- `class_weight=balanced, normalize=minmax`
- `lr=2.5, normalize=zscore`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting lr=0.25, normalize=minmax | settings | 41% | 0.9 sigma (fits every claim) | run with lr=0.25, normalize=minmax |
| 2 | the setting lr=0.0005, normalize=zscore | settings | 19% | 0.6 sigma (fits every claim) | run with lr=0.0005, normalize=zscore |
| 3 | the setting lr=2.5, normalize=zscore | settings | 15% | 0.8 sigma (fits every claim) | run with lr=2.5, normalize=zscore |

### History matching (every measured configuration, all claims together)
- 25 of 61 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr, normalize`: lr=0.0005, normalize=zscore (max I 0.62); lr=2.5, normalize=zscore (max I 0.77); lr=0.25, normalize=minmax (max I 0.95); lr=0.001, normalize=zscore (max I 1.39); +2 more
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 1.31); class_weight=balanced, normalize=zscore (max I 1.43)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.72); lr_schedule=step, normalize=zscore (max I 1.72)
- 2 separate islands (no single-knob move joins them): lr=0.0005, normalize=zscore; lr=2.5, normalize=zscore; lr=0.25, normalize=minmax | lr=0.0005, lr_schedule=step

Notes:
- configurations the target claim can't tell apart from the answer: lr=0.25, normalize=minmax; lr=0.0005, normalize=zscore; class_weight=balanced, normalize=minmax; lr=2.5, normalize=zscore
- spec knobs no ledger assumption names (batch_size, data_seed, epochs, label_noise, n, positive_rate, split, threshold, weight_decay) were screened too; no better answer
- lr: values from 0.2229 to 1.054 fit every claim (a bisection, 3 runs a side, one run a value: approximate)
- not identifiable from the paper's numbers: 3 configuration(s) of other knobs fit every claim as well as the answer (lr=0.25, normalize=minmax: class_weight=balanced, normalize=minmax; lr=0.0005, normalize=zscore; lr=2.5, normalize=zscore), and the paper reports no other condition that could separate them: the answer is one of them, not the identified cause

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax`, `lr=0.25` | 6 | -1.7% | -4.7% | 3.2% |
| `normalize=zscore`, `lr=2.5` | 6 | +2.2% | +4.2% | 3.2% |
| `normalize=zscore`, `lr=0.0005` | 6 | +2.5% | +4.7% | 3.6% |
| `normalize=minmax`, `class_weight=balanced` | 6 | +1.9% | +8.1% | 5.0% |
| `normalize=zscore`, `class_weight=balanced` | 6 | +4.1% | +8.9% | 6.5% |

## Runtime trace (one dry run)
1 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `PYTHONHASHSEED`, `PYTHON_VERSION`, `OMP_NUM_THREADS`, `CPU_MODEL`, `OS_TYPE`, `MEMORY_GB`, `FLOAT_DETERMINISM`, `DISK_TYPE`, `--out`, `NETWORK_LATENCY`

## Provenance
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `a5ee8e94932cc1397dd02c920427dbe9702911f36a6fbfee753b818e8d60994f`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
