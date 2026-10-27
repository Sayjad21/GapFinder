# Gap Report: test-v12-03

Artifact `mlbench` · generated 2026-10-15 19:50 · 147 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -23.2% | +0.0% | ±0.8% | `normalize=minmax`, `positive_rate=0.15` |

## C1: test_accuracy (paper 0.7)
**Fits but unsupported** · gap -23.2% → +0.0% · 62 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0076`, `B0106`, `B0134` (3 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `positive_rate` naive `0.3`, changed to `0.15`
- Command:

  Replay: fork checkpoint `780d9155-874e-4691-9303-6297b1608850` and run
  ```
  RUN_TAG=1f36d0bcd406 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.15 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7, 0.7, 0.7; gap after +0.0%; result checkpoint `681a879b-3915-48c2-87e6-39372149a34a`
- Effect: candidate 0.7 minus naive 0.5375 = +0.1625, 95% bootstrap interval [+0.1625, +0.1759] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.700 test accuracy and 0.500 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5333, 0.5375, 0.5375, 0.5375, 0.5208
- Spread: range 0.5208 to 0.5375, noise band ±0.005375 (2 x MAD), CV 1.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -23.2% (noise band ±0.8% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -27.4% (it comes back)
- PASS · Counterfactual (reversal test): without `positive_rate` the gap is -14.9% (it comes back)
- PASS · Held-out claim: C2: +8.4% to +0.0% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- FAIL · Evidence: `positive_rate=0.15`: no evidence mentions '0.15'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.1625 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (15.5 noise units, gap -11.3%); `normalize=zscore` (6.2 noise units, gap +18.5%); `positive_rate=0.006` (3.11 noise units, gap -20.8%); `lr_schedule=step` (2.33 noise units, gap -21.4%)
- Near alternatives (closest across all claims):
  - `positive_rate=0.1`, `normalize=minmax`: this claim +11.9%, mean |gap| 6.0% (3 runs)
  - `normalize=minmax`: this claim -14.9%, mean |gap| 7.4% (4 runs)
  - `normalize=minmax`, `lr_schedule=cosine`: this claim -14.9%, mean |gap| 7.4% (2 runs)

### History matching (every measured configuration, all claims together)
- 6 of 60 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 6 configurations
  - `normalize, positive_rate`: normalize=minmax, positive_rate=0.15 (max I 0); normalize=minmax, positive_rate=0.1 (max I 2.35)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=minmax (max I 2.93); lr_schedule=step, normalize=minmax (max I 2.93)
  - `lr_schedule, positive_rate`: lr_schedule=cosine, positive_rate=0.03 (max I 2.93)
  - `normalize`: normalize=minmax (max I 2.95)
- 2 separate islands (no single-knob move joins them): normalize=minmax, positive_rate=0.15; normalize=minmax, positive_rate=0.1; lr_schedule=cosine, normalize=minmax | lr_schedule=cosine, positive_rate=0.03

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax`, `positive_rate=0.15` | 3 | +0.0% | +0.0% | 0.0% |
| `positive_rate=0.1`, `normalize=minmax` | 3 | +11.9% | +0.0% | 6.0% |
| `normalize=minmax` | 4 | -14.9% | +0.0% | 7.4% |
| `normalize=minmax`, `lr_schedule=cosine` | 2 | -14.9% | +0.0% | 7.4% |
| `normalize=minmax`, `lr_schedule=step` | 2 | -14.9% | +0.0% | 7.4% |

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
