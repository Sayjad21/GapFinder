# Gap Report: test-v12-01

Artifact `mlbench` · generated 2026-10-15 07:10 · 199 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -31.4% | +0.5% | ±4.7% | `normalize=zscore`, `n=120` |

## C1: test_accuracy (paper 0.705)
**Fits but unsupported** · gap -31.4% → +0.5% · 60 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0058`, `B0124`, `B0125`, `B0126`, `B0127` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Config: `n` naive `1200`, changed to `120`
- Command:

  Replay: fork checkpoint `df7974f8-4360-4b34-b94c-b53c9ad53f5e` and run
  ```
  RUN_TAG=35b76c4dd5b4 "${PYTHON:-python3}" train.py --n 120 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.75, 0.7083, 0.7083, 0.7083, 0.7083; gap after +0.5%; result checkpoint `bf34e648-1e69-48fd-8aa9-07bc60f3fe70`
- Effect: candidate 0.7083 minus naive 0.4833 = +0.225, 95% bootstrap interval [+0.1541, +0.2567] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.705 test accuracy.

- p. 1; value used: `test_accuracy` = 0.705 (headline claim)

### What did we measure?
- Naive median 0.4833 over 5 runs; repeats: 0.5375, 0.475, 0.5792, 0.4667, 0.4833
- Spread: range 0.4667 to 0.5792, noise band ±0.0332 (2 x MAD), CV 9.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -31.4% (noise band ±4.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -17.3% (it comes back)
- PASS · Counterfactual (reversal test): without `n` the gap is +17.6% (it comes back)
- PASS · Held-out claim: C2: -23.5% to +13.5% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- FAIL · Evidence: `n=120`: no evidence mentions '120'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.225 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `hardware`, `python_version`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (4.02 noise units, gap -12.5%); `normalize=minmax` (3.39 noise units, gap -15.5%); `n=6000` (3.29 noise units, gap -16.0%); `n=2400` (2.39 noise units, gap -20.2%); `n=12000` (2.16 noise units, gap -21.3%)
- Near alternatives (closest across all claims):
  - `normalize=minmax`, `n=6000`: this claim -0.7%, mean |gap| 1.2% (5 runs)
  - `n=12000`, `lr_schedule=cosine`: this claim -4.8%, mean |gap| 4.3% (5 runs)
  - `lr_schedule=step`, `n=120`: this claim -5.4%, mean |gap| 5.3% (5 runs)

### History matching (every measured configuration, all claims together)
- 40 of 58 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `n, normalize`: n=6000, normalize=minmax (max I 0.17); n=12000, normalize=minmax (max I 1.15); n=2400, normalize=zscore (max I 1.6)
  - `lr_schedule, n`: lr_schedule=cosine, n=12000 (max I 0.75); lr_schedule=cosine, n=5000 (max I 1.11); lr_schedule=cosine, n=120 (max I 1.16); lr_schedule=step, n=120 (max I 1.16); +2 more
  - `lr_schedule`: lr_schedule=cosine (max I 1.77)

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'lr_schedule': 'step', 'normalize': 'zscore'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax`, `n=6000` | 5 | -0.7% | -1.6% | 1.2% |
| `n=12000`, `lr_schedule=cosine` | 5 | -4.8% | +3.9% | 4.3% |
| `lr_schedule=step`, `n=120` | 5 | -5.4% | +5.1% | 5.3% |
| `normalize=minmax`, `n=12000` | 5 | +4.0% | +7.7% | 5.8% |
| `n=2400`, `normalize=zscore` | 5 | +0.8% | +11.1% | 6.0% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `n=1`: invalid_value, The value n=1 caused an IndexError because the training set became empty, indicating that n must be larger than 1 for the algorithm to function; retried as `n=2`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `hardware`, `python_version`

## Provenance
- GapFinder commit: `f01fe3d9a0095f98d6304ad0543b917ca8e529eb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0007, sandbox reported $0.0000 (total $0.0007; this search; ledger extraction is included only if it shared the search's router)
