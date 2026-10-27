# Gap Report: test-v11-03

Artifact `mlbench` · generated 2026-10-14 21:46 · 197 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -31.9% | +5.3% | ±7.5% | `normalize=zscore` |

## C1: test_accuracy (paper 0.7833)
**Fits but unsupported** · gap -31.9% → +5.3% · 75 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0036`, `B0091`, `B0092`, `B0093`, `B0094`, `B0095` (6 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Command:

  Replay: fork checkpoint `0868bbc1-244f-42ff-8319-128e35466d8f` and run
  ```
  RUN_TAG=0c8e96cd8b25 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.8292, 0.825, 0.825, 0.825, 0.825, 0.825; gap after +5.3%; result checkpoint `c475d8f4-b1e0-4470-977b-00fe9407d581`
- Effect: candidate 0.825 minus naive 0.5333 = +0.2917, 95% bootstrap interval [+0.2658, +0.345] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.783 test accuracy and 0.752 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7833 (headline claim)

### What did we measure?
- Naive median 0.5333 over 5 runs; repeats: 0.5, 0.5458, 0.4667, 0.5333, 0.5625
- Spread: range 0.4667 to 0.5625, noise band ±0.0584 (2 x MAD), CV 7.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -31.9% (noise band ±7.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -31.9% (it comes back)
- PASS · Held-out claim: C2: -28.4% to +7.3% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2917 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `aggregation_method`, `num_runs`, `shuffling_seed_method`, `SCALES`, `WEIGHTS`, `weight_init_scale`, `bias_init`, `logit_intercept_formula`, `label_noise_mechanism`, `sigmoid_clip_range`, `random_module`, `hardware_cpu`, `os_python_version`, `batch_gradient_aggregation`, `class_weight_balanced_formula`, `floating_point_precision`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `batch_size=1` (1.93 noise units, gap -17.6%); `lr_schedule=cosine` (1.78 noise units, gap -18.6%); `normalize=minmax` (1.07 noise units, gap -23.9%)
- Near alternatives (closest across all claims):
  - `normalize=zscore`, `positive_rate=0.5`: this claim +0.5%, mean |gap| 2.6% (5 runs)
  - `normalize=zscore`, `batch_size=1`: this claim +3.2%, mean |gap| 4.3% (5 runs)
  - `normalize=zscore`, `label_noise=0.1`: this claim +3.7%, mean |gap| 4.5% (5 runs)

### History matching (every measured configuration, all claims together)
- 14 of 74 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `normalize, positive_rate`: normalize=minmax, positive_rate=0.5 (max I 0.66); normalize=zscore, positive_rate=0.5 (max I 0.74)
  - `batch_size, normalize`: batch_size=1, normalize=minmax (max I 0.72); batch_size=1, normalize=zscore (max I 0.89); batch_size=64, normalize=zscore (max I 1.26)
  - `label_noise, normalize`: label_noise=0.1, normalize=zscore (max I 0.82)
  - `batch_size, lr_schedule`: batch_size=1, lr_schedule=cosine (max I 1.15)
  - `normalize`: normalize=zscore (max I 1.2)
  - `lr_schedule, normalize`: lr_schedule=step, normalize=zscore (max I 1.24); lr_schedule=cosine, normalize=zscore (max I 1.26)
- 4 separate islands (no single-knob move joins them): normalize=minmax, positive_rate=0.5; batch_size=1, normalize=minmax; normalize=zscore, positive_rate=0.5 | batch_size=1, lr_schedule=cosine; batch_size=1, lr_schedule=step | lr_schedule=cosine, positive_rate=0.5 | label_noise=0.1, lr_schedule=step

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'lr_schedule': 'cosine', 'positive_rate': '0.5'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore`, `positive_rate=0.5` | 5 | +0.5% | +4.7% | 2.6% |
| `normalize=zscore`, `batch_size=1` | 5 | +3.2% | +5.4% | 4.3% |
| `normalize=zscore`, `label_noise=0.1` | 5 | +3.7% | +5.2% | 4.5% |
| `batch_size=1`, `normalize=minmax` | 5 | +3.7% | +5.6% | 4.7% |
| `normalize=zscore` | 6 | +5.3% | +7.3% | 6.3% |

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
