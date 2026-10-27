# Gap Report: test-gen-06

Artifact `mlbench` · generated 2026-10-15 01:09 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -26.4% | +0.0% | ±4.5% | `normalize=zscore`, `n=600` |

## C1: test_accuracy (paper 0.7417)
**Fits but unsupported** · gap -26.4% → +0.0% · 58 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0055`, `B0125`, `B0126`, `B0127`, `B0128` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Config: `n` naive `1200`, changed to `600`
- Command:

  Replay: fork checkpoint `548f84a1-d364-4294-af29-14eabe17a9d3` and run
  ```
  RUN_TAG=9fd3c4dbc93f "${PYTHON:-python3}" train.py --n 600 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7417, 0.7417, 0.7417, 0.7417, 0.7417; gap after +0.0%; result checkpoint `43f1c188-0e65-42ff-9ce0-3d0a6fdb04f0`
- Effect: candidate 0.7417 minus naive 0.5458 = +0.1959, 95% bootstrap interval [+0.1567, +0.2192] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.742 test accuracy and 0.700 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7417 (headline claim)

### What did we measure?
- Naive median 0.5458 over 5 runs; repeats: 0.5458, 0.5625, 0.5417, 0.5958, 0.5167
- Spread: range 0.5167 to 0.5958, noise band ±0.0334 (2 x MAD), CV 5.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -26.4% (noise band ±4.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -24.7% (it comes back)
- PASS · Counterfactual (reversal test): without `n` the gap is +11.8% (it comes back)
- PASS · Held-out claim: C2: -21.8% to +0.0% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- FAIL · Evidence: `n=600`: no evidence mentions '600'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.1959 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `hardware`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (2.5 noise units, gap -15.2%); `normalize=minmax` (1.5 noise units, gap -19.7%); `n=5000` (1.5 noise units, gap -19.6%); `n=120` (1.12 noise units, gap -21.4%)
- Near alternatives (closest across all claims):
  - `normalize=zscore`, `n=6000`: this claim +1.0%, mean |gap| 1.7% (5 runs)
  - `normalize=zscore`, `n=2400`: this claim -3.9%, mean |gap| 2.2% (5 runs)
  - `normalize=zscore`, `n=120`: this claim -4.5%, mean |gap| 2.9% (5 runs)

### History matching (every measured configuration, all claims together)
- 22 of 56 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `n, normalize`: n=600, normalize=zscore (max I 0); n=6000, normalize=zscore (max I 0.43); n=120, normalize=zscore (max I 0.63); n=1000, normalize=zscore (max I 0.64); +5 more
  - `lr_schedule, n, normalize`: lr_schedule=cosine, n=120, normalize=zscore (max I 0.89)

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'n': '2000', 'class_weight': 'balanced'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore`, `n=600` | 5 | +0.0% | +0.0% | 0.0% |
| `normalize=zscore`, `n=6000` | 5 | +1.0% | +2.5% | 1.7% |
| `normalize=zscore`, `n=2400` | 5 | -3.9% | -0.4% | 2.2% |
| `normalize=zscore`, `n=120` | 5 | -4.5% | +1.3% | 2.9% |
| `normalize=zscore`, `lr_schedule=cosine`, `n=120` | 5 | -4.5% | +1.3% | 2.9% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `n=1`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `hardware`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
