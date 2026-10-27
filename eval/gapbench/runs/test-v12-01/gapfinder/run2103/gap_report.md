# Gap Report: test-v12-01

Artifact `mlbench` · generated 2026-10-15 21:07 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -29.1% | -0.5% | ±9.4% | `n=6000`, `normalize=minmax` |

## C1: test_accuracy (paper 0.705)
**Fits but unsupported** · gap -29.1% → -0.5% · 61 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0092`, `B0124`, `B0165`, `B0166`, `B0167` (5 run(s) of the same config)
- Config: `n` naive `1200`, changed to `6000`
- Config: `normalize` naive `none`, changed to `minmax`
- Command:

  Replay: fork checkpoint `9dcf4626-25e6-4c34-93ab-bdcf08ec9044` and run
  ```
  RUN_TAG=627c52a83788 "${PYTHON:-python3}" train.py --n 6000 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7008, 0.6883, 0.7075, 0.7017, 0.7075; gap after -0.5%; result checkpoint `3505da59-bb47-4e49-b251-f272f7f0b595`
- Effect: candidate 0.7017 minus naive 0.5 = +0.2017, 95% bootstrap interval [+0.1473, +0.227] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.705 test accuracy.

- p. 1; value used: `test_accuracy` = 0.705 (headline claim)

### What did we measure?
- Naive median 0.5 over 5 runs; repeats: 0.5, 0.4917, 0.4667, 0.55, 0.5542
- Spread: range 0.4667 to 0.5542, noise band ±0.0666 (2 x MAD), CV 7.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -29.1% (noise band ±9.4% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `n` the gap is -15.5% (it comes back)
- PASS · Counterfactual (reversal test): without `normalize` the gap is -19.1% (it comes back)
- PASS · Held-out claim: C2: -20.7% to -1.1% (not worse beyond noise)
- FAIL · Evidence: `n=6000`: no evidence mentions '6000'; it fits, but nothing says the authors used it
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2017 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `env_python_version`, `env_os`, `env_cpu_arch`, `env_memory_gb`, `env_storage_type`, `env_python_random_module`, `env_math_module`, `env_json_module`, `env_os_module`, `env_argparse_module`, `env_random_seed_shuffling`, `env_run_tag_seed_source`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `n=120` (2.5 noise units, gap -5.4%); `lr_schedule=cosine` (1.94 noise units, gap -10.8%); `n=24` (1.65 noise units, gap +13.5%); `normalize=zscore` (1.21 noise units, gap +17.6%); `n=10000` (1.07 noise units, gap -18.9%)
- Near alternatives (closest across all claims):
  - `n=12000`, `lr_schedule=cosine`: this claim -5.3%, mean |gap| 4.3% (5 runs)
  - `normalize=zscore`, `n=500`: this claim -5.0%, mean |gap| 4.7% (5 runs)
  - `lr_schedule=cosine`, `n=10000`: this claim -5.3%, mean |gap| 4.9% (5 runs)

### History matching (every measured configuration, all claims together)
- 34 of 58 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `n, normalize`: n=6000, normalize=minmax (max I 0.16); n=500, normalize=zscore (max I 0.81); n=10000, normalize=minmax (max I 1.08); n=12000, normalize=minmax (max I 1.11); +2 more
  - `lr_schedule, n`: lr_schedule=cosine, n=12000 (max I 0.84); lr_schedule=cosine, n=10000 (max I 0.89); lr_schedule=step, n=12000 (max I 1.46); lr_schedule=cosine, n=6000 (max I 1.6)
- 2 separate islands (no single-knob move joins them): n=6000, normalize=minmax; n=500, normalize=zscore; lr_schedule=cosine, n=12000 | class_weight=balanced, n=10000; class_weight=balanced, n=6000; class_weight=balanced, n=12000

Notes:
- stopped early: run budget of 200 reached (wanted 3 more run(s) of {'n': '12000', 'normalize': 'zscore'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `n=6000`, `normalize=minmax` | 5 | -0.5% | -1.1% | 0.8% |
| `n=12000`, `lr_schedule=cosine` | 5 | -5.3% | +3.3% | 4.3% |
| `normalize=zscore`, `n=500` | 5 | -5.0% | +4.4% | 4.7% |
| `lr_schedule=cosine`, `n=10000` | 5 | -5.3% | +4.6% | 4.9% |
| `n=12000`, `lr_schedule=step` | 2 | -9.9% | -0.0% | 5.0% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `n=1`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `env_python_version`, `env_os`, `env_cpu_arch`, `env_memory_gb`, `env_storage_type`, `env_python_random_module`, `env_math_module`, `env_json_module`, `env_os_module`, `env_argparse_module`, `env_random_seed_shuffling`, `env_run_tag_seed_source`, `--out`

## Provenance
- GapFinder commit: `cd8c8af2b9d079dd9a57443ed501c0dd8a467d34` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
