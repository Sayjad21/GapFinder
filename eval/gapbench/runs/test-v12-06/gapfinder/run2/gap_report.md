# Gap Report: test-v12-06

Artifact `mlbench` · generated 2026-10-15 08:15 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -30.3% | +1.1% | ±2.2% | `positive_rate=0.15`, `normalize=zscore` |

## C1: test_accuracy (paper 0.7708)
**Fits but unsupported** · gap -30.3% → +1.1% · 68 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0097`, `B0165`, `B0166`, `B0167`, `B0168` (5 run(s) of the same config)
- Config: `positive_rate` naive `0.3`, changed to `0.15`
- Config: `normalize` naive `none`, changed to `zscore`
- Command:

  Replay: fork checkpoint `fa65e1e1-7c8f-43e8-a31f-d91e19063804` and run
  ```
  RUN_TAG=b249983d5234 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.15 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7792, 0.775, 0.7792, 0.7792, 0.7792; gap after +1.1%; result checkpoint `73e13615-957f-4a09-b53c-ddfde048e5a8`
- Effect: candidate 0.7792 minus naive 0.5375 = +0.2417, 95% bootstrap interval [+0.2234, +0.2909] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.771 test accuracy and 0.745 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7708 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.475, 0.5583, 0.5375, 0.5458, 0.5375
- Spread: range 0.475 to 0.5583, noise band ±0.0166 (2 x MAD), CV 6.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -30.3% (noise band ±2.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `positive_rate` the gap is +7.3% (it comes back)
- PASS · Counterfactual (reversal test): without `normalize` the gap is -34.0% (it comes back)
- PASS · Held-out claim: C2: -27.2% to -8.7% (not worse beyond noise)
- FAIL · Evidence: `positive_rate=0.15`: no evidence mentions '0.15'; it fits, but nothing says the authors used it
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2417 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `SCALES`, `WEIGHTS`, `RUN_TAG`, `num_runs`, `aggregation_method`, `python_version`, `os`, `cpu_arch`, `memory_size`, `storage_type`, `out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (4.52 noise units, gap -20.5%); `normalize=minmax` (3.51 noise units, gap -22.7%); `weight_decay=1e-3` (1.51 noise units, gap -27.0%)
- Near alternatives (closest across all claims):
  - `normalize=zscore`, `positive_rate=0.86`: this claim +5.4%, mean |gap| 5.1% (5 runs)
  - `normalize=zscore`, `positive_rate=0.65`: this claim +7.0%, mean |gap| 7.9% (5 runs)
  - `normalize=zscore`: this claim +7.3%, mean |gap| 7.9% (6 runs)

### History matching (every measured configuration, all claims together)
- 16 of 65 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `normalize, positive_rate`: normalize=zscore, positive_rate=0.5 (max I 0.72); normalize=zscore, positive_rate=0.86 (max I 0.93); normalize=zscore, positive_rate=0.65 (max I 1.49); normalize=zscore, positive_rate=0.15 (max I 1.52); +1 more
  - `normalize, weight_decay`: normalize=zscore, weight_decay=1e-4 (max I 1.46); normalize=zscore, weight_decay=1e-3 (max I 1.5)
  - `normalize`: normalize=zscore (max I 1.47)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.5); lr_schedule=step, normalize=zscore (max I 1.5)
- 2 separate islands (no single-knob move joins them): normalize=zscore, positive_rate=0.5; normalize=zscore, positive_rate=0.86; normalize=zscore, weight_decay=1e-4 | lr_schedule=cosine, positive_rate=0.15; lr_schedule=cosine, positive_rate=0.65; lr_schedule=cosine, positive_rate=0.93

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'normalize': 'minmax', 'weight_decay': '1e-4'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `positive_rate=0.15`, `normalize=zscore` | 5 | +1.1% | -8.7% | 4.9% |
| `normalize=zscore`, `positive_rate=0.86` | 5 | +5.4% | -4.9% | 5.1% |
| `normalize=zscore`, `positive_rate=0.65` | 5 | +7.0% | +8.8% | 7.9% |
| `normalize=zscore` | 6 | +7.3% | +8.6% | 7.9% |
| `normalize=zscore`, `lr_schedule=cosine` | 5 | +7.6% | +8.8% | 8.2% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: invalid_value, The code computes math.log(positive_rate / (1 - positive_rate)), which requires positive_rate to be strictly between 0 and 1. A value of 0.0 leads to log(0) and a ValueError. Using a small positive value like 0.001 preserves the intent of a very low positive rate while avoiding the domain error; retried as `positive_rate=0.001`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `SCALES`, `WEIGHTS`, `RUN_TAG`, `num_runs`, `aggregation_method`, `python_version`, `os`, `cpu_arch`, `memory_size`, `storage_type`, `out`

## Provenance
- GapFinder commit: `f01fe3d9a0095f98d6304ad0543b917ca8e529eb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0769, sandbox reported $0.0000 (total $0.0769; this search; ledger extraction is included only if it shared the search's router)
