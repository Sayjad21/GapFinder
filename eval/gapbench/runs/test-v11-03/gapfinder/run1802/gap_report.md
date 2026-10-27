# Gap Report: test-v11-03

Artifact `mlbench` · generated 2026-10-15 19:43 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -31.9% | +5.3% | ±5.3% | `normalize=zscore` |

## C1: test_accuracy (paper 0.7833)
**Fits but unsupported** · gap -31.9% → +5.3% · 34 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0035`, `B0096`, `B0097`, `B0102`, `B0103`, `B0104` (6 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Command:

  Replay: fork checkpoint `6772593b-f3f2-4ec4-bea8-6f2b008adc1e` and run
  ```
  RUN_TAG=a3aef0d04d20 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.8292, 0.825, 0.825, 0.825, 0.825, 0.8292; gap after +5.3%; result checkpoint `b4480005-cdab-44df-9680-1657c0ce5124`
- Effect: candidate 0.825 minus naive 0.5333 = +0.2917, 95% bootstrap interval [+0.2741, +0.3533] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.783 test accuracy and 0.752 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7833 (headline claim)

### What did we measure?
- Naive median 0.5333 over 5 runs; repeats: 0.4833, 0.5542, 0.5333, 0.4667, 0.5375
- Spread: range 0.4667 to 0.5542, noise band ±0.0418 (2 x MAD), CV 7.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -31.9% (noise band ±5.3% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -31.9% (it comes back)
- PASS · Held-out claim: C2: -28.4% to +7.3% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2917 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `aggregation_method`, `run_tag_seeds`, `cpu`, `memory`, `os`, `python_version`, `random_module`, `disk`, `network`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (2.09 noise units, gap -20.7%); `label_noise=0.81` (1.7 noise units, gap -22.9%); `label_noise=0.981` (1.7 noise units, gap -22.9%); `normalize=minmax` (1.5 noise units, gap -23.9%)
- Near alternatives (closest across all claims):
  - `lr_schedule=cosine`: this claim -20.7%, mean |gap| 19.3% (3 runs)
  - `normalize=minmax`: this claim -23.9%, mean |gap| 28.7% (3 runs)
  - `positive_rate=0.006`: this claim -36.7%, mean |gap| 28.9% (6 runs)

### History matching (every measured configuration, all claims together)
- 9 of 45 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 9 configurations
  - `normalize, positive_rate`: normalize=zscore, positive_rate=0.5 (max I 0.6); normalize=zscore, positive_rate=0.65 (max I 0.93)
  - `class_weight, normalize`: class_weight=balanced, normalize=zscore (max I 0.62)
  - `label_noise, normalize`: label_noise=0.981, normalize=zscore (max I 0.91); label_noise=0.81, normalize=zscore (max I 1.24)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 0.99); lr_schedule=step, normalize=zscore (max I 0.99)
  - `normalize`: normalize=zscore (max I 1.23)
  - `label_noise, lr_schedule`: label_noise=0.981, lr_schedule=cosine (max I 2.62)
- 2 separate islands (no single-knob move joins them): normalize=zscore, positive_rate=0.5; class_weight=balanced, normalize=zscore; label_noise=0.981, normalize=zscore | label_noise=0.981, lr_schedule=cosine

Notes:
- stopped early: run budget of 200 reached (wanted 1 more run(s) of {'lr_schedule': 'cosine', 'class_weight': 'balanced'} for 'combine')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore` | 6 | +5.3% | +7.3% | 6.3% |
| `lr_schedule=cosine` | 3 | -20.7% | -17.9% | 19.3% |
| `normalize=minmax` | 3 | -23.9% | -33.5% | 28.7% |
| `positive_rate=0.006` | 6 | -36.7% | -21.1% | 28.9% |
| `positive_rate=0.65` | 6 | -30.3% | -27.6% | 29.0% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `aggregation_method`, `run_tag_seeds`, `cpu`, `memory`, `os`, `python_version`, `random_module`, `disk`, `network`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
