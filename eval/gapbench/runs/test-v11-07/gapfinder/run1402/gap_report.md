# Gap Report: test-v11-07

Artifact `mlbench` · generated 2026-10-15 18:58 · 32 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -9.8% | -3.2% | ±1.5% | `lr_schedule=step` |

## C1: test_accuracy (paper 0.5361)
**Fits but unsupported** · gap -9.8% → -3.2% · 13 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0007`, `B0016`, `B0017`, `B0018`, `B0019`, `B0020` (6 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `step`
- Command:

  Replay: fork checkpoint `cdc885e1-720d-47b3-af8b-7e650ca2ad66` and run
  ```
  RUN_TAG=e45198661f15 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize none --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule step --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.4958, 0.5417, 0.5958, 0.5667, 0.4875, 0.4958; gap after -3.2%; result checkpoint `a9f43190-2c81-4b90-8d5a-7b061a1ea2c3`
- Effect: candidate 0.5188 minus naive 0.4833 = +0.03545, 95% bootstrap interval [-0.02334, +0.08166] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.536 test accuracy and 0.543 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.5361 (headline claim)

### What did we measure?
- Naive median 0.4833 over 5 runs; repeats: 0.5625, 0.4792, 0.4833, 0.4833, 0.5333
- Spread: range 0.4792 to 0.5625, noise band ±0.0082 (2 x MAD), CV 7.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -9.8% (noise band ±1.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is -9.8% (it comes back)
- PASS · Held-out claim: C2: -11.8% to -4.3% (not worse beyond noise)
- FAIL · Evidence: `lr_schedule=step`: no evidence mentions 'step'; it fits, but nothing says the authors used it
- FAIL · Effect vs noise: candidate minus naive is +0.03545 with a 95% bootstrap interval that includes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `hardware`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `class_weight=balanced` (6.27 noise units, gap +0.3%)
- Near alternatives (closest across all claims):
  - `class_weight=balanced`: this claim -0.1%, mean |gap| 0.3% (6 runs)
  - `lr_schedule=step`, `class_weight=balanced`: this claim +7.3%, mean |gap| 7.0% (5 runs)

### Equally good configurations
The target claim can't tell these 2 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `lr_schedule=step` (reported)
- `class_weight=balanced, lr_schedule=step`

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 8 configurations
  - `lr_schedule`: lr_schedule=step (max I 0.37); lr_schedule=cosine (max I 1.71)
  - `class_weight`: class_weight=balanced (max I 0.54)
  - `class_weight, lr_schedule`: class_weight=balanced, lr_schedule=step (max I 1.16); class_weight=balanced, lr_schedule=cosine (max I 1.21)
  - `normalize`: normalize=minmax (max I 1.21)
  - `lr_schedule, normalize`: lr_schedule=step, normalize=minmax (max I 1.21); lr_schedule=cosine, normalize=minmax (max I 1.21)

Notes:
- configurations the target claim can't tell apart from the answer: lr_schedule=step; class_weight=balanced, lr_schedule=step

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `class_weight=balanced` | 6 | -0.1% | -0.4% | 0.3% |
| `lr_schedule=step` | 6 | -3.2% | -4.3% | 3.8% |
| `lr_schedule=step`, `class_weight=balanced` | 5 | +7.3% | +6.7% | 7.0% |
| naive (reproduction as run) | 5 | -9.8% | -11.8% | 10.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `hardware`, `--out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
