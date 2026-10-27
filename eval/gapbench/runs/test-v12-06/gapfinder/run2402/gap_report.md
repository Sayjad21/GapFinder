# Gap Report: test-v12-06

Artifact `mlbench` · generated 2026-10-16 01:29 · 158 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -30.3% | +1.1% | ±2.2% | `normalize=zscore`, `positive_rate=0.15` |

## C1: test_accuracy (paper 0.7708)
**Fits but unsupported** · gap -30.3% → +1.1% · 63 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0064`, `B0109`, `B0142` (3 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Config: `positive_rate` naive `0.3`, changed to `0.15`
- Command:

  Replay: fork checkpoint `e40e04ed-e8c2-4832-a54b-18447203c81b` and run
  ```
  RUN_TAG=f32b55a2cb8d "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.15 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7792, 0.7792, 0.7792; gap after +1.1%; result checkpoint `a682dada-db83-4bb0-b6dd-be089c22f5fa`
- Effect: candidate 0.7792 minus naive 0.5375 = +0.2417, 95% bootstrap interval [+0.2351, +0.2892] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.771 test accuracy and 0.745 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7708 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.4833, 0.5458, 0.5375, 0.5167, 0.5375
- Spread: range 0.4833 to 0.5458, noise band ±0.0166 (2 x MAD), CV 4.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -30.3% (noise band ±2.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -28.9% (it comes back)
- PASS · Counterfactual (reversal test): without `positive_rate` the gap is +7.0% (it comes back)
- PASS · Held-out claim: C2: -27.2% to -8.7% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- FAIL · Evidence: `positive_rate=0.15`: no evidence mentions '0.15'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2417 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `SCALES`, `WEIGHTS`, `RUN_TAG`, `num_runs`, `aggregation_method`, `python_version`, `os`, `cpu_arch`, `memory_size`, `storage_type`, `out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (6.28 noise units, gap -16.7%); `normalize=minmax` (3.51 noise units, gap -22.7%); `class_weight=balanced` (1.51 noise units, gap -27.0%); `weight_decay=1e-3` (1.51 noise units, gap -27.0%)
- Near alternatives (closest across all claims):
  - `positive_rate=0.2`, `normalize=zscore`: this claim +3.2%, mean |gap| 1.7% (3 runs)
  - `normalize=zscore`, `class_weight=balanced`: this claim +1.6%, mean |gap| 3.5% (3 runs)
  - `normalize=minmax`, `class_weight=balanced`: this claim -3.2%, mean |gap| 3.5% (3 runs)

### Equally good configurations
The target claim can't tell these 6 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `normalize=zscore, positive_rate=0.15` (reported)
- `class_weight=balanced, normalize=zscore`
- `lr_schedule=cosine, positive_rate=0.1`
- `normalize=zscore, positive_rate=0.5`
- `normalize=minmax, positive_rate=0.5`
- `class_weight=balanced, normalize=minmax`

### History matching (every measured configuration, all claims together)
- 13 of 60 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `normalize, positive_rate`: normalize=zscore, positive_rate=0.2 (max I 0.58); normalize=zscore, positive_rate=0.5 (max I 0.96); normalize=minmax, positive_rate=0.5 (max I 1); normalize=zscore, positive_rate=0.4 (max I 1.4); +2 more
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 0.62); class_weight=balanced, normalize=zscore (max I 0.97)
  - `normalize`: normalize=zscore (max I 1.48)
  - `lr_schedule, normalize`: lr_schedule=step, normalize=zscore (max I 1.49)
- 2 separate islands (no single-knob move joins them): normalize=zscore, positive_rate=0.2; class_weight=balanced, normalize=minmax; normalize=zscore, positive_rate=0.5 | lr_schedule=cosine, positive_rate=0.93; lr_schedule=cosine, positive_rate=0.2
- Equally good values: `positive_rate` in {0.15, 0.2, 0.5}

Notes:
- configurations the target claim can't tell apart from the answer: normalize=zscore, positive_rate=0.15; class_weight=balanced, normalize=zscore; lr_schedule=cosine, positive_rate=0.1; normalize=zscore, positive_rate=0.5; normalize=minmax, positive_rate=0.5; class_weight=balanced, normalize=minmax
- equally good values within one noise band (measured): positive_rate in {0.15, 0.2, 0.5}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `positive_rate=0.2`, `normalize=zscore` | 3 | +3.2% | -0.2% | 1.7% |
| `normalize=zscore`, `class_weight=balanced` | 3 | +1.6% | +5.4% | 3.5% |
| `normalize=minmax`, `class_weight=balanced` | 3 | -3.2% | +3.9% | 3.5% |
| `normalize=minmax`, `positive_rate=0.5` | 3 | +2.2% | +5.7% | 3.9% |
| `normalize=zscore`, `positive_rate=0.5` | 3 | +2.2% | +5.7% | 4.0% |

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
