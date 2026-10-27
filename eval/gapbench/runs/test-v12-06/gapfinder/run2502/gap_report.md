# Gap Report: test-v12-06

Artifact `mlbench` · generated 2026-10-16 02:00 · 199 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -35.7% | +1.1% | ±2.2% | `positive_rate=0.15`, `normalize=zscore` |

## C1: test_accuracy (paper 0.7708)
**Fits but unsupported** · gap -35.7% → +1.1% · 63 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0095`, `B0137`, `B0176`, `B0177`, `B0178` (5 run(s) of the same config)
- Config: `positive_rate` naive `0.3`, changed to `0.15`
- Config: `normalize` naive `none`, changed to `zscore`
- Command:

  Replay: fork checkpoint `8977b56d-04e7-4ee7-9b8d-46d8f6805e90` and run
  ```
  RUN_TAG=311aabaa2854 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.15 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.775, 0.7792, 0.7792, 0.7792, 0.7792; gap after +1.1%; result checkpoint `b97dc181-10df-42a6-b123-9af7a538658d`
- Effect: candidate 0.7792 minus naive 0.4958 = +0.2834, 95% bootstrap interval [+0.2301, +0.2917] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.771 test accuracy and 0.745 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7708 (headline claim)

### What did we measure?
- Naive median 0.4958 over 5 runs; repeats: 0.5583, 0.4875, 0.4958, 0.5333, 0.4875
- Spread: range 0.4875 to 0.5583, noise band ±0.0166 (2 x MAD), CV 6.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -35.7% (noise band ±2.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `positive_rate` the gap is +7.3% (it comes back)
- PASS · Counterfactual (reversal test): without `normalize` the gap is -34.3% (it comes back)
- PASS · Held-out claim: C2: -33.9% to -8.7% (not worse beyond noise)
- FAIL · Evidence: `positive_rate=0.15`: no evidence mentions '0.15'; it fits, but nothing says the authors used it
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2834 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `SCALES`, `WEIGHTS`, `RUN_TAG`, `num_runs`, `aggregation_method`, `python_version`, `os`, `cpu_arch`, `memory_size`, `storage_type`, `out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (7.03 noise units, gap -20.5%); `normalize=minmax` (6.02 noise units, gap -22.7%); `positive_rate=0.65` (4.77 noise units, gap -25.4%); `positive_rate=0.03` (3.27 noise units, gap -28.6%); `lr_schedule=step` (3.27 noise units, gap -28.6%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `positive_rate=0.2`, `normalize=zscore`: this claim +3.2%, mean |gap| 1.7% (5 runs)
  - `class_weight=balanced`, `normalize=minmax`: this claim -0.5%, mean |gap| 3.0% (5 runs)
  - `positive_rate=0.5`, `normalize=zscore`: this claim +1.6%, mean |gap| 3.4% (5 runs)

### History matching (every measured configuration, all claims together)
- 15 of 60 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `normalize, positive_rate`: normalize=zscore, positive_rate=0.2 (max I 0.57); normalize=zscore, positive_rate=0.5 (max I 0.95); normalize=zscore, positive_rate=0.65 (max I 1.39); normalize=zscore, positive_rate=0.4 (max I 1.39); +1 more
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 0.9); class_weight=balanced, normalize=zscore (max I 0.96)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.38); lr_schedule=step, normalize=zscore (max I 1.38)
  - `normalize`: normalize=zscore (max I 1.48)
- 2 separate islands (no single-knob move joins them): normalize=zscore, positive_rate=0.2; class_weight=balanced, normalize=minmax; normalize=zscore, positive_rate=0.5 | lr_schedule=cosine, positive_rate=0.2; lr_schedule=cosine, positive_rate=0.93; lr_schedule=cosine, positive_rate=0.65

Notes:
- stopped early: run budget of 200 reached (wanted 3 more run(s) of {'lr_schedule': 'cosine', 'positive_rate': '0.1'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `positive_rate=0.2`, `normalize=zscore` | 5 | +3.2% | -0.2% | 1.7% |
| `class_weight=balanced`, `normalize=minmax` | 5 | -0.5% | +5.6% | 3.0% |
| `positive_rate=0.5`, `normalize=zscore` | 5 | +1.6% | +5.2% | 3.4% |
| `class_weight=balanced`, `normalize=zscore` | 5 | +1.6% | +5.4% | 3.5% |
| `positive_rate=0.15`, `normalize=zscore` | 5 | +1.1% | -8.7% | 4.9% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `SCALES`, `WEIGHTS`, `RUN_TAG`, `num_runs`, `aggregation_method`, `python_version`, `os`, `cpu_arch`, `memory_size`, `storage_type`, `out`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
