# Gap Report: test-v12-01

Artifact `mlbench` · generated 2026-10-15 08:00 · 144 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Explained | -22.0% | +0.8% | ±2.4% | `normalize=zscore`, `n=2400` |

## C1: test_accuracy (paper 0.705)
**Explained** · gap -22.0% → +0.8% · 61 hypotheses tested
> Interacting factors: these changes close the gap only together, and every check passes

### Which experiment changed it?
- Branch: `B0040`, `B0093`, `B0094` (3 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Config: `n` naive `1200`, changed to `2400`
- Command:

  Replay: fork checkpoint `772e2e71-84ff-4639-88d0-265d0bc5b651` and run
  ```
  RUN_TAG=546a503d94dd "${PYTHON:-python3}" train.py --n 2400 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7104, 0.7167, 0.7104; gap after +0.8%; result checkpoint `9356043b-bff9-430d-9f87-ebe358da10b9`
- Effect: candidate 0.7104 minus naive 0.55 = +0.1604, 95% bootstrap interval [+0.1417, +0.1763] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.705 test accuracy.

- p. 1; value used: `test_accuracy` = 0.705 (headline claim)

### What did we measure?
- Naive median 0.55 over 5 runs; repeats: 0.5333, 0.5417, 0.5792, 0.55, 0.5583
- Spread: range 0.5333 to 0.5792, noise band ±0.0166 (2 x MAD), CV 3.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -22.0% (noise band ±2.4% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is +0.1604 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `python_version`, `hardware`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (3.51 noise units, gap -13.7%); `normalize=minmax` (2.76 noise units, gap -15.5%)
- Near alternatives (closest across all claims):
  - `n=6000`, `normalize=minmax`: this claim -0.4%, mean |gap| 0.7% (3 runs)
  - `lr_schedule=cosine`, `n=12000`: this claim -5.0%, mean |gap| 4.3% (3 runs)
  - `n=120`, `lr_schedule=cosine`: this claim -5.4%, mean |gap| 5.8% (3 runs)

### Equally good configurations
The target claim can't tell these 2 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `n=2400, normalize=zscore` (reported)
- `n=6000, normalize=minmax`

### History matching (every measured configuration, all claims together)
- 15 of 58 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `n, normalize`: n=6000, normalize=minmax (max I 0.09); n=12000, normalize=minmax (max I 1.59); n=2400, normalize=zscore (max I 2.19); n=600, normalize=zscore (max I 2.28)
  - `lr_schedule, n`: lr_schedule=cosine, n=12000 (max I 0.86); lr_schedule=cosine, n=120 (max I 1.11); lr_schedule=cosine, n=6000 (max I 2.19); lr_schedule=step, n=12000 (max I 2.29)
  - `lr_schedule`: lr_schedule=cosine (max I 2.15)
  - `class_weight, lr_schedule`: class_weight=balanced, lr_schedule=cosine (max I 2.53)
- 2 separate islands (no single-knob move joins them): lr_schedule=cosine, n=12000; lr_schedule=cosine, n=120; lr_schedule=cosine | n=6000, normalize=minmax; n=12000, normalize=minmax; n=2400, normalize=zscore

Notes:
- configurations the target claim can't tell apart from the answer: n=2400, normalize=zscore; n=6000, normalize=minmax

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `n=6000`, `normalize=minmax` | 3 | -0.4% | -1.0% | 0.7% |
| `lr_schedule=cosine`, `n=12000` | 3 | -5.0% | +3.6% | 4.3% |
| `n=120`, `lr_schedule=cosine` | 3 | -5.4% | +6.2% | 5.8% |
| `normalize=zscore`, `n=2400` | 3 | +0.8% | +11.1% | 6.0% |
| `lr_schedule=cosine` | 4 | -11.9% | -1.1% | 6.5% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `n=1`: crash, Setting n=1 likely reduces the dataset size to a point where after splitting there are no training samples, causing Xtr to be empty and the subsequent indexing operation to raise an IndexError

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `python_version`, `hardware`, `--out`

## Provenance
- GapFinder commit: `f01fe3d9a0095f98d6304ad0543b917ca8e529eb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0006, sandbox reported $0.0000 (total $0.0006; this search; ledger extraction is included only if it shared the search's router)
