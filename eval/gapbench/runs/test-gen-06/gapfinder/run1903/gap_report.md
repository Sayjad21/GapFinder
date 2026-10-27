# Gap Report: test-gen-06

Artifact `mlbench` · generated 2026-10-15 19:39 · 122 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -27.5% | +0.0% | ±2.2% | `n=600`, `normalize=zscore` |

## C1: test_accuracy (paper 0.7417)
**Fits but unsupported** · gap -27.5% → +0.0% · 53 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0051`, `B0079`, `B0108` (3 run(s) of the same config)
- Config: `n` naive `1200`, changed to `600`
- Config: `normalize` naive `none`, changed to `zscore`
- Command:

  Replay: fork checkpoint `282bcc6c-003b-40f0-8cd0-84e7764c867f` and run
  ```
  RUN_TAG=1e6a243f24b7 "${PYTHON:-python3}" train.py --n 600 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7417, 0.7417, 0.7417; gap after +0.0%; result checkpoint `af64cf42-082c-4093-90df-dc9da7aaaf70`
- Effect: candidate 0.7417 minus naive 0.5375 = +0.2042, 95% bootstrap interval [+0.1992, +0.2408] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.742 test accuracy and 0.700 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7417 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5208, 0.4917, 0.5375, 0.5458, 0.5375
- Spread: range 0.4917 to 0.5458, noise band ±0.0166 (2 x MAD), CV 4.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -27.5% (noise band ±2.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `n` the gap is +11.8% (it comes back)
- PASS · Counterfactual (reversal test): without `normalize` the gap is -24.7% (it comes back)
- PASS · Held-out claim: C2: -22.6% to +0.0% (not worse beyond noise)
- FAIL · Evidence: `n=600`: no evidence mentions '600'; it fits, but nothing says the authors used it
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2042 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `SCALES`, `WEIGHTS`, `RUN_TAG`, `num_runs`, `aggregation_method`, `feature_count`, `python_version`, `os`, `cpu`, `memory`, `random_module`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `n=24` (8.79 noise units, gap +7.9%); `lr_schedule=cosine` (6.02 noise units, gap -14.0%); `normalize=minmax` (3.51 noise units, gap -19.7%); `n=6000` (2.86 noise units, gap -21.1%); `lr_schedule=step` (2.01 noise units, gap -23.0%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `n=6000`, `normalize=zscore`: this claim +1.1%, mean |gap| 1.9% (3 runs)
  - `n=12000`, `normalize=minmax`: this claim -1.1%, mean |gap| 2.3% (3 runs)
  - `normalize=zscore`, `n=2400`: this claim -4.2%, mean |gap| 2.5% (3 runs)

### Equally good configurations
The target claim can't tell these 5 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `n=600, normalize=zscore` (reported)
- `n=6000, normalize=zscore`
- `n=12000, normalize=minmax`
- `n=12000, normalize=zscore`
- `class_weight=balanced, normalize=minmax`

### History matching (every measured configuration, all claims together)
- 16 of 52 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `n, normalize`: n=600, normalize=zscore (max I 0); n=6000, normalize=zscore (max I 0.48); n=12000, normalize=minmax (max I 0.69); n=12000, normalize=zscore (max I 0.71); +3 more
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 1.84); class_weight=balanced, normalize=zscore (max I 2.11)
  - `lr_schedule, n`: lr_schedule=cosine, n=12000 (max I 1.87)
- Equally good values: `n` in {600, 6000, 12000}

Notes:
- configurations the target claim can't tell apart from the answer: n=600, normalize=zscore; n=6000, normalize=zscore; n=12000, normalize=minmax; n=12000, normalize=zscore; class_weight=balanced, normalize=minmax
- equally good values within one noise band (measured): n in {600, 6000, 12000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `n=600`, `normalize=zscore` | 3 | +0.0% | +0.0% | 0.0% |
| `n=6000`, `normalize=zscore` | 3 | +1.1% | +2.7% | 1.9% |
| `n=12000`, `normalize=minmax` | 3 | -1.1% | -3.6% | 2.3% |
| `normalize=zscore`, `n=2400` | 3 | -4.2% | -0.7% | 2.5% |
| `n=12000`, `normalize=zscore` | 3 | +2.1% | +4.1% | 3.1% |

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
