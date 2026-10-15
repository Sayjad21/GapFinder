# Gap Report: test-v13-01

Artifact `mlbench` · generated 2026-10-15 23:34 · 169 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -29.1% | +0.0% | ±2.2% | `normalize=zscore`, `threshold=0.3` |

## C1: test_accuracy (paper 0.7583)
**Fits but unsupported** · gap -29.1% → +0.0% · 61 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0053`, `B0092`, `B0118`, `B0119`, `B0120` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Config: `threshold` naive `0.5`, changed to `0.3`
- Command:

  Replay: fork checkpoint `caf721cd-3c94-4eaa-8743-8cad1f844144` and run
  ```
  RUN_TAG=3263972a01c5 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.3 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7625, 0.7583, 0.7583, 0.7583, 0.7583; gap after +0.0%; result checkpoint `74ae25ae-73e5-46b3-92a1-4b2595d4754e`
- Effect: candidate 0.7583 minus naive 0.5375 = +0.2208, 95% bootstrap interval [+0.2158, +0.2742] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.758 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7583 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.4833, 0.4875, 0.5458, 0.5375, 0.5375
- Spread: range 0.4833 to 0.5458, noise band ±0.0166 (2 x MAD), CV 5.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -29.1% (noise band ±2.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -29.7% (it comes back)
- PASS · Counterfactual (reversal test): without `threshold` the gap is +9.3% (it comes back)
- PASS · Held-out claim: C2: -27.5% to +4.9% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: evidence gate off: no evidence was looked for
- FAIL · Evidence: `threshold=0.3`: evidence gate off: no evidence was looked for
- PASS · Effect vs noise: candidate minus naive is +0.2208 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (6.28 noise units, gap -15.4%); `normalize=minmax` (3.51 noise units, gap -21.4%); `threshold=0.05` (1.51 noise units, gap -25.8%); `threshold=0.25` (1.51 noise units, gap -25.8%); `threshold=0.9` (1.51 noise units, gap -25.8%)
- Near alternatives (closest across all claims):
  - `normalize=minmax`, `class_weight=balanced`: this claim -0.5%, mean |gap| 2.0% (5 runs)
  - `normalize=zscore`, `threshold=0.25`: this claim -4.9%, mean |gap| 3.0% (5 runs)
  - `normalize=zscore`, `class_weight=balanced`: this claim +3.3%, mean |gap| 4.2% (5 runs)

### Equally good configurations
The target claim can't tell these 2 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `normalize=zscore, threshold=0.3` (reported)
- `class_weight=balanced, normalize=minmax`

### History matching (every measured configuration, all claims together)
- 9 of 61 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 9 configurations
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 0.56); class_weight=balanced, normalize=zscore (max I 0.87)
  - `normalize, threshold`: normalize=zscore, threshold=0.3 (max I 0.85); normalize=zscore, threshold=0.25 (max I 0.92); normalize=zscore, threshold=0.7 (max I 2.32)
  - `normalize`: normalize=zscore (max I 1.64)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.66); lr_schedule=step, normalize=zscore (max I 1.66)
  - `lr_schedule, threshold`: lr_schedule=cosine, threshold=0.75 (max I 2.85)
- 2 separate islands (no single-knob move joins them): class_weight=balanced, normalize=minmax; normalize=zscore, threshold=0.3; class_weight=balanced, normalize=zscore | lr_schedule=cosine, threshold=0.75

Notes:
- evidence gate off: no evidence was checked, so this cannot be labelled Explained
- configurations the target claim can't tell apart from the answer: normalize=zscore, threshold=0.3; class_weight=balanced, normalize=minmax

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax`, `class_weight=balanced` | 5 | -0.5% | +3.5% | 2.0% |
| `normalize=zscore`, `threshold=0.3` | 5 | +0.0% | +4.9% | 2.4% |
| `normalize=zscore`, `threshold=0.25` | 5 | -4.9% | +1.1% | 3.0% |
| `normalize=zscore`, `class_weight=balanced` | 5 | +3.3% | +5.0% | 4.2% |
| `normalize=zscore` | 6 | +9.3% | +8.4% | 8.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `e9c31fd1405f5c8aae4bd880eadcdc8d491fad02` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
