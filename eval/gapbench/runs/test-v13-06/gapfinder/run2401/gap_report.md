# Gap Report: test-v13-06

Artifact `mlbench` · generated 2026-10-16 01:36 · 162 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -28.9% | +0.0% | ±2.2% | `normalize=zscore`, `n=12000` |

## C1: test_accuracy (paper 0.7558)
**Fits but unsupported** · gap -28.9% → +0.0% · 53 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0068`, `B0087`, `B0115`, `B0116`, `B0117` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Config: `n` naive `1200`, changed to `12000`
- Command:

  Replay: fork checkpoint `39871cee-5509-400c-b560-ac20e3f31460` and run
  ```
  RUN_TAG=62194eb1e4df "${PYTHON:-python3}" train.py --n 12000 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7575, 0.7558, 0.7554, 0.755, 0.7575; gap after +0.0%; result checkpoint `53aa8610-d916-40a8-8db5-2340feea946d`
- Effect: candidate 0.7558 minus naive 0.5375 = +0.2183, 95% bootstrap interval [+0.1967, +0.2754] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.756 test accuracy and 0.728 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7558 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5458, 0.5375, 0.5375, 0.4667, 0.5625
- Spread: range 0.4667 to 0.5625, noise band ±0.0166 (2 x MAD), CV 6.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -28.9% (noise band ±2.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -27.2% (it comes back)
- PASS · Counterfactual (reversal test): without `n` the gap is +9.2% (it comes back)
- PASS · Held-out claim: C2: -25.5% to +0.0% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- FAIL · Evidence: `n=12000`: no evidence mentions '12000'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2183 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (5.77 noise units, gap -16.2%); `normalize=minmax` (3.51 noise units, gap -21.2%); `n=120` (2.76 noise units, gap -22.8%); `n=10000` (2.11 noise units, gap -24.3%); `n=500` (1.96 noise units, gap -24.6%) (and 2 more in the JSON)
- Near alternatives (closest across all claims):
  - `n=10000`, `normalize=zscore`: this claim -0.7%, mean |gap| 0.4% (5 runs)
  - `n=600`, `normalize=zscore`: this claim -1.9%, mean |gap| 2.8% (5 runs)
  - `normalize=minmax`, `class_weight=balanced`: this claim +1.4%, mean |gap| 4.1% (5 runs)

### Equally good configurations
The target claim can't tell these 4 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `n=12000, normalize=zscore` (reported)
- `n=10000, normalize=zscore`
- `class_weight=balanced, normalize=minmax`
- `n=600, normalize=zscore`

### History matching (every measured configuration, all claims together)
- 16 of 52 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `n, normalize`: n=12000, normalize=zscore (max I 0.02); n=10000, normalize=zscore (max I 0.13); n=600, normalize=zscore (max I 0.61); n=120, normalize=zscore (max I 0.88); +3 more
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 1.14); class_weight=balanced, normalize=zscore (max I 1.33)
  - `normalize`: normalize=zscore (max I 1.8)
- Equally good values: `n` in {600, 10000, 12000}

Notes:
- configurations the target claim can't tell apart from the answer: n=12000, normalize=zscore; n=10000, normalize=zscore; class_weight=balanced, normalize=minmax; n=600, normalize=zscore
- equally good values within one noise band (measured): n in {600, 10000, 12000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore`, `n=12000` | 5 | +0.0% | +0.0% | 0.0% |
| `n=10000`, `normalize=zscore` | 5 | -0.7% | -0.2% | 0.4% |
| `n=600`, `normalize=zscore` | 5 | -1.9% | -3.8% | 2.8% |
| `normalize=minmax`, `class_weight=balanced` | 5 | +1.4% | +6.8% | 4.1% |
| `normalize=zscore`, `n=120` | 5 | -6.3% | -2.5% | 4.4% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `n=1`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
