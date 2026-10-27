# Gap Report: test-v12-06

Artifact `mlbench` · generated 2026-10-15 21:09 · 192 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -37.8% | +1.1% | ±3.2% | `normalize=zscore`, `positive_rate=0.15` |

## C1: test_accuracy (paper 0.7708)
**Fits but unsupported** · gap -37.8% → +1.1% · 60 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0105`, `B0110`, `B0148`, `B0149`, `B0150` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Config: `positive_rate` naive `0.3`, changed to `0.15`
- Command:

  Replay: fork checkpoint `44aa85ce-efb7-46eb-a96d-3981b2758f34` and run
  ```
  RUN_TAG=be5b57230b39 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.15 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7792, 0.775, 0.7708, 0.7792, 0.7792; gap after +1.1%; result checkpoint `62a11155-147e-40df-8d12-5808aa2f921a`
- Effect: candidate 0.7792 minus naive 0.4792 = +0.3, 95% bootstrap interval [+0.2392, +0.3067] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.771 test accuracy and 0.745 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7708 (headline claim)

### What did we measure?
- Naive median 0.4792 over 5 runs; repeats: 0.4792, 0.5333, 0.4667, 0.475, 0.5375
- Spread: range 0.4667 to 0.5375, noise band ±0.025 (2 x MAD), CV 6.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -37.8% (noise band ±3.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -36.8% (it comes back)
- PASS · Counterfactual (reversal test): without `positive_rate` the gap is +7.6% (it comes back)
- PASS · Held-out claim: C2: -36.4% to -8.7% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- FAIL · Evidence: `positive_rate=0.15`: no evidence mentions '0.15'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.3 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `SCALES[0]`, `SCALES[1]`, `SCALES[2]`, `SCALES[3]`, `SCALES[4]`, `SCALES[5]`, `SCALES[6]`, `SCALES[7]`, `WEIGHTS[0]`, `WEIGHTS[1]`, `WEIGHTS[2]`, `WEIGHTS[3]`, `WEIGHTS[4]`, `WEIGHTS[5]`, `WEIGHTS[6]`, `WEIGHTS[7]`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (5.33 noise units, gap -20.5%); `normalize=minmax` (4.66 noise units, gap -22.7%); `lr_schedule=step` (4.33 noise units, gap -23.8%); `positive_rate=0.65` (3.83 noise units, gap -25.4%); `weight_decay=1e-3` (3 noise units, gap -28.1%) (and 7 more in the JSON)
- Near alternatives (closest across all claims):
  - `positive_rate=0.5`, `normalize=zscore`: this claim +2.2%, mean |gap| 4.0% (5 runs)
  - `positive_rate=0.5`, `normalize=minmax`: this claim +2.2%, mean |gap| 4.0% (5 runs)
  - `positive_rate=0.86`, `normalize=zscore`: this claim +5.4%, mean |gap| 5.1% (5 runs)

### Equally good configurations
The target claim can't tell these 6 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `normalize=zscore, positive_rate=0.15` (reported)
- `normalize=minmax, positive_rate=0.1`
- `normalize=minmax, positive_rate=0.5`
- `lr_schedule=cosine, positive_rate=0.03`
- `normalize=zscore, positive_rate=0.5`
- `lr_schedule=cosine, positive_rate=0.1`

### History matching (every measured configuration, all claims together)
- 13 of 58 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `normalize, positive_rate`: normalize=minmax, positive_rate=0.5 (max I 0.88); normalize=zscore, positive_rate=0.86 (max I 0.94); normalize=zscore, positive_rate=0.5 (max I 0.95); normalize=zscore, positive_rate=0.65 (max I 1.4)
  - `normalize, weight_decay`: normalize=zscore, weight_decay=1e-4 (max I 1.36); normalize=zscore, weight_decay=1e-3 (max I 1.42)
  - `normalize`: normalize=zscore (max I 1.43)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.44); lr_schedule=step, normalize=zscore (max I 1.44)
  - `lr_schedule, normalize, positive_rate`: lr_schedule=cosine, normalize=zscore, positive_rate=0.65 (max I 1.45)
- Equally good values: `positive_rate` in {0.15, 0.5}

Notes:
- configurations the target claim can't tell apart from the answer: normalize=zscore, positive_rate=0.15; normalize=minmax, positive_rate=0.1; normalize=minmax, positive_rate=0.5; lr_schedule=cosine, positive_rate=0.03; normalize=zscore, positive_rate=0.5; lr_schedule=cosine, positive_rate=0.1
- equally good values within one noise band (measured): positive_rate in {0.15, 0.5}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `positive_rate=0.5`, `normalize=zscore` | 5 | +2.2% | +5.8% | 4.0% |
| `positive_rate=0.5`, `normalize=minmax` | 5 | +2.2% | +5.9% | 4.0% |
| `positive_rate=0.15`, `normalize=zscore` | 5 | +1.1% | -8.7% | 4.9% |
| `positive_rate=0.86`, `normalize=zscore` | 5 | +5.4% | -4.9% | 5.1% |
| `positive_rate=0.65`, `normalize=zscore` | 5 | +6.5% | +8.4% | 7.4% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `SCALES[0]`, `SCALES[1]`, `SCALES[2]`, `SCALES[3]`, `SCALES[4]`, `SCALES[5]`, `SCALES[6]`, `SCALES[7]`, `WEIGHTS[0]`, `WEIGHTS[1]`, `WEIGHTS[2]`, `WEIGHTS[3]`, `WEIGHTS[4]`, `WEIGHTS[5]`, `WEIGHTS[6]`, `WEIGHTS[7]`

## Provenance
- GapFinder commit: `cd8c8af2b9d079dd9a57443ed501c0dd8a467d34` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
