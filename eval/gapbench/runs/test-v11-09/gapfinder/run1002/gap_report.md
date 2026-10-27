# Gap Report: test-v11-09

Artifact `mlbench` · generated 2026-10-15 00:25 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -29.3% | +1.1% | ±1.1% | `lr=0.25`, `normalize=minmax` |

## C1: test_accuracy (paper 0.7542)
**Fits but unsupported** · gap -29.3% → +1.1% · 61 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0069`, `B0181`, `B0182`, `B0183`, `B0184` (5 run(s) of the same config)
- Config: `lr` naive `0.05`, changed to `0.25`
- Config: `normalize` naive `none`, changed to `minmax`
- Command:

  Replay: fork checkpoint `9fda76b8-ac78-4d97-8f9f-35a0edcb798f` and run
  ```
  RUN_TAG=2aca34f19cb0 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.25 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7708, 0.7542, 0.7625, 0.7667, 0.6917; gap after +1.1%; result checkpoint `12da24c2-9dab-48b3-b91a-dcd490bb719a`
- Effect: candidate 0.7625 minus naive 0.5333 = +0.2292, 95% bootstrap interval [+0.1867, +0.2858] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.754 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7542 (headline claim)

### What did we measure?
- Naive median 0.5333 over 5 runs; repeats: 0.4667, 0.5333, 0.5375, 0.475, 0.5333
- Spread: range 0.4667 to 0.5375, noise band ±0.0084 (2 x MAD), CV 6.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -29.3% (noise band ±1.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr` the gap is -21.0% (it comes back)
- PASS · Counterfactual (reversal test): without `normalize` the gap is -28.7% (it comes back)
- PASS · Held-out claim: C2: -25.4% to +0.3% (not worse beyond noise)
- FAIL · Evidence: `lr=0.25`: no evidence mentions '0.25'; it fits, but nothing says the authors used it
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2292 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (17.37 noise units, gap +9.9%); `lr_schedule=cosine` (9.43 noise units, gap -18.8%); `lr=0.5` (4.46 noise units, gap -24.3%); `lr=0.025` (2.98 noise units, gap -26.0%); `lr=0.001` (2.98 noise units, gap -26.0%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr=0.5`, `normalize=minmax`: this claim +4.4%, mean |gap| 4.5% (5 runs)
  - `class_weight=balanced`, `normalize=minmax`: this claim +1.7%, mean |gap| 4.7% (5 runs)
  - `normalize=zscore`, `class_weight=balanced`: this claim +3.9%, mean |gap| 6.3% (5 runs)

### History matching (every measured configuration, all claims together)
- 21 of 61 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr, normalize`: lr=0.25, normalize=minmax (max I 0.45); lr=0.5, normalize=minmax (max I 0.76); lr=2.5, normalize=zscore (max I 0.76); lr=0.0005, normalize=zscore (max I 1.1); +4 more
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 1.26); class_weight=balanced, normalize=zscore (max I 1.41)
- 2 separate islands (no single-knob move joins them): lr=0.25, normalize=minmax; lr=0.5, normalize=minmax; lr=2.5, normalize=zscore | lr=0.1, lr_schedule=cosine; lr=0.01, lr_schedule=cosine; lr=2.5, lr_schedule=cosine

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'lr_schedule': 'step', 'lr': '0.001'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr=0.25`, `normalize=minmax` | 5 | +1.1% | +0.3% | 0.7% |
| `lr=0.5`, `normalize=minmax` | 5 | +4.4% | +4.6% | 4.5% |
| `class_weight=balanced`, `normalize=minmax` | 5 | +1.7% | +7.7% | 4.7% |
| `normalize=zscore`, `class_weight=balanced` | 5 | +3.9% | +8.7% | 6.3% |
| `normalize=zscore`, `lr=0.001` | 5 | +6.1% | +8.5% | 7.3% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
