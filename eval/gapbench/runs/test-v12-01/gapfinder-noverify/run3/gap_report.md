# Gap Report: test-v12-01

Artifact `mlbench` · generated 2026-10-15 08:46 · 199 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Explained | -30.9% | -0.5% | ±2.4% | `n=6000`, `normalize=minmax` |

## C1: test_accuracy (paper 0.705)
**Explained** · gap -30.9% → -0.5% · 64 hypotheses tested
> Interacting factors: these changes close the gap only together, and every check passes

### Which experiment changed it?
- Branch: `B0099`, `B0176`, `B0177`, `B0178`, `B0179` (5 run(s) of the same config)
- Config: `n` naive `1200`, changed to `6000`
- Config: `normalize` naive `none`, changed to `minmax`
- Command:

  Replay: fork checkpoint `e0bb0efb-63b0-4808-ad7d-c336066fd8fd` and run
  ```
  RUN_TAG=c78eb43cea7e "${PYTHON:-python3}" train.py --n 6000 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7017, 0.7017, 0.7158, 0.7025, 0.7; gap after -0.5%; result checkpoint `faadb506-e756-4d09-b29d-fa16010cd40d`
- Effect: candidate 0.7017 minus naive 0.4875 = +0.2142, 95% bootstrap interval [+0.1765, +0.235] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.705 test accuracy.

- p. 1; value used: `test_accuracy` = 0.705 (headline claim)

### What did we measure?
- Naive median 0.4875 over 5 runs; repeats: 0.4667, 0.4833, 0.5375, 0.4958, 0.4875
- Spread: range 0.4667 to 0.5375, noise band ±0.0166 (2 x MAD), CV 5.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -30.9% (noise band ±2.4% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is +0.2142 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `env_python_version`, `env_os`, `env_cpu_arch`, `env_memory_gb`, `env_storage_type`, `env_python_random_module`, `env_math_module`, `env_json_module`, `env_os_module`, `env_argparse_module`, `env_random_seed_shuffling`, `env_run_tag_seed_source`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `n=100` (10.39 noise units, gap +6.4%); `lr_schedule=cosine` (7.53 noise units, gap -13.1%); `n=10000` (6.05 noise units, gap -16.6%); `n=2400` (5.65 noise units, gap -17.5%); `normalize=zscore` (5.62 noise units, gap +17.6%) (and 4 more in the JSON)
- Near alternatives (closest across all claims):
  - `normalize=minmax`, `n=10000`: this claim +2.2%, mean |gap| 3.6% (5 runs)
  - `n=12000`, `lr_schedule=cosine`: this claim -5.6%, mean |gap| 4.3% (5 runs)
  - `lr_schedule=cosine`, `n=10000`: this claim -5.5%, mean |gap| 4.9% (5 runs)

### History matching (every measured configuration, all claims together)
- 34 of 61 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `n, normalize`: n=6000, normalize=minmax (max I 0.06); n=500, normalize=zscore (max I 0.76); n=10000, normalize=minmax (max I 0.87); n=12000, normalize=minmax (max I 1.11); +1 more
  - `lr_schedule, n`: lr_schedule=cosine, n=12000 (max I 0.95); lr_schedule=cosine, n=10000 (max I 0.99); lr_schedule=step, n=100 (max I 1.15); lr_schedule=cosine, n=100 (max I 1.47)
  - `n`: n=100 (max I 1.13)
- 3 separate islands (no single-knob move joins them): n=6000, normalize=minmax; n=500, normalize=zscore; n=10000, normalize=minmax | class_weight=balanced, n=12000; class_weight=balanced, n=10000 | lr_schedule=step, normalize=minmax

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'n': '6000', 'normalize': 'zscore'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `n=6000`, `normalize=minmax` | 5 | -0.5% | -1.1% | 0.8% |
| `normalize=minmax`, `n=10000` | 5 | +2.2% | +5.1% | 3.6% |
| `n=12000`, `lr_schedule=cosine` | 5 | -5.6% | +3.1% | 4.3% |
| `lr_schedule=cosine`, `n=10000` | 5 | -5.5% | +4.3% | 4.9% |
| `n=2400`, `normalize=zscore` | 5 | +0.8% | +11.1% | 6.0% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `n=1`: invalid_value, Setting n=1 produced an empty training dataset after the 0.8 split, causing an IndexError when trying to access Xtr[0]; the value is below the minimum needed for a non‑empty split; retried as `n=100`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `env_python_version`, `env_os`, `env_cpu_arch`, `env_memory_gb`, `env_storage_type`, `env_python_random_module`, `env_math_module`, `env_json_module`, `env_os_module`, `env_argparse_module`, `env_random_seed_shuffling`, `env_run_tag_seed_source`, `--out`

## Provenance
- GapFinder commit: `f01fe3d9a0095f98d6304ad0543b917ca8e529eb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0007, sandbox reported $0.0000 (total $0.0007; this search; ledger extraction is included only if it shared the search's router)
