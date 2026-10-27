# Gap Report: test-gen-07

Artifact `mlbench` · generated 2026-10-14 23:42 · 24 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | +11.4% | -0.4% | ±5.1% | `class_weight=balanced` |

## C1: test_accuracy (paper 0.4938)
**Fits but unsupported** · gap +11.4% → -0.4% · 13 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0006`, `B0011`, `B0012`, `B0013` (4 run(s) of the same config)
- Config: `class_weight` naive `none`, changed to `balanced`
- Command:

  Replay: fork checkpoint `3d0c740b-7150-4ac9-9e27-8db2ac7ac7f2` and run
  ```
  RUN_TAG=3bdba324ff50 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize none --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight balanced --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.4792, 0.4917, 0.4917, 0.5333; gap after -0.4%; result checkpoint `7668b80b-3fb6-440a-b419-cd8d2eb732a7`
- Effect: candidate 0.4917 minus naive 0.55 = -0.0583, 95% bootstrap interval [-0.06748, -0.01502] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.494 test accuracy.

- p. 1; value used: `test_accuracy` = 0.4938 (headline claim)

### What did we measure?
- Naive median 0.55 over 5 runs; repeats: 0.5667, 0.5375, 0.5375, 0.5583, 0.55
- Spread: range 0.5375 to 0.5667, noise band ±0.025 (2 x MAD), CV 2.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +11.4% (noise band ±5.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `class_weight` the gap is +11.4% (it comes back)
- PASS · Held-out claim: C2: +14.1% to +0.6% (not worse beyond noise)
- FAIL · Evidence: `class_weight=balanced`: no evidence mentions 'balanced'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -0.0583 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=step` (1.83 noise units, gap -2.1%)
- Near alternatives (closest across all claims):
  - `lr_schedule=step`: this claim -2.1%, mean |gap| 1.5% (4 runs)

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `class_weight`: class_weight=balanced (max I 0.5)
  - `lr_schedule`: lr_schedule=step (max I 1.17)
  - `class_weight, lr_schedule`: class_weight=balanced, lr_schedule=step (max I 2.3)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `class_weight=balanced` | 4 | -0.4% | +0.6% | 0.5% |
| `lr_schedule=step` | 4 | -2.1% | -0.9% | 1.5% |
| naive (reproduction as run) | 5 | +11.4% | +14.1% | 12.7% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `efb2f63a257a40b9982099a274f2e882f272b80c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
