# Gap Report: test-v12-01

Artifact `mlbench` · generated 2026-10-15 19:02 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -22.6% | +0.8% | ±4.7% | `normalize=zscore`, `n=2400` |

## C1: test_accuracy (paper 0.705)
**Fits but unsupported** · gap -22.6% → +0.8% · 61 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0102`, `B0125`, `B0165`, `B0166`, `B0167` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Config: `n` naive `1200`, changed to `2400`
- Command:

  Replay: fork checkpoint `b3e93d2e-07ea-4373-9bde-16e15da3c180` and run
  ```
  RUN_TAG=022096d82f9b "${PYTHON:-python3}" train.py --n 2400 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7104, 0.7104, 0.7125, 0.7083, 0.7104; gap after +0.8%; result checkpoint `31bd8a03-e4ac-452d-93ee-30808f8e0cfe`
- Effect: candidate 0.7104 minus naive 0.5458 = +0.1646, 95% bootstrap interval [+0.1475, +0.2379] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.705 test accuracy.

- p. 1; value used: `test_accuracy` = 0.705 (headline claim)

### What did we measure?
- Naive median 0.5458 over 5 runs; repeats: 0.4792, 0.5458, 0.5625, 0.4667, 0.5625
- Spread: range 0.4667 to 0.5625, noise band ±0.0334 (2 x MAD), CV 8.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -22.6% (noise band ±4.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -19.9% (it comes back)
- PASS · Counterfactual (reversal test): without `n` the gap is +17.0% (it comes back)
- PASS · Held-out claim: C2: -12.5% to +11.1% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- FAIL · Evidence: `n=2400`: no evidence mentions '2400'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.1646 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `env_python_version`, `env_os`, `env_cpu_arch`, `env_memory_gb`, `env_storage_type`, `env_python_random_module`, `env_math_module`, `env_json_module`, `env_os_module`, `env_argparse_module`, `env_random_seed_shuffling`, `env_run_tag_seed_source`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (2.25 noise units, gap -11.9%); `n=6000` (1.75 noise units, gap -14.3%); `n=24` (1.62 noise units, gap -14.9%); `normalize=minmax` (1.5 noise units, gap -15.5%); `n=240` (1.12 noise units, gap -17.3%)
- Near alternatives (closest across all claims):
  - `n=6000`, `normalize=minmax`: this claim -0.6%, mean |gap| 1.0% (5 runs)
  - `n=10000`, `normalize=minmax`: this claim +2.1%, mean |gap| 3.5% (5 runs)
  - `n=12000`, `lr_schedule=cosine`: this claim -4.8%, mean |gap| 4.3% (5 runs)

### History matching (every measured configuration, all claims together)
- 36 of 59 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `n, normalize`: n=6000, normalize=minmax (max I 0.13); n=10000, normalize=minmax (max I 0.67); n=500, normalize=zscore (max I 0.75); n=12000, normalize=minmax (max I 1.08); +1 more
  - `lr_schedule, n`: lr_schedule=cosine, n=12000 (max I 0.77); lr_schedule=cosine, n=6000 (max I 1.49); lr_schedule=step, n=6000 (max I 1.84)
  - `lr_schedule`: lr_schedule=cosine (max I 1.7)
  - `class_weight, n`: class_weight=balanced, n=500 (max I 1.79)
- 2 separate islands (no single-knob move joins them): n=6000, normalize=minmax; n=10000, normalize=minmax; n=500, normalize=zscore | class_weight=balanced, n=500; class_weight=balanced, n=6000; class_weight=balanced, n=240

Notes:
- stopped early: run budget of 200 reached (wanted 3 more run(s) of {'lr_schedule': 'cosine', 'n': '6000'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `n=6000`, `normalize=minmax` | 5 | -0.6% | -1.4% | 1.0% |
| `n=10000`, `normalize=minmax` | 5 | +2.1% | +4.9% | 3.5% |
| `n=12000`, `lr_schedule=cosine` | 5 | -4.8% | +3.9% | 4.3% |
| `n=500`, `normalize=zscore` | 5 | -5.0% | +4.4% | 4.7% |
| `n=120`, `lr_schedule=cosine` | 5 | -5.4% | +5.1% | 5.3% |

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
