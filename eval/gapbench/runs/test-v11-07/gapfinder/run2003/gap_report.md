# Gap Report: test-v11-07

Artifact `mlbench` · generated 2026-10-15 21:03 · 32 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -9.1% | +1.0% | ±7.8% | `lr_schedule=step` |

## C1: test_accuracy (paper 0.5361)
**Fits but unsupported** · gap -9.1% → +1.0% · 13 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0006`, `B0011`, `B0012`, `B0013`, `B0014`, `B0015` (6 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `step`
- Command:

  Replay: fork checkpoint `a213eb74-ccc5-4f80-92ed-45f3a6241588` and run
  ```
  RUN_TAG=6c1f7a84f764 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize none --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule step --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.5417, 0.5417, 0.5417, 0.5417, 0.575, 0.5542; gap after +1.0%; result checkpoint `a3423cae-e657-4cf3-9300-a30b39a5d98e`
- Effect: candidate 0.5417 minus naive 0.4875 = +0.0542, 95% bootstrap interval [+0.01168, +0.08416] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.536 test accuracy and 0.543 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.5361 (headline claim)

### What did we measure?
- Naive median 0.4875 over 5 runs; repeats: 0.4875, 0.4667, 0.4667, 0.5417, 0.5458
- Spread: range 0.4667 to 0.5458, noise band ±0.0416 (2 x MAD), CV 7.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -9.1% (noise band ±7.8% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is -9.1% (it comes back)
- PASS · Held-out claim: C2: -11.2% to +0.6% (not worse beyond noise)
- FAIL · Evidence: `lr_schedule=step`: no evidence mentions 'step'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.0542 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `class_weight=balanced` (1.1 noise units, gap -0.5%)
- Near alternatives (closest across all claims):
  - `class_weight=balanced`, `lr_schedule=step`: this claim -0.5%, mean |gap| 0.6% (5 runs)
  - `class_weight=balanced`: this claim -8.3%, mean |gap| 9.2% (6 runs)

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 8 configurations
  - `lr_schedule`: lr_schedule=step (max I 0.36); lr_schedule=cosine (max I 1.49)
  - `class_weight, lr_schedule`: class_weight=balanced, lr_schedule=step (max I 0.44); class_weight=balanced, lr_schedule=cosine (max I 1.25)
  - `normalize`: normalize=minmax (max I 1.17)
  - `lr_schedule, normalize`: lr_schedule=step, normalize=minmax (max I 1.17); lr_schedule=cosine, normalize=minmax (max I 1.17)
  - `class_weight`: class_weight=balanced (max I 1.21)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `class_weight=balanced`, `lr_schedule=step` | 5 | -0.5% | -0.7% | 0.6% |
| `lr_schedule=step` | 6 | +1.0% | +0.6% | 0.8% |
| `class_weight=balanced` | 6 | -8.3% | -10.2% | 9.2% |
| naive (reproduction as run) | 5 | -9.1% | -11.2% | 10.1% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `cd8c8af2b9d079dd9a57443ed501c0dd8a467d34` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
