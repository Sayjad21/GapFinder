# Gap Report: test-v12-01

Artifact `mlbench` · generated 2026-10-15 07:09 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -31.4% | +0.2% | ±2.4% | `normalize=minmax`, `n=6000` |

## C1: test_accuracy (paper 0.705)
**Fits but unsupported** · gap -31.4% → +0.2% · 59 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0075`, `B0195`, `B0196`, `B0197`, `B0198` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `n` naive `1200`, changed to `6000`
- Command:

  Replay: fork checkpoint `a2590fa3-e198-4373-90f6-f2736228077d` and run
  ```
  RUN_TAG=e5b2b5e9a961 "${PYTHON:-python3}" train.py --n 6000 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7017, 0.7067, 0.705, 0.7083, 0.7067; gap after +0.2%; result checkpoint `18837166-e463-4873-9713-55d33927869e`
- Effect: candidate 0.7067 minus naive 0.4833 = +0.2234, 95% bootstrap interval [+0.1678, +0.23] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.705 test accuracy.

- p. 1; value used: `test_accuracy` = 0.705 (headline claim)

### What did we measure?
- Naive median 0.4833 over 5 runs; repeats: 0.4833, 0.475, 0.5375, 0.5375, 0.4792
- Spread: range 0.475 to 0.5375, noise band ±0.0166 (2 x MAD), CV 6.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -31.4% (noise band ±2.4% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -35.1% (it comes back)
- PASS · Counterfactual (reversal test): without `n` the gap is -15.5% (it comes back)
- PASS · Held-out claim: C2: -23.5% to +0.4% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- FAIL · Evidence: `n=6000`: no evidence mentions '6000'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2234 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `hardware`, `python_version`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (8.79 noise units, gap -10.8%); `normalize=zscore` (6.13 noise units, gap +17.0%); `n=120` (6.02 noise units, gap -17.3%); `n=600` (4.52 noise units, gap -20.8%); `lr_schedule=step` (3.01 noise units, gap -24.4%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `n=12000`, `lr_schedule=cosine`: this claim -5.4%, mean |gap| 4.4% (5 runs)
  - `n=12000`, `normalize=minmax`: this claim +3.5%, mean |gap| 5.2% (5 runs)
  - `lr_schedule=cosine`: this claim -11.0%, mean |gap| 5.6% (6 runs)

### History matching (every measured configuration, all claims together)
- 24 of 57 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `n, normalize`: n=6000, normalize=minmax (max I 0.04); n=12000, normalize=minmax (max I 0.92); n=6000, normalize=zscore (max I 1.82); n=600, normalize=zscore (max I 1.9)
  - `lr_schedule, n`: lr_schedule=cosine, n=12000 (max I 0.92); lr_schedule=cosine, n=120 (max I 1.34); lr_schedule=cosine, n=5000 (max I 1.62); lr_schedule=cosine, n=6000 (max I 2); +1 more
  - `lr_schedule`: lr_schedule=cosine (max I 2.03)
- 3 separate islands (no single-knob move joins them): lr_schedule=cosine, n=12000; lr_schedule=cosine, n=120; lr_schedule=cosine, n=5000 | n=6000, normalize=minmax; n=12000, normalize=minmax; n=6000, normalize=zscore | class_weight=balanced, n=120; class_weight=balanced, n=6000; class_weight=balanced, n=12000

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'normalize': 'zscore', 'n': '6000'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax`, `n=6000` | 5 | +0.2% | +0.4% | 0.3% |
| `n=12000`, `lr_schedule=cosine` | 5 | -5.4% | +3.3% | 4.4% |
| `n=12000`, `normalize=minmax` | 5 | +3.5% | +6.9% | 5.2% |
| `lr_schedule=cosine` | 6 | -11.0% | -0.2% | 5.6% |
| `n=120`, `lr_schedule=cosine` | 5 | -11.3% | -2.2% | 6.8% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `n=1`: invalid_value, The value n=1 leads to an empty training set, causing an IndexError when accessing Xtr[0]; a minimal valid value that preserves the intent of a small n is 2; retried as `n=2`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `hardware`, `python_version`

## Provenance
- GapFinder commit: `f01fe3d9a0095f98d6304ad0543b917ca8e529eb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0433, sandbox reported $0.0000 (total $0.0433; this search; ledger extraction is included only if it shared the search's router)
