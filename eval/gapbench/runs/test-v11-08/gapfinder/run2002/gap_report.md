# Gap Report: test-v11-08

Artifact `mlbench` · generated 2026-10-15 21:03 · 28 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -5.6% | +0.0% | ±1.4% | `normalize=minmax` |

## C1: test_accuracy (paper 0.5958)
**Fits but unsupported** · gap -5.6% → +0.0% · 13 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0007`, `B0014`, `B0015`, `B0016` (4 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Command:

  Replay: fork checkpoint `6d2d4962-59dc-45ce-bc7b-eb05a157be22` and run
  ```
  RUN_TAG=74974bfe0a0e "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.5958, 0.5958, 0.5958, 0.5958; gap after +0.0%; result checkpoint `5eafec69-c46d-459b-bbf3-e9d0585e4d58`
- Effect: candidate 0.5958 minus naive 0.5625 = +0.0333, 95% bootstrap interval [+0.03078, +0.06414] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.596 test accuracy and 0.500 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.5958 (headline claim)

### What did we measure?
- Naive median 0.5625 over 5 runs; repeats: 0.5125, 0.5625, 0.5625, 0.5583, 0.5667
- Spread: range 0.5125 to 0.5667, noise band ±0.0084 (2 x MAD), CV 4.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -5.6% (noise band ±1.4% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -5.6% (it comes back)
- PASS · Held-out claim: C2: +11.7% to +0.0% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.0333 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives (closest across all claims):
  - `lr_schedule=cosine`, `normalize=minmax`: this claim +0.0%, mean |gap| 0.0% (3 runs)
  - `lr_schedule=step`, `normalize=minmax`: this claim +0.0%, mean |gap| 0.0% (3 runs)
  - `normalize=zscore`: this claim +38.8%, mean |gap| 50.3% (4 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `normalize=minmax` (reported)
- `lr_schedule=cosine, normalize=minmax`
- `lr_schedule=step, normalize=minmax`

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 6 configurations
  - `normalize`: normalize=minmax (max I 0)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=minmax (max I 0); lr_schedule=step, normalize=minmax (max I 0)
  - `class_weight, lr_schedule`: class_weight=balanced, lr_schedule=step (max I 1.4)
  - `class_weight`: class_weight=balanced (max I 1.61)
  - `lr_schedule`: lr_schedule=step (max I 3)

Notes:
- configurations the target claim can't tell apart from the answer: normalize=minmax; lr_schedule=cosine, normalize=minmax; lr_schedule=step, normalize=minmax

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax` | 4 | +0.0% | +0.0% | 0.0% |
| `lr_schedule=cosine`, `normalize=minmax` | 3 | +0.0% | +0.0% | 0.0% |
| `lr_schedule=step`, `normalize=minmax` | 3 | +0.0% | +0.0% | 0.0% |
| naive (reproduction as run) | 5 | -5.6% | +11.7% | 8.6% |
| `normalize=zscore` | 4 | +38.8% | +61.7% | 50.3% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `cd8c8af2b9d079dd9a57443ed501c0dd8a467d34` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
