# Gap Report: test-v12-01

Artifact `mlbench` · generated 2026-10-16 01:57 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -24.4% | +0.2% | ±1.2% | `n=6000`, `normalize=minmax` |

## C1: test_accuracy (paper 0.705)
**Fits but unsupported** · gap -24.4% → +0.2% · 61 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0106`, `B0129`, `B0168`, `B0169`, `B0170` (5 run(s) of the same config)
- Config: `n` naive `1200`, changed to `6000`
- Config: `normalize` naive `none`, changed to `minmax`
- Command:

  Replay: fork checkpoint `bcf38d94-a145-47a5-8ce4-92d153ccdde2` and run
  ```
  RUN_TAG=10f5558ea061 "${PYTHON:-python3}" train.py --n 6000 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7067, 0.7075, 0.705, 0.7117, 0.7067; gap after +0.2%; result checkpoint `465ffeb2-87bf-41ae-8c10-a62bb306d9f2`
- Effect: candidate 0.7067 minus naive 0.5333 = +0.1734, 95% bootstrap interval [+0.1702, +0.2285] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.705 test accuracy.

- p. 1; value used: `test_accuracy` = 0.705 (headline claim)

### What did we measure?
- Naive median 0.5333 over 5 runs; repeats: 0.475, 0.5333, 0.4875, 0.5333, 0.5375
- Spread: range 0.475 to 0.5375, noise band ±0.0084 (2 x MAD), CV 5.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -24.4% (noise band ±1.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `n` the gap is -15.5% (it comes back)
- PASS · Counterfactual (reversal test): without `normalize` the gap is -23.8% (it comes back)
- PASS · Held-out claim: C2: -13.9% to +0.7% (not worse beyond noise)
- FAIL · Evidence: `n=6000`: no evidence mentions '6000'; it fits, but nothing says the authors used it
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.1734 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `env_python_version`, `env_os`, `env_cpu_arch`, `env_memory_gb`, `env_storage_type`, `env_python_random_module`, `env_math_module`, `env_json_module`, `env_os_module`, `env_argparse_module`, `env_random_seed_shuffling`, `env_run_tag_seed_source`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (11.42 noise units, gap -10.8%); `n=10000` (6.39 noise units, gap -16.7%); `normalize=zscore` (5.65 noise units, gap +17.6%); `n=240` (3.48 noise units, gap -20.2%); `n=600` (2.98 noise units, gap -20.8%) (and 3 more in the JSON)
- Near alternatives (closest across all claims):
  - `normalize=minmax`, `n=10000`: this claim +2.1%, mean |gap| 3.2% (5 runs)
  - `n=12000`, `lr_schedule=cosine`: this claim -4.8%, mean |gap| 4.3% (5 runs)
  - `n=500`, `normalize=zscore`: this claim -5.0%, mean |gap| 4.7% (5 runs)

### History matching (every measured configuration, all claims together)
- 29 of 58 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `n, normalize`: n=6000, normalize=minmax (max I 0.13); n=10000, normalize=minmax (max I 0.77); n=500, normalize=zscore (max I 0.87); n=12000, normalize=minmax (max I 1.3); +2 more
  - `lr_schedule, n`: lr_schedule=cosine, n=12000 (max I 0.86); lr_schedule=cosine, n=10000 (max I 0.98); lr_schedule=cosine, n=6000 (max I 1.89); lr_schedule=step, n=10000 (max I 1.92)
- 3 separate islands (no single-knob move joins them): n=6000, normalize=minmax; n=10000, normalize=minmax; n=500, normalize=zscore | lr_schedule=cosine, n=12000; lr_schedule=cosine, n=10000; lr_schedule=cosine, n=6000 | class_weight=balanced, n=10000; class_weight=balanced, n=6000

Notes:
- stopped early: run budget of 200 reached (wanted 3 more run(s) of {'normalize': 'zscore', 'n': '10000'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `n=6000`, `normalize=minmax` | 5 | +0.2% | +0.7% | 0.5% |
| `normalize=minmax`, `n=10000` | 5 | +2.1% | +4.3% | 3.2% |
| `n=12000`, `lr_schedule=cosine` | 5 | -4.8% | +3.9% | 4.3% |
| `n=500`, `normalize=zscore` | 5 | -5.0% | +4.4% | 4.7% |
| `lr_schedule=cosine`, `n=10000` | 5 | -5.4% | +4.5% | 4.9% |

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
