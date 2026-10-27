# Gap Report: test-v12-01

Artifact `mlbench` · generated 2026-10-16 01:57 · 185 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -23.8% | -0.4% | ±2.4% | `normalize=minmax`, `n=6000` |

## C1: test_accuracy (paper 0.705)
**Fits but unsupported** · gap -23.8% → -0.4% · 61 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0094`, `B0099`, `B0137`, `B0138`, `B0139` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `n` naive `1200`, changed to `6000`
- Command:

  Replay: fork checkpoint `7d2b6d27-7d4e-48cf-ac5d-2053b17634ab` and run
  ```
  RUN_TAG=19469f96acf8 "${PYTHON:-python3}" train.py --n 6000 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7192, 0.7, 0.7025, 0.7117, 0.7; gap after -0.4%; result checkpoint `8cb967f1-2a8a-4536-becf-993ab08948d0`
- Effect: candidate 0.7025 minus naive 0.5375 = +0.165, 95% bootstrap interval [+0.1604, +0.2173] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.705 test accuracy.

- p. 1; value used: `test_accuracy` = 0.705 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.4875, 0.5375, 0.5375, 0.4875, 0.5458
- Spread: range 0.4875 to 0.5458, noise band ±0.0166 (2 x MAD), CV 5.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -23.8% (noise band ±2.4% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -36.8% (it comes back)
- PASS · Counterfactual (reversal test): without `n` the gap is -15.5% (it comes back)
- PASS · Held-out claim: C2: -13.3% to -1.0% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- FAIL · Evidence: `n=6000`: no evidence mentions '6000'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.165 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `python_version`, `hardware`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (6.28 noise units, gap -9.0%); `n=240` (5.27 noise units, gap -11.3%); `normalize=zscore` (2.86 noise units, gap +17.0%); `n=120` (2.76 noise units, gap -17.3%); `n=2400` (2.39 noise units, gap -18.1%)
- Near alternatives (closest across all claims):
  - `n=12000`, `lr_schedule=cosine`: this claim -5.0%, mean |gap| 4.3% (5 runs)
  - `n=120`, `lr_schedule=cosine`: this claim -5.4%, mean |gap| 5.3% (5 runs)
  - `n=120`, `lr_schedule=step`: this claim -5.4%, mean |gap| 5.3% (5 runs)

### Equally good configurations
The target claim can't tell these 4 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `n=6000, normalize=minmax` (reported)
- `n=2400, normalize=zscore`
- `n=240, normalize=zscore`
- `n=120, normalize=zscore`

### History matching (every measured configuration, all claims together)
- 24 of 58 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `n, normalize`: n=6000, normalize=minmax (max I 0.05); n=12000, normalize=minmax (max I 1.4); n=2400, normalize=zscore (max I 1.88); n=600, normalize=zscore (max I 1.97); +1 more
  - `lr_schedule, n`: lr_schedule=cosine, n=12000 (max I 0.89); lr_schedule=cosine, n=120 (max I 1.37); lr_schedule=step, n=120 (max I 1.37); lr_schedule=cosine, n=6000 (max I 1.94)
  - `lr_schedule`: lr_schedule=cosine (max I 2.11)
- 3 separate islands (no single-knob move joins them): lr_schedule=cosine, n=12000; lr_schedule=cosine, n=120; lr_schedule=step, n=120 | n=6000, normalize=minmax; n=12000, normalize=minmax; n=2400, normalize=zscore | class_weight=balanced, n=600

Notes:
- configurations the target claim can't tell apart from the answer: n=6000, normalize=minmax; n=2400, normalize=zscore; n=240, normalize=zscore; n=120, normalize=zscore

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `n=6000`, `normalize=minmax` | 5 | -0.4% | -1.0% | 0.7% |
| `n=12000`, `lr_schedule=cosine` | 5 | -5.0% | +3.5% | 4.3% |
| `n=120`, `lr_schedule=cosine` | 5 | -5.4% | +5.1% | 5.3% |
| `n=120`, `lr_schedule=step` | 5 | -5.4% | +5.1% | 5.3% |
| `n=12000`, `normalize=minmax` | 5 | +4.1% | +8.3% | 6.2% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `n=1`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `python_version`, `hardware`, `--out`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
