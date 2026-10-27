# Gap Report: test-v12-01

Artifact `mlbench` · generated 2026-10-15 19:02 · 197 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -31.4% | +0.8% | ±4.7% | `normalize=zscore`, `n=2400` |

## C1: test_accuracy (paper 0.705)
**Fits but unsupported** · gap -31.4% → +0.8% · 61 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0097`, `B0102`, `B0139`, `B0140`, `B0141` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Config: `n` naive `1200`, changed to `2400`
- Command:

  Replay: fork checkpoint `7b872bea-caf0-4303-a77e-572e22d15d92` and run
  ```
  RUN_TAG=4708ebf61024 "${PYTHON:-python3}" train.py --n 2400 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7104, 0.7146, 0.7167, 0.7104, 0.7104; gap after +0.8%; result checkpoint `e9ddc902-9817-4e4e-a277-cc32e7d217fd`
- Effect: candidate 0.7104 minus naive 0.4833 = +0.2271, 95% bootstrap interval [+0.175, +0.2429] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.705 test accuracy.

- p. 1; value used: `test_accuracy` = 0.705 (headline claim)

### What did we measure?
- Naive median 0.4833 over 5 runs; repeats: 0.4667, 0.475, 0.5375, 0.5375, 0.4833
- Spread: range 0.4667 to 0.5375, noise band ±0.0332 (2 x MAD), CV 6.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -31.4% (noise band ±4.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -37.9% (it comes back)
- PASS · Counterfactual (reversal test): without `n` the gap is +17.3% (it comes back)
- PASS · Held-out claim: C2: -23.5% to +11.1% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- FAIL · Evidence: `n=2400`: no evidence mentions '2400'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2271 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `python_version`, `hardware`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `n=120` (5.52 noise units, gap -5.4%); `lr_schedule=cosine` (4.89 noise units, gap -8.4%); `normalize=minmax` (3.39 noise units, gap -15.5%); `n=240` (3.01 noise units, gap -17.3%); `lr_schedule=step` (2.51 noise units, gap -19.6%) (and 2 more in the JSON)
- Near alternatives (closest across all claims):
  - `normalize=minmax`, `n=6000`: this claim +0.0%, mean |gap| 0.2% (5 runs)
  - `n=12000`, `lr_schedule=cosine`: this claim -5.4%, mean |gap| 4.3% (5 runs)
  - `n=12000`, `normalize=minmax`: this claim +4.2%, mean |gap| 6.2% (5 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `n=2400, normalize=zscore` (reported)
- `n=6000, normalize=minmax`
- `n=240, normalize=zscore`

### History matching (every measured configuration, all claims together)
- 23 of 58 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `n, normalize`: n=6000, normalize=minmax (max I 0.07); n=12000, normalize=minmax (max I 1.19); n=2400, normalize=zscore (max I 1.77); n=600, normalize=zscore (max I 1.84); +1 more
  - `lr_schedule, n`: lr_schedule=cosine, n=12000 (max I 0.86); lr_schedule=cosine, n=120 (max I 1.31); lr_schedule=cosine, n=2000 (max I 2.26)
  - `lr_schedule`: lr_schedule=cosine (max I 1.77)
  - `class_weight, n`: class_weight=balanced, n=120 (max I 2.19)
- 3 separate islands (no single-knob move joins them): n=6000, normalize=minmax; n=12000, normalize=minmax; n=2400, normalize=zscore | lr_schedule=cosine, n=12000; lr_schedule=cosine, n=120; lr_schedule=cosine | class_weight=balanced, n=120; class_weight=balanced, n=12000
- Equally good values: `n` in {240, 600, 2400}

Notes:
- configurations the target claim can't tell apart from the answer: n=2400, normalize=zscore; n=6000, normalize=minmax; n=240, normalize=zscore
- equally good values within one noise band (measured): n in {240, 600, 2400}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax`, `n=6000` | 5 | +0.0% | -0.3% | 0.2% |
| `n=12000`, `lr_schedule=cosine` | 5 | -5.4% | +3.3% | 4.3% |
| `normalize=zscore`, `n=2400` | 5 | +0.8% | +11.1% | 6.0% |
| `n=12000`, `normalize=minmax` | 5 | +4.2% | +8.2% | 6.2% |
| `n=120` | 6 | -11.3% | -1.6% | 6.5% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `n=1`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `python_version`, `hardware`, `--out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
