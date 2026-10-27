# Gap Report: test-v11-05

Artifact `mlbench` · generated 2026-10-15 21:03 · 180 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -23.4% | -0.6% | ±3.4% | `epochs=150`, `lr_schedule=cosine` |

## C1: test_accuracy (paper 0.7292)
**Fits but unsupported** · gap -23.4% → -0.6% · 61 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0050`, `B0092`, `B0129`, `B0130`, `B0131` (5 run(s) of the same config)
- Config: `epochs` naive `15`, changed to `150`
- Config: `lr_schedule` naive `const`, changed to `cosine`
- Command:

  Replay: fork checkpoint `09abfa9d-4513-4589-ba17-6cad6a88f7f5` and run
  ```
  RUN_TAG=12a9fca9e5cb "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize none --epochs 150 --batch_size 32 --lr 0.05 --lr_schedule cosine --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.725, 0.7208, 0.725, 0.7083, 0.725; gap after -0.6%; result checkpoint `44bedd7c-9273-4488-8e44-6c0e5ad11061`
- Effect: candidate 0.725 minus naive 0.5583 = +0.1667, 95% bootstrap interval [+0.1492, +0.2141] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.729 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7292 (headline claim)

### What did we measure?
- Naive median 0.5583 over 5 runs; repeats: 0.5667, 0.4917, 0.5333, 0.5708, 0.5583
- Spread: range 0.4917 to 0.5708, noise band ±0.025 (2 x MAD), CV 6.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -23.4% (noise band ±3.4% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `epochs` the gap is -15.7% (it comes back)
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is -26.0% (it comes back)
- PASS · Held-out claim: C2: -18.3% to +4.2% (not worse beyond noise)
- FAIL · Evidence: `epochs=150`: no evidence mentions '150'; it fits, but nothing says the authors used it
- FAIL · Evidence: `lr_schedule=cosine`: no evidence mentions 'cosine'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.1667 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (3 noise units, gap +13.1%); `normalize=minmax` (1.5 noise units, gap -18.3%); `epochs=75` (1.17 noise units, gap -19.4%)
- Near alternatives (closest across all claims):
  - `epochs=75`, `normalize=minmax`: this claim -2.3%, mean |gap| 2.7% (5 runs)
  - `epochs=75`, `lr_schedule=cosine`: this claim -8.0%, mean |gap| 5.1% (5 runs)
  - `epochs=750`, `lr_schedule=step`: this claim +4.6%, mean |gap| 6.3% (5 runs)

### Equally good configurations
The target claim can't tell these 4 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `epochs=150, lr_schedule=cosine` (reported)
- `epochs=75, normalize=minmax`
- `epochs=750, lr_schedule=step`
- `class_weight=balanced, normalize=minmax`

### History matching (every measured configuration, all claims together)
- 16 of 61 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `epochs, normalize`: epochs=75, normalize=minmax (max I 0.26); epochs=150, normalize=minmax (max I 1.68)
  - `epochs, lr_schedule`: epochs=750, lr_schedule=step (max I 0.38); epochs=150, lr_schedule=cosine (max I 0.64); epochs=75, lr_schedule=cosine (max I 1.38); epochs=30, lr_schedule=cosine (max I 2.14); +3 more
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 2.55)
- 3 separate islands (no single-knob move joins them): epochs=750, lr_schedule=step; epochs=150, lr_schedule=cosine; epochs=75, lr_schedule=cosine | epochs=75, normalize=minmax; epochs=150, normalize=minmax | class_weight=balanced, normalize=minmax; class_weight=balanced, normalize=zscore

Notes:
- configurations the target claim can't tell apart from the answer: epochs=150, lr_schedule=cosine; epochs=75, normalize=minmax; epochs=750, lr_schedule=step; class_weight=balanced, normalize=minmax

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `epochs=150`, `lr_schedule=cosine` | 5 | -0.6% | +4.2% | 2.4% |
| `epochs=75`, `normalize=minmax` | 5 | -2.3% | -3.1% | 2.7% |
| `epochs=75`, `lr_schedule=cosine` | 5 | -8.0% | -2.1% | 5.1% |
| `epochs=750`, `lr_schedule=step` | 5 | +4.6% | +8.1% | 6.3% |
| `epochs=150`, `normalize=minmax` | 5 | +6.3% | +9.7% | 8.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `cd8c8af2b9d079dd9a57443ed501c0dd8a467d34` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
