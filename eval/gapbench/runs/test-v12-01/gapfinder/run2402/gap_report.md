# Gap Report: test-v12-01

Artifact `mlbench` · generated 2026-10-16 01:28 · 194 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -31.4% | +0.8% | ±4.7% | `n=2400`, `normalize=zscore` |

## C1: test_accuracy (paper 0.705)
**Fits but unsupported** · gap -31.4% → +0.8% · 61 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0081`, `B0098`, `B0137`, `B0138`, `B0139` (5 run(s) of the same config)
- Config: `n` naive `1200`, changed to `2400`
- Config: `normalize` naive `none`, changed to `zscore`
- Command:

  Replay: fork checkpoint `8697cfa8-048c-4ccd-b4e8-23720eea7eeb` and run
  ```
  RUN_TAG=5cf6899bc58e "${PYTHON:-python3}" train.py --n 2400 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7104, 0.7146, 0.7104, 0.7104, 0.7125; gap after +0.8%; result checkpoint `bf365c39-765c-44fd-a09b-80b80b667c2f`
- Effect: candidate 0.7104 minus naive 0.4833 = +0.2271, 95% bootstrap interval [+0.1704, +0.2412] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.705 test accuracy.

- p. 1; value used: `test_accuracy` = 0.705 (headline claim)

### What did we measure?
- Naive median 0.4833 over 5 runs; repeats: 0.5458, 0.4833, 0.4667, 0.5375, 0.475
- Spread: range 0.4667 to 0.5458, noise band ±0.0332 (2 x MAD), CV 7.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -31.4% (noise band ±4.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `n` the gap is +17.6% (it comes back)
- PASS · Counterfactual (reversal test): without `normalize` the gap is -36.5% (it comes back)
- PASS · Held-out claim: C2: -23.5% to +11.2% (not worse beyond noise)
- FAIL · Evidence: `n=2400`: no evidence mentions '2400'; it fits, but nothing says the authors used it
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2271 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `python_version`, `hardware`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `n=12000` (4.39 noise units, gap -10.8%); `lr_schedule=cosine` (4.14 noise units, gap -11.9%); `normalize=minmax` (3.39 noise units, gap -15.5%); `n=120` (3.01 noise units, gap -17.3%); `n=600` (2.26 noise units, gap -20.8%)
- Near alternatives (closest across all claims):
  - `normalize=minmax`, `n=6000`: this claim -1.8%, mean |gap| 2.5% (5 runs)
  - `n=12000`, `lr_schedule=cosine`: this claim -5.1%, mean |gap| 4.3% (5 runs)
  - `lr_schedule=cosine`, `n=120`: this claim -5.4%, mean |gap| 5.3% (5 runs)

### Equally good configurations
The target claim can't tell these 2 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `n=2400, normalize=zscore` (reported)
- `n=6000, normalize=minmax`

### History matching (every measured configuration, all claims together)
- 23 of 58 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `n, normalize`: n=6000, normalize=minmax (max I 0.29); n=12000, normalize=minmax (max I 1.1); n=2400, normalize=zscore (max I 1.72); n=600, normalize=zscore (max I 1.8)
  - `lr_schedule, n`: lr_schedule=cosine, n=12000 (max I 0.87); lr_schedule=cosine, n=120 (max I 1.87); lr_schedule=cosine, n=6000 (max I 1.93); lr_schedule=cosine, n=2400 (max I 2.15); +1 more
  - `lr_schedule`: lr_schedule=cosine (max I 2.21)
- 3 separate islands (no single-knob move joins them): lr_schedule=cosine, n=12000; lr_schedule=cosine, n=120; lr_schedule=cosine, n=6000 | n=6000, normalize=minmax; n=12000, normalize=minmax; n=2400, normalize=zscore | class_weight=balanced, n=120
- Equally good values: `n` in {600, 2400}

Notes:
- configurations the target claim can't tell apart from the answer: n=2400, normalize=zscore; n=6000, normalize=minmax
- equally good values within one noise band (measured): n in {600, 2400}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax`, `n=6000` | 5 | -1.8% | -3.3% | 2.5% |
| `n=12000`, `lr_schedule=cosine` | 5 | -5.1% | +3.5% | 4.3% |
| `lr_schedule=cosine`, `n=120` | 5 | -5.4% | +5.1% | 5.3% |
| `n=12000`, `normalize=minmax` | 5 | +3.9% | +7.6% | 5.7% |
| `normalize=zscore`, `n=2400` | 5 | +0.8% | +11.2% | 6.0% |

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
