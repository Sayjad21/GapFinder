# Gap Report: test-v13-01

Artifact `mlbench` · generated 2026-10-16 00:00 · 198 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -37.9% | +0.0% | ±1.1% | `normalize=zscore`, `threshold=0.3` |

## C1: test_accuracy (paper 0.7583)
**Fits but unsupported** · gap -37.9% → +0.0% · 57 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0125`, `B0129`, `B0163`, `B0164`, `B0165` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Config: `threshold` naive `0.5`, changed to `0.3`
- Command:

  Replay: fork checkpoint `10cae920-728d-41b7-bade-d493ec654358` and run
  ```
  RUN_TAG=ee5c184c58d4 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.3 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7583, 0.7583, 0.7583, 0.7583, 0.7542; gap after +0.0%; result checkpoint `af6275f4-fbdb-4dfe-8603-e050680304a1`
- Effect: candidate 0.7583 minus naive 0.4708 = +0.2875, 95% bootstrap interval [+0.2317, +0.2916] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.758 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7583 (headline claim)

### What did we measure?
- Naive median 0.4708 over 5 runs; repeats: 0.4667, 0.4667, 0.475, 0.4708, 0.5375
- Spread: range 0.4667 to 0.5375, noise band ±0.0082 (2 x MAD), CV 6.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -37.9% (noise band ±1.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -29.1% (it comes back)
- PASS · Counterfactual (reversal test): without `threshold` the gap is +9.3% (it comes back)
- PASS · Held-out claim: C2: -37.8% to +4.9% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: evidence gate off: no evidence was looked for
- FAIL · Evidence: `threshold=0.3`: evidence gate off: no evidence was looked for
- PASS · Effect vs noise: candidate minus naive is +0.2875 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `data_gen_stddev`, `label_noise_distribution`, `OS`, `intercept_calculation`, `logit_noise_application`, `out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (18.29 noise units, gap -18.1%); `normalize=minmax` (15.24 noise units, gap -21.4%); `lr_schedule=step` (12.71 noise units, gap -24.2%); `threshold=0.9` (11.7 noise units, gap -25.3%); `threshold=0.01` (10.67 noise units, gap -26.4%) (and 7 more in the JSON)
- Near alternatives (closest across all claims):
  - `normalize=minmax`, `class_weight=balanced`: this claim -2.2%, mean |gap| 2.7% (5 runs)
  - `threshold=0.25`, `normalize=zscore`: this claim -5.5%, mean |gap| 3.1% (5 runs)
  - `normalize=zscore`, `class_weight=balanced`: this claim +3.3%, mean |gap| 4.2% (5 runs)

### History matching (every measured configuration, all claims together)
- 8 of 57 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 8 configurations
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 0.64); class_weight=balanced, normalize=zscore (max I 0.87)
  - `normalize, threshold`: normalize=zscore, threshold=0.3 (max I 0.82); normalize=zscore, threshold=0.25 (max I 0.93); normalize=zscore, threshold=0.7 (max I 2.32)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.66); lr_schedule=step, normalize=zscore (max I 1.66)
  - `normalize`: normalize=zscore (max I 1.67)

Notes:
- stopped early: run budget of 200 reached (wanted 3 more run(s) of {'lr_schedule': 'cosine', 'threshold': '0.25'} for 'confirm-combo')
- evidence gate off: no evidence was checked, so this cannot be labelled Explained
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore`, `threshold=0.3` | 5 | +0.0% | +4.9% | 2.4% |
| `normalize=minmax`, `class_weight=balanced` | 5 | -2.2% | +3.2% | 2.7% |
| `threshold=0.25`, `normalize=zscore` | 5 | -5.5% | +0.6% | 3.1% |
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
