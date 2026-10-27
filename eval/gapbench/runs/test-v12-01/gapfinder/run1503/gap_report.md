# Gap Report: test-v12-01

Artifact `mlbench` · generated 2026-10-15 19:25 · 150 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -22.6% | +1.1% | ±1.2% | `normalize=zscore`, `n=2400` |

## C1: test_accuracy (paper 0.705)
**Fits but unsupported** · gap -22.6% → +1.1% · 58 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0074`, `B0100`, `B0134` (3 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Config: `n` naive `1200`, changed to `2400`
- Command:

  Replay: fork checkpoint `3d102f75-b60b-488a-bd70-9bf0b2607b18` and run
  ```
  RUN_TAG=56482eb5d486 "${PYTHON:-python3}" train.py --n 2400 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7104, 0.7125, 0.7125; gap after +1.1%; result checkpoint `44efc174-54d7-4377-8c67-21d992543724`
- Effect: candidate 0.7125 minus naive 0.5458 = +0.1667, 95% bootstrap interval [+0.1626, +0.2133] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.705 test accuracy.

- p. 1; value used: `test_accuracy` = 0.705 (headline claim)

### What did we measure?
- Naive median 0.5458 over 5 runs; repeats: 0.55, 0.5375, 0.5458, 0.4875, 0.5458
- Spread: range 0.4875 to 0.55, noise band ±0.0084 (2 x MAD), CV 4.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -22.6% (noise band ±1.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -20.1% (it comes back)
- PASS · Counterfactual (reversal test): without `n` the gap is +17.6% (it comes back)
- PASS · Held-out claim: C2: -12.7% to +11.5% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- FAIL · Evidence: `n=2400`: no evidence mentions '2400'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.1667 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `env_python_version`, `env_os`, `env_cpu_arch`, `env_memory_gb`, `env_storage_type`, `env_python_random_module`, `env_math_module`, `env_json_module`, `env_os_module`, `env_argparse_module`, `env_random_seed_shuffling`, `env_run_tag_seed_source`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (11.9 noise units, gap -8.4%); `normalize=minmax` (5.95 noise units, gap -15.5%); `n=120` (4.46 noise units, gap -17.3%); `n=500` (2.88 noise units, gap -19.1%); `n=600` (2.49 noise units, gap -19.6%)
- Near alternatives (closest across all claims):
  - `normalize=minmax`, `n=10000`: this claim +1.9%, mean |gap| 2.8% (3 runs)
  - `normalize=minmax`, `lr_schedule=cosine`, `n=10000`: this claim -2.7%, mean |gap| 4.2% (3 runs)
  - `lr_schedule=cosine`, `n=12000`: this claim -5.6%, mean |gap| 4.4% (3 runs)

### Equally good configurations
The target claim can't tell these 4 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `n=2400, normalize=zscore` (reported)
- `n=10000, normalize=minmax`
- `lr_schedule=cosine, n=120`
- `lr_schedule=cosine, n=10000, normalize=minmax`

### History matching (every measured configuration, all claims together)
- 23 of 56 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `n, normalize`: n=10000, normalize=minmax (max I 0.66); n=500, normalize=zscore (max I 0.82); n=12000, normalize=minmax (max I 1.4); n=2400, normalize=zscore (max I 1.86); +1 more
  - `lr_schedule, n, normalize`: lr_schedule=cosine, n=10000, normalize=minmax (max I 0.89)
  - `lr_schedule, n`: lr_schedule=cosine, n=10000 (max I 0.9); lr_schedule=cosine, n=12000 (max I 0.94); lr_schedule=cosine, n=120 (max I 1.3)
  - `lr_schedule`: lr_schedule=cosine (max I 1.97)
- 2 separate islands (no single-knob move joins them): n=10000, normalize=minmax; n=500, normalize=zscore; lr_schedule=cosine, n=10000, normalize=minmax | class_weight=balanced, n=10000

Notes:
- configurations the target claim can't tell apart from the answer: n=2400, normalize=zscore; n=10000, normalize=minmax; lr_schedule=cosine, n=120; lr_schedule=cosine, n=10000, normalize=minmax

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax`, `n=10000` | 3 | +1.9% | +3.6% | 2.8% |
| `normalize=minmax`, `lr_schedule=cosine`, `n=10000` | 3 | -2.7% | -5.6% | 4.2% |
| `lr_schedule=cosine`, `n=12000` | 3 | -5.6% | +3.2% | 4.4% |
| `normalize=zscore`, `n=500` | 3 | -5.0% | +4.4% | 4.7% |
| `lr_schedule=cosine`, `n=10000` | 3 | -5.0% | +4.7% | 4.8% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `n=1`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `env_python_version`, `env_os`, `env_cpu_arch`, `env_memory_gb`, `env_storage_type`, `env_python_random_module`, `env_math_module`, `env_json_module`, `env_os_module`, `env_argparse_module`, `env_random_seed_shuffling`, `env_run_tag_seed_source`, `--out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
