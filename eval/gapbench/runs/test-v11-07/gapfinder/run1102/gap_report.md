# Gap Report: test-v11-07

Artifact `mlbench` · generated 2026-10-15 00:36 · 24 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -11.4% | -1.7% | ±3.1% | `lr_schedule=step` |

## C1: test_accuracy (paper 0.5361)
**Fits but unsupported** · gap -11.4% → -1.7% · 13 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0007`, `B0014`, `B0015`, `B0016` (4 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `step`
- Command:

  Replay: fork checkpoint `071bfb35-101c-466d-8b64-4b992f92dabb` and run
  ```
  RUN_TAG=317a101929e3 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize none --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule step --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.5125, 0.5417, 0.5125, 0.5417; gap after -1.7%; result checkpoint `45997fe8-aebc-4d3c-a003-9691a9cff420`
- Effect: candidate 0.5271 minus naive 0.475 = +0.0521, 95% bootstrap interval [+0.03582, +0.0725] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.536 test accuracy and 0.543 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.5361 (headline claim)

### What did we measure?
- Naive median 0.475 over 5 runs; repeats: 0.475, 0.4875, 0.4667, 0.4667, 0.4792
- Spread: range 0.4667 to 0.4875, noise band ±0.0166 (2 x MAD), CV 1.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -11.4% (noise band ±3.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is -11.4% (it comes back)
- PASS · Held-out claim: C2: -13.4% to -2.9% (not worse beyond noise)
- FAIL · Evidence: `lr_schedule=step`: no evidence mentions 'step'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.0521 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `hardware`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `class_weight=balanced` (3.6 noise units, gap +0.3%)
- Near alternatives (closest across all claims):
  - `class_weight=balanced`: this claim -4.4%, mean |gap| 4.9% (4 runs)

### Equally good configurations
The target claim can't tell these 2 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `lr_schedule=step` (reported)
- `class_weight=balanced`

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 8 configurations
  - `lr_schedule`: lr_schedule=step (max I 0.53); lr_schedule=cosine (max I 2.83)
  - `class_weight`: class_weight=balanced (max I 0.89)
  - `normalize`: normalize=minmax (max I 2.09)
  - `lr_schedule, normalize`: lr_schedule=step, normalize=minmax (max I 2.09); lr_schedule=cosine, normalize=minmax (max I 2.09)
  - `class_weight, lr_schedule`: class_weight=balanced, lr_schedule=step (max I 2.39); class_weight=balanced, lr_schedule=cosine (max I 2.39)

Notes:
- configurations the target claim can't tell apart from the answer: lr_schedule=step; class_weight=balanced

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=step` | 4 | -1.7% | -2.9% | 2.3% |
| `class_weight=balanced` | 4 | -4.4% | -5.5% | 4.9% |
| naive (reproduction as run) | 5 | -11.4% | -13.4% | 12.4% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `hardware`, `--out`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
