# Gap Report: test-v11-09

Artifact `mlbench` · generated 2026-10-14 23:50 · 158 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -28.7% | +1.1% | ±0.7% | `normalize=minmax`, `class_weight=balanced` |

## C1: test_accuracy (paper 0.7542)
**Fits but unsupported** · gap -28.7% → +1.1% · 53 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0091`, `B0149`, `B0150` (3 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `class_weight` naive `none`, changed to `balanced`
- Command:

  Replay: fork checkpoint `6096e45a-c564-448c-8371-1a739dbf8ed9` and run
  ```
  RUN_TAG=9335f8690f64 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight balanced --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7417, 0.7625, 0.7708; gap after +1.1%; result checkpoint `6de98764-91b4-4cb7-aaf5-31583fcb8405`
- Effect: candidate 0.7625 minus naive 0.5375 = +0.225, 95% bootstrap interval [+0.1692, +0.2333] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.754 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7542 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5458, 0.5375, 0.5958, 0.5375, 0.5375
- Spread: range 0.5375 to 0.5958, noise band ±0.005375 (2 x MAD), CV 4.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -28.7% (noise band ±0.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -29.3% (it comes back)
- PASS · Counterfactual (reversal test): without `class_weight` the gap is -21.0% (it comes back)
- PASS · Held-out claim: C2: -24.9% to +8.1% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- FAIL · Evidence: `class_weight=balanced`: no evidence mentions 'balanced'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.225 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `PYTHONHASHSEED`, `PYTHON_VERSION`, `OMP_NUM_THREADS`, `CPU_MODEL`, `OS_TYPE`, `MEMORY_GB`, `FLOAT_DETERMINISM`, `DISK_TYPE`, `--out`, `NETWORK_LATENCY`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (27.14 noise units, gap +9.4%); `lr_schedule=cosine` (13.95 noise units, gap -18.8%); `lr=0.25` (4.65 noise units, gap -25.4%); `lr=0.01` (3.87 noise units, gap -26.0%); `lr_schedule=step` (1.54 noise units, gap -27.6%)
- Near alternatives (closest across all claims):
  - `lr=0.5`, `normalize=minmax`: this claim +3.3%, mean |gap| 2.9% (3 runs)
  - `normalize=zscore`, `class_weight=balanced`: this claim +4.4%, mean |gap| 6.8% (3 runs)
  - `normalize=zscore`, `lr=0.0005`: this claim +5.5%, mean |gap| 6.9% (3 runs)

### Equally good configurations
The target claim can't tell these 2 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `class_weight=balanced, normalize=minmax` (reported)
- `lr=0.5, normalize=minmax`

### History matching (every measured configuration, all claims together)
- 12 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr, normalize`: lr=0.5, normalize=minmax (max I 0.1); lr=0.0005, normalize=zscore (max I 1.71); lr=0.5, normalize=zscore (max I 1.92); lr=0.25, normalize=minmax (max I 1.97); +2 more
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 1.43); class_weight=balanced, normalize=zscore (max I 1.67)
  - `normalize`: normalize=zscore (max I 2.2)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 2.26)

Notes:
- configurations the target claim can't tell apart from the answer: class_weight=balanced, normalize=minmax; lr=0.5, normalize=minmax

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr=0.5`, `normalize=minmax` | 3 | +3.3% | +2.5% | 2.9% |
| `class_weight=balanced`, `normalize=minmax` | 3 | +1.1% | +8.1% | 4.6% |
| `normalize=zscore`, `class_weight=balanced` | 3 | +4.4% | +9.2% | 6.8% |
| `normalize=zscore`, `lr=0.0005` | 3 | +5.5% | +8.3% | 6.9% |
| `lr=0.25`, `normalize=minmax` | 3 | -6.1% | -10.4% | 8.2% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `PYTHONHASHSEED`, `PYTHON_VERSION`, `OMP_NUM_THREADS`, `CPU_MODEL`, `OS_TYPE`, `MEMORY_GB`, `FLOAT_DETERMINISM`, `DISK_TYPE`, `--out`, `NETWORK_LATENCY`

## Provenance
- GapFinder commit: `efb2f63a257a40b9982099a274f2e882f272b80c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
