# Gap Report: test-v11-03

Artifact `mlbench` · generated 2026-10-14 11:10 · 185 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -31.4% | +0.5% | ±2.1% | `normalize=zscore`, `positive_rate=0.5` |

## C1: test_accuracy (paper 0.7833)
**Fits but unsupported** · gap -31.4% → +0.5% · 64 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0100`, `B0144`, `B0145` (3 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Config: `positive_rate` naive `0.3`, changed to `0.5`
- Command:

  Replay: fork checkpoint `5af32422-74a5-469f-8b57-e0288d453767` and run
  ```
  RUN_TAG=0c54d31b9a43 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.5 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7917, 0.7875, 0.7875; gap after +0.5%; result checkpoint `9a906ce5-f386-4716-94ae-3d8612aad75e`
- Effect: candidate 0.7875 minus naive 0.5375 = +0.25, 95% bootstrap interval [+0.2308, +0.2889] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.783 test accuracy and 0.752 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7833 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5458, 0.5375, 0.5333, 0.5625, 0.4917
- Spread: range 0.4917 to 0.5625, noise band ±0.0166 (2 x MAD), CV 4.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -31.4% (noise band ±2.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -36.2% (it comes back)
- PASS · Counterfactual (reversal test): without `positive_rate` the gap is +5.9% (it comes back)
- PASS · Held-out claim: C2: -27.9% to +4.7% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- FAIL · Evidence: `positive_rate=0.5`: no evidence mentions '0.5'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.25 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `NUM_RUNS`, `AGGREGATION_METHOD`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `batch_size=1` (5.52 noise units, gap -19.7%); `lr_schedule=cosine` (4.77 noise units, gap -21.3%); `normalize=minmax` (3.51 noise units, gap -23.9%); `positive_rate=0.15` (1.76 noise units, gap -27.7%); `class_weight=balanced` (1.01 noise units, gap -29.2%)
- Near alternatives (closest across all claims):
  - `label_noise=0.905`, `normalize=zscore`: this claim +0.0%, mean |gap| 0.8% (3 runs)
  - `batch_size=3`, `normalize=minmax`: this claim -1.1%, mean |gap| 1.9% (3 runs)
  - `normalize=minmax`, `positive_rate=0.5`: this claim +1.1%, mean |gap| 3.1% (3 runs)

### History matching (every measured configuration, all claims together)
- 14 of 63 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `batch_size, normalize`: batch_size=3, normalize=minmax (max I 0.26); batch_size=1, normalize=zscore (max I 0.75); batch_size=1, normalize=minmax (max I 1.08); batch_size=3, normalize=zscore (max I 1.26)
  - `label_noise, normalize`: label_noise=0.905, normalize=zscore (max I 0.27)
  - `normalize, positive_rate`: normalize=zscore, positive_rate=0.5 (max I 0.86); normalize=minmax, positive_rate=0.5 (max I 0.92)
  - `batch_size, lr_schedule`: batch_size=1, lr_schedule=cosine (max I 1.3)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.35); lr_schedule=step, normalize=zscore (max I 1.35)
- 2 separate islands (no single-knob move joins them): batch_size=3, normalize=minmax; label_noise=0.905, normalize=zscore; batch_size=1, normalize=zscore | batch_size=1, lr_schedule=cosine; batch_size=3, lr_schedule=cosine
- Equally good values: `normalize` in {minmax, zscore}; `positive_rate` in {0.15, 0.5}

Notes:
- equally good values within one noise band (measured): normalize in {minmax, zscore}; positive_rate in {0.15, 0.5}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `label_noise=0.905`, `normalize=zscore` | 3 | +0.0% | +1.5% | 0.8% |
| `batch_size=3`, `normalize=minmax` | 3 | -1.1% | -2.7% | 1.9% |
| `normalize=zscore`, `positive_rate=0.5` | 3 | +0.5% | +4.7% | 2.6% |
| `normalize=minmax`, `positive_rate=0.5` | 3 | +1.1% | +5.2% | 3.1% |
| `normalize=zscore`, `batch_size=1` | 3 | +2.1% | +4.9% | 3.5% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: invalid_value, The code computes log(positive_rate/(1-positive_rate)); with positive_rate=0.0 the argument is 0 causing a math domain error. A small positive value like 0.01 preserves the intent of a low positive rate while avoiding the domain error; retried as `positive_rate=0.01`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `NUM_RUNS`, `AGGREGATION_METHOD`

## Provenance
- GapFinder commit: `b05f7288e1a4df8af69bb0b5e7633827b4cb46c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0884, sandbox reported $0.0000 (total $0.0884; this search; ledger extraction is included only if it shared the search's router)
