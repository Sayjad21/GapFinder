# Gap Report: test-v11-07

Artifact `mlbench` · generated 2026-10-14 12:00 · 27 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -9.8% | -4.4% | ±3.1% | `class_weight=balanced` |

## C1: test_accuracy (paper 0.5361)
**Fits but unsupported** · gap -9.8% → -4.4% · 13 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0006`, `B0011`, `B0012`, `B0013`, `B0014`, `B0015` (6 run(s) of the same config)
- Config: `class_weight` naive `none`, changed to `balanced`
- Command:

  Replay: fork checkpoint `637ca2ca-6058-4804-87ad-5a3d49748c5b` and run
  ```
  RUN_TAG=2e400e4753d7 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize none --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight balanced --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.5375, 0.4667, 0.4667, 0.55, 0.4875, 0.5375; gap after -4.4%; result checkpoint `6f831a53-d6b6-4da0-9887-232790c6f354`
- Effect: candidate 0.5125 minus naive 0.4833 = +0.0292, 95% bootstrap interval [-0.03082, +0.04668] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.536 test accuracy and 0.543 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.5361 (headline claim)

### What did we measure?
- Naive median 0.4833 over 5 runs; repeats: 0.4875, 0.55, 0.4833, 0.475, 0.475
- Spread: range 0.475 to 0.55, noise band ±0.0166 (2 x MAD), CV 6.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -9.8% (noise band ±3.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `class_weight` the gap is -9.8% (it comes back)
- PASS · Held-out claim: C2: -11.5% to -5.5% (not worse beyond noise)
- FAIL · Evidence: `class_weight=balanced`: evidence gate off: no evidence was looked for
- FAIL · Effect vs noise: candidate minus naive is +0.0292 with a 95% bootstrap interval that includes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `hardware`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives (closest across all claims):
  - `lr_schedule=step`, `class_weight=balanced`: this claim +3.4%, mean |gap| 2.6% (5 runs)

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 8 configurations
  - `class_weight, lr_schedule`: class_weight=balanced, lr_schedule=step (max I 0.66); class_weight=balanced, lr_schedule=cosine (max I 1.51)
  - `class_weight`: class_weight=balanced (max I 1.03)
  - `normalize`: normalize=minmax (max I 1.35)
  - `lr_schedule, normalize`: lr_schedule=step, normalize=minmax (max I 1.35); lr_schedule=cosine, normalize=minmax (max I 1.35)
  - `lr_schedule`: lr_schedule=step (max I 1.45); lr_schedule=cosine (max I 1.92)

Notes:
- evidence gate off: no evidence was checked, so this cannot be labelled Explained

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=step`, `class_weight=balanced` | 5 | +3.4% | +1.9% | 2.6% |
| `class_weight=balanced` | 6 | -4.4% | -5.5% | 4.9% |
| naive (reproduction as run) | 5 | -9.8% | -11.5% | 10.7% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `hardware`, `--out`

## Provenance
- GapFinder commit: `b05f7288e1a4df8af69bb0b5e7633827b4cb46c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
