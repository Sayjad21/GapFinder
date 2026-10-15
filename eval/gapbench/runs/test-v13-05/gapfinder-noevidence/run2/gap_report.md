# Gap Report: test-v13-05

Artifact `mlbench` · generated 2026-10-16 00:12 · 174 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -31.0% | +5.9% | ±6.4% | `normalize=zscore` |

## C1: test_accuracy (paper 0.7792)
**Fits but unsupported** · gap -31.0% → +5.9% · 35 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0020`, `B0054`, `B0055`, `B0082`, `B0083`, `B0084` (6 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Command:

  Replay: fork checkpoint `5a0f2f2f-b408-4971-b9e0-8deba8eba12a` and run
  ```
  RUN_TAG=56c965af3deb "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.825, 0.825, 0.825, 0.825, 0.825, 0.8292; gap after +5.9%; result checkpoint `4b70197d-8fda-4e00-a64e-27d3c4ec00c0`
- Effect: candidate 0.825 minus naive 0.5375 = +0.2875, 95% bootstrap interval [+0.2692, +0.34] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.779 test accuracy and 0.750 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7792 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.4792, 0.5625, 0.5083, 0.5375, 0.5375
- Spread: range 0.4792 to 0.5625, noise band ±0.05 (2 x MAD), CV 6.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -31.0% (noise band ±6.4% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -31.0% (it comes back)
- PASS · Held-out claim: C2: -27.7% to +7.6% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: evidence gate off: no evidence was looked for
- PASS · Effect vs noise: candidate minus naive is +0.2875 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (1.5 noise units, gap -21.4%); `normalize=minmax` (1.17 noise units, gap -23.5%)
- Near alternatives (closest across all claims):
  - `weight_decay=0.0001`, `normalize=zscore`: this claim +5.9%, mean |gap| 6.7% (5 runs)
  - `lr_schedule=cosine`, `normalize=zscore`: this claim +6.4%, mean |gap| 7.2% (5 runs)
  - `epochs=10`, `normalize=zscore`: this claim +6.4%, mean |gap| 7.2% (5 runs)

### History matching (every measured configuration, all claims together)
- 7 of 34 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 7 configurations
  - `normalize, weight_decay`: normalize=zscore, weight_decay=0.0001 (max I 1.31)
  - `normalize`: normalize=zscore (max I 1.32)
  - `epochs, normalize`: epochs=2, normalize=zscore (max I 1.34); epochs=10, normalize=zscore (max I 1.37)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.37)
  - `label_noise, normalize`: label_noise=0.0, normalize=zscore (max I 1.43); label_noise=0.81, normalize=zscore (max I 1.57)

Notes:
- evidence gate off: no evidence was checked, so this cannot be labelled Explained

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore` | 6 | +5.9% | +7.6% | 6.7% |
| `weight_decay=0.0001`, `normalize=zscore` | 5 | +5.9% | +7.6% | 6.7% |
| `lr_schedule=cosine`, `normalize=zscore` | 5 | +6.4% | +8.0% | 7.2% |
| `epochs=10`, `normalize=zscore` | 5 | +6.4% | +8.0% | 7.2% |
| `normalize=zscore`, `epochs=2` | 5 | +6.4% | +8.0% | 7.2% |

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
