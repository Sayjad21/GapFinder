# Gap Report: test-v12-06

Artifact `mlbench` · generated 2026-10-15 19:52 · 194 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -36.2% | +0.5% | ±6.5% | `lr_schedule=cosine`, `positive_rate=0.1` |

## C1: test_accuracy (paper 0.7708)
**Fits but unsupported** · gap -36.2% → +0.5% · 70 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0090`, `B0100`, `B0140`, `B0141`, `B0142` (5 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `cosine`
- Config: `positive_rate` naive `0.3`, changed to `0.1`
- Command:

  Replay: fork checkpoint `64253a35-a25d-4a69-a4b0-6c9a8dde211d` and run
  ```
  RUN_TAG=34063ff1562c "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.1 --label_noise 0.05 --split 0.8 --normalize none --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule cosine --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7417, 0.775, 0.7875, 0.775, 0.7708; gap after +0.5%; result checkpoint `110c8929-2564-419d-9b3a-954f1623fc6f`
- Effect: candidate 0.775 minus naive 0.4917 = +0.2833, 95% bootstrap interval [+0.215, +0.3066] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.771 test accuracy and 0.745 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7708 (headline claim)

### What did we measure?
- Naive median 0.4917 over 5 runs; repeats: 0.5667, 0.4667, 0.5375, 0.4917, 0.4667
- Spread: range 0.4667 to 0.5667, noise band ±0.05 (2 x MAD), CV 8.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -36.2% (noise band ±6.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is -35.1% (it comes back)
- PASS · Counterfactual (reversal test): without `positive_rate` the gap is -20.5% (it comes back)
- PASS · Held-out claim: C2: -34.8% to -19.9% (not worse beyond noise)
- FAIL · Evidence: `lr_schedule=cosine`: no evidence mentions 'cosine'; it fits, but nothing says the authors used it
- FAIL · Evidence: `positive_rate=0.1`: no evidence mentions '0.1'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2833 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `SCALES[0]`, `SCALES[1]`, `SCALES[2]`, `SCALES[3]`, `SCALES[4]`, `SCALES[5]`, `SCALES[6]`, `SCALES[7]`, `WEIGHTS[0]`, `WEIGHTS[1]`, `WEIGHTS[2]`, `WEIGHTS[3]`, `WEIGHTS[4]`, `WEIGHTS[5]`, `WEIGHTS[6]`, `WEIGHTS[7]`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (4.41 noise units, gap +7.6%); `normalize=minmax` (2.08 noise units, gap -22.7%); `positive_rate=0.65` (1.33 noise units, gap -27.6%); `lr_schedule=step` (1 noise units, gap -29.7%)
- Near alternatives (closest across all claims):
  - `normalize=minmax`, `class_weight=balanced`: this claim -0.5%, mean |gap| 2.4% (5 runs)
  - `normalize=zscore`, `positive_rate=0.5`: this claim +1.6%, mean |gap| 3.4% (5 runs)
  - `class_weight=balanced`, `normalize=zscore`: this claim +1.6%, mean |gap| 3.5% (5 runs)

### Equally good configurations
The target claim can't tell these 6 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `lr_schedule=cosine, positive_rate=0.1` (reported)
- `class_weight=balanced, normalize=minmax`
- `normalize=zscore, positive_rate=0.15`
- `class_weight=balanced, normalize=zscore`
- `normalize=zscore, positive_rate=0.5`
- `lr_schedule=cosine, positive_rate=0.03`

### History matching (every measured configuration, all claims together)
- 21 of 67 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 0.65); class_weight=balanced, normalize=zscore (max I 0.8)
  - `normalize, positive_rate`: normalize=zscore, positive_rate=0.5 (max I 0.79); normalize=zscore, positive_rate=0.86 (max I 0.85); normalize=zscore, positive_rate=0.65 (max I 1.3)
  - `normalize, weight_decay`: normalize=zscore, weight_decay=1e-3 (max I 1.29); normalize=zscore, weight_decay=1e-4 (max I 1.3)
  - `normalize`: normalize=zscore (max I 1.31)
  - `lr_schedule, normalize`: lr_schedule=step, normalize=zscore (max I 1.33); lr_schedule=cosine, normalize=zscore (max I 1.34)
- 4 separate islands (no single-knob move joins them): class_weight=balanced, normalize=minmax; normalize=zscore, positive_rate=0.5; class_weight=balanced, normalize=zscore | lr_schedule=cosine, positive_rate=0.93; lr_schedule=cosine, positive_rate=0.65; lr_schedule=cosine, positive_rate=0.86 | lr_schedule=cosine, weight_decay=1e-4; lr_schedule=cosine, weight_decay=1e-3 | class_weight=balanced, lr_schedule=cosine
- Equally good values: `positive_rate` in {0.03, 0.1}

Notes:
- configurations the target claim can't tell apart from the answer: lr_schedule=cosine, positive_rate=0.1; class_weight=balanced, normalize=minmax; normalize=zscore, positive_rate=0.15; class_weight=balanced, normalize=zscore; normalize=zscore, positive_rate=0.5; lr_schedule=cosine, positive_rate=0.03
- equally good values within one noise band (measured): positive_rate in {0.03, 0.1}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax`, `class_weight=balanced` | 5 | -0.5% | +4.2% | 2.4% |
| `normalize=zscore`, `positive_rate=0.5` | 5 | +1.6% | +5.2% | 3.4% |
| `class_weight=balanced`, `normalize=zscore` | 5 | +1.6% | +5.4% | 3.5% |
| `positive_rate=0.15`, `normalize=zscore` | 5 | +1.1% | -8.7% | 4.9% |
| `positive_rate=0.86`, `normalize=zscore` | 5 | +5.4% | -4.9% | 5.1% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `SCALES[0]`, `SCALES[1]`, `SCALES[2]`, `SCALES[3]`, `SCALES[4]`, `SCALES[5]`, `SCALES[6]`, `SCALES[7]`, `WEIGHTS[0]`, `WEIGHTS[1]`, `WEIGHTS[2]`, `WEIGHTS[3]`, `WEIGHTS[4]`, `WEIGHTS[5]`, `WEIGHTS[6]`, `WEIGHTS[7]`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
