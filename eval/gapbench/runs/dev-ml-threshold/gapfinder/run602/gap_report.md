# Gap Report: dev-ml-threshold

Artifact `mlbench` · generated 2026-10-14 22:24 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -34.6% | +0.0% | ±5.5% | `normalize=zscore`, `threshold=0.3` |

## C1: test_accuracy (paper 0.7583)
**Fits but unsupported** · gap -34.6% → +0.0% · 53 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0093`, `B0137`, `B0138`, `B0139`, `B0140` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Config: `threshold` naive `0.5`, changed to `0.3`
- Command:

  Replay: fork checkpoint `e8d8d154-9581-4013-ac89-2d5767be62ed` and run
  ```
  RUN_TAG=ed519f5226ce "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.3 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7583, 0.7583, 0.7583, 0.7583, 0.7583; gap after +0.0%; result checkpoint `9733385d-57b7-4194-9bba-a4b96ec34a71`
- Effect: candidate 0.7583 minus naive 0.4958 = +0.2625, 95% bootstrap interval [+0.2116, +0.28] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> On imbalanced screening data, accuracy depends as much on the decision rule as on the model.

- p. 1; value used: `test_accuracy` = 0.7583 (headline claim)

### What did we measure?
- Naive median 0.4958 over 5 runs; repeats: 0.475, 0.4833, 0.55, 0.5417, 0.4958
- Spread: range 0.475 to 0.55, noise band ±0.0416 (2 x MAD), CV 6.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -34.6% (noise band ±5.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -29.1% (it comes back)
- PASS · Counterfactual (reversal test): without `threshold` the gap is +9.3% (it comes back)
- PASS · Held-out claim: C2: -37.4% to +0.0% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- FAIL · Evidence: `threshold=0.3`: no evidence mentions '0.3'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2625 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (3 noise units, gap -18.1%); `lr_schedule=step` (2.7 noise units, gap -19.8%); `normalize=minmax` (2.4 noise units, gap -21.4%); `threshold=0.05` (1.3 noise units, gap -27.5%); `class_weight=balanced` (1.2 noise units, gap -28.0%) (and 3 more in the JSON)
- Near alternatives (closest across all claims):
  - `normalize=zscore`, `class_weight=balanced`: this claim +3.3%, mean |gap| 1.7% (5 runs)
  - `normalize=zscore`, `threshold=0.25`: this claim -5.5%, mean |gap| 4.8% (5 runs)
  - `normalize=zscore`: this claim +9.3%, mean |gap| 6.4% (6 runs)

### History matching (every measured configuration, all claims together)
- 7 of 52 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 7 configurations
  - `normalize, threshold`: normalize=zscore, threshold=0.3 (max I 0); normalize=zscore, threshold=0.25 (max I 0.94)
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 0.23); class_weight=balanced, normalize=zscore (max I 0.61)
  - `normalize`: normalize=zscore (max I 1.6)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.61); lr_schedule=step, normalize=zscore (max I 1.61)

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'normalize': 'minmax', 'class_weight': 'balanced'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore`, `threshold=0.3` | 5 | +0.0% | +0.0% | 0.0% |
| `normalize=zscore`, `class_weight=balanced` | 5 | +3.3% | +0.1% | 1.7% |
| `normalize=zscore`, `threshold=0.25` | 5 | -5.5% | -4.0% | 4.8% |
| `normalize=zscore` | 6 | +9.3% | +3.4% | 6.4% |
| `normalize=zscore`, `lr_schedule=cosine` | 5 | +9.3% | +3.4% | 6.4% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `threshold=auto`: invalid_value, The program expects a numeric float for --threshold, but received the string 'auto', which is not a valid float; suggested `0.3`, already measured

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `e0f13d101585ad1609a15fbf67b70128f4cfffc8` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
