# Gap Report: dev-ml-threshold

Artifact `mlbench` · generated 2026-10-16 01:41 · 193 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -36.3% | +0.0% | ±2.2% | `normalize=minmax`, `threshold=0.4` |

## C1: test_accuracy (paper 0.7583)
**Fits but unsupported** · gap -36.3% → +0.0% · 61 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0106`, `B0128`, `B0153`, `B0154`, `B0155` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `threshold` naive `0.5`, changed to `0.4`
- Command:

  Replay: fork checkpoint `85200b38-498a-4e0e-a36e-72beaa426f8d` and run
  ```
  RUN_TAG=ab37da6d7240 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.4 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7625, 0.7542, 0.7583, 0.7583, 0.7458; gap after +0.0%; result checkpoint `380a1265-3a47-4fc5-93e0-d59701877988`
- Effect: candidate 0.7583 minus naive 0.4833 = +0.275, 95% bootstrap interval [+0.23, +0.2883] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> On imbalanced screening data, accuracy depends as much on the decision rule as on the model.

- p. 1; value used: `test_accuracy` = 0.7583 (headline claim)

### What did we measure?
- Naive median 0.4833 over 5 runs; repeats: 0.4667, 0.4833, 0.475, 0.5333, 0.4833
- Spread: range 0.4667 to 0.5333, noise band ±0.0166 (2 x MAD), CV 5.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -36.3% (noise band ±2.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -32.1% (it comes back)
- PASS · Counterfactual (reversal test): without `threshold` the gap is -21.4% (it comes back)
- PASS · Held-out claim: C2: -38.9% to -4.7% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- FAIL · Evidence: `threshold=0.4`: no evidence mentions '0.4'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.275 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (12.3 noise units, gap +9.3%); `lr_schedule=cosine` (8.28 noise units, gap -18.1%); `lr_schedule=step` (8.04 noise units, gap -18.7%); `threshold=0.3` (5.27 noise units, gap -24.7%); `threshold=0.1` (4.02 noise units, gap -27.5%) (and 3 more in the JSON)
- Near alternatives (closest across all claims):
  - `normalize=zscore`, `threshold=0.3`: this claim +0.0%, mean |gap| 0.0% (5 runs)
  - `class_weight=balanced`, `normalize=minmax`: this claim +2.2%, mean |gap| 1.2% (5 runs)
  - `normalize=zscore`, `threshold=0.4`: this claim +3.3%, mean |gap| 1.7% (5 runs)

### Equally good configurations
The target claim can't tell these 4 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `normalize=minmax, threshold=0.4` (reported)
- `normalize=zscore, threshold=0.3`
- `class_weight=balanced, normalize=minmax`
- `normalize=zscore, threshold=0.6`

### History matching (every measured configuration, all claims together)
- 10 of 58 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `normalize, threshold`: normalize=zscore, threshold=0.3 (max I 0.04); normalize=zscore, threshold=0.4 (max I 0.6); normalize=minmax, threshold=0.4 (max I 0.8); normalize=zscore, threshold=0.25 (max I 0.92); +1 more
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 0.5); class_weight=balanced, normalize=zscore (max I 0.66)
  - `normalize`: normalize=zscore (max I 1.67)
  - `lr_schedule, normalize`: lr_schedule=step, normalize=zscore (max I 1.69); lr_schedule=cosine, normalize=zscore (max I 1.71)

Notes:
- configurations the target claim can't tell apart from the answer: normalize=minmax, threshold=0.4; normalize=zscore, threshold=0.3; class_weight=balanced, normalize=minmax; normalize=zscore, threshold=0.6

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore`, `threshold=0.3` | 5 | +0.0% | +0.0% | 0.0% |
| `class_weight=balanced`, `normalize=minmax` | 5 | +2.2% | +0.1% | 1.2% |
| `normalize=zscore`, `threshold=0.4` | 5 | +3.3% | -0.1% | 1.7% |
| `normalize=zscore`, `class_weight=balanced` | 5 | +3.9% | +0.6% | 2.2% |
| `normalize=minmax`, `threshold=0.4` | 5 | +0.0% | -4.7% | 2.3% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `threshold=auto`: invalid_value, The program expects a numeric float for --threshold, but received the string 'auto', which is not a valid float; suggested `0.3`, already measured

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
