# Gap Report: test-v13-01

Artifact `mlbench` · generated 2026-10-15 23:59 · 150 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Partially explained | -29.1% | +1.6% | ±11.0% | `normalize=minmax`, `class_weight=balanced` |

## C1: test_accuracy (paper 0.7583)
**Partially explained** · gap -29.1% → +1.6% · 57 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0102`, `B0121`, `B0133`, `B0134`, `B0135` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `class_weight` naive `none`, changed to `balanced`
- Command:

  Replay: fork checkpoint `a0c92b9d-2d11-4cbf-84fc-e55a38a89fbd` and run
  ```
  RUN_TAG=d49164073bce "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight balanced --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7708, 0.7708, 0.7375, 0.7667, 0.7833; gap after +1.6%; result checkpoint `032e9185-c3c7-46ac-abc1-e69357d1f3ce`
- Effect: candidate 0.7708 minus naive 0.5375 = +0.2333, 95% bootstrap interval [+0.185, +0.29] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.758 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7583 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5375, 0.5792, 0.5625, 0.475, 0.4833
- Spread: range 0.475 to 0.5792, noise band ±0.0834 (2 x MAD), CV 8.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -29.1% (noise band ±11.0% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is +0.2333 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `data_gen_stddev`, `label_noise_distribution`, `OS`, `intercept_calculation`, `logit_noise_application`, `out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (1.8 noise units, gap +9.3%); `lr_schedule=cosine` (1.1 noise units, gap -17.0%)
- Near alternatives (closest across all claims):
  - `normalize=zscore`, `threshold=0.3`: this claim +0.0%, mean |gap| 2.4% (5 runs)
  - `normalize=zscore`, `threshold=0.25`: this claim -5.5%, mean |gap| 3.1% (5 runs)
  - `normalize=zscore`, `class_weight=balanced`: this claim +3.3%, mean |gap| 4.2% (5 runs)

### Equally good configurations
The target claim can't tell these 2 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `class_weight=balanced, normalize=minmax` (reported)
- `normalize=zscore, threshold=0.3`

### History matching (every measured configuration, all claims together)
- 18 of 57 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 0.66); class_weight=balanced, normalize=zscore (max I 0.78)
  - `normalize, threshold`: normalize=zscore, threshold=0.3 (max I 0.75); normalize=zscore, threshold=0.25 (max I 0.84); normalize=zscore, threshold=0.7 (max I 2.1)
  - `normalize`: normalize=zscore (max I 1.45)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.46); lr_schedule=step, normalize=zscore (max I 1.46)
  - `class_weight, lr_schedule`: class_weight=balanced, lr_schedule=cosine (max I 2.21)
  - `lr_schedule, threshold`: lr_schedule=cosine, threshold=0.7 (max I 2.24)
- Equally good values: `normalize` in {minmax, zscore}

Notes:
- configurations the target claim can't tell apart from the answer: class_weight=balanced, normalize=minmax; normalize=zscore, threshold=0.3
- equally good values within one noise band (measured): normalize in {minmax, zscore}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore`, `threshold=0.3` | 5 | +0.0% | +4.9% | 2.4% |
| `normalize=zscore`, `threshold=0.25` | 5 | -5.5% | +0.6% | 3.1% |
| `normalize=minmax`, `class_weight=balanced` | 5 | +1.6% | +4.5% | 3.1% |
| `normalize=zscore`, `class_weight=balanced` | 5 | +3.3% | +5.0% | 4.2% |
| `normalize=zscore` | 6 | +9.3% | +8.4% | 8.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `data_gen_stddev`, `label_noise_distribution`, `OS`, `intercept_calculation`, `logit_noise_application`, `out`

## Provenance
- GapFinder commit: `e9c31fd1405f5c8aae4bd880eadcdc8d491fad02` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
