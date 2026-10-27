# Gap Report: test-v12-06

Artifact `mlbench` · generated 2026-10-15 19:52 · 194 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -33.0% | +0.5% | ±10.8% | `lr_schedule=cosine`, `positive_rate=0.1` |

## C1: test_accuracy (paper 0.7708)
**Fits but unsupported** · gap -33.0% → +0.5% · 65 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0120`, `B0128`, `B0156`, `B0157`, `B0158` (5 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `cosine`
- Config: `positive_rate` naive `0.3`, changed to `0.1`
- Command:

  Replay: fork checkpoint `e71c9b7e-bb86-41d0-ab07-81795ddc941c` and run
  ```
  RUN_TAG=1cf0cddeeeee "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.1 --label_noise 0.05 --split 0.8 --normalize none --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule cosine --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7875, 0.7292, 0.7083, 0.775, 0.7792; gap after +0.5%; result checkpoint `e6517957-0963-423e-9e8e-40e20d3f8c9c`
- Effect: candidate 0.775 minus naive 0.5167 = +0.2583, 95% bootstrap interval [+0.1683, +0.2892] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.771 test accuracy and 0.745 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7708 (headline claim)

### What did we measure?
- Naive median 0.5167 over 5 runs; repeats: 0.475, 0.5667, 0.5625, 0.5167, 0.4875
- Spread: range 0.475 to 0.5667, noise band ±0.0834 (2 x MAD), CV 8.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -33.0% (noise band ±10.8% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is -34.3% (it comes back)
- PASS · Counterfactual (reversal test): without `positive_rate` the gap is -19.5% (it comes back)
- PASS · Held-out claim: C2: -31.1% to -19.4% (not worse beyond noise)
- FAIL · Evidence: `lr_schedule=cosine`: no evidence mentions 'cosine'; it fits, but nothing says the authors used it
- FAIL · Evidence: `positive_rate=0.1`: no evidence mentions '0.1'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2583 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `SCALES`, `WEIGHTS`, `RUN_TAG`, `num_runs`, `aggregation_method`, `python_version`, `os`, `cpu_arch`, `memory_size`, `storage_type`, `out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (2.35 noise units, gap +7.6%)
- Near alternatives (closest across all claims):
  - `normalize=zscore`, `positive_rate=0.5`: this claim +1.6%, mean |gap| 3.4% (5 runs)
  - `normalize=zscore`, `positive_rate=0.15`: this claim +1.1%, mean |gap| 4.9% (5 runs)
  - `positive_rate=0.86`, `normalize=zscore`: this claim +5.4%, mean |gap| 5.1% (5 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `lr_schedule=cosine, positive_rate=0.1` (reported)
- `normalize=zscore, positive_rate=0.15`
- `normalize=zscore, positive_rate=0.5`

### History matching (every measured configuration, all claims together)
- 17 of 62 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `normalize, positive_rate`: normalize=zscore, positive_rate=0.5 (max I 0.86); normalize=zscore, positive_rate=0.86 (max I 0.88); normalize=zscore, positive_rate=0.65 (max I 1.36); normalize=zscore, positive_rate=0.15 (max I 1.45)
  - `normalize, weight_decay`: normalize=zscore, weight_decay=1e-4 (max I 1.36); normalize=zscore, weight_decay=1e-3 (max I 1.4)
  - `normalize`: normalize=zscore (max I 1.38)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.4); lr_schedule=step, normalize=zscore (max I 1.4)
  - `lr_schedule, positive_rate`: lr_schedule=cosine, positive_rate=0.93 (max I 2.5)
- 3 separate islands (no single-knob move joins them): normalize=zscore, positive_rate=0.5; normalize=zscore, positive_rate=0.86; normalize=zscore, positive_rate=0.65 | lr_schedule=cosine, positive_rate=0.93; lr_schedule=cosine, positive_rate=0.86; lr_schedule=cosine, positive_rate=0.15 | lr_schedule=cosine, weight_decay=1e-4; lr_schedule=cosine, weight_decay=1e-3
- Equally good values: `positive_rate` in {0.03, 0.06, 0.1}

Notes:
- configurations the target claim can't tell apart from the answer: lr_schedule=cosine, positive_rate=0.1; normalize=zscore, positive_rate=0.15; normalize=zscore, positive_rate=0.5
- equally good values within one noise band (measured): positive_rate in {0.03, 0.06, 0.1}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore`, `positive_rate=0.5` | 5 | +1.6% | +5.2% | 3.4% |
| `normalize=zscore`, `positive_rate=0.15` | 5 | +1.1% | -8.7% | 4.9% |
| `positive_rate=0.86`, `normalize=zscore` | 5 | +5.4% | -4.9% | 5.1% |
| `normalize=zscore`, `positive_rate=0.65` | 5 | +6.5% | +8.4% | 7.4% |
| `normalize=zscore` | 6 | +7.3% | +8.6% | 7.9% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `SCALES`, `WEIGHTS`, `RUN_TAG`, `num_runs`, `aggregation_method`, `python_version`, `os`, `cpu_arch`, `memory_size`, `storage_type`, `out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
