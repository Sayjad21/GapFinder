# Gap Report: test-v11-03

Artifact `mlbench` · generated 2026-10-16 01:22 · 190 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -38.3% | +5.6% | ±4.2% | `normalize=zscore` |

## C1: test_accuracy (paper 0.7833)
**Fits but unsupported** · gap -38.3% → +5.6% · 51 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0021`, `B0061`, `B0062`, `B0087`, `B0088`, `B0089` (6 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Command:

  Replay: fork checkpoint `94aa3199-2995-40fc-8840-123879030f99` and run
  ```
  RUN_TAG=d720d1bd8e07 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.825, 0.825, 0.8292, 0.8292, 0.825, 0.8292; gap after +5.6%; result checkpoint `9750680b-7e29-4060-93c9-21fc57977c35`
- Effect: candidate 0.8271 minus naive 0.4833 = +0.3438, 95% bootstrap interval [+0.2484, +0.3567] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.783 test accuracy and 0.752 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7833 (headline claim)

### What did we measure?
- Naive median 0.4833 over 5 runs; repeats: 0.4667, 0.4833, 0.5875, 0.5458, 0.4833
- Spread: range 0.4667 to 0.5875, noise band ±0.0332 (2 x MAD), CV 10.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -38.3% (noise band ±4.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -38.3% (it comes back)
- PASS · Held-out claim: C2: -36.3% to +7.5% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.3438 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `aggregation_method`, `num_runs`, `shuffling_seed_method`, `SCALES`, `WEIGHTS`, `weight_init_scale`, `bias_init`, `logit_intercept_formula`, `label_noise_mechanism`, `sigmoid_clip_range`, `random_module`, `hardware_cpu`, `os_python_version`, `batch_gradient_aggregation`, `class_weight_balanced_formula`, `floating_point_precision`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (4.14 noise units, gap -20.7%); `normalize=minmax` (3.39 noise units, gap -23.9%); `label_noise=0.1` (2.26 noise units, gap -28.7%); `positive_rate=0.7` (2.14 noise units, gap -29.2%); `label_noise=0.981` (2.14 noise units, gap -29.2%) (and 16 more in the JSON)
- Near alternatives (closest across all claims):
  - `normalize=zscore`, `label_noise=0.1`: this claim +3.7%, mean |gap| 4.5% (5 runs)
  - `normalize=zscore`, `label_noise=0.981`: this claim +4.8%, mean |gap| 5.7% (5 runs)
  - `normalize=zscore`, `batch_size=3`: this claim +5.9%, mean |gap| 6.8% (5 runs)

### Equally good configurations
The target claim can't tell these 4 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `normalize=zscore` (reported)
- `batch_size=3, lr_schedule=cosine`
- `label_noise=0.1, normalize=zscore`
- `normalize=zscore, positive_rate=0.1`

### History matching (every measured configuration, all claims together)
- 14 of 50 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `label_noise, normalize`: label_noise=0.1, normalize=zscore (max I 0.77); label_noise=0.981, normalize=zscore (max I 1.02)
  - `batch_size, normalize`: batch_size=3, normalize=zscore (max I 1.08); batch_size=128, normalize=zscore (max I 1.14)
  - `normalize`: normalize=zscore (max I 1.15)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.17); lr_schedule=step, normalize=zscore (max I 1.17)
  - `normalize, positive_rate`: normalize=zscore, positive_rate=0.7 (max I 1.21)
  - `batch_size, lr_schedule`: batch_size=3, lr_schedule=cosine (max I 1.67)
  - `lr_schedule, positive_rate`: lr_schedule=cosine, positive_rate=0.7 (max I 2.35)

Notes:
- label_noise dropped: with repeats, {'normalize': 'zscore', 'label_noise': '0.1'} fits {'normalize': 'zscore'}'s gap by less than one noise band, so it is not needed
- configurations the target claim can't tell apart from the answer: normalize=zscore; batch_size=3, lr_schedule=cosine; label_noise=0.1, normalize=zscore; normalize=zscore, positive_rate=0.1

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore`, `label_noise=0.1` | 5 | +3.7% | +5.2% | 4.5% |
| `normalize=zscore`, `label_noise=0.981` | 5 | +4.8% | +6.7% | 5.7% |
| `normalize=zscore` | 6 | +5.6% | +7.5% | 6.6% |
| `normalize=zscore`, `batch_size=3` | 5 | +5.9% | +7.7% | 6.8% |
| `normalize=zscore`, `lr_schedule=cosine` | 5 | +5.9% | +7.8% | 6.8% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `aggregation_method`, `num_runs`, `shuffling_seed_method`, `SCALES`, `WEIGHTS`, `weight_init_scale`, `bias_init`, `logit_intercept_formula`, `label_noise_mechanism`, `sigmoid_clip_range`, `random_module`, `hardware_cpu`, `os_python_version`, `batch_gradient_aggregation`, `class_weight_balanced_formula`, `floating_point_precision`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
