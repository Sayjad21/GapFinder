# Gap Report: dev-ml-threshold

Artifact `mlbench` · generated 2026-10-15 00:43 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -29.1% | +1.1% | ±1.1% | `normalize=minmax`, `class_weight=balanced` |

## C1: test_accuracy (paper 0.7583)
**Fits but unsupported** · gap -29.1% → +1.1% · 57 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0092`, `B0165`, `B0166`, `B0167`, `B0168` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `class_weight` naive `none`, changed to `balanced`
- Command:

  Replay: fork checkpoint `77ab9a96-7305-48b5-8a97-6d987bc84a39` and run
  ```
  RUN_TAG=37820f190fe0 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight balanced --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7792, 0.7417, 0.7708, 0.7667, 0.75; gap after +1.1%; result checkpoint `968d044a-71cd-4037-8fe2-8060be294958`
- Effect: candidate 0.7667 minus naive 0.5375 = +0.2292, 95% bootstrap interval [+0.2108, +0.2834] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> On imbalanced screening data, accuracy depends as much on the decision rule as on the model.

- p. 1; value used: `test_accuracy` = 0.7583 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.4958, 0.5375, 0.5375, 0.475, 0.5417
- Spread: range 0.475 to 0.5417, noise band ±0.0084 (2 x MAD), CV 5.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -29.1% (noise band ±1.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -28.6% (it comes back)
- PASS · Counterfactual (reversal test): without `class_weight` the gap is -21.4% (it comes back)
- PASS · Held-out claim: C2: -30.8% to -1.1% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- PASS · Evidence: `class_weight=balanced`: code evidence at train.py:75: 'cw = {1: 0.5 / pos, 0: 0.5 / (1 - pos)} if a.class_weight == "balanced" else {1: 1.0, 0: 1.0}'
- PASS · Effect vs noise: candidate minus naive is +0.2292 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (17.85 noise units, gap +9.3%); `lr_schedule=cosine` (10.92 noise units, gap -17.0%); `lr_schedule=step` (3.48 noise units, gap -25.3%)
- Near alternatives (closest across all claims):
  - `class_weight=balanced`, `normalize=zscore`: this claim +3.9%, mean |gap| 2.2% (5 runs)
  - `threshold=0.25`, `normalize=zscore`: this claim -5.5%, mean |gap| 4.8% (5 runs)
  - `normalize=zscore`: this claim +9.3%, mean |gap| 6.4% (6 runs)

### History matching (every measured configuration, all claims together)
- 7 of 55 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 7 configurations
  - `normalize, threshold`: normalize=zscore, threshold=0.3 (max I 0); normalize=zscore, threshold=0.25 (max I 0.95)
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 0.16); class_weight=balanced, normalize=zscore (max I 0.66)
  - `normalize`: normalize=zscore (max I 1.64)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.66); lr_schedule=step, normalize=zscore (max I 1.66)

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'lr_schedule': 'step', 'threshold': '0.1'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax`, `class_weight=balanced` | 5 | +1.1% | -1.1% | 1.1% |
| `class_weight=balanced`, `normalize=zscore` | 5 | +3.9% | +0.6% | 2.2% |
| `threshold=0.25`, `normalize=zscore` | 5 | -5.5% | -4.0% | 4.8% |
| `normalize=zscore` | 6 | +9.3% | +3.4% | 6.4% |
| `lr_schedule=cosine`, `normalize=zscore` | 5 | +9.3% | +3.4% | 6.4% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `threshold=auto`: invalid_value, The program expects a numeric float for --threshold, but received the string 'auto', which is not a valid float; suggested `0.3`, already measured

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
