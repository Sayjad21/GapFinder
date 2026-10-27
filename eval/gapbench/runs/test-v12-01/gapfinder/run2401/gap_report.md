# Gap Report: test-v12-01

Artifact `mlbench` · generated 2026-10-16 01:26 · 143 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -32.6% | +0.7% | ±2.4% | `normalize=minmax`, `n=5000` |

## C1: test_accuracy (paper 0.705)
**Fits but unsupported** · gap -32.6% → +0.7% · 57 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0067`, `B0093`, `B0128` (3 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `n` naive `1200`, changed to `5000`
- Command:

  Replay: fork checkpoint `9230fe5e-f2f8-46f3-9197-d2392a2fb748` and run
  ```
  RUN_TAG=fe9c9af34d88 "${PYTHON:-python3}" train.py --n 5000 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.713, 0.71, 0.708; gap after +0.7%; result checkpoint `33dcefaa-7907-4c2b-801c-b4945c13f40b`
- Effect: candidate 0.71 minus naive 0.475 = +0.235, 95% bootstrap interval [+0.2287, +0.2446] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.705 test accuracy.

- p. 1; value used: `test_accuracy` = 0.705 (headline claim)

### What did we measure?
- Naive median 0.475 over 5 runs; repeats: 0.4667, 0.4833, 0.475, 0.4667, 0.475
- Spread: range 0.4667 to 0.4833, noise band ±0.0166 (2 x MAD), CV 1.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -32.6% (noise band ±2.4% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -22.6% (it comes back)
- PASS · Counterfactual (reversal test): without `n` the gap is -15.5% (it comes back)
- PASS · Held-out claim: C2: -24.9% to +2.3% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- FAIL · Evidence: `n=5000`: no evidence mentions '5000'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.235 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `hardware`, `python_version`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (9.04 noise units, gap -11.3%); `lr_schedule=step` (7.28 noise units, gap -15.5%); `n=2400` (7.16 noise units, gap -15.8%); `n=2000` (7.08 noise units, gap -16.0%); `normalize=zscore` (6.37 noise units, gap +17.6%) (and 4 more in the JSON)
- Near alternatives (closest across all claims):
  - `normalize=minmax`, `n=6000`: this claim -0.7%, mean |gap| 1.2% (3 runs)
  - `lr_schedule=cosine`, `n=12000`: this claim -5.1%, mean |gap| 4.3% (3 runs)
  - `lr_schedule=step`, `n=12000`: this claim -5.8%, mean |gap| 4.5% (3 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `n=5000, normalize=minmax` (reported)
- `n=6000, normalize=minmax`
- `n=2400, normalize=zscore`

### History matching (every measured configuration, all claims together)
- 10 of 55 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `n, normalize`: n=6000, normalize=minmax (max I 0.18); n=5000, normalize=minmax (max I 0.47); n=12000, normalize=minmax (max I 1.57); n=2400, normalize=zscore (max I 2.22); +1 more
  - `lr_schedule, n`: lr_schedule=cosine, n=12000 (max I 1.06); lr_schedule=step, n=12000 (max I 1.91); lr_schedule=cosine, n=5000 (max I 2.22); lr_schedule=cosine, n=6000 (max I 2.34)
  - `lr_schedule`: lr_schedule=cosine (max I 2.25)
- 2 separate islands (no single-knob move joins them): n=6000, normalize=minmax; n=5000, normalize=minmax; n=12000, normalize=minmax | lr_schedule=cosine, n=12000; lr_schedule=step, n=12000; lr_schedule=cosine, n=5000
- Equally good values: `n` in {5000, 6000}

Notes:
- configurations the target claim can't tell apart from the answer: n=5000, normalize=minmax; n=6000, normalize=minmax; n=2400, normalize=zscore
- equally good values within one noise band (measured): n in {5000, 6000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax`, `n=6000` | 3 | -0.7% | -1.6% | 1.2% |
| `normalize=minmax`, `n=5000` | 3 | +0.7% | +2.3% | 1.5% |
| `lr_schedule=cosine`, `n=12000` | 3 | -5.1% | +3.4% | 4.3% |
| `lr_schedule=step`, `n=12000` | 3 | -5.8% | +3.2% | 4.5% |
| `lr_schedule=cosine`, `n=5000` | 3 | -11.1% | -0.7% | 5.9% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `n=1`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `hardware`, `python_version`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
