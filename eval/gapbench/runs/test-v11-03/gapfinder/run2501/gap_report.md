# Gap Report: test-v11-03

Artifact `mlbench` · generated 2026-10-16 01:51 · 198 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -37.2% | +5.9% | ±3.2% | `normalize=zscore` |

## C1: test_accuracy (paper 0.7833)
**Fits but unsupported** · gap -37.2% → +5.9% · 35 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0020`, `B0069`, `B0070`, `B0112`, `B0113`, `B0114` (6 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Command:

  Replay: fork checkpoint `2c439566-2275-43e7-8646-08c170df607b` and run
  ```
  RUN_TAG=228d95a865b7 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.8292, 0.825, 0.8292, 0.8292, 0.825, 0.8292; gap after +5.9%; result checkpoint `7400a575-3637-4925-9ef0-08e116ddb7e4`
- Effect: candidate 0.8292 minus naive 0.4917 = +0.3375, 95% bootstrap interval [+0.2933, +0.3517] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.783 test accuracy and 0.752 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7833 (headline claim)

### What did we measure?
- Naive median 0.4917 over 5 runs; repeats: 0.4667, 0.4917, 0.4792, 0.5667, 0.4917
- Spread: range 0.4667 to 0.5667, noise band ±0.025 (2 x MAD), CV 7.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -37.2% (noise band ±3.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -37.2% (it comes back)
- PASS · Held-out claim: C2: -35.0% to +7.8% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.3375 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `NUM_RUNS`, `AGGREGATION_METHOD`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (5.5 noise units, gap -19.7%); `normalize=minmax` (4.16 noise units, gap -23.9%); `batch_size=16` (3.16 noise units, gap -27.1%); `batch_size=128` (2 noise units, gap -30.8%); `batch_size=320` (2 noise units, gap -30.8%) (and 16 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=cosine`: this claim -20.7%, mean |gap| 19.4% (6 runs)
  - `batch_size=3`: this claim -29.8%, mean |gap| 28.2% (6 runs)
  - `batch_size=1`: this claim -30.0%, mean |gap| 28.4% (6 runs)

### History matching (every measured configuration, all claims together)
- 1 of 34 tested configurations fit every claim within 3 sigma

Notes:
- stopped early: run budget of 200 reached (wanted 3 more run(s) of {'positive_rate': '0.03'} for 'confirm')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore` | 6 | +5.9% | +7.8% | 6.8% |
| `lr_schedule=cosine` | 6 | -20.7% | -18.0% | 19.4% |
| `batch_size=3` | 6 | -29.8% | -26.6% | 28.2% |
| `batch_size=1` | 6 | -30.0% | -26.7% | 28.4% |
| `normalize=minmax` | 3 | -23.9% | -33.5% | 28.7% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `NUM_RUNS`, `AGGREGATION_METHOD`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
