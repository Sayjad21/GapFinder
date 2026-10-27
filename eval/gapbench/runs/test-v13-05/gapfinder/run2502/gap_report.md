# Gap Report: test-v13-05

Artifact `mlbench` · generated 2026-10-16 02:06 · 195 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -31.0% | +0.5% | ±2.1% | `normalize=zscore`, `label_noise=0.905` |

## C1: test_accuracy (paper 0.7792)
**Fits but unsupported** · gap -31.0% → +0.5% · 74 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0107`, `B0151`, `B0181` (3 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Config: `label_noise` naive `0.05`, changed to `0.905`
- Command:

  Replay: fork checkpoint `6c1772f0-a60e-42f1-9613-8a884e8f98ef` and run
  ```
  RUN_TAG=690aac528f57 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.905 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7833, 0.7875, 0.7833; gap after +0.5%; result checkpoint `1678e3c9-7142-4cde-b873-aa30c8564176`
- Effect: candidate 0.7833 minus naive 0.5375 = +0.2458, 95% bootstrap interval [+0.2358, +0.2872] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.779 test accuracy and 0.750 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7792 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.4875, 0.55, 0.5375, 0.5458, 0.5375
- Spread: range 0.4875 to 0.55, noise band ±0.0166 (2 x MAD), CV 4.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -31.0% (noise band ±2.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -29.7% (it comes back)
- PASS · Counterfactual (reversal test): without `label_noise` the gap is +5.9% (it comes back)
- PASS · Held-out claim: C2: -27.7% to +1.8% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- FAIL · Evidence: `label_noise=0.905`: no evidence mentions '0.905'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2458 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (5.52 noise units, gap -19.3%); `normalize=minmax` (3.51 noise units, gap -23.5%); `epochs=10` (1.51 noise units, gap -27.8%); `class_weight=balanced` (1.51 noise units, gap -27.8%); `epochs=2` (1.25 noise units, gap -28.3%)
- Near alternatives (closest across all claims):
  - `normalize=zscore`, `label_noise=0.1`: this claim +3.7%, mean |gap| 4.4% (3 runs)
  - `normalize=zscore`, `label_noise=0.981`: this claim +5.3%, mean |gap| 6.0% (3 runs)
  - `normalize=zscore`, `epochs=1`: this claim +5.3%, mean |gap| 6.1% (3 runs)

### History matching (every measured configuration, all claims together)
- 16 of 73 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `label_noise, normalize`: label_noise=0.905, normalize=zscore (max I 0.35); label_noise=0.1, normalize=zscore (max I 0.92); label_noise=0.981, normalize=zscore (max I 1.21); label_noise=0.025, normalize=zscore (max I 1.39)
  - `epochs, normalize`: epochs=1, normalize=zscore (max I 1.16); epochs=75, normalize=zscore (max I 1.28); epochs=2, normalize=zscore (max I 1.32); epochs=10, normalize=zscore (max I 1.36)
  - `normalize`: normalize=zscore (max I 1.35)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.4)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore`, `label_noise=0.905` | 3 | +0.5% | +1.8% | 1.2% |
| `normalize=zscore`, `label_noise=0.1` | 3 | +3.7% | +5.0% | 4.4% |
| `normalize=zscore`, `label_noise=0.981` | 3 | +5.3% | +6.7% | 6.0% |
| `normalize=zscore`, `epochs=1` | 3 | +5.3% | +6.9% | 6.1% |
| `normalize=zscore`, `epochs=2` | 3 | +5.9% | +7.3% | 6.6% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `weight_decay=none`: invalid_value, The argument --weight_decay expects a float value; 'none' is not a valid float. To express no weight decay, a value of 0.0 is used, but since that default has already been measured, a small positive value like 0.0001 approximates the intent of negligible regularization; retried as `weight_decay=0.0001`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
