# Gap Report: test-v11-03

Artifact `mlbench` · generated 2026-10-14 22:18 · 164 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -30.3% | -1.1% | ±3.2% | `lr_schedule=cosine`, `positive_rate=0.1` |

## C1: test_accuracy (paper 0.7833)
**Fits but unsupported** · gap -30.3% → -1.1% · 72 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0093`, `B0139`, `B0140` (3 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `cosine`
- Config: `positive_rate` naive `0.3`, changed to `0.1`
- Command:

  Replay: fork checkpoint `cbeca520-90e0-48db-8c6c-e26e2cbeccd0` and run
  ```
  RUN_TAG=3b97fb968cdd "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.1 --label_noise 0.05 --split 0.8 --normalize none --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule cosine --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7542, 0.7917, 0.775; gap after -1.1%; result checkpoint `40210529-b514-4c93-8f2c-a4c6f0d2af9e`
- Effect: candidate 0.775 minus naive 0.5458 = +0.2292, 95% bootstrap interval [+0.1967, +0.2634] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.783 test accuracy and 0.752 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7833 (headline claim)

### What did we measure?
- Naive median 0.5458 over 5 runs; repeats: 0.5583, 0.5625, 0.5458, 0.5167, 0.5333
- Spread: range 0.5167 to 0.5625, noise band ±0.025 (2 x MAD), CV 3.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -30.3% (noise band ±3.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is -35.1% (it comes back)
- PASS · Counterfactual (reversal test): without `positive_rate` the gap is -20.7% (it comes back)
- PASS · Held-out claim: C2: -27.1% to -21.2% (not worse beyond noise)
- FAIL · Evidence: `lr_schedule=cosine`: no evidence mentions 'cosine'; it fits, but nothing says the authors used it
- FAIL · Evidence: `positive_rate=0.1`: no evidence mentions '0.1'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2292 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `aggregation_method`, `num_runs`, `shuffling_seed_method`, `SCALES`, `WEIGHTS`, `weight_init_scale`, `bias_init`, `logit_intercept_formula`, `label_noise_mechanism`, `sigmoid_clip_range`, `random_module`, `hardware_cpu`, `os_python_version`, `batch_gradient_aggregation`, `class_weight_balanced_formula`, `floating_point_precision`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (7.66 noise units, gap +5.9%); `normalize=minmax` (2 noise units, gap -23.9%); `positive_rate=0.65` (1 noise units, gap -27.1%)
- Near alternatives (closest across all claims):
  - `normalize=minmax`, `batch_size=1`: this claim +2.7%, mean |gap| 2.7% (3 runs)
  - `normalize=zscore`, `batch_size=1`: this claim +3.2%, mean |gap| 4.0% (3 runs)
  - `normalize=zscore`, `batch_size=3200`: this claim +4.8%, mean |gap| 5.6% (3 runs)

### Equally good configurations
The target claim can't tell these 2 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `lr_schedule=cosine, positive_rate=0.1` (reported)
- `batch_size=1, normalize=minmax`

### History matching (every measured configuration, all claims together)
- 8 of 71 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 8 configurations
  - `batch_size, normalize`: batch_size=1, normalize=minmax (max I 0.52); batch_size=1, normalize=zscore (max I 0.98); batch_size=3200, normalize=zscore (max I 1.2); batch_size=320, normalize=zscore (max I 1.35)
  - `batch_size, lr_schedule`: batch_size=1, lr_schedule=cosine (max I 1.37)
  - `normalize`: normalize=zscore (max I 1.42)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.45); lr_schedule=step, normalize=zscore (max I 1.45)
- 2 separate islands (no single-knob move joins them): batch_size=1, normalize=minmax; batch_size=1, normalize=zscore; batch_size=3200, normalize=zscore | batch_size=1, lr_schedule=cosine

Notes:
- configurations the target claim can't tell apart from the answer: lr_schedule=cosine, positive_rate=0.1; batch_size=1, normalize=minmax

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax`, `batch_size=1` | 3 | +2.7% | +2.8% | 2.7% |
| `normalize=zscore`, `batch_size=1` | 3 | +3.2% | +4.8% | 4.0% |
| `normalize=zscore`, `batch_size=3200` | 3 | +4.8% | +6.4% | 5.6% |
| `normalize=zscore` | 4 | +5.6% | +7.5% | 6.6% |
| `normalize=zscore`, `batch_size=320` | 3 | +5.9% | +7.5% | 6.7% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `aggregation_method`, `num_runs`, `shuffling_seed_method`, `SCALES`, `WEIGHTS`, `weight_init_scale`, `bias_init`, `logit_intercept_formula`, `label_noise_mechanism`, `sigmoid_clip_range`, `random_module`, `hardware_cpu`, `os_python_version`, `batch_gradient_aggregation`, `class_weight_balanced_formula`, `floating_point_precision`

## Provenance
- GapFinder commit: `e0f13d101585ad1609a15fbf67b70128f4cfffc8` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
