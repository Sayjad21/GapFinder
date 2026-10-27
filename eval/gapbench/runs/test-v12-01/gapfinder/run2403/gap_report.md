# Gap Report: test-v12-01

Artifact `mlbench` · generated 2026-10-16 01:28 · 199 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -23.8% | +0.2% | ±0.8% | `n=6000`, `normalize=minmax` |

## C1: test_accuracy (paper 0.705)
**Fits but unsupported** · gap -23.8% → +0.2% · 61 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0117`, `B0124`, `B0161`, `B0162`, `B0163` (5 run(s) of the same config)
- Config: `n` naive `1200`, changed to `6000`
- Config: `normalize` naive `none`, changed to `minmax`
- Command:

  Replay: fork checkpoint `f0114ad1-6351-4043-b0a1-0376bc9557eb` and run
  ```
  RUN_TAG=a1db0e34ec1f "${PYTHON:-python3}" train.py --n 6000 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7017, 0.7217, 0.6917, 0.7117, 0.7067; gap after +0.2%; result checkpoint `446c9c1b-1de2-478e-9d74-e4456985bbe7`
- Effect: candidate 0.7067 minus naive 0.5375 = +0.1692, 95% bootstrap interval [+0.1612, +0.2222] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.705 test accuracy.

- p. 1; value used: `test_accuracy` = 0.705 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5375, 0.4875, 0.5375, 0.5375, 0.4875
- Spread: range 0.4875 to 0.5375, noise band ±0.005375 (2 x MAD), CV 5.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -23.8% (noise band ±0.8% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `n` the gap is -15.5% (it comes back)
- PASS · Counterfactual (reversal test): without `normalize` the gap is -38.4% (it comes back)
- PASS · Held-out claim: C2: -13.3% to +0.2% (not worse beyond noise)
- FAIL · Evidence: `n=6000`: no evidence mentions '6000'; it fits, but nothing says the authors used it
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.1692 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `env_python_version`, `env_os`, `env_cpu_arch`, `env_memory_gb`, `env_storage_type`, `env_python_random_module`, `env_math_module`, `env_json_module`, `env_os_module`, `env_argparse_module`, `env_random_seed_shuffling`, `env_run_tag_seed_source`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `n=120` (16.28 noise units, gap -11.3%); `lr_schedule=cosine` (15.5 noise units, gap -11.9%); `n=10000` (11.63 noise units, gap -14.9%); `normalize=zscore` (8.06 noise units, gap +17.6%); `n=2400` (6.98 noise units, gap -18.4%) (and 3 more in the JSON)
- Near alternatives (closest across all claims):
  - `n=10000`, `normalize=minmax`: this claim +2.1%, mean |gap| 3.5% (5 runs)
  - `n=12000`, `lr_schedule=cosine`: this claim -5.4%, mean |gap| 4.3% (5 runs)
  - `normalize=zscore`, `n=500`: this claim -5.0%, mean |gap| 4.7% (5 runs)

### History matching (every measured configuration, all claims together)
- 22 of 58 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `n, normalize`: n=6000, normalize=minmax (max I 0.07); n=10000, normalize=minmax (max I 0.83); n=500, normalize=zscore (max I 0.89); n=12000, normalize=minmax (max I 1.35); +2 more
  - `lr_schedule, n`: lr_schedule=cosine, n=12000 (max I 0.94); lr_schedule=cosine, n=120 (max I 0.99); lr_schedule=cosine, n=10000 (max I 0.99)
  - `lr_schedule`: lr_schedule=cosine (max I 2.17)
- 3 separate islands (no single-knob move joins them): n=6000, normalize=minmax; n=10000, normalize=minmax; n=500, normalize=zscore | lr_schedule=cosine, n=12000; lr_schedule=cosine, n=120; lr_schedule=cosine, n=10000 | class_weight=balanced, n=2400

Notes:
- stopped early: run budget of 200 reached (wanted 3 more run(s) of {'normalize': 'minmax', 'class_weight': 'balanced'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `n=6000`, `normalize=minmax` | 5 | +0.2% | +0.2% | 0.2% |
| `n=10000`, `normalize=minmax` | 5 | +2.1% | +5.0% | 3.5% |
| `n=12000`, `lr_schedule=cosine` | 5 | -5.4% | +3.2% | 4.3% |
| `normalize=zscore`, `n=500` | 5 | -5.0% | +4.4% | 4.7% |
| `n=10000`, `lr_schedule=cosine` | 5 | -5.4% | +4.4% | 4.9% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `n=1`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `env_python_version`, `env_os`, `env_cpu_arch`, `env_memory_gb`, `env_storage_type`, `env_python_random_module`, `env_math_module`, `env_json_module`, `env_os_module`, `env_argparse_module`, `env_random_seed_shuffling`, `env_run_tag_seed_source`, `--out`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
