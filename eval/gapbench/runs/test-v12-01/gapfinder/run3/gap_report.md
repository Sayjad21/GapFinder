# Gap Report: test-v12-01

Artifact `mlbench` · generated 2026-10-15 08:46 · 172 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -23.8% | +0.4% | ±1.2% | `normalize=minmax`, `n=6000` |

## C1: test_accuracy (paper 0.705)
**Fits but unsupported** · gap -23.8% → +0.4% · 61 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0097`, `B0163`, `B0164` (3 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `n` naive `1200`, changed to `6000`
- Command:

  Replay: fork checkpoint `4b7fd42e-a015-4919-8465-26f93679cc14` and run
  ```
  RUN_TAG=8348653f184e "${PYTHON:-python3}" train.py --n 6000 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7075, 0.7117, 0.7042; gap after +0.4%; result checkpoint `7a2a78ca-fe6e-4456-ac62-c52c84e83667`
- Effect: candidate 0.7075 minus naive 0.5375 = +0.17, 95% bootstrap interval [+0.1458, +0.1759] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.705 test accuracy.

- p. 1; value used: `test_accuracy` = 0.705 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5667, 0.5417, 0.5375, 0.5333, 0.5375
- Spread: range 0.5333 to 0.5667, noise band ±0.0084 (2 x MAD), CV 2.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -23.8% (noise band ±1.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -27.1% (it comes back)
- PASS · Counterfactual (reversal test): without `n` the gap is -15.5% (it comes back)
- PASS · Held-out claim: C2: -13.3% to +0.3% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- FAIL · Evidence: `n=6000`: no evidence mentions '6000'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.17 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `env_python_version`, `env_os`, `env_cpu_arch`, `env_memory_gb`, `env_storage_type`, `env_python_random_module`, `env_math_module`, `env_json_module`, `env_os_module`, `env_argparse_module`, `env_random_seed_shuffling`, `env_run_tag_seed_source`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (10.42 noise units, gap -11.3%); `n=24` (8.63 noise units, gap +13.5%); `lr_schedule=step` (6.94 noise units, gap -15.5%); `n=600` (6.45 noise units, gap -16.1%); `normalize=zscore` (5.15 noise units, gap +17.6%) (and 3 more in the JSON)
- Near alternatives (closest across all claims):
  - `normalize=minmax`, `n=10000`: this claim +2.1%, mean |gap| 3.7% (3 runs)
  - `n=12000`, `lr_schedule=cosine`: this claim -5.4%, mean |gap| 4.4% (3 runs)
  - `n=500`, `normalize=zscore`: this claim -5.0%, mean |gap| 4.7% (3 runs)

### Equally good configurations
The target claim can't tell these 4 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `n=6000, normalize=minmax` (reported)
- `n=2400, normalize=zscore`
- `n=10000, normalize=minmax`
- `n=240, normalize=zscore`

### History matching (every measured configuration, all claims together)
- 15 of 58 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `n, normalize`: n=6000, normalize=minmax (max I 0.12); n=500, normalize=zscore (max I 0.96); n=10000, normalize=minmax (max I 1.01); n=12000, normalize=minmax (max I 1.67); +1 more
  - `lr_schedule, n`: lr_schedule=cosine, n=10000 (max I 1.01); lr_schedule=cosine, n=12000 (max I 1.01); lr_schedule=step, n=12000 (max I 1.71); lr_schedule=step, n=10000 (max I 2.3)
  - `lr_schedule`: lr_schedule=cosine (max I 2.3)
- 2 separate islands (no single-knob move joins them): n=6000, normalize=minmax; n=500, normalize=zscore; n=10000, normalize=minmax | lr_schedule=cosine, n=10000; lr_schedule=cosine, n=12000; lr_schedule=step, n=12000

Notes:
- configurations the target claim can't tell apart from the answer: n=6000, normalize=minmax; n=2400, normalize=zscore; n=10000, normalize=minmax; n=240, normalize=zscore

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax`, `n=6000` | 3 | +0.4% | +0.3% | 0.3% |
| `normalize=minmax`, `n=10000` | 3 | +2.1% | +5.2% | 3.7% |
| `n=12000`, `lr_schedule=cosine` | 3 | -5.4% | +3.4% | 4.4% |
| `n=500`, `normalize=zscore` | 3 | -5.0% | +4.4% | 4.7% |
| `lr_schedule=step`, `n=12000` | 3 | -6.3% | +3.4% | 4.8% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `n=1`: invalid_value, 

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `env_python_version`, `env_os`, `env_cpu_arch`, `env_memory_gb`, `env_storage_type`, `env_python_random_module`, `env_math_module`, `env_json_module`, `env_os_module`, `env_argparse_module`, `env_random_seed_shuffling`, `env_run_tag_seed_source`, `--out`

## Provenance
- GapFinder commit: `f01fe3d9a0095f98d6304ad0543b917ca8e529eb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0550, sandbox reported $0.0000 (total $0.0550; this search; ledger extraction is included only if it shared the search's router)
