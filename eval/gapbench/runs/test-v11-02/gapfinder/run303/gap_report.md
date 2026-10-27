# Gap Report: test-v11-02

Artifact `mlbench` · generated 2026-10-14 21:45 · 53 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -27.5% | -10.6% | ±5.0% | `normalize=minmax` |

## C1: test_accuracy (paper 0.6666)
**Fits but unsupported** · gap -27.5% → -10.6% · 13 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0008`, `B0011`, `B0012`, `B0013`, `B0014`, `B0015` (6 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Command:

  Replay: fork checkpoint `b22f4b2d-67fa-43d9-9e89-249692cff289` and run
  ```
  RUN_TAG=afc0daf97a92 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.5958, 0.5958, 0.5958, 0.5958, 0.5958, 0.5958; gap after -10.6%; result checkpoint `541ea949-5a50-4366-b9cf-86ea67a6804a`
- Effect: candidate 0.5958 minus naive 0.4833 = +0.1125, 95% bootstrap interval [+0.06914, +0.1258] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.667 test accuracy and 0.485 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.6666 (headline claim)

### What did we measure?
- Naive median 0.4833 over 5 runs; repeats: 0.5375, 0.4667, 0.4833, 0.4667, 0.5208
- Spread: range 0.4667 to 0.5375, noise band ±0.0332 (2 x MAD), CV 6.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -27.5% (noise band ±5.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -27.5% (it comes back)
- PASS · Held-out claim: C2: -1.3% to +3.1% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.1125 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (4.14 noise units, gap -6.9%); `lr_schedule=step` (1.76 noise units, gap -18.7%)
- Near alternatives (closest across all claims):
  - `lr_schedule=cosine`, `normalize=minmax`: this claim -10.6%, mean |gap| 6.9% (5 runs)
  - `normalize=minmax`, `lr_schedule=step`: this claim -10.6%, mean |gap| 6.9% (5 runs)
  - `lr_schedule=step`: this claim -20.3%, mean |gap| 15.1% (6 runs)

### History matching (every measured configuration, all claims together)
- 3 of 13 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=minmax (max I 1.8); lr_schedule=step, normalize=minmax (max I 1.8)
  - `normalize`: normalize=minmax (max I 1.82)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax` | 6 | -10.6% | +3.1% | 6.9% |
| `lr_schedule=cosine`, `normalize=minmax` | 5 | -10.6% | +3.1% | 6.9% |
| `normalize=minmax`, `lr_schedule=step` | 5 | -10.6% | +3.1% | 6.9% |
| naive (reproduction as run) | 5 | -27.5% | -1.3% | 14.4% |
| `lr_schedule=step` | 6 | -20.3% | +9.9% | 15.1% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `--out`

## Provenance
- GapFinder commit: `e0f13d101585ad1609a15fbf67b70128f4cfffc8` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
