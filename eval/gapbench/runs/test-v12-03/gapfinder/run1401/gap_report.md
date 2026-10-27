# Gap Report: test-v12-03

Artifact `mlbench` · generated 2026-10-15 19:02 · 177 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -29.8% | +0.0% | ±7.1% | `normalize=minmax`, `positive_rate=0.15` |

## C1: test_accuracy (paper 0.7)
**Fits but unsupported** · gap -29.8% → +0.0% · 57 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0083`, `B0117`, `B0140`, `B0141`, `B0142` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `positive_rate` naive `0.3`, changed to `0.15`
- Command:

  Replay: fork checkpoint `3886755d-d127-41d3-b858-c99c85bf1458` and run
  ```
  RUN_TAG=6924806821d0 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.15 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7, 0.7, 0.7, 0.7, 0.7; gap after +0.0%; result checkpoint `513e69b8-b81d-4b58-ade0-ea841a3152b5`
- Effect: candidate 0.7 minus naive 0.4917 = +0.2083, 95% bootstrap interval [+0.1317, +0.23] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.700 test accuracy and 0.500 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7 (headline claim)

### What did we measure?
- Naive median 0.4917 over 5 runs; repeats: 0.5875, 0.5333, 0.4917, 0.4833, 0.4667
- Spread: range 0.4667 to 0.5875, noise band ±0.05 (2 x MAD), CV 9.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -29.8% (noise band ±7.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -26.5% (it comes back)
- PASS · Counterfactual (reversal test): without `positive_rate` the gap is -14.9% (it comes back)
- PASS · Held-out claim: C2: -2.6% to +0.0% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- FAIL · Evidence: `positive_rate=0.15`: no evidence mentions '0.15'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2083 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (2.42 noise units, gap -12.5%); `normalize=zscore` (1.58 noise units, gap +18.5%); `class_weight=balanced` (1 noise units, gap -22.6%)
- Near alternatives (closest across all claims):
  - `positive_rate=0.1`, `normalize=minmax`: this claim +11.9%, mean |gap| 6.0% (5 runs)
  - `lr_schedule=cosine`, `positive_rate=0.03`: this claim +10.7%, mean |gap| 6.4% (5 runs)
  - `normalize=minmax`: this claim -14.9%, mean |gap| 7.4% (5 runs)

### History matching (every measured configuration, all claims together)
- 29 of 55 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `normalize, positive_rate`: normalize=minmax, positive_rate=0.15 (max I 0); normalize=minmax, positive_rate=0.1 (max I 1.77); normalize=zscore, positive_rate=0.1 (max I 2.26); normalize=minmax, positive_rate=0.93 (max I 2.31)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=minmax (max I 1.93); lr_schedule=step, normalize=minmax (max I 1.93)
  - `lr_schedule, positive_rate`: lr_schedule=cosine, positive_rate=0.03 (max I 1.94); lr_schedule=cosine, positive_rate=0.1 (max I 2.25)
  - `normalize`: normalize=minmax (max I 2.21)
  - `class_weight, lr_schedule`: class_weight=balanced, lr_schedule=cosine (max I 2.38)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `positive_rate=0.15`, `normalize=minmax` | 5 | +0.0% | +0.0% | 0.0% |
| `positive_rate=0.1`, `normalize=minmax` | 5 | +11.9% | +0.0% | 6.0% |
| `lr_schedule=cosine`, `positive_rate=0.03` | 5 | +10.7% | -2.1% | 6.4% |
| `normalize=minmax` | 5 | -14.9% | +0.0% | 7.4% |
| `lr_schedule=cosine`, `normalize=minmax` | 2 | -14.9% | +0.0% | 7.4% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
