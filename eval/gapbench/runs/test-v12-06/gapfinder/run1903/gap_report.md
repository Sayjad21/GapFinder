# Gap Report: test-v12-06

Artifact `mlbench` · generated 2026-10-15 19:52 · 135 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -30.8% | +1.6% | ±11.9% | `normalize=minmax`, `positive_rate=0.5` |

## C1: test_accuracy (paper 0.7708)
**Fits but unsupported** · gap -30.8% → +1.6% · 59 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0053`, `B0073`, `B0098`, `B0099`, `B0100` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `positive_rate` naive `0.3`, changed to `0.5`
- Command:

  Replay: fork checkpoint `bd2ca7c0-694b-4bcb-bfbd-02fd095e6b74` and run
  ```
  RUN_TAG=016b13d28f68 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.5 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.8, 0.7833, 0.7917, 0.7792, 0.775; gap after +1.6%; result checkpoint `1e91f4b9-b1c0-4f4b-a796-743b35747b33`
- Effect: candidate 0.7833 minus naive 0.5333 = +0.25, 95% bootstrap interval [+0.2267, +0.2908] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.771 test accuracy and 0.745 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7708 (headline claim)

### What did we measure?
- Naive median 0.5333 over 5 runs; repeats: 0.5375, 0.5333, 0.4875, 0.5833, 0.4875
- Spread: range 0.4875 to 0.5833, noise band ±0.0916 (2 x MAD), CV 7.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -30.8% (noise band ±11.9% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -32.4% (it comes back)
- PASS · Counterfactual (reversal test): without `positive_rate` the gap is -22.7% (it comes back)
- PASS · Held-out claim: C2: -27.7% to +5.2% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- FAIL · Evidence: `positive_rate=0.5`: no evidence mentions '0.5'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.25 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `SCALES[0]`, `SCALES[1]`, `SCALES[2]`, `SCALES[3]`, `SCALES[4]`, `SCALES[5]`, `SCALES[6]`, `SCALES[7]`, `WEIGHTS[0]`, `WEIGHTS[1]`, `WEIGHTS[2]`, `WEIGHTS[3]`, `WEIGHTS[4]`, `WEIGHTS[5]`, `WEIGHTS[6]`, `WEIGHTS[7]`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (1.96 noise units, gap +7.6%)
- Near alternatives (closest across all claims):
  - `positive_rate=0.5`, `normalize=zscore`: this claim +1.6%, mean |gap| 3.4% (5 runs)
  - `positive_rate=0.15`, `normalize=zscore`: this claim +1.1%, mean |gap| 4.9% (5 runs)
  - `positive_rate=0.86`, `normalize=zscore`: this claim +5.4%, mean |gap| 5.1% (5 runs)

### Equally good configurations
The target claim can't tell these 5 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `normalize=minmax, positive_rate=0.5` (reported)
- `normalize=zscore, positive_rate=0.15`
- `lr_schedule=cosine, positive_rate=0.1`
- `normalize=minmax, positive_rate=0.1`
- `normalize=zscore, positive_rate=0.5`

### History matching (every measured configuration, all claims together)
- 18 of 57 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `normalize, positive_rate`: normalize=zscore, positive_rate=0.5 (max I 0.88); normalize=zscore, positive_rate=0.86 (max I 0.9); normalize=minmax, positive_rate=0.5 (max I 0.91); normalize=zscore, positive_rate=0.65 (max I 1.41); +1 more
  - `normalize, weight_decay`: normalize=zscore, weight_decay=1e-4 (max I 1.37); normalize=zscore, weight_decay=1e-3 (max I 1.4)
  - `normalize`: normalize=zscore (max I 1.43)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.43); lr_schedule=step, normalize=zscore (max I 1.43)
- Equally good values: `normalize` in {minmax, zscore}; `positive_rate` in {0.1, 0.15, 0.5, 0.93}

Notes:
- configurations the target claim can't tell apart from the answer: normalize=minmax, positive_rate=0.5; normalize=zscore, positive_rate=0.15; lr_schedule=cosine, positive_rate=0.1; normalize=minmax, positive_rate=0.1; normalize=zscore, positive_rate=0.5
- equally good values within one noise band (measured): normalize in {minmax, zscore}; positive_rate in {0.1, 0.15, 0.5, 0.93}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `positive_rate=0.5`, `normalize=zscore` | 5 | +1.6% | +5.2% | 3.4% |
| `positive_rate=0.5`, `normalize=minmax` | 5 | +1.6% | +5.2% | 3.4% |
| `positive_rate=0.15`, `normalize=zscore` | 5 | +1.1% | -8.7% | 4.9% |
| `positive_rate=0.86`, `normalize=zscore` | 5 | +5.4% | -4.9% | 5.1% |
| `weight_decay=1e-4`, `normalize=zscore` | 5 | +7.0% | +8.3% | 7.7% |

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
