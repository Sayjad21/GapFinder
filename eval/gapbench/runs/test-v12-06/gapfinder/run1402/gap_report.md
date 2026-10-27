# Gap Report: test-v12-06

Artifact `mlbench` · generated 2026-10-15 19:05 · 199 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -27.0% | +1.6% | ±4.3% | `positive_rate=0.5`, `normalize=zscore` |

## C1: test_accuracy (paper 0.7708)
**Fits but unsupported** · gap -27.0% → +1.6% · 63 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0118`, `B0127`, `B0161`, `B0162`, `B0163` (5 run(s) of the same config)
- Config: `positive_rate` naive `0.3`, changed to `0.5`
- Config: `normalize` naive `none`, changed to `zscore`
- Command:

  Replay: fork checkpoint `977c00ba-0551-4489-9a90-f27e51e7a7fa` and run
  ```
  RUN_TAG=a73f35330665 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.5 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7833, 0.7875, 0.7833, 0.7833, 0.7833; gap after +1.6%; result checkpoint `9b730982-58f3-4457-b1bb-4d52affb2e82`
- Effect: candidate 0.7833 minus naive 0.5625 = +0.2208, 95% bootstrap interval [+0.2083, +0.2966] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.771 test accuracy and 0.745 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7708 (headline claim)

### What did we measure?
- Naive median 0.5625 over 5 runs; repeats: 0.5792, 0.5625, 0.4667, 0.5708, 0.5375
- Spread: range 0.4667 to 0.5792, noise band ±0.0334 (2 x MAD), CV 8.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -27.0% (noise band ±4.3% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `positive_rate` the gap is +7.6% (it comes back)
- PASS · Counterfactual (reversal test): without `normalize` the gap is -36.2% (it comes back)
- PASS · Held-out claim: C2: -24.8% to +5.2% (not worse beyond noise)
- FAIL · Evidence: `positive_rate=0.5`: no evidence mentions '0.5'; it fits, but nothing says the authors used it
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2208 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `SCALES`, `WEIGHTS`, `RUN_TAG`, `num_runs`, `aggregation_method`, `python_version`, `os`, `cpu_arch`, `memory_size`, `storage_type`, `out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (1.87 noise units, gap -18.9%); `normalize=minmax` (1 noise units, gap -22.7%)
- Near alternatives (closest across all claims):
  - `class_weight=balanced`, `normalize=minmax`: this claim +0.5%, mean |gap| 2.7% (5 runs)
  - `class_weight=balanced`, `normalize=zscore`: this claim +2.2%, mean |gap| 4.0% (5 runs)
  - `positive_rate=0.15`, `normalize=zscore`: this claim +1.1%, mean |gap| 4.9% (5 runs)

### History matching (every measured configuration, all claims together)
- 17 of 60 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 0.78); class_weight=balanced, normalize=zscore (max I 0.9)
  - `normalize, positive_rate`: normalize=zscore, positive_rate=0.86 (max I 0.84); normalize=zscore, positive_rate=0.5 (max I 0.84); normalize=zscore, positive_rate=0.65 (max I 1.34); normalize=zscore, positive_rate=0.15 (max I 1.41)
  - `normalize`: normalize=zscore (max I 1.38)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.39); lr_schedule=step, normalize=zscore (max I 1.39)
  - `lr_schedule, positive_rate`: lr_schedule=cosine, positive_rate=0.86 (max I 2.44)
- 3 separate islands (no single-knob move joins them): class_weight=balanced, normalize=minmax; normalize=zscore, positive_rate=0.86; normalize=zscore, positive_rate=0.5 | lr_schedule=cosine, positive_rate=0.86; lr_schedule=cosine, positive_rate=0.93; lr_schedule=cosine, positive_rate=0.65 | class_weight=balanced, lr_schedule=cosine

Notes:
- stopped early: run budget of 200 reached (wanted 3 more run(s) of {'normalize': 'minmax', 'positive_rate': '0.15'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `class_weight=balanced`, `normalize=minmax` | 5 | +0.5% | +4.9% | 2.7% |
| `positive_rate=0.5`, `normalize=zscore` | 5 | +1.6% | +5.2% | 3.4% |
| `class_weight=balanced`, `normalize=zscore` | 5 | +2.2% | +5.9% | 4.0% |
| `positive_rate=0.15`, `normalize=zscore` | 5 | +1.1% | -8.7% | 4.9% |
| `positive_rate=0.86`, `normalize=zscore` | 5 | +5.4% | -4.9% | 5.1% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `SCALES`, `WEIGHTS`, `RUN_TAG`, `num_runs`, `aggregation_method`, `python_version`, `os`, `cpu_arch`, `memory_size`, `storage_type`, `out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
