# Gap Report: test-v13-05

Artifact `mlbench` · generated 2026-10-16 00:12 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -35.8% | +0.0% | ±6.4% | `epochs=150`, `normalize=minmax` |

## C1: test_accuracy (paper 0.7792)
**Fits but unsupported** · gap -35.8% → +0.0% · 99 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0072`, `B0133`, `B0189`, `B0190`, `B0191` (5 run(s) of the same config)
- Config: `epochs` naive `15`, changed to `150`
- Config: `normalize` naive `none`, changed to `minmax`
- Command:

  Replay: fork checkpoint `1b11d44f-4308-4125-b7b5-d8fe656efb7f` and run
  ```
  RUN_TAG=026c79905bda "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 150 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7875, 0.775, 0.7708, 0.7792, 0.7792; gap after +0.0%; result checkpoint `03a96a34-18a9-4ff5-bd94-e5902e3ba48f`
- Effect: candidate 0.7792 minus naive 0.5 = +0.2792, 95% bootstrap interval [+0.2292, +0.305] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.779 test accuracy and 0.750 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7792 (headline claim)

### What did we measure?
- Naive median 0.5 over 5 runs; repeats: 0.5625, 0.525, 0.4667, 0.5, 0.4833
- Spread: range 0.4667 to 0.5625, noise band ±0.05 (2 x MAD), CV 7.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -35.8% (noise band ±6.4% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `epochs` the gap is -23.5% (it comes back)
- PASS · Counterfactual (reversal test): without `normalize` the gap is -30.7% (it comes back)
- PASS · Held-out claim: C2: -33.9% to -0.9% (not worse beyond noise)
- FAIL · Evidence: `epochs=150`: no evidence mentions '150'; it fits, but nothing says the authors used it
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2792 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (4.67 noise units, gap +5.9%); `lr_schedule=cosine` (2 noise units, gap -23.0%); `epochs=750` (1.25 noise units, gap -27.8%); `label_noise=0.905` (1.17 noise units, gap -28.3%); `label_noise=0.981` (1.08 noise units, gap -28.9%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `normalize=zscore`, `label_noise=0.905`: this claim +0.5%, mean |gap| 1.2% (5 runs)
  - `epochs=750`, `lr_schedule=cosine`: this claim +1.6%, mean |gap| 1.4% (5 runs)
  - `normalize=zscore`, `label_noise=0.1`: this claim +4.3%, mean |gap| 5.0% (5 runs)

### History matching (every measured configuration, all claims together)
- 35 of 97 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `epochs, normalize`: epochs=150, normalize=minmax (max I 0.16); epochs=750, normalize=minmax (max I 1.09); epochs=3, normalize=zscore (max I 1.09); epochs=150, normalize=zscore (max I 1.11); +2 more
  - `epochs, lr_schedule`: epochs=750, lr_schedule=cosine (max I 0.31)
  - `label_noise, normalize`: label_noise=0.905, normalize=zscore (max I 0.32); label_noise=0.1, normalize=zscore (max I 0.93); label_noise=0.981, normalize=zscore (max I 1.14)
- 4 separate islands (no single-knob move joins them): epochs=150, normalize=minmax; label_noise=0.905, normalize=zscore; label_noise=0.1, normalize=zscore | epochs=750, lr_schedule=cosine; epochs=150, lr_schedule=cosine; epochs=750, lr_schedule=step | label_noise=0.981, lr_schedule=cosine | lr_schedule=cosine, weight_decay=0.0001

Notes:
- stopped early: run budget of 200 reached (wanted 3 more run(s) of {'normalize': 'zscore', 'epochs': '3'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `epochs=150`, `normalize=minmax` | 5 | +0.0% | -0.9% | 0.4% |
| `normalize=zscore`, `label_noise=0.905` | 5 | +0.5% | +1.8% | 1.2% |
| `epochs=750`, `lr_schedule=cosine` | 5 | +1.6% | +1.2% | 1.4% |
| `normalize=zscore`, `label_noise=0.1` | 5 | +4.3% | +5.7% | 5.0% |
| `normalize=zscore`, `epochs=3` | 2 | +5.6% | +7.1% | 6.4% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `weight_decay=none`: invalid_value, The argument --weight_decay expects a float value; 'none' is not a valid float. To express no weight decay, a value of 0.0 is used, but since that default has already been measured, a small positive value like 0.0001 approximates the intent of negligible regularization; retried as `weight_decay=0.0001`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`

## Provenance
- GapFinder commit: `e9c31fd1405f5c8aae4bd880eadcdc8d491fad02` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
