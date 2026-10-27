# Gap Report: test-v11-03

Artifact `mlbench` · generated 2026-10-15 18:56 · 198 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -38.3% | +5.3% | ±2.1% | `normalize=zscore` |

## C1: test_accuracy (paper 0.7833)
**Fits but unsupported** · gap -38.3% → +5.3% · 35 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0038`, `B0103`, `B0104`, `B0109`, `B0110`, `B0111` (6 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Command:

  Replay: fork checkpoint `4d1fd497-9fc9-48a3-8ec4-e21af44ef22c` and run
  ```
  RUN_TAG=09054c355966 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.825, 0.8292, 0.8292, 0.825, 0.825, 0.825; gap after +5.3%; result checkpoint `0a51f09b-3ebc-41b2-a7ea-ebd6da59b313`
- Effect: candidate 0.825 minus naive 0.4833 = +0.3417, 95% bootstrap interval [+0.2925, +0.3475] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.783 test accuracy and 0.752 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7833 (headline claim)

### What did we measure?
- Naive median 0.4833 over 5 runs; repeats: 0.4833, 0.5458, 0.4833, 0.5458, 0.475
- Spread: range 0.475 to 0.5458, noise band ±0.0166 (2 x MAD), CV 7.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -38.3% (noise band ±2.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -38.3% (it comes back)
- PASS · Held-out claim: C2: -36.3% to +7.3% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.3417 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `NUM_RUNS`, `AGGREGATION_METHOD`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (8.28 noise units, gap -20.7%); `normalize=minmax` (6.78 noise units, gap -23.9%); `lr_schedule=step` (4.77 noise units, gap -28.2%); `batch_size=6` (4.52 noise units, gap -28.7%); `batch_size=128` (4.02 noise units, gap -29.8%) (and 13 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=cosine`: this claim -21.0%, mean |gap| 19.4% (6 runs)
  - `batch_size=6`: this claim -28.5%, mean |gap| 27.3% (6 runs)
  - `batch_size=1`: this claim -29.0%, mean |gap| 27.5% (6 runs)

### History matching (every measured configuration, all claims together)
- 1 of 34 tested configurations fit every claim within 3 sigma

Notes:
- stopped early: run budget of 200 reached (wanted 3 more run(s) of {'positive_rate': '0.15'} for 'confirm')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore` | 6 | +5.3% | +7.3% | 6.3% |
| `lr_schedule=cosine` | 6 | -21.0% | -17.7% | 19.4% |
| `batch_size=6` | 6 | -28.5% | -26.1% | 27.3% |
| `batch_size=1` | 6 | -29.0% | -26.0% | 27.5% |
| `normalize=minmax` | 3 | -23.9% | -33.5% | 28.7% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `NUM_RUNS`, `AGGREGATION_METHOD`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
