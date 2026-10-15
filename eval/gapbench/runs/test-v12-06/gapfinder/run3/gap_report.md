# Gap Report: test-v12-06

Artifact `mlbench` · generated 2026-10-15 08:59 · 198 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -39.5% | +1.1% | ±0.6% | `positive_rate=0.15`, `normalize=zscore` |

## C1: test_accuracy (paper 0.7708)
**Fits but unsupported** · gap -39.5% → +1.1% · 68 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0086`, `B0139`, `B0140`, `B0141`, `B0142` (5 run(s) of the same config)
- Config: `positive_rate` naive `0.3`, changed to `0.15`
- Config: `normalize` naive `none`, changed to `zscore`
- Command:

  Replay: fork checkpoint `477c964f-0a4d-4910-b538-e4182bcb6b0b` and run
  ```
  RUN_TAG=c0b7f8847045 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.15 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7792, 0.7792, 0.7792, 0.7792, 0.7708; gap after +1.1%; result checkpoint `8b28a9bb-3395-4fd4-aaf3-b28d5f403d2c`
- Effect: candidate 0.7792 minus naive 0.4667 = +0.3125, 95% bootstrap interval [+0.2433, +0.3125] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.771 test accuracy and 0.745 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7708 (headline claim)

### What did we measure?
- Naive median 0.4667 over 5 runs; repeats: 0.4667, 0.4667, 0.5125, 0.5375, 0.4667
- Spread: range 0.4667 to 0.5375, noise band ±0.004667 (2 x MAD), CV 6.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -39.5% (noise band ±0.6% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `positive_rate` the gap is +7.0% (it comes back)
- PASS · Counterfactual (reversal test): without `normalize` the gap is -33.5% (it comes back)
- PASS · Held-out claim: C2: -38.1% to -8.7% (not worse beyond noise)
- FAIL · Evidence: `positive_rate=0.15`: no evidence mentions '0.15'; it fits, but nothing says the authors used it
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.3125 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `SCALES[0]`, `SCALES[1]`, `SCALES[2]`, `SCALES[3]`, `SCALES[4]`, `SCALES[5]`, `SCALES[6]`, `SCALES[7]`, `WEIGHTS[0]`, `WEIGHTS[1]`, `WEIGHTS[2]`, `WEIGHTS[3]`, `WEIGHTS[4]`, `WEIGHTS[5]`, `WEIGHTS[6]`, `WEIGHTS[7]`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (33.02 noise units, gap -19.5%); `normalize=minmax` (27.66 noise units, gap -22.7%); `weight_decay=1e-3` (16.95 noise units, gap -29.2%); `positive_rate=0.65` (16.95 noise units, gap -29.2%); `positive_rate=0.5` (13.39 noise units, gap -31.3%) (and 10 more in the JSON)
- Near alternatives (closest across all claims):
  - `normalize=zscore`, `positive_rate=0.5`: this claim +1.6%, mean |gap| 3.4% (5 runs)
  - `normalize=zscore`: this claim +7.0%, mean |gap| 7.7% (6 runs)
  - `positive_rate=0.65`, `normalize=zscore`: this claim +7.0%, mean |gap| 7.9% (5 runs)

### History matching (every measured configuration, all claims together)
- 15 of 65 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `normalize, positive_rate`: normalize=minmax, positive_rate=0.5 (max I 0.31); normalize=zscore, positive_rate=0.86 (max I 0.78); normalize=zscore, positive_rate=0.5 (max I 0.89); normalize=zscore, positive_rate=0.65 (max I 1.45); +1 more
  - `normalize`: normalize=zscore (max I 1.43)
  - `normalize, weight_decay`: normalize=zscore, weight_decay=1e-3 (max I 1.46); normalize=zscore, weight_decay=1e-4 (max I 1.48)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.48); lr_schedule=step, normalize=zscore (max I 1.48)
- 3 separate islands (no single-knob move joins them): normalize=minmax, positive_rate=0.5; normalize=zscore, positive_rate=0.86; normalize=zscore, positive_rate=0.5 | lr_schedule=cosine, positive_rate=0.1; lr_schedule=cosine, positive_rate=0.86; lr_schedule=cosine, positive_rate=0.65 | lr_schedule=cosine, weight_decay=1e-4

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'normalize': 'minmax', 'weight_decay': '1e-3'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore`, `positive_rate=0.5` | 5 | +1.6% | +5.2% | 3.4% |
| `positive_rate=0.15`, `normalize=zscore` | 5 | +1.1% | -8.7% | 4.9% |
| `normalize=zscore` | 6 | +7.0% | +8.3% | 7.7% |
| `positive_rate=0.65`, `normalize=zscore` | 5 | +7.0% | +8.8% | 7.9% |
| `normalize=zscore`, `lr_schedule=cosine` | 5 | +7.6% | +8.8% | 8.2% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: invalid_value, The code computes math.log(positive_rate / (1 - positive_rate)). With positive_rate = 0.0 the argument becomes 0, causing a math domain error because log(0) is undefined. A strictly positive rate is required; retried as `positive_rate=0.001`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `SCALES[0]`, `SCALES[1]`, `SCALES[2]`, `SCALES[3]`, `SCALES[4]`, `SCALES[5]`, `SCALES[6]`, `SCALES[7]`, `WEIGHTS[0]`, `WEIGHTS[1]`, `WEIGHTS[2]`, `WEIGHTS[3]`, `WEIGHTS[4]`, `WEIGHTS[5]`, `WEIGHTS[6]`, `WEIGHTS[7]`

## Provenance
- GapFinder commit: `f01fe3d9a0095f98d6304ad0543b917ca8e529eb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0917, sandbox reported $0.0000 (total $0.0917; this search; ledger extraction is included only if it shared the search's router)
