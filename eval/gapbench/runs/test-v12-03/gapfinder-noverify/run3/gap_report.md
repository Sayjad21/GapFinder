# Gap Report: test-v12-03

Artifact `mlbench` · generated 2026-10-15 08:52 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Explained | -31.0% | +0.0% | ±4.7% | `positive_rate=0.15`, `normalize=minmax` |

## C1: test_accuracy (paper 0.7)
**Explained** · gap -31.0% → +0.0% · 59 hypotheses tested
> Interacting factors: these changes close the gap only together, and every check passes

### Which experiment changed it?
- Branch: `B0101`, `B0189`, `B0190`, `B0191`, `B0192` (5 run(s) of the same config)
- Config: `positive_rate` naive `0.3`, changed to `0.15`
- Config: `normalize` naive `none`, changed to `minmax`
- Command:

  Replay: fork checkpoint `04f02375-8d3b-4696-983b-9b2f3d22a00c` and run
  ```
  RUN_TAG=33f66004c77b "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.15 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7, 0.7, 0.7, 0.7, 0.7; gap after +0.0%; result checkpoint `a1ea3bc7-ea4f-4264-b107-76881574d694`
- Effect: candidate 0.7 minus naive 0.4833 = +0.2167, 95% bootstrap interval [+0.1525, +0.2317] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.700 test accuracy and 0.500 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7 (headline claim)

### What did we measure?
- Naive median 0.4833 over 5 runs; repeats: 0.4708, 0.55, 0.5375, 0.4667, 0.4833
- Spread: range 0.4667 to 0.55, noise band ±0.0332 (2 x MAD), CV 7.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -31.0% (noise band ±4.7% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is +0.2167 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (4.14 noise units, gap -11.3%); `normalize=zscore` (2.64 noise units, gap +18.5%); `positive_rate=0.65` (1.88 noise units, gap -22.0%); `lr_schedule=step` (1.76 noise units, gap -22.6%); `positive_rate=0.5` (1.63 noise units, gap -23.2%) (and 2 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=cosine`, `positive_rate=0.03`: this claim +11.9%, mean |gap| 6.1% (5 runs)
  - `normalize=minmax`: this claim -14.9%, mean |gap| 7.4% (3 runs)
  - `lr_schedule=cosine`, `normalize=minmax`: this claim -14.9%, mean |gap| 7.4% (5 runs)

### History matching (every measured configuration, all claims together)
- 15 of 57 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `normalize, positive_rate`: normalize=minmax, positive_rate=0.15 (max I 0); normalize=minmax, positive_rate=0.65 (max I 2.6)
  - `class_weight, lr_schedule`: class_weight=balanced, lr_schedule=cosine (max I 1.97); class_weight=balanced, lr_schedule=step (max I 2.55)
  - `lr_schedule, positive_rate`: lr_schedule=cosine, positive_rate=0.1 (max I 2.05); lr_schedule=cosine, positive_rate=0.03 (max I 2.12); lr_schedule=cosine, positive_rate=0.86 (max I 2.48)
  - `normalize`: normalize=minmax (max I 2.29)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=minmax (max I 2.41); lr_schedule=step, normalize=minmax (max I 2.41)
- 6 separate islands (no single-knob move joins them): normalize=minmax, positive_rate=0.15; normalize=minmax; lr_schedule=cosine, normalize=minmax | lr_schedule=cosine, positive_rate=0.1; lr_schedule=cosine, positive_rate=0.03; lr_schedule=cosine, positive_rate=0.86 | class_weight=balanced, lr_schedule=cosine; class_weight=balanced, lr_schedule=step | lr_schedule=step, positive_rate=0.65

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'lr_schedule': 'cosine', 'class_weight': 'balanced'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `positive_rate=0.15`, `normalize=minmax` | 5 | +0.0% | +0.0% | 0.0% |
| `lr_schedule=cosine`, `positive_rate=0.03` | 5 | +11.9% | -0.2% | 6.1% |
| `normalize=minmax` | 3 | -14.9% | +0.0% | 7.4% |
| `lr_schedule=cosine`, `normalize=minmax` | 5 | -14.9% | +0.0% | 7.4% |
| `normalize=minmax`, `lr_schedule=step` | 5 | -14.9% | +0.0% | 7.4% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: invalid_value, The code computes log(p/(1-p)); p=0 leads to log(0) which raises a ValueError. A valid positive_rate must be strictly between 0 and 1. Using a small value like 0.001 approximates the intent of almost no positives while keeping the computation valid; retried as `positive_rate=0.001`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `f01fe3d9a0095f98d6304ad0543b917ca8e529eb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0007, sandbox reported $0.0000 (total $0.0007; this search; ledger extraction is included only if it shared the search's router)
