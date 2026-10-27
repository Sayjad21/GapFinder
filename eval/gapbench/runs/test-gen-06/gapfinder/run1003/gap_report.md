# Gap Report: test-gen-06

Artifact `mlbench` · generated 2026-10-15 00:18 · 199 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -34.3% | +0.0% | ±5.6% | `n=600`, `normalize=zscore` |

## C1: test_accuracy (paper 0.7417)
**Fits but unsupported** · gap -34.3% → +0.0% · 53 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0083`, `B0154`, `B0155`, `B0156`, `B0157` (5 run(s) of the same config)
- Config: `n` naive `1200`, changed to `600`
- Config: `normalize` naive `none`, changed to `zscore`
- Command:

  Replay: fork checkpoint `e419abb5-8485-42f0-b9c9-278f747ba554` and run
  ```
  RUN_TAG=1f3ccc2ed856 "${PYTHON:-python3}" train.py --n 600 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7417, 0.7417, 0.7417, 0.7417, 0.7417; gap after +0.0%; result checkpoint `b874feb0-c205-451f-b423-c28286381349`
- Effect: candidate 0.7417 minus naive 0.4875 = +0.2542, 95% bootstrap interval [+0.2042, +0.2708] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.742 test accuracy and 0.700 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7417 (headline claim)

### What did we measure?
- Naive median 0.4875 over 5 runs; repeats: 0.5375, 0.4875, 0.5375, 0.4667, 0.4875
- Spread: range 0.4667 to 0.5375, noise band ±0.0416 (2 x MAD), CV 6.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -34.3% (noise band ±5.6% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `n` the gap is +11.8% (it comes back)
- PASS · Counterfactual (reversal test): without `normalize` the gap is -24.7% (it comes back)
- PASS · Held-out claim: C2: -30.9% to +0.0% (not worse beyond noise)
- FAIL · Evidence: `n=600`: no evidence mentions '600'; it fits, but nothing says the authors used it
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2542 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `SCALES`, `WEIGHTS`, `RUN_TAG`, `num_runs`, `aggregation_method`, `feature_count`, `python_version`, `os`, `cpu`, `memory`, `random_module`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `n=24` (4.71 noise units, gap +7.9%); `n=120` (4.31 noise units, gap -10.1%); `lr_schedule=cosine` (3.31 noise units, gap -15.7%); `normalize=minmax` (2.6 noise units, gap -19.7%); `n=6000` (1.98 noise units, gap -23.1%) (and 6 more in the JSON)
- Near alternatives (closest across all claims):
  - `n=6000`, `normalize=zscore`: this claim +1.0%, mean |gap| 1.8% (5 runs)
  - `n=12000`, `normalize=minmax`: this claim -1.0%, mean |gap| 2.3% (5 runs)
  - `normalize=zscore`, `n=2400`: this claim -4.2%, mean |gap| 2.5% (5 runs)

### History matching (every measured configuration, all claims together)
- 19 of 52 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `n, normalize`: n=600, normalize=zscore (max I 0); n=6000, normalize=zscore (max I 0.42); n=12000, normalize=minmax (max I 0.49); n=12000, normalize=zscore (max I 0.65); +3 more
  - `lr_schedule, n`: lr_schedule=cosine, n=12000 (max I 1.75); lr_schedule=cosine, n=120 (max I 1.96)
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 1.79)
- 2 separate islands (no single-knob move joins them): n=600, normalize=zscore; n=6000, normalize=zscore; n=12000, normalize=minmax | class_weight=balanced, n=24

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'n': '600', 'normalize': 'minmax'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `n=600`, `normalize=zscore` | 5 | +0.0% | +0.0% | 0.0% |
| `n=6000`, `normalize=zscore` | 5 | +1.0% | +2.6% | 1.8% |
| `n=12000`, `normalize=minmax` | 5 | -1.0% | -3.5% | 2.3% |
| `normalize=zscore`, `n=2400` | 5 | -4.2% | -0.7% | 2.5% |
| `n=12000`, `normalize=zscore` | 5 | +2.0% | +4.0% | 3.0% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `n=1`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `SCALES`, `WEIGHTS`, `RUN_TAG`, `num_runs`, `aggregation_method`, `feature_count`, `python_version`, `os`, `cpu`, `memory`, `random_module`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
