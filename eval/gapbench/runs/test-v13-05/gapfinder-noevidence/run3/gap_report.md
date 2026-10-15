# Gap Report: test-v13-05

Artifact `mlbench` · generated 2026-10-16 00:44 · 199 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -31.6% | +0.5% | ±3.2% | `normalize=zscore`, `class_weight=balanced` |

## C1: test_accuracy (paper 0.7792)
**Fits but unsupported** · gap -31.6% → +0.5% · 71 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0114`, `B0151`, `B0185`, `B0186`, `B0187` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Config: `class_weight` naive `none`, changed to `balanced`
- Command:

  Replay: fork checkpoint `edc16b2f-1445-43a9-bdc1-f18cfeddb47d` and run
  ```
  RUN_TAG=eb585ce86788 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight balanced --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7833, 0.7833, 0.7833, 0.7875, 0.7833; gap after +0.5%; result checkpoint `36e9910a-a9c8-404a-a3e5-87f8c11520ce`
- Effect: candidate 0.7833 minus naive 0.5333 = +0.25, 95% bootstrap interval [+0.2417, +0.3] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.779 test accuracy and 0.750 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7792 (headline claim)

### What did we measure?
- Naive median 0.5333 over 5 runs; repeats: 0.5375, 0.5333, 0.5458, 0.4833, 0.4875
- Spread: range 0.4833 to 0.5458, noise band ±0.025 (2 x MAD), CV 5.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -31.6% (noise band ±3.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -32.1% (it comes back)
- PASS · Counterfactual (reversal test): without `class_weight` the gap is +6.1% (it comes back)
- PASS · Held-out claim: C2: -28.2% to +4.7% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: evidence gate off: no evidence was looked for
- FAIL · Evidence: `class_weight=balanced`: evidence gate off: no evidence was looked for
- PASS · Effect vs noise: candidate minus naive is +0.25 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (3.34 noise units, gap -20.9%); `epochs=75` (2.84 noise units, gap -22.5%); `normalize=minmax` (2.5 noise units, gap -23.5%); `label_noise=0.981` (2.17 noise units, gap -24.6%); `lr_schedule=step` (1.34 noise units, gap -27.3%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `normalize=minmax`, `class_weight=balanced`: this claim -1.1%, mean |gap| 2.5% (5 runs)
  - `normalize=zscore`, `label_noise=0.1`: this claim +3.7%, mean |gap| 4.4% (5 runs)
  - `normalize=zscore`, `epochs=75`: this claim +5.3%, mean |gap| 6.1% (5 runs)

### History matching (every measured configuration, all claims together)
- 25 of 71 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 0.59); class_weight=balanced, normalize=zscore (max I 0.81)
  - `label_noise, normalize`: label_noise=0.1, normalize=zscore (max I 0.9); label_noise=0.981, normalize=zscore (max I 1.12)
  - `epochs, normalize`: epochs=150, normalize=zscore (max I 1.14); epochs=750, normalize=zscore (max I 1.14); epochs=20, normalize=zscore (max I 1.2); epochs=30, normalize=zscore (max I 1.2); +2 more
- 3 separate islands (no single-knob move joins them): class_weight=balanced, normalize=minmax; class_weight=balanced, normalize=zscore; label_noise=0.1, normalize=zscore | epochs=75, lr_schedule=cosine | label_noise=0.0, lr_schedule=cosine

Notes:
- stopped early: run budget of 200 reached (wanted 3 more run(s) of {'normalize': 'zscore', 'label_noise': '0.981'} for 'confirm-combo')
- evidence gate off: no evidence was checked, so this cannot be labelled Explained
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax`, `class_weight=balanced` | 5 | -1.1% | +3.9% | 2.5% |
| `normalize=zscore`, `class_weight=balanced` | 5 | +0.5% | +4.7% | 2.6% |
| `normalize=zscore`, `label_noise=0.1` | 5 | +3.7% | +5.0% | 4.4% |
| `normalize=zscore`, `epochs=75` | 5 | +5.3% | +6.9% | 6.1% |
| `normalize=zscore`, `epochs=1` | 5 | +5.3% | +7.3% | 6.3% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `out`

## Provenance
- GapFinder commit: `e9c31fd1405f5c8aae4bd880eadcdc8d491fad02` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
