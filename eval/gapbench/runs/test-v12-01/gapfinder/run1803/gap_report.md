# Gap Report: test-v12-01

Artifact `mlbench` · generated 2026-10-15 19:50 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -31.4% | +0.1% | ±4.7% | `normalize=minmax`, `n=6000` |

## C1: test_accuracy (paper 0.705)
**Fits but unsupported** · gap -31.4% → +0.1% · 57 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0083`, `B0124`, `B0162`, `B0163`, `B0164` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `n` naive `1200`, changed to `6000`
- Command:

  Replay: fork checkpoint `40b3453b-ed99-4ce6-9a93-dbd7bb2acfc6` and run
  ```
  RUN_TAG=a66f57c9ee9b "${PYTHON:-python3}" train.py --n 6000 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7058, 0.6967, 0.7075, 0.7025, 0.7067; gap after +0.1%; result checkpoint `dfa89a63-cea4-45ef-b744-15f205c6712a`
- Effect: candidate 0.7058 minus naive 0.4833 = +0.2225, 95% bootstrap interval [+0.1415, +0.2382] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.705 test accuracy.

- p. 1; value used: `test_accuracy` = 0.705 (headline claim)

### What did we measure?
- Naive median 0.4833 over 5 runs; repeats: 0.4833, 0.55, 0.5667, 0.4667, 0.4667
- Spread: range 0.4667 to 0.5667, noise band ±0.0332 (2 x MAD), CV 9.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -31.4% (noise band ±4.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -18.7% (it comes back)
- PASS · Counterfactual (reversal test): without `n` the gap is -15.5% (it comes back)
- PASS · Held-out claim: C2: -23.5% to +0.3% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- FAIL · Evidence: `n=6000`: no evidence mentions '6000'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2225 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `env_python_version`, `env_os`, `env_cpu_arch`, `env_memory_gb`, `env_storage_type`, `env_python_random_module`, `env_math_module`, `env_json_module`, `env_os_module`, `env_argparse_module`, `env_random_seed_shuffling`, `env_run_tag_seed_source`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (3.39 noise units, gap -15.5%); `normalize=zscore` (3.06 noise units, gap +17.0%); `n=2400` (2.7 noise units, gap -18.7%); `lr_schedule=step` (2.64 noise units, gap -19.0%); `n=12000` (2.32 noise units, gap -20.5%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `normalize=minmax`, `n=10000`: this claim +2.3%, mean |gap| 4.1% (5 runs)
  - `lr_schedule=cosine`, `n=12000`: this claim -5.4%, mean |gap| 4.4% (5 runs)
  - `n=500`, `normalize=zscore`: this claim -5.0%, mean |gap| 4.7% (5 runs)

### History matching (every measured configuration, all claims together)
- 35 of 55 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `n, normalize`: n=6000, normalize=minmax (max I 0.06); n=500, normalize=zscore (max I 0.7); n=10000, normalize=minmax (max I 0.8); n=12000, normalize=minmax (max I 1.04); +2 more
  - `lr_schedule, n`: lr_schedule=cosine, n=12000 (max I 0.79); lr_schedule=cosine, n=10000 (max I 0.85); lr_schedule=step, n=12000 (max I 1.34); lr_schedule=cosine, n=6000 (max I 1.51)
- 3 separate islands (no single-knob move joins them): n=6000, normalize=minmax; n=500, normalize=zscore; lr_schedule=cosine, n=12000 | class_weight=balanced, n=10000; class_weight=balanced, n=12000; class_weight=balanced, n=600 | class_weight=balanced, normalize=zscore

Notes:
- stopped early: run budget of 200 reached (wanted 3 more run(s) of {'n': '12000', 'lr_schedule': 'step'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax`, `n=6000` | 5 | +0.1% | +0.3% | 0.2% |
| `normalize=minmax`, `n=10000` | 5 | +2.3% | +5.9% | 4.1% |
| `lr_schedule=cosine`, `n=12000` | 5 | -5.4% | +3.3% | 4.4% |
| `n=500`, `normalize=zscore` | 5 | -5.0% | +4.4% | 4.7% |
| `lr_schedule=cosine`, `n=10000` | 5 | -5.7% | +4.2% | 4.9% |

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
