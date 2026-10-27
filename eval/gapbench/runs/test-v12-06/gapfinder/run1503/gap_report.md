# Gap Report: test-v12-06

Artifact `mlbench` · generated 2026-10-15 19:28 · 150 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -30.3% | +2.2% | ±7.6% | `normalize=minmax`, `positive_rate=0.5` |

## C1: test_accuracy (paper 0.7708)
**Fits but unsupported** · gap -30.3% → +2.2% · 65 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0048`, `B0083`, `B0118`, `B0119`, `B0120` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `positive_rate` naive `0.3`, changed to `0.5`
- Command:

  Replay: fork checkpoint `edb14fe0-443b-4cc2-b67d-7d9e4caa98e4` and run
  ```
  RUN_TAG=4c9cc51b0c50 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.5 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7875, 0.7875, 0.7875, 0.775, 0.7958; gap after +2.2%; result checkpoint `c9e8dafd-45d7-45d8-8c7f-9137189a2b70`
- Effect: candidate 0.7875 minus naive 0.5375 = +0.25, 95% bootstrap interval [+0.2308, +0.2967] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.771 test accuracy and 0.745 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7708 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5375, 0.5667, 0.4667, 0.5083, 0.5417
- Spread: range 0.4667 to 0.5667, noise band ±0.0584 (2 x MAD), CV 7.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -30.3% (noise band ±7.6% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -29.2% (it comes back)
- PASS · Counterfactual (reversal test): without `positive_rate` the gap is -22.7% (it comes back)
- PASS · Held-out claim: C2: -27.2% to +5.9% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- FAIL · Evidence: `positive_rate=0.5`: no evidence mentions '0.5'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.25 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `SCALES[0]`, `SCALES[1]`, `SCALES[2]`, `SCALES[3]`, `SCALES[4]`, `SCALES[5]`, `SCALES[6]`, `SCALES[7]`, `WEIGHTS[0]`, `WEIGHTS[1]`, `WEIGHTS[2]`, `WEIGHTS[3]`, `WEIGHTS[4]`, `WEIGHTS[5]`, `WEIGHTS[6]`, `WEIGHTS[7]`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (3.07 noise units, gap +7.0%); `lr_schedule=cosine` (1.36 noise units, gap -20.0%)
- Near alternatives (closest across all claims):
  - `normalize=zscore`, `positive_rate=0.5`: this claim +2.2%, mean |gap| 4.0% (5 runs)
  - `normalize=zscore`, `positive_rate=0.15`: this claim +1.1%, mean |gap| 4.9% (5 runs)
  - `normalize=zscore`, `positive_rate=0.86`: this claim +4.9%, mean |gap| 5.4% (5 runs)

### Equally good configurations
The target claim can't tell these 5 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `normalize=minmax, positive_rate=0.5` (reported)
- `normalize=zscore, positive_rate=0.15`
- `lr_schedule=cosine, positive_rate=0.1`
- `normalize=zscore, positive_rate=0.5`
- `normalize=minmax, positive_rate=0.86`

### History matching (every measured configuration, all claims together)
- 16 of 62 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `normalize, positive_rate`: normalize=zscore, positive_rate=0.5 (max I 0.92); normalize=minmax, positive_rate=0.5 (max I 0.93); normalize=zscore, positive_rate=0.86 (max I 0.94); normalize=zscore, positive_rate=0.65 (max I 1.39); +1 more
  - `normalize, weight_decay`: normalize=zscore, weight_decay=1e-3 (max I 1.35); normalize=zscore, weight_decay=1e-4 (max I 1.37)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.43); lr_schedule=step, normalize=zscore (max I 1.43)
  - `normalize`: normalize=zscore (max I 1.44)
- 2 separate islands (no single-knob move joins them): normalize=zscore, positive_rate=0.5; normalize=minmax, positive_rate=0.5; normalize=zscore, positive_rate=0.86 | lr_schedule=cosine, positive_rate=0.93; lr_schedule=cosine, positive_rate=0.65; lr_schedule=cosine, positive_rate=0.5
- Equally good values: `normalize` in {minmax, zscore}; `positive_rate` in {0.5, 0.86, 0.93}

Notes:
- configurations the target claim can't tell apart from the answer: normalize=minmax, positive_rate=0.5; normalize=zscore, positive_rate=0.15; lr_schedule=cosine, positive_rate=0.1; normalize=zscore, positive_rate=0.5; normalize=minmax, positive_rate=0.86
- equally good values within one noise band (measured): normalize in {minmax, zscore}; positive_rate in {0.5, 0.86, 0.93}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore`, `positive_rate=0.5` | 5 | +2.2% | +5.7% | 4.0% |
| `normalize=minmax`, `positive_rate=0.5` | 5 | +2.2% | +5.9% | 4.0% |
| `normalize=zscore`, `positive_rate=0.15` | 5 | +1.1% | -8.7% | 4.9% |
| `normalize=zscore`, `positive_rate=0.86` | 5 | +4.9% | -6.0% | 5.4% |
| `normalize=zscore`, `positive_rate=0.65` | 5 | +6.5% | +8.4% | 7.4% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `SCALES[0]`, `SCALES[1]`, `SCALES[2]`, `SCALES[3]`, `SCALES[4]`, `SCALES[5]`, `SCALES[6]`, `SCALES[7]`, `WEIGHTS[0]`, `WEIGHTS[1]`, `WEIGHTS[2]`, `WEIGHTS[3]`, `WEIGHTS[4]`, `WEIGHTS[5]`, `WEIGHTS[6]`, `WEIGHTS[7]`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
