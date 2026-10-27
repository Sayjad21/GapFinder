# Gap Report: test-v12-01

Artifact `mlbench` · generated 2026-10-15 19:01 · 128 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -23.8% | +0.8% | ±0.8% | `normalize=zscore`, `n=2400` |

## C1: test_accuracy (paper 0.705)
**Fits but unsupported** · gap -23.8% → +0.8% · 53 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0058`, `B0083`, `B0114` (3 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Config: `n` naive `1200`, changed to `2400`
- Command:

  Replay: fork checkpoint `178be6d3-84f9-4c7f-bf30-715817a7da36` and run
  ```
  RUN_TAG=907965690547 "${PYTHON:-python3}" train.py --n 2400 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7104, 0.7104, 0.7125; gap after +0.8%; result checkpoint `66765efe-89c6-4e35-94f4-723f987af1a7`
- Effect: candidate 0.7104 minus naive 0.5375 = +0.1729, 95% bootstrap interval [+0.1496, +0.175] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.705 test accuracy.

- p. 1; value used: `test_accuracy` = 0.705 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5625, 0.5583, 0.5375, 0.5375, 0.5375
- Spread: range 0.5375 to 0.5625, noise band ±0.005375 (2 x MAD), CV 2.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -23.8% (noise band ±0.8% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -22.4% (it comes back)
- PASS · Counterfactual (reversal test): without `n` the gap is +17.0% (it comes back)
- PASS · Held-out claim: C2: -13.3% to +11.1% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- FAIL · Evidence: `n=2400`: no evidence mentions '2400'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.1729 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `hardware`, `python_version`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (14.73 noise units, gap -12.5%); `normalize=minmax` (10.85 noise units, gap -15.5%); `lr_schedule=step` (6.98 noise units, gap -18.4%); `n=5000` (5.67 noise units, gap -19.4%); `n=240` (4.65 noise units, gap -20.2%) (and 2 more in the JSON)
- Near alternatives (closest across all claims):
  - `n=5000`, `normalize=minmax`: this claim +0.1%, mean |gap| 0.8% (3 runs)
  - `n=12000`, `lr_schedule=cosine`: this claim -5.4%, mean |gap| 4.3% (3 runs)
  - `n=5000`, `lr_schedule=cosine`: this claim -10.5%, mean |gap| 5.4% (3 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `n=2400, normalize=zscore` (reported)
- `n=5000, normalize=minmax`
- `n=240, normalize=zscore`

### History matching (every measured configuration, all claims together)
- 11 of 52 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `n, normalize`: n=5000, normalize=minmax (max I 0.26); n=12000, normalize=minmax (max I 1.77); n=2400, normalize=zscore (max I 2.2); n=240, normalize=zscore (max I 2.78)
  - `lr_schedule, n`: lr_schedule=cosine, n=12000 (max I 1.04); lr_schedule=cosine, n=5000 (max I 2.03); lr_schedule=cosine, n=2400 (max I 2.79); lr_schedule=cosine, n=2000 (max I 2.88)
  - `lr_schedule`: lr_schedule=cosine (max I 2.54)
  - `class_weight, lr_schedule`: class_weight=balanced, lr_schedule=cosine (max I 2.79)
- 2 separate islands (no single-knob move joins them): lr_schedule=cosine, n=12000; lr_schedule=cosine, n=5000; lr_schedule=cosine | n=5000, normalize=minmax; n=12000, normalize=minmax; n=2400, normalize=zscore

Notes:
- configurations the target claim can't tell apart from the answer: n=2400, normalize=zscore; n=5000, normalize=minmax; n=240, normalize=zscore

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `n=5000`, `normalize=minmax` | 3 | +0.1% | +1.5% | 0.8% |
| `n=12000`, `lr_schedule=cosine` | 3 | -5.4% | +3.2% | 4.3% |
| `n=5000`, `lr_schedule=cosine` | 3 | -10.5% | -0.4% | 5.4% |
| `n=2400`, `normalize=zscore` | 3 | +0.8% | +11.1% | 6.0% |
| `n=12000`, `normalize=minmax` | 3 | +4.8% | +9.7% | 7.2% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `n=1`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `hardware`, `python_version`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
