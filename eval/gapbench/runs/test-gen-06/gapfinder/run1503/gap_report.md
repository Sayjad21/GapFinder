# Gap Report: test-gen-06

Artifact `mlbench` · generated 2026-10-15 19:15 · 182 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -34.3% | +0.0% | ±5.6% | `normalize=zscore`, `n=600` |

## C1: test_accuracy (paper 0.7417)
**Fits but unsupported** · gap -34.3% → +0.0% · 61 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0048`, `B0093`, `B0129`, `B0130`, `B0131` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Config: `n` naive `1200`, changed to `600`
- Command:

  Replay: fork checkpoint `1e90add8-33fd-48a5-a7a7-e53d3cf772b9` and run
  ```
  RUN_TAG=4912630d5d5b "${PYTHON:-python3}" train.py --n 600 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7417, 0.7417, 0.7417, 0.7417, 0.7417; gap after +0.0%; result checkpoint `a3deba02-923b-4b3d-878e-c84a8ca68543`
- Effect: candidate 0.7417 minus naive 0.4875 = +0.2542, 95% bootstrap interval [+0.2, +0.2684] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.742 test accuracy and 0.700 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7417 (headline claim)

### What did we measure?
- Naive median 0.4875 over 5 runs; repeats: 0.4667, 0.4875, 0.5417, 0.5417, 0.4833
- Spread: range 0.4667 to 0.5417, noise band ±0.0416 (2 x MAD), CV 7.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -34.3% (noise band ±5.6% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -25.8% (it comes back)
- PASS · Counterfactual (reversal test): without `n` the gap is +11.2% (it comes back)
- PASS · Held-out claim: C2: -30.9% to +0.0% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- FAIL · Evidence: `n=600`: no evidence mentions '600'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2542 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `SCALES`, `WEIGHTS`, `RUN_TAG`, `num_runs`, `aggregation_method`, `feature_count`, `python_version`, `os`, `cpu`, `memory`, `random_module`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (3.5 noise units, gap -14.6%); `normalize=minmax` (2.6 noise units, gap -19.7%); `n=6000` (1.88 noise units, gap -23.7%); `lr_schedule=step` (1.8 noise units, gap -24.2%); `n=12000` (1.5 noise units, gap -25.8%)
- Near alternatives (closest across all claims):
  - `normalize=zscore`, `n=6000`: this claim +0.9%, mean |gap| 1.7% (5 runs)
  - `normalize=zscore`, `n=2400`: this claim -4.2%, mean |gap| 2.5% (5 runs)
  - `normalize=minmax`, `n=12000`: this claim -1.3%, mean |gap| 2.7% (5 runs)

### Equally good configurations
The target claim can't tell these 5 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `n=600, normalize=zscore` (reported)
- `n=6000, normalize=zscore`
- `n=12000, normalize=minmax`
- `n=120, normalize=zscore`
- `n=12000, normalize=zscore`

### History matching (every measured configuration, all claims together)
- 22 of 58 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `n, normalize`: n=600, normalize=zscore (max I 0); n=6000, normalize=zscore (max I 0.4); n=120, normalize=zscore (max I 0.58); n=12000, normalize=minmax (max I 0.65); +5 more
  - `lr_schedule, n`: lr_schedule=cosine, n=12000 (max I 1.69)
- Equally good values: `n` in {120, 600, 1000, 2000, 2400, 6000, 12000}

Notes:
- configurations the target claim can't tell apart from the answer: n=600, normalize=zscore; n=6000, normalize=zscore; n=12000, normalize=minmax; n=120, normalize=zscore; n=12000, normalize=zscore
- equally good values within one noise band (measured): n in {120, 600, 1000, 2000, 2400, 6000, 12000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore`, `n=600` | 5 | +0.0% | +0.0% | 0.0% |
| `normalize=zscore`, `n=6000` | 5 | +0.9% | +2.5% | 1.7% |
| `normalize=zscore`, `n=2400` | 5 | -4.2% | -0.7% | 2.5% |
| `normalize=minmax`, `n=12000` | 5 | -1.3% | -4.0% | 2.7% |
| `normalize=zscore`, `n=120` | 5 | -4.5% | +1.3% | 2.9% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `n=1`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `SCALES`, `WEIGHTS`, `RUN_TAG`, `num_runs`, `aggregation_method`, `feature_count`, `python_version`, `os`, `cpu`, `memory`, `random_module`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
