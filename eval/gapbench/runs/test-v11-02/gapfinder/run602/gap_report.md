# Gap Report: test-v11-02

Artifact `mlbench` · generated 2026-10-14 22:30 · 80 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -30.0% | -10.6% | ±0.7% | `normalize=minmax` |

## C1: test_accuracy (paper 0.6666)
**Fits but unsupported** · gap -30.0% → -10.6% · 14 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0010`, `B0031`, `B0032`, `B0033`, `B0034`, `B0035` (6 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Command:

  Replay: fork checkpoint `747f795c-f91b-4221-becd-912062963346` and run
  ```
  RUN_TAG=0f2f13fa53d5 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.5958, 0.5958, 0.5958, 0.5958, 0.5958, 0.5958; gap after -10.6%; result checkpoint `60490965-90a4-4743-860b-6b488c2eab36`
- Effect: candidate 0.5958 minus naive 0.4667 = +0.1291, 95% bootstrap interval [+0.0691, +0.1291] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.667 test accuracy and 0.485 balanced accuracy on a synthetic screening task.

- p. 1, Table 1; value used: `test_accuracy` = 0.6666 (headline claim)

### What did we measure?
- Naive median 0.4667 over 5 runs; repeats: 0.4833, 0.5417, 0.4667, 0.4667, 0.4667
- Spread: range 0.4667 to 0.5417, noise band ±0.004667 (2 x MAD), CV 6.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -30.0% (noise band ±0.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -30.0% (it comes back)
- PASS · Held-out claim: C2: -4.8% to +3.1% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.1291 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (31.24 noise units, gap -8.1%); `class_weight=balanced` (23.21 noise units, gap -13.7%); `lr_schedule=step` (21.43 noise units, gap -15.0%); `normalize=zscore` (7.99 noise units, gap +24.4%)
- Near alternatives (closest across all claims):
  - `lr_schedule=cosine`, `normalize=minmax`: this claim -10.6%, mean |gap| 6.9% (5 runs)
  - `lr_schedule=step`, `normalize=minmax`: this claim -10.6%, mean |gap| 6.9% (5 runs)
  - `lr_schedule=step`: this claim -22.5%, mean |gap| 14.5% (6 runs)

### History matching (every measured configuration, all claims together)
- 4 of 14 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 4 configurations
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=minmax (max I 1.79); lr_schedule=step, normalize=minmax (max I 1.79)
  - `normalize`: normalize=minmax (max I 1.82)
  - `class_weight, lr_schedule`: class_weight=balanced, lr_schedule=step (max I 3)
- 2 separate islands (no single-knob move joins them): lr_schedule=cosine, normalize=minmax; lr_schedule=step, normalize=minmax; normalize=minmax | class_weight=balanced, lr_schedule=step

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax` | 6 | -10.6% | +3.1% | 6.9% |
| `lr_schedule=cosine`, `normalize=minmax` | 5 | -10.6% | +3.1% | 6.9% |
| `lr_schedule=step`, `normalize=minmax` | 5 | -10.6% | +3.1% | 6.9% |
| `lr_schedule=step` | 6 | -22.5% | +6.5% | 14.5% |
| `class_weight=balanced` | 6 | -17.8% | +13.3% | 15.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `e0f13d101585ad1609a15fbf67b70128f4cfffc8` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
