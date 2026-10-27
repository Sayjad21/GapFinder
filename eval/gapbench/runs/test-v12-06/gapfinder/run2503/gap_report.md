# Gap Report: test-v12-06

Artifact `mlbench` · generated 2026-10-16 01:59 · 167 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -30.3% | +7.6% | ±6.5% | `normalize=zscore` |

## C1: test_accuracy (paper 0.7708)
**Fits but unsupported** · gap -30.3% → +7.6% · 65 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0006`, `B0023`, `B0024`, `B0025`, `B0026`, `B0027` (6 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Command:

  Replay: fork checkpoint `374eb311-fbec-4b58-a47b-ae49d78b663f` and run
  ```
  RUN_TAG=d40e9ffbeef7 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.8292, 0.8292, 0.8292, 0.825, 0.8292, 0.8292; gap after +7.6%; result checkpoint `a50a769d-c9f9-4e2d-b743-a07e837e74c1`
- Effect: candidate 0.8292 minus naive 0.5375 = +0.2917, 95% bootstrap interval [+0.2734, +0.3558] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.771 test accuracy and 0.745 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7708 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5625, 0.475, 0.4667, 0.5458, 0.5375
- Spread: range 0.4667 to 0.5625, noise band ±0.05 (2 x MAD), CV 8.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -30.3% (noise band ±6.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -30.3% (it comes back)
- PASS · Held-out claim: C2: -27.2% to +8.8% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2917 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `SCALES[0]`, `SCALES[1]`, `SCALES[2]`, `SCALES[3]`, `SCALES[4]`, `SCALES[5]`, `SCALES[6]`, `SCALES[7]`, `WEIGHTS[0]`, `WEIGHTS[1]`, `WEIGHTS[2]`, `WEIGHTS[3]`, `WEIGHTS[4]`, `WEIGHTS[5]`, `WEIGHTS[6]`, `WEIGHTS[7]`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (1.33 noise units, gap -21.6%); `normalize=minmax` (1.17 noise units, gap -22.7%)
- Near alternatives (closest across all claims):
  - `normalize=zscore`, `positive_rate=0.2`: this claim +3.2%, mean |gap| 1.7% (5 runs)
  - `normalize=zscore`, `positive_rate=0.5`: this claim +1.6%, mean |gap| 3.4% (5 runs)
  - `normalize=zscore`, `positive_rate=0.15`: this claim +1.1%, mean |gap| 4.9% (5 runs)

### Equally good configurations
The target claim can't tell these 6 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `normalize=zscore` (reported)
- `normalize=zscore, positive_rate=0.15`
- `lr_schedule=cosine, positive_rate=0.1`
- `normalize=zscore, positive_rate=0.5`
- `normalize=zscore, positive_rate=0.2`
- `normalize=zscore, positive_rate=0.06`

### History matching (every measured configuration, all claims together)
- 16 of 62 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `normalize, positive_rate`: normalize=zscore, positive_rate=0.2 (max I 0.52); normalize=zscore, positive_rate=0.5 (max I 0.82); normalize=zscore, positive_rate=0.4 (max I 1.23); normalize=zscore, positive_rate=0.65 (max I 1.35); +1 more
  - `normalize, weight_decay`: normalize=zscore, weight_decay=1e-3 (max I 1.29); normalize=zscore, weight_decay=1e-4 (max I 1.36)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.36); lr_schedule=step, normalize=zscore (max I 1.36)
  - `normalize`: normalize=zscore (max I 1.37)
- 3 separate islands (no single-knob move joins them): normalize=zscore, positive_rate=0.2; normalize=zscore, positive_rate=0.5; normalize=zscore, positive_rate=0.4 | lr_schedule=cosine, positive_rate=0.2; lr_schedule=cosine, positive_rate=0.93; lr_schedule=cosine, positive_rate=0.65 | lr_schedule=cosine, weight_decay=1e-3

Notes:
- positive_rate dropped: with repeats, {'normalize': 'zscore', 'positive_rate': '0.5'} fits {'normalize': 'zscore'}'s gap by less than one noise band, so it is not needed
- configurations the target claim can't tell apart from the answer: normalize=zscore; normalize=zscore, positive_rate=0.15; lr_schedule=cosine, positive_rate=0.1; normalize=zscore, positive_rate=0.5; normalize=zscore, positive_rate=0.2; normalize=zscore, positive_rate=0.06

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore`, `positive_rate=0.2` | 5 | +3.2% | -0.2% | 1.7% |
| `normalize=zscore`, `positive_rate=0.5` | 5 | +1.6% | +5.2% | 3.4% |
| `normalize=zscore`, `positive_rate=0.15` | 5 | +1.1% | -8.7% | 4.9% |
| `normalize=zscore`, `positive_rate=0.4` | 5 | +4.9% | +7.9% | 6.4% |
| `normalize=zscore`, `weight_decay=1e-3` | 5 | +7.0% | +8.3% | 7.7% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `SCALES[0]`, `SCALES[1]`, `SCALES[2]`, `SCALES[3]`, `SCALES[4]`, `SCALES[5]`, `SCALES[6]`, `SCALES[7]`, `WEIGHTS[0]`, `WEIGHTS[1]`, `WEIGHTS[2]`, `WEIGHTS[3]`, `WEIGHTS[4]`, `WEIGHTS[5]`, `WEIGHTS[6]`, `WEIGHTS[7]`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
