# Gap Report: test-v11-03

Artifact `mlbench` · generated 2026-10-15 18:57 · 196 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -30.3% | -0.5% | ±0.7% | `normalize=minmax`, `positive_rate=0.5` |

## C1: test_accuracy (paper 0.7833)
**Fits but unsupported** · gap -30.3% → -0.5% · 86 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0102`, `B0138`, `B0174` (3 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `positive_rate` naive `0.3`, changed to `0.5`
- Command:

  Replay: fork checkpoint `d3787756-6fef-4138-ae64-c6dc034bf445` and run
  ```
  RUN_TAG=5cfb0f140027 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.5 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7792, 0.7875, 0.7792; gap after -0.5%; result checkpoint `7479a4a2-2058-45c4-8077-3c02895b836d`
- Effect: candidate 0.7792 minus naive 0.5458 = +0.2334, 95% bootstrap interval [+0.2334, +0.2828] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.783 test accuracy and 0.752 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7833 (headline claim)

### What did we measure?
- Naive median 0.5458 over 5 runs; repeats: 0.4875, 0.5375, 0.5458, 0.5458, 0.5458
- Spread: range 0.4875 to 0.5458, noise band ±0.005458 (2 x MAD), CV 4.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -30.3% (noise band ±0.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -33.0% (it comes back)
- PASS · Counterfactual (reversal test): without `positive_rate` the gap is -23.9% (it comes back)
- PASS · Held-out claim: C2: -27.2% to +3.7% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- FAIL · Evidence: `positive_rate=0.5`: no evidence mentions '0.5'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2334 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `aggregation_method`, `num_runs`, `shuffling_seed_method`, `SCALES`, `WEIGHTS`, `weight_init_scale`, `bias_init`, `logit_intercept_formula`, `label_noise_mechanism`, `sigmoid_clip_range`, `random_module`, `hardware_cpu`, `os_python_version`, `batch_gradient_aggregation`, `class_weight_balanced_formula`, `floating_point_precision`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (35.1 noise units, gap +5.9%); `lr_schedule=cosine` (12.22 noise units, gap -21.8%); `batch_size=1600` (2.29 noise units, gap -28.7%); `positive_rate=0.7` (2.29 noise units, gap -28.7%); `label_noise=0.0` (1.54 noise units, gap -29.2%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `batch_size=3200`, `normalize=zscore`: this claim +1.6%, mean |gap| 2.5% (3 runs)
  - `positive_rate=0.5`, `normalize=zscore`: this claim +0.5%, mean |gap| 2.6% (3 runs)
  - `batch_size=1`, `normalize=zscore`: this claim +2.1%, mean |gap| 3.0% (3 runs)

### Equally good configurations
The target claim can't tell these 5 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `normalize=minmax, positive_rate=0.5` (reported)
- `normalize=zscore, positive_rate=0.5`
- `normalize=zscore, positive_rate=0.15`
- `batch_size=1, normalize=zscore`
- `batch_size=3200, normalize=zscore`

### History matching (every measured configuration, all claims together)
- 20 of 84 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `batch_size, normalize`: batch_size=1, normalize=zscore (max I 0.28); batch_size=3200, normalize=zscore (max I 0.77); batch_size=1600, normalize=zscore (max I 0.96); batch_size=3, normalize=zscore (max I 1.2); +3 more
  - `normalize, positive_rate`: normalize=minmax, positive_rate=0.5 (max I 0.71); normalize=zscore, positive_rate=0.5 (max I 0.79); normalize=zscore, positive_rate=0.86 (max I 1.01)
- 2 separate islands (no single-knob move joins them): batch_size=1, normalize=zscore; normalize=minmax, positive_rate=0.5; batch_size=3200, normalize=zscore | lr_schedule=cosine, positive_rate=0.7
- Equally good values: `normalize` in {minmax, zscore}

Notes:
- configurations the target claim can't tell apart from the answer: normalize=minmax, positive_rate=0.5; normalize=zscore, positive_rate=0.5; normalize=zscore, positive_rate=0.15; batch_size=1, normalize=zscore; batch_size=3200, normalize=zscore
- equally good values within one noise band (measured): normalize in {minmax, zscore}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `positive_rate=0.5`, `normalize=minmax` | 3 | -0.5% | +3.7% | 2.1% |
| `batch_size=3200`, `normalize=zscore` | 3 | +1.6% | +3.4% | 2.5% |
| `positive_rate=0.5`, `normalize=zscore` | 3 | +0.5% | +4.7% | 2.6% |
| `batch_size=1`, `normalize=zscore` | 3 | +2.1% | +3.9% | 3.0% |
| `batch_size=1600`, `normalize=zscore` | 3 | +3.2% | +5.7% | 4.4% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `aggregation_method`, `num_runs`, `shuffling_seed_method`, `SCALES`, `WEIGHTS`, `weight_init_scale`, `bias_init`, `logit_intercept_formula`, `label_noise_mechanism`, `sigmoid_clip_range`, `random_module`, `hardware_cpu`, `os_python_version`, `batch_gradient_aggregation`, `class_weight_balanced_formula`, `floating_point_precision`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
