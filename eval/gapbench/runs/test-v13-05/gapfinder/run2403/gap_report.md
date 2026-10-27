# Gap Report: test-v13-05

Artifact `mlbench` · generated 2026-10-16 01:36 · 176 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -31.0% | -0.5% | ±2.1% | `normalize=minmax`, `epochs=150` |

## C1: test_accuracy (paper 0.7792)
**Fits but unsupported** · gap -31.0% → -0.5% · 73 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0086`, `B0119`, `B0156` (3 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `epochs` naive `15`, changed to `150`
- Command:

  Replay: fork checkpoint `3c0b3daf-79ab-4a38-bcc6-59e1a2adb9d8` and run
  ```
  RUN_TAG=ddb6ff8a4129 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 150 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7792, 0.775, 0.775; gap after -0.5%; result checkpoint `4f3ea05e-4b33-412a-942b-e774c907f821`
- Effect: candidate 0.775 minus naive 0.5375 = +0.2375, 95% bootstrap interval [+0.2292, +0.2789] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.779 test accuracy and 0.750 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7792 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5458, 0.5333, 0.5458, 0.5375, 0.4875
- Spread: range 0.4875 to 0.5458, noise band ±0.0166 (2 x MAD), CV 4.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -31.0% (noise band ±2.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -30.0% (it comes back)
- PASS · Counterfactual (reversal test): without `epochs` the gap is -23.5% (it comes back)
- PASS · Held-out claim: C2: -28.2% to -1.3% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- FAIL · Evidence: `epochs=150`: no evidence mentions '150'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2375 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (11.55 noise units, gap +6.4%); `lr_schedule=cosine` (4.77 noise units, gap -20.9%); `label_noise=0.905` (1.51 noise units, gap -27.8%); `label_noise=0.01` (1.25 noise units, gap -28.3%)
- Near alternatives (closest across all claims):
  - `label_noise=0.905`, `normalize=zscore`: this claim +0.5%, mean |gap| 1.2% (3 runs)
  - `class_weight=balanced`, `normalize=minmax`: this claim -2.7%, mean |gap| 3.0% (3 runs)
  - `class_weight=balanced`, `normalize=zscore`: this claim +1.1%, mean |gap| 3.1% (3 runs)

### Equally good configurations
The target claim can't tell these 4 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `epochs=150, normalize=minmax` (reported)
- `label_noise=0.905, normalize=zscore`
- `class_weight=balanced, normalize=zscore`
- `class_weight=balanced, normalize=minmax`

### History matching (every measured configuration, all claims together)
- 27 of 73 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `epochs, normalize`: epochs=150, normalize=minmax (max I 0.22); epochs=150, normalize=zscore (max I 1.25); epochs=2, normalize=zscore (max I 1.26); epochs=1, normalize=zscore (max I 1.26); +1 more
  - `label_noise, normalize`: label_noise=0.905, normalize=zscore (max I 0.35); label_noise=0.1, normalize=zscore (max I 1); label_noise=0.981, normalize=zscore (max I 1.23)
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 0.65); class_weight=balanced, normalize=zscore (max I 0.88)
- 2 separate islands (no single-knob move joins them): epochs=150, normalize=minmax; label_noise=0.905, normalize=zscore; class_weight=balanced, normalize=minmax | epochs=150, lr_schedule=cosine; epochs=150, lr_schedule=step

Notes:
- configurations the target claim can't tell apart from the answer: epochs=150, normalize=minmax; label_noise=0.905, normalize=zscore; class_weight=balanced, normalize=zscore; class_weight=balanced, normalize=minmax

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `epochs=150`, `normalize=minmax` | 3 | -0.5% | -1.3% | 0.9% |
| `label_noise=0.905`, `normalize=zscore` | 3 | +0.5% | +1.8% | 1.2% |
| `class_weight=balanced`, `normalize=minmax` | 3 | -2.7% | +3.4% | 3.0% |
| `class_weight=balanced`, `normalize=zscore` | 3 | +1.1% | +5.1% | 3.1% |
| `normalize=zscore`, `label_noise=0.1` | 3 | +4.3% | +5.7% | 5.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `out`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
