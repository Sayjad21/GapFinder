# Gap Report: dev-ml-threshold

Artifact `mlbench` · generated 2026-10-16 01:41 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -34.6% | +0.0% | ±3.3% | `normalize=zscore`, `threshold=0.3` |

## C1: test_accuracy (paper 0.7583)
**Fits but unsupported** · gap -34.6% → +0.0% · 61 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0095`, `B0132`, `B0166`, `B0167`, `B0168` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Config: `threshold` naive `0.5`, changed to `0.3`
- Command:

  Replay: fork checkpoint `b96acaea-97a6-4340-a886-d25d70a332aa` and run
  ```
  RUN_TAG=db69fbd4986f "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.3 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7583, 0.7583, 0.7583, 0.7583, 0.7583; gap after +0.0%; result checkpoint `fbb9216f-8a66-45e4-85fc-41afbb5e24d3`
- Effect: candidate 0.7583 minus naive 0.4958 = +0.2625, 95% bootstrap interval [+0.2142, +0.2716] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> On imbalanced screening data, accuracy depends as much on the decision rule as on the model.

- p. 1; value used: `test_accuracy` = 0.7583 (headline claim)

### What did we measure?
- Naive median 0.4958 over 5 runs; repeats: 0.4958, 0.4917, 0.4833, 0.5375, 0.5458
- Spread: range 0.4833 to 0.5458, noise band ±0.025 (2 x MAD), CV 5.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -34.6% (noise band ±3.3% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -33.0% (it comes back)
- PASS · Counterfactual (reversal test): without `threshold` the gap is +9.3% (it comes back)
- PASS · Held-out claim: C2: -37.4% to +0.0% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- FAIL · Evidence: `threshold=0.3`: no evidence mentions '0.3'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2625 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=minmax` (4 noise units, gap -21.4%); `lr_schedule=cosine` (3.84 noise units, gap -22.0%); `lr_schedule=step` (3.34 noise units, gap -23.6%); `threshold=0.95` (2 noise units, gap -28.0%); `threshold=0.1` (2 noise units, gap -28.0%) (and 3 more in the JSON)
- Near alternatives (closest across all claims):
  - `normalize=minmax`, `class_weight=balanced`: this claim +1.6%, mean |gap| 1.1% (5 runs)
  - `normalize=zscore`, `threshold=0.4`: this claim +3.3%, mean |gap| 1.7% (5 runs)
  - `class_weight=balanced`, `normalize=zscore`: this claim +3.9%, mean |gap| 2.2% (5 runs)

### History matching (every measured configuration, all claims together)
- 10 of 58 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `normalize, threshold`: normalize=zscore, threshold=0.3 (max I 0); normalize=zscore, threshold=0.4 (max I 0.59); normalize=minmax, threshold=0.4 (max I 0.74); normalize=zscore, threshold=0.25 (max I 0.98); +1 more
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 0.28); class_weight=balanced, normalize=zscore (max I 0.65)
  - `normalize`: normalize=zscore (max I 1.66)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.68); lr_schedule=step, normalize=zscore (max I 1.68)

Notes:
- stopped early: run budget of 200 reached (wanted 3 more run(s) of {'lr_schedule': 'cosine', 'threshold': '0.95'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore`, `threshold=0.3` | 5 | +0.0% | +0.0% | 0.0% |
| `normalize=minmax`, `class_weight=balanced` | 5 | +1.6% | -0.6% | 1.1% |
| `normalize=zscore`, `threshold=0.4` | 5 | +3.3% | -0.1% | 1.7% |
| `class_weight=balanced`, `normalize=zscore` | 5 | +3.9% | +0.6% | 2.2% |
| `normalize=minmax`, `threshold=0.4` | 5 | -0.5% | -4.4% | 2.5% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `threshold=auto`: invalid_value, The program expects a numeric float for --threshold, but received the string 'auto', which is not a valid float; suggested `0.3`, already measured

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
