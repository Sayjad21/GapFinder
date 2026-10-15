# Gap Report: test-v12-01

Artifact `mlbench` · generated 2026-10-15 08:46 · 175 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -22.6% | +0.2% | ±2.4% | `n=6000`, `normalize=minmax` |

## C1: test_accuracy (paper 0.705)
**Fits but unsupported** · gap -22.6% → +0.2% · 61 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0069`, `B0126`, `B0127` (3 run(s) of the same config)
- Config: `n` naive `1200`, changed to `6000`
- Config: `normalize` naive `none`, changed to `minmax`
- Command:

  Replay: fork checkpoint `9ae4cac7-793b-42d9-8afa-70b0f364a4f8` and run
  ```
  RUN_TAG=f0bebcbebe35 "${PYTHON:-python3}" train.py --n 6000 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7067, 0.6975, 0.7075; gap after +0.2%; result checkpoint `c5d7d836-81a5-4bf5-905c-75557d32605c`
- Effect: candidate 0.7067 minus naive 0.5458 = +0.1609, 95% bootstrap interval [+0.1414, +0.1683] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.705 test accuracy.

- p. 1; value used: `test_accuracy` = 0.705 (headline claim)

### What did we measure?
- Naive median 0.5458 over 5 runs; repeats: 0.5375, 0.5458, 0.5375, 0.5667, 0.5458
- Spread: range 0.5375 to 0.5667, noise band ±0.0166 (2 x MAD), CV 2.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -22.6% (noise band ±2.4% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `n` the gap is -15.5% (it comes back)
- PASS · Counterfactual (reversal test): without `normalize` the gap is -25.7% (it comes back)
- PASS · Held-out claim: C2: -13.3% to +0.3% (not worse beyond noise)
- FAIL · Evidence: `n=6000`: evidence gate off: no evidence was looked for
- FAIL · Evidence: `normalize=minmax`: evidence gate off: no evidence was looked for
- PASS · Effect vs noise: candidate minus naive is +0.1609 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `env_python_version`, `env_os`, `env_cpu_arch`, `env_memory_gb`, `env_storage_type`, `env_python_random_module`, `env_math_module`, `env_json_module`, `env_os_module`, `env_argparse_module`, `env_random_seed_shuffling`, `env_run_tag_seed_source`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `n=120` (7.28 noise units, gap -5.4%); `lr_schedule=cosine` (4.52 noise units, gap -11.9%); `n=10000` (4.32 noise units, gap -12.4%); `n=24` (3.87 noise units, gap +13.5%); `normalize=zscore` (2.11 noise units, gap +17.6%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `n=10000`, `normalize=minmax`: this claim +1.9%, mean |gap| 3.2% (3 runs)
  - `normalize=zscore`, `n=500`: this claim -3.5%, mean |gap| 4.9% (3 runs)
  - `n=10000`, `lr_schedule=cosine`: this claim -5.4%, mean |gap| 5.0% (3 runs)

### Equally good configurations
The target claim can't tell these 5 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `n=6000, normalize=minmax` (reported)
- `n=120, normalize=zscore`
- `n=2400, normalize=zscore`
- `n=240, normalize=zscore`
- `n=10000, normalize=minmax`

### History matching (every measured configuration, all claims together)
- 15 of 58 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `n, normalize`: n=6000, normalize=minmax (max I 0.09); n=10000, normalize=minmax (max I 0.9); n=500, normalize=zscore (max I 1.11); n=24, normalize=minmax (max I 1.32); +2 more
  - `lr_schedule, n`: lr_schedule=cosine, n=10000 (max I 1.03); lr_schedule=cosine, n=120 (max I 1.44); lr_schedule=cosine, n=6000 (max I 2.29)
  - `lr_schedule`: lr_schedule=cosine (max I 2.24)
- 2 separate islands (no single-knob move joins them): n=6000, normalize=minmax; n=10000, normalize=minmax; n=500, normalize=zscore | lr_schedule=cosine, n=10000; lr_schedule=cosine, n=120; lr_schedule=cosine
- Equally good values: `n` in {6000, 10000}

Notes:
- evidence gate off: no evidence was checked, so this cannot be labelled Explained
- configurations the target claim can't tell apart from the answer: n=6000, normalize=minmax; n=120, normalize=zscore; n=2400, normalize=zscore; n=240, normalize=zscore; n=10000, normalize=minmax
- equally good values within one noise band (measured): n in {6000, 10000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax`, `n=6000` | 3 | +0.2% | +0.3% | 0.3% |
| `n=10000`, `normalize=minmax` | 3 | +1.9% | +4.5% | 3.2% |
| `normalize=zscore`, `n=500` | 3 | -3.5% | +6.3% | 4.9% |
| `n=10000`, `lr_schedule=cosine` | 3 | -5.4% | +4.6% | 5.0% |
| `lr_schedule=cosine`, `n=120` | 3 | -5.4% | +5.1% | 5.3% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `n=1`: crash, The script crashed with an IndexError when trying to access Xtr[0]; the training set ended up empty, likely because the chosen n=1 resulted in insufficient data for the requested split/processing

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `env_python_version`, `env_os`, `env_cpu_arch`, `env_memory_gb`, `env_storage_type`, `env_python_random_module`, `env_math_module`, `env_json_module`, `env_os_module`, `env_argparse_module`, `env_random_seed_shuffling`, `env_run_tag_seed_source`, `--out`

## Provenance
- GapFinder commit: `f01fe3d9a0095f98d6304ad0543b917ca8e529eb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0005, sandbox reported $0.0000 (total $0.0005; this search; ledger extraction is included only if it shared the search's router)
