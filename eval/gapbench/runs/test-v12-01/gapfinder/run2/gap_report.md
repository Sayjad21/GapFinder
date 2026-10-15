# Gap Report: test-v12-01

Artifact `mlbench` · generated 2026-10-15 08:00 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -30.9% | +0.8% | ±5.9% | `normalize=zscore`, `n=2400` |

## C1: test_accuracy (paper 0.705)
**Fits but unsupported** · gap -30.9% → +0.8% · 64 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0071`, `B0141`, `B0142`, `B0143`, `B0144` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Config: `n` naive `1200`, changed to `2400`
- Command:

  Replay: fork checkpoint `29ff47a3-1c13-4c23-80b1-d93be645d45a` and run
  ```
  RUN_TAG=dc202c27ad7b "${PYTHON:-python3}" train.py --n 2400 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7104, 0.7104, 0.7125, 0.7125, 0.7083; gap after +0.8%; result checkpoint `f29e4e38-d816-46e5-80fb-c80ed4ca3b97`
- Effect: candidate 0.7104 minus naive 0.4875 = +0.2229, 95% bootstrap interval [+0.1729, +0.2366] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.705 test accuracy.

- p. 1; value used: `test_accuracy` = 0.705 (headline claim)

### What did we measure?
- Naive median 0.4875 over 5 runs; repeats: 0.5375, 0.5375, 0.4667, 0.4875, 0.4875
- Spread: range 0.4667 to 0.5375, noise band ±0.0416 (2 x MAD), CV 6.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -30.9% (noise band ±5.9% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -37.5% (it comes back)
- PASS · Counterfactual (reversal test): without `n` the gap is +17.3% (it comes back)
- PASS · Held-out claim: C2: -22.7% to +11.1% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- FAIL · Evidence: `n=2400`: no evidence mentions '2400'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2229 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `python_version`, `hardware`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (3.11 noise units, gap -12.5%); `n=200` (2.7 noise units, gap -14.9%); `normalize=minmax` (2.6 noise units, gap -15.5%); `n=240` (2.3 noise units, gap -17.3%); `n=600` (1.7 noise units, gap -20.8%) (and 2 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=cosine`, `n=12000`: this claim -5.4%, mean |gap| 4.4% (5 runs)
  - `normalize=zscore`, `n=200`: this claim -4.3%, mean |gap| 6.1% (5 runs)
  - `normalize=minmax`, `n=12000`: this claim +4.6%, mean |gap| 6.8% (5 runs)

### History matching (every measured configuration, all claims together)
- 22 of 61 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `n, normalize`: n=6000, normalize=minmax (max I 0.06); n=200, normalize=zscore (max I 1.13); n=12000, normalize=minmax (max I 1.44); n=2400, normalize=zscore (max I 1.77); +4 more
  - `lr_schedule, n`: lr_schedule=cosine, n=12000 (max I 0.9)
  - `lr_schedule`: lr_schedule=cosine (max I 2.13)
- 4 separate islands (no single-knob move joins them): n=6000, normalize=minmax; n=200, normalize=zscore; n=12000, normalize=minmax | lr_schedule=cosine, n=12000; lr_schedule=cosine; class_weight=balanced, lr_schedule=cosine | lr_schedule=step, normalize=minmax | class_weight=balanced, n=12000

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'n': '12000', 'normalize': 'zscore'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=cosine`, `n=12000` | 5 | -5.4% | +3.4% | 4.4% |
| `normalize=zscore`, `n=2400` | 5 | +0.8% | +11.1% | 6.0% |
| `normalize=zscore`, `n=200` | 5 | -4.3% | +7.9% | 6.1% |
| `normalize=minmax`, `n=12000` | 5 | +4.6% | +9.1% | 6.8% |
| `lr_schedule=cosine` | 3 | -12.5% | -1.9% | 7.2% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `n=1`: invalid_value, Setting n=1 results in too few samples after the data split, leading to an empty training set and an IndexError when trying to access Xtr[0]. A small but valid value like 200 preserves the intent of using a reduced dataset size while avoiding the crash; retried as `n=200`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `python_version`, `hardware`, `--out`

## Provenance
- GapFinder commit: `f01fe3d9a0095f98d6304ad0543b917ca8e529eb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0599, sandbox reported $0.0000 (total $0.0599; this search; ledger extraction is included only if it shared the search's router)
