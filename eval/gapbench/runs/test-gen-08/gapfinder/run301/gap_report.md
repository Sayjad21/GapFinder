# Gap Report: test-gen-08

Artifact `mlbench` · generated 2026-10-14 21:44 · 171 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -15.4% | +0.0% | ±9.8% | `normalize=minmax` |

## C1: test_accuracy (paper 0.5958)
**Fits but unsupported** · gap -15.4% → +0.0% · 53 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0020`, `B0081`, `B0082`, `B0083`, `B0084`, `B0085` (6 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Command:

  Replay: fork checkpoint `29e2d6b1-718c-411e-8e17-025a2282d888` and run
  ```
  RUN_TAG=8d8b8f95c6a6 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.5958, 0.5958, 0.5958, 0.5958, 0.5958, 0.5958; gap after +0.0%; result checkpoint `c61a958f-1575-4a0c-bbc5-72fd4442d36f`
- Effect: candidate 0.5958 minus naive 0.5042 = +0.0916, 95% bootstrap interval [+0.05914, +0.1191] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.596 test accuracy.

- p. 1; value used: `test_accuracy` = 0.5958 (headline claim)

### What did we measure?
- Naive median 0.5042 over 5 runs; repeats: 0.4792, 0.5042, 0.475, 0.5333, 0.5375
- Spread: range 0.475 to 0.5375, noise band ±0.0582 (2 x MAD), CV 5.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -15.4% (noise band ±9.8% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -15.4% (it comes back)
- PASS · Held-out claim: C2: +0.2% to +0.0% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.0916 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `SCALES`, `WEIGHTS`, `RUN_TAG`, `num_runs`, `train_test_split_order`, `python_version`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (1.21 noise units, gap +3.5%); `epochs=75` (1.07 noise units, gap -4.9%)
- Near alternatives (closest across all claims):
  - `lr_schedule=cosine`, `normalize=minmax`: this claim +0.0%, mean |gap| 0.0% (5 runs)
  - `epochs=10`, `normalize=minmax`: this claim +0.0%, mean |gap| 0.0% (5 runs)
  - `epochs=3`, `normalize=minmax`: this claim +0.0%, mean |gap| 0.0% (5 runs)

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `normalize`: normalize=minmax (max I 0)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=minmax (max I 0); lr_schedule=step, normalize=minmax (max I 0)
  - `epochs, normalize`: epochs=10, normalize=minmax (max I 0); epochs=3, normalize=minmax (max I 0); epochs=20, normalize=minmax (max I 0); epochs=30, normalize=minmax (max I 0.91)
  - `class_weight, epochs`: class_weight=balanced, epochs=75 (max I 1.23)
  - `epochs, lr_schedule`: epochs=30, lr_schedule=step (max I 1.33)
  - `epochs`: epochs=150 (max I 1.47)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax` | 6 | +0.0% | +0.0% | 0.0% |
| `lr_schedule=cosine`, `normalize=minmax` | 5 | +0.0% | +0.0% | 0.0% |
| `epochs=10`, `normalize=minmax` | 5 | +0.0% | +0.0% | 0.0% |
| `epochs=3`, `normalize=minmax` | 5 | +0.0% | +0.0% | 0.0% |
| `epochs=20`, `normalize=minmax` | 5 | +0.0% | +0.0% | 0.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `SCALES`, `WEIGHTS`, `RUN_TAG`, `num_runs`, `train_test_split_order`, `python_version`

## Provenance
- GapFinder commit: `e0f13d101585ad1609a15fbf67b70128f4cfffc8` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
