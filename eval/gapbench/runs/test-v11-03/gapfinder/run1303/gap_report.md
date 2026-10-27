# Gap Report: test-v11-03

Artifact `mlbench` · generated 2026-10-15 01:13 · 199 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Unexplained | -31.4% | -31.4% | ±1.1% | — |

## C1: test_accuracy (paper 0.7833)
**Unexplained** · gap -31.4% → -31.4% · 99 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (99 hypotheses tested).

### What did the paper report?
> A plain logistic-regression baseline reaches 0.783 test accuracy and 0.752 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7833 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5375, 0.5625, 0.5417, 0.4667, 0.5375
- Spread: range 0.4667 to 0.5625, noise band ±0.0084 (2 x MAD), CV 6.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -31.4% (noise band ±1.1% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `aggregation_method`, `num_runs`, `shuffling_seed_method`, `SCALES`, `WEIGHTS`, `weight_init_scale`, `bias_init`, `logit_intercept_formula`, `label_noise_mechanism`, `sigmoid_clip_range`, `random_module`, `hardware_cpu`, `os_python_version`, `batch_gradient_aggregation`, `class_weight_balanced_formula`, `floating_point_precision`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (23.8 noise units, gap +5.9%); `lr_schedule=cosine` (11.4 noise units, gap -19.1%); `normalize=minmax` (6.94 noise units, gap -23.9%); `label_noise=0.001` (5.95 noise units, gap -25.0%); `class_weight=balanced` (5.45 noise units, gap -25.5%) (and 2 more in the JSON)
- Near alternatives (closest across all claims):
  - `normalize=zscore`, `class_weight=balanced`: this claim +0.5%, mean |gap| 2.7% (5 runs)
  - `normalize=zscore`, `label_noise=0.981`: this claim +4.8%, mean |gap| 5.6% (5 runs)
  - `batch_size=6`, `normalize=zscore`: this claim +5.3%, mean |gap| 6.2% (5 runs)

### History matching (every measured configuration, all claims together)
- 36 of 97 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `label_noise, normalize`: label_noise=0.905, normalize=zscore (max I 0.2); label_noise=0.1, normalize=zscore (max I 0.78)
  - `batch_size, normalize`: batch_size=3200, normalize=zscore (max I 0.47); batch_size=1600, normalize=zscore (max I 0.53); batch_size=1, normalize=zscore (max I 0.81); batch_size=320, normalize=zscore (max I 0.87)
  - `normalize, positive_rate`: normalize=zscore, positive_rate=0.5 (max I 0.55); normalize=minmax, positive_rate=0.5 (max I 0.55)
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 0.67); class_weight=balanced, normalize=zscore (max I 0.78)
- 4 separate islands (no single-knob move joins them): label_noise=0.905, normalize=zscore; batch_size=3200, normalize=zscore; batch_size=1600, normalize=zscore | batch_size=6, lr_schedule=cosine; batch_size=6, lr_schedule=step | lr_schedule=cosine, positive_rate=0.93 | label_noise=0.001, lr_schedule=cosine

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'normalize': 'zscore', 'batch_size': '64'} for 'confirm-combo')
- closest configuration not verified: {'label_noise': '0.905', 'normalize': 'zscore'} (gap +0.0%, 1 of 5 confirmation runs); the budget ran out first, so no attribution is made
- history matching: 36 of 97 tested configurations fit every claim within 3 sigma

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore`, `class_weight=balanced` | 5 | +0.5% | +4.9% | 2.7% |
| `normalize=zscore`, `label_noise=0.981` | 5 | +4.8% | +6.4% | 5.6% |
| `batch_size=6`, `normalize=zscore` | 5 | +5.3% | +7.1% | 6.2% |
| `normalize=zscore` | 6 | +5.6% | +7.5% | 6.6% |
| `label_noise=0.001`, `normalize=zscore` | 5 | +5.9% | +7.7% | 6.8% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `aggregation_method`, `num_runs`, `shuffling_seed_method`, `SCALES`, `WEIGHTS`, `weight_init_scale`, `bias_init`, `logit_intercept_formula`, `label_noise_mechanism`, `sigmoid_clip_range`, `random_module`, `hardware_cpu`, `os_python_version`, `batch_gradient_aggregation`, `class_weight_balanced_formula`, `floating_point_precision`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
