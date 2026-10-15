# Gap Report: test-v13-05

Artifact `mlbench` · generated 2026-10-16 00:44 · 148 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -31.0% | +0.5% | ±0.7% | `normalize=zscore`, `class_weight=balanced` |

## C1: test_accuracy (paper 0.7792)
**Fits but unsupported** · gap -31.0% → +0.5% · 67 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0050`, `B0092`, `B0129` (3 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Config: `class_weight` naive `none`, changed to `balanced`
- Command:

  Replay: fork checkpoint `57b2ca51-c8a9-44f7-a911-d7cf1f6da00d` and run
  ```
  RUN_TAG=1a64aa6d05f5 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight balanced --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7875, 0.7833, 0.7833; gap after +0.5%; result checkpoint `4344360a-09ed-4496-8a89-47f35c6fa4ed`
- Effect: candidate 0.7833 minus naive 0.5375 = +0.2458, 95% bootstrap interval [+0.2458, +0.2906] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.779 test accuracy and 0.750 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7792 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5375, 0.5375, 0.4875, 0.5375, 0.4958
- Spread: range 0.4875 to 0.5375, noise band ±0.005375 (2 x MAD), CV 4.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -31.0% (noise band ±0.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -31.0% (it comes back)
- PASS · Counterfactual (reversal test): without `class_weight` the gap is +6.4% (it comes back)
- PASS · Held-out claim: C2: -27.7% to +4.7% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- PASS · Evidence: `class_weight=balanced`: paper evidence at p.1: 'A plain logistic-regression baseline reaches 0.779 test accuracy and 0.750 balanced accuracy on a synthetic screening ta'
- PASS · Effect vs noise: candidate minus naive is +0.2458 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (16.28 noise units, gap -19.8%); `normalize=minmax` (10.85 noise units, gap -23.5%); `epochs=10` (4.65 noise units, gap -27.8%); `label_noise=0.005` (3.11 noise units, gap -28.9%); `label_noise=0.01` (1.54 noise units, gap -30.0%)
- Near alternatives (closest across all claims):
  - `epochs=150`, `normalize=minmax`: this claim -0.5%, mean |gap| 1.1% (3 runs)
  - `lr_schedule=cosine`, `epochs=750`: this claim +1.6%, mean |gap| 1.4% (3 runs)
  - `class_weight=balanced`, `normalize=minmax`: this claim -1.1%, mean |gap| 2.6% (3 runs)

### Equally good configurations
The target claim can't tell these 4 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `class_weight=balanced, normalize=zscore` (reported)
- `epochs=150, normalize=minmax`
- `epochs=750, lr_schedule=cosine`
- `class_weight=balanced, normalize=minmax`

### History matching (every measured configuration, all claims together)
- 21 of 67 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `epochs, normalize`: epochs=150, normalize=minmax (max I 0.25); epochs=2, normalize=zscore (max I 1.17); epochs=1, normalize=zscore (max I 1.2); epochs=150, normalize=zscore (max I 1.22); +3 more
  - `epochs, lr_schedule`: epochs=750, lr_schedule=cosine (max I 0.32)
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 0.64); class_weight=balanced, normalize=zscore (max I 0.83)
- 3 separate islands (no single-knob move joins them): epochs=150, normalize=minmax; class_weight=balanced, normalize=minmax; class_weight=balanced, normalize=zscore | epochs=750, lr_schedule=cosine; epochs=150, lr_schedule=cosine; epochs=750, lr_schedule=step | class_weight=balanced, epochs=750
- Equally good values: `normalize` in {minmax, zscore}

Notes:
- configurations the target claim can't tell apart from the answer: class_weight=balanced, normalize=zscore; epochs=150, normalize=minmax; epochs=750, lr_schedule=cosine; class_weight=balanced, normalize=minmax
- equally good values within one noise band (measured): normalize in {minmax, zscore}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `epochs=150`, `normalize=minmax` | 3 | -0.5% | -1.6% | 1.1% |
| `lr_schedule=cosine`, `epochs=750` | 3 | +1.6% | +1.2% | 1.4% |
| `class_weight=balanced`, `normalize=zscore` | 3 | +0.5% | +4.7% | 2.6% |
| `class_weight=balanced`, `normalize=minmax` | 3 | -1.1% | +4.2% | 2.6% |
| `epochs=1`, `normalize=zscore` | 3 | +5.3% | +6.7% | 6.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `out`

## Provenance
- GapFinder commit: `e9c31fd1405f5c8aae4bd880eadcdc8d491fad02` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
