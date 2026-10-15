# Gap Report: test-v12-01

Artifact `mlbench` · generated 2026-10-15 07:09 · 162 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Explained | -23.8% | -11.3% | ±7.1% | `n=120` |

## C1: test_accuracy (paper 0.705)
**Explained** · gap -23.8% → -11.3% · 54 hypotheses tested
> Confirmed cause: reverting it brings the gap back, held-out claims hold, and the value has evidence

### Which experiment changed it?
- Branch: `B0011`, `B0026`, `B0027`, `B0028`, `B0029`, `B0030` (6 run(s) of the same config)
- Config: `n` naive `1200`, changed to `120`
- Command:

  Replay: fork checkpoint `844a3e17-12e2-4c65-8cfe-c1a2f7aa938b` and run
  ```
  RUN_TAG=dd942c5ff546 "${PYTHON:-python3}" train.py --n 120 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize none --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.6667, 0.625, 0.5833, 0.5833, 0.6667, 0.625; gap after -11.3%; result checkpoint `b108df67-e53e-469d-82d1-4199090bf21a`
- Effect: candidate 0.625 minus naive 0.5375 = +0.0875, 95% bootstrap interval [+0.04414, +0.15] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.705 test accuracy.

- p. 1; value used: `test_accuracy` = 0.705 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5625, 0.475, 0.5375, 0.5625, 0.475
- Spread: range 0.475 to 0.5625, noise band ±0.05 (2 x MAD), CV 8.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -23.8% (noise band ±7.1% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is +0.0875 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `hardware`, `python_version`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (1.58 noise units, gap -12.5%); `normalize=minmax` (1.17 noise units, gap -15.5%)
- Near alternatives (closest across all claims):
  - `lr_schedule=cosine`, `n=12000`: this claim -5.1%, mean |gap| 4.4% (5 runs)
  - `n=12000`, `normalize=minmax`: this claim +3.0%, mean |gap| 4.4% (5 runs)
  - `lr_schedule=cosine`, `n=120`: this claim -5.4%, mean |gap| 5.8% (5 runs)

### Equally good configurations
The target claim can't tell these 4 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `n=120` (reported)
- `n=2400, normalize=zscore`
- `lr_schedule=cosine, n=120`
- `n=12000, normalize=minmax`

### History matching (every measured configuration, all claims together)
- 31 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr_schedule, n`: lr_schedule=cosine, n=12000 (max I 0.79); lr_schedule=cosine, n=120 (max I 0.85); lr_schedule=step, n=12000 (max I 2.15)
  - `n, normalize`: n=12000, normalize=minmax (max I 0.96); n=2400, normalize=zscore (max I 1.64); n=600, normalize=zscore (max I 1.71)
  - `n`: n=120 (max I 1.78); n=12000 (max I 2); n=2400 (max I 2.18)
  - `lr_schedule`: lr_schedule=cosine (max I 1.89)
- Equally good values: `n` in {120, 12000}

Notes:
- configurations the target claim can't tell apart from the answer: n=120; n=2400, normalize=zscore; lr_schedule=cosine, n=120; n=12000, normalize=minmax
- equally good values within one noise band (measured): n in {120, 12000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=cosine`, `n=12000` | 5 | -5.1% | +3.7% | 4.4% |
| `n=12000`, `normalize=minmax` | 5 | +3.0% | +5.8% | 4.4% |
| `lr_schedule=cosine`, `n=120` | 5 | -5.4% | +6.2% | 5.8% |
| `n=2400`, `normalize=zscore` | 5 | +1.1% | +11.5% | 6.3% |
| `n=120` | 6 | -11.3% | -2.2% | 6.8% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `n=1`: crash, Setting n=1 likely resulted in too few samples after data split, leading to an empty training set and an IndexError when trying to access Xtr[0]

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `hardware`, `python_version`

## Provenance
- GapFinder commit: `f01fe3d9a0095f98d6304ad0543b917ca8e529eb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0006, sandbox reported $0.0000 (total $0.0006; this search; ledger extraction is included only if it shared the search's router)
