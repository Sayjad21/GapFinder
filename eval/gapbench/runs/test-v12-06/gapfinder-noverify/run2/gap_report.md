# Gap Report: test-v12-06

Artifact `mlbench` · generated 2026-10-15 08:15 · 199 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Partially explained | -30.3% | +1.6% | ±3.2% | `positive_rate=0.1`, `normalize=minmax` |

## C1: test_accuracy (paper 0.7708)
**Partially explained** · gap -30.3% → +1.6% · 61 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0109`, `B0196`, `B0197`, `B0198`, `B0199` (5 run(s) of the same config)
- Config: `positive_rate` naive `0.3`, changed to `0.1`
- Config: `normalize` naive `none`, changed to `minmax`
- Command:

  Replay: fork checkpoint `4ee4a264-3d1d-418d-83fd-1c03c1c6570f` and run
  ```
  RUN_TAG=df5d272910d7 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.1 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7833, 0.7833, 0.7833, 0.7833, 0.7833; gap after +1.6%; result checkpoint `f5fd385b-0bc7-411d-af81-313244b57ebf`
- Effect: candidate 0.7833 minus naive 0.5375 = +0.2458, 95% bootstrap interval [+0.2341, +0.3149] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.771 test accuracy and 0.745 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7708 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5458, 0.55, 0.5375, 0.475, 0.4667
- Spread: range 0.4667 to 0.55, noise band ±0.025 (2 x MAD), CV 7.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -30.3% (noise band ±3.2% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is +0.2458 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `SCALES`, `WEIGHTS`, `RUN_TAG`, `num_runs`, `aggregation_method`, `python_version`, `os`, `cpu_arch`, `memory_size`, `storage_type`, `out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (7 noise units, gap +7.6%); `lr_schedule=cosine` (3.17 noise units, gap -20.0%); `lr_schedule=step` (1.83 noise units, gap -24.3%); `weight_decay=1e-3` (1.33 noise units, gap -25.9%)
- Near alternatives (closest across all claims):
  - `positive_rate=0.5`, `normalize=zscore`: this claim +2.2%, mean |gap| 4.0% (5 runs)
  - `positive_rate=0.86`, `normalize=zscore`: this claim +5.4%, mean |gap| 5.1% (5 runs)
  - `positive_rate=0.65`, `normalize=zscore`: this claim +6.5%, mean |gap| 7.4% (5 runs)

### History matching (every measured configuration, all claims together)
- 16 of 59 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `normalize, positive_rate`: normalize=minmax, positive_rate=0.5 (max I 0.57); normalize=zscore, positive_rate=0.86 (max I 0.86); normalize=zscore, positive_rate=0.5 (max I 0.87); normalize=zscore, positive_rate=0.15 (max I 1.28); +1 more
  - `normalize, weight_decay`: normalize=zscore, weight_decay=1e-3 (max I 1.32); normalize=zscore, weight_decay=1e-4 (max I 1.37)
  - `normalize`: normalize=zscore (max I 1.39)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.39); lr_schedule=step, normalize=zscore (max I 1.39)
- 3 separate islands (no single-knob move joins them): normalize=minmax, positive_rate=0.5; normalize=zscore, positive_rate=0.86; normalize=zscore, positive_rate=0.5 | lr_schedule=cosine, positive_rate=0.5; lr_schedule=cosine, positive_rate=0.65; lr_schedule=cosine, positive_rate=0.86 | lr_schedule=cosine, weight_decay=1e-4

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'normalize': 'minmax', 'positive_rate': '0.65'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `positive_rate=0.5`, `normalize=zscore` | 5 | +2.2% | +5.7% | 4.0% |
| `positive_rate=0.86`, `normalize=zscore` | 5 | +5.4% | -4.9% | 5.1% |
| `positive_rate=0.65`, `normalize=zscore` | 5 | +6.5% | +8.4% | 7.4% |
| `normalize=zscore`, `weight_decay=1e-3` | 5 | +7.0% | +8.1% | 7.6% |
| `normalize=zscore` | 6 | +7.6% | +8.8% | 8.2% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: invalid_value, The code computes math.log(positive_rate / (1 - positive_rate)). With positive_rate = 0.0 the argument becomes 0, causing a math domain error. A small positive value such as 0.001 keeps the intent of a very low positive rate while avoiding the domain error; retried as `positive_rate=0.001`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `SCALES`, `WEIGHTS`, `RUN_TAG`, `num_runs`, `aggregation_method`, `python_version`, `os`, `cpu_arch`, `memory_size`, `storage_type`, `out`

## Provenance
- GapFinder commit: `f01fe3d9a0095f98d6304ad0543b917ca8e529eb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0006, sandbox reported $0.0000 (total $0.0006; this search; ledger extraction is included only if it shared the search's router)
