# Gap Report: test-v11-03

Artifact `mlbench` · generated 2026-10-15 19:21 · 198 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -36.2% | +5.9% | ±8.5% | `normalize=zscore` |

## C1: test_accuracy (paper 0.7833)
**Fits but unsupported** · gap -36.2% → +5.9% · 86 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0036`, `B0063`, `B0064`, `B0071`, `B0072`, `B0073` (6 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Command:

  Replay: fork checkpoint `92e4797b-1520-4fb7-b1d0-23cf7b729fb0` and run
  ```
  RUN_TAG=062ce40986df "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.8292, 0.8292, 0.8292, 0.8292, 0.825, 0.8292; gap after +5.9%; result checkpoint `d771b360-1d53-4f10-9f63-d0cfa6482d4b`
- Effect: candidate 0.8292 minus naive 0.5 = +0.3292, 95% bootstrap interval [+0.2759, +0.3625] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.783 test accuracy and 0.752 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7833 (headline claim)

### What did we measure?
- Naive median 0.5 over 5 runs; repeats: 0.5375, 0.4667, 0.5625, 0.5, 0.4667
- Spread: range 0.4667 to 0.5625, noise band ±0.0666 (2 x MAD), CV 8.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -36.2% (noise band ±8.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -36.2% (it comes back)
- PASS · Held-out claim: C2: -34.0% to +7.8% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.3292 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `aggregation_method`, `num_runs`, `shuffling_seed_method`, `SCALES`, `WEIGHTS`, `weight_init_scale`, `bias_init`, `logit_intercept_formula`, `label_noise_mechanism`, `sigmoid_clip_range`, `random_module`, `hardware_cpu`, `os_python_version`, `batch_gradient_aggregation`, `class_weight_balanced_formula`, `floating_point_precision`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (2.19 noise units, gap -17.6%); `lr_schedule=step` (1.5 noise units, gap -23.4%); `normalize=minmax` (1.44 noise units, gap -23.9%); `positive_rate=0.7` (1.06 noise units, gap -27.1%)
- Near alternatives (closest across all claims):
  - `positive_rate=0.5`, `normalize=zscore`: this claim +0.5%, mean |gap| 2.6% (2 runs)
  - `batch_size=1`, `normalize=zscore`: this claim +2.1%, mean |gap| 3.1% (2 runs)
  - `batch_size=1`, `normalize=minmax`: this claim +4.3%, mean |gap| 4.8% (2 runs)

### History matching (every measured configuration, all claims together)
- 27 of 84 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `batch_size, normalize`: batch_size=1, normalize=zscore (max I 0.56); batch_size=1, normalize=minmax (max I 0.73); batch_size=3200, normalize=zscore (max I 0.85); batch_size=1600, normalize=zscore (max I 0.85); +3 more
  - `normalize, positive_rate`: normalize=zscore, positive_rate=0.5 (max I 0.66); normalize=zscore, positive_rate=0.86 (max I 0.8); normalize=zscore, positive_rate=0.65 (max I 1.05)

Notes:
- stopped early: run budget of 200 reached (wanted 3 more run(s) of {'normalize': 'minmax', 'positive_rate': '0.1'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `positive_rate=0.5`, `normalize=zscore` | 2 | +0.5% | +4.7% | 2.6% |
| `batch_size=1`, `normalize=zscore` | 2 | +2.1% | +4.1% | 3.1% |
| `batch_size=1`, `normalize=minmax` | 2 | +4.3% | +5.3% | 4.8% |
| `normalize=zscore`, `positive_rate=0.86` | 2 | +3.7% | -5.8% | 4.8% |
| `batch_size=1600`, `normalize=zscore` | 2 | +4.0% | +6.1% | 5.1% |

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
