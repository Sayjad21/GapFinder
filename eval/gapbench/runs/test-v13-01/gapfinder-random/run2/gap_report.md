# Gap Report: test-v13-01

Artifact `mlbench` · generated 2026-10-16 00:00 · 127 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -29.7% | +0.0% | ±8.8% | `normalize=zscore`, `threshold=0.3` |

## C1: test_accuracy (paper 0.7583)
**Fits but unsupported** · gap -29.7% → +0.0% · 61 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0071`, `B0077`, `B0092`, `B0093`, `B0094` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Config: `threshold` naive `0.5`, changed to `0.3`
- Command:

  Replay: fork checkpoint `5d91b384-3d43-4ab5-8035-33d7ebc4bb05` and run
  ```
  RUN_TAG=24256b9f431c "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.3 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7583, 0.7583, 0.7583, 0.7583, 0.7583; gap after +0.0%; result checkpoint `b65218da-1cae-4c51-a137-d8d0cc556a16`
- Effect: candidate 0.7583 minus naive 0.5333 = +0.225, 95% bootstrap interval [+0.1983, +0.2783] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.758 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7583 (headline claim)

### What did we measure?
- Naive median 0.5333 over 5 runs; repeats: 0.4833, 0.5333, 0.5583, 0.5667, 0.4667
- Spread: range 0.4667 to 0.5667, noise band ±0.0668 (2 x MAD), CV 8.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -29.7% (noise band ±8.8% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -32.4% (it comes back)
- PASS · Counterfactual (reversal test): without `threshold` the gap is +9.1% (it comes back)
- PASS · Held-out claim: C2: -27.9% to +4.9% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- FAIL · Evidence: `threshold=0.3`: no evidence mentions '0.3'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.225 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `data_gen_stddev`, `label_noise_distribution`, `OS`, `intercept_calculation`, `logit_noise_application`, `out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (1.37 noise units, gap -17.6%)
- Near alternatives (closest across all claims):
  - `class_weight=balanced`, `normalize=minmax`: this claim +0.6%, mean |gap| 2.4% (5 runs)
  - `normalize=zscore`, `threshold=0.25`: this claim -5.5%, mean |gap| 3.1% (5 runs)
  - `class_weight=balanced`, `normalize=zscore`: this claim +3.3%, mean |gap| 4.2% (5 runs)

### Equally good configurations
The target claim can't tell these 2 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `normalize=zscore, threshold=0.3` (reported)
- `class_weight=balanced, normalize=minmax`

### History matching (every measured configuration, all claims together)
- 20 of 61 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 0.58); class_weight=balanced, normalize=zscore (max I 0.8)
  - `normalize, threshold`: normalize=zscore, threshold=0.3 (max I 0.75); normalize=zscore, threshold=0.25 (max I 0.85); normalize=zscore, threshold=0.7 (max I 2.1)
  - `normalize`: normalize=zscore (max I 1.46)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.48); lr_schedule=step, normalize=zscore (max I 1.48)
  - `lr_schedule, threshold`: lr_schedule=cosine, threshold=0.7 (max I 2.37); lr_schedule=cosine, threshold=0.9 (max I 2.44)
- 2 separate islands (no single-knob move joins them): class_weight=balanced, normalize=minmax; normalize=zscore, threshold=0.3; class_weight=balanced, normalize=zscore | class_weight=balanced, threshold=0.1
- Equally good values: `threshold` in {0.25, 0.3, 0.7}

Notes:
- configurations the target claim can't tell apart from the answer: normalize=zscore, threshold=0.3; class_weight=balanced, normalize=minmax
- equally good values within one noise band (measured): threshold in {0.25, 0.3, 0.7}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `class_weight=balanced`, `normalize=minmax` | 5 | +0.6% | +4.3% | 2.4% |
| `threshold=0.3`, `normalize=zscore` | 5 | +0.0% | +4.9% | 2.4% |
| `normalize=zscore`, `threshold=0.25` | 5 | -5.5% | +0.6% | 3.1% |
| `class_weight=balanced`, `normalize=zscore` | 5 | +3.3% | +5.0% | 4.2% |
| `normalize=zscore` | 6 | +9.1% | +8.2% | 8.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `data_gen_stddev`, `label_noise_distribution`, `OS`, `intercept_calculation`, `logit_noise_application`, `out`

## Provenance
- GapFinder commit: `e9c31fd1405f5c8aae4bd880eadcdc8d491fad02` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
