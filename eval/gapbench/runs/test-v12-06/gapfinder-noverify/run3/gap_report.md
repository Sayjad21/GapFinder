# Gap Report: test-v12-06

Artifact `mlbench` · generated 2026-10-15 08:59 · 195 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Explained | -30.3% | +1.1% | ±9.7% | `normalize=minmax`, `positive_rate=0.5` |

## C1: test_accuracy (paper 0.7708)
**Explained** · gap -30.3% → +1.1% · 68 hypotheses tested
> Interacting factors: these changes close the gap only together, and every check passes

### Which experiment changed it?
- Branch: `B0050`, `B0132`, `B0133`, `B0134`, `B0135` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `positive_rate` naive `0.3`, changed to `0.5`
- Command:

  Replay: fork checkpoint `42ef5978-db35-40f2-b263-3a5f381e86e2` and run
  ```
  RUN_TAG=a4cc7f02c846 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.5 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7833, 0.775, 0.7875, 0.7792, 0.775; gap after +1.1%; result checkpoint `d7a731fa-889d-4ce4-9b55-0e7b73c1134e`
- Effect: candidate 0.7792 minus naive 0.5375 = +0.2417, 95% bootstrap interval [+0.2183, +0.3016] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.771 test accuracy and 0.745 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7708 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5375, 0.4667, 0.475, 0.5417, 0.575
- Spread: range 0.4667 to 0.575, noise band ±0.075 (2 x MAD), CV 9.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -30.3% (noise band ±9.7% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is +0.2417 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `SCALES[0]`, `SCALES[1]`, `SCALES[2]`, `SCALES[3]`, `SCALES[4]`, `SCALES[5]`, `SCALES[6]`, `SCALES[7]`, `WEIGHTS[0]`, `WEIGHTS[1]`, `WEIGHTS[2]`, `WEIGHTS[3]`, `WEIGHTS[4]`, `WEIGHTS[5]`, `WEIGHTS[6]`, `WEIGHTS[7]`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (2.33 noise units, gap +7.6%); `lr_schedule=cosine` (1 noise units, gap -20.5%)
- Near alternatives (closest across all claims):
  - `normalize=zscore`, `positive_rate=0.5`: this claim +2.2%, mean |gap| 4.0% (5 runs)
  - `normalize=zscore`, `positive_rate=0.15`: this claim +1.1%, mean |gap| 4.9% (5 runs)
  - `normalize=zscore`, `positive_rate=0.86`: this claim +5.4%, mean |gap| 5.1% (5 runs)

### Equally good configurations
The target claim can't tell these 4 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `normalize=minmax, positive_rate=0.5` (reported)
- `normalize=zscore, positive_rate=0.15`
- `lr_schedule=cosine, positive_rate=0.1`
- `normalize=zscore, positive_rate=0.5`

### History matching (every measured configuration, all claims together)
- 17 of 65 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `normalize, positive_rate`: normalize=minmax, positive_rate=0.5 (max I 0.74); normalize=zscore, positive_rate=0.86 (max I 0.85); normalize=zscore, positive_rate=0.5 (max I 0.86); normalize=zscore, positive_rate=0.15 (max I 1.35); +1 more
  - `normalize, weight_decay`: normalize=zscore, weight_decay=1e-4 (max I 1.33); normalize=zscore, weight_decay=1e-3 (max I 1.33)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.36); lr_schedule=step, normalize=zscore (max I 1.36)
  - `normalize`: normalize=zscore (max I 1.37)
- 4 separate islands (no single-knob move joins them): normalize=minmax, positive_rate=0.5; normalize=zscore, positive_rate=0.86; normalize=zscore, positive_rate=0.5 | lr_schedule=cosine, positive_rate=0.93; lr_schedule=cosine, positive_rate=0.65; lr_schedule=cosine, positive_rate=0.86 | lr_schedule=cosine, weight_decay=1e-3 | positive_rate=0.15, weight_decay=1e-3
- Equally good values: `normalize` in {minmax, zscore}; `positive_rate` in {0.15, 0.5, 0.93}

Notes:
- configurations the target claim can't tell apart from the answer: normalize=minmax, positive_rate=0.5; normalize=zscore, positive_rate=0.15; lr_schedule=cosine, positive_rate=0.1; normalize=zscore, positive_rate=0.5
- equally good values within one noise band (measured): normalize in {minmax, zscore}; positive_rate in {0.15, 0.5, 0.93}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax`, `positive_rate=0.5` | 5 | +1.1% | +4.8% | 2.9% |
| `normalize=zscore`, `positive_rate=0.5` | 5 | +2.2% | +5.8% | 4.0% |
| `normalize=zscore`, `positive_rate=0.15` | 5 | +1.1% | -8.7% | 4.9% |
| `normalize=zscore`, `positive_rate=0.86` | 5 | +5.4% | -4.9% | 5.1% |
| `normalize=zscore`, `positive_rate=0.65` | 5 | +7.0% | +8.8% | 7.9% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: invalid_value, Setting positive_rate to 0.0 causes a math domain error when computing log(p/(1-p)) because log(0) is undefined. A small positive value like 0.001 preserves the intent of having a very low positive rate while keeping the computation valid; retried as `positive_rate=0.001`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `SCALES[0]`, `SCALES[1]`, `SCALES[2]`, `SCALES[3]`, `SCALES[4]`, `SCALES[5]`, `SCALES[6]`, `SCALES[7]`, `WEIGHTS[0]`, `WEIGHTS[1]`, `WEIGHTS[2]`, `WEIGHTS[3]`, `WEIGHTS[4]`, `WEIGHTS[5]`, `WEIGHTS[6]`, `WEIGHTS[7]`

## Provenance
- GapFinder commit: `f01fe3d9a0095f98d6304ad0543b917ca8e529eb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0006, sandbox reported $0.0000 (total $0.0006; this search; ledger extraction is included only if it shared the search's router)
