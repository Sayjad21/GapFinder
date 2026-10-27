# Gap Report: test-v12-01

Artifact `mlbench` · generated 2026-10-15 21:07 · 199 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -24.4% | +0.7% | ±4.7% | `normalize=minmax`, `n=6000` |

## C1: test_accuracy (paper 0.705)
**Fits but unsupported** · gap -24.4% → +0.7% · 57 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0118`, `B0121`, `B0158`, `B0159`, `B0160` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `n` naive `1200`, changed to `6000`
- Command:

  Replay: fork checkpoint `62a38cd9-bebe-4741-93aa-b5b151baba88` and run
  ```
  RUN_TAG=d9ffea8be4b2 "${PYTHON:-python3}" train.py --n 6000 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7083, 0.7217, 0.7075, 0.71, 0.7175; gap after +0.7%; result checkpoint `a7daeeda-043b-4b64-b20c-5b596ea85e06`
- Effect: candidate 0.71 minus naive 0.5333 = +0.1767, 95% bootstrap interval [+0.165, +0.2393] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.705 test accuracy.

- p. 1; value used: `test_accuracy` = 0.705 (headline claim)

### What did we measure?
- Naive median 0.5333 over 5 runs; repeats: 0.55, 0.5333, 0.5375, 0.5083, 0.4625
- Spread: range 0.4625 to 0.55, noise band ±0.0334 (2 x MAD), CV 6.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -24.4% (noise band ±4.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -28.2% (it comes back)
- PASS · Counterfactual (reversal test): without `n` the gap is -15.5% (it comes back)
- PASS · Held-out claim: C2: -13.9% to +1.6% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- FAIL · Evidence: `n=6000`: no evidence mentions '6000'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.1767 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `env_python_version`, `env_os`, `env_cpu_arch`, `env_memory_gb`, `env_storage_type`, `env_python_random_module`, `env_math_module`, `env_json_module`, `env_os_module`, `env_argparse_module`, `env_random_seed_shuffling`, `env_run_tag_seed_source`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `n=120` (3.99 noise units, gap -5.4%); `lr_schedule=cosine` (2.37 noise units, gap -13.1%); `n=24` (2.3 noise units, gap +13.5%); `normalize=zscore` (1.42 noise units, gap +17.6%)
- Near alternatives (closest across all claims):
  - `normalize=minmax`, `n=10000`: this claim +2.1%, mean |gap| 3.3% (5 runs)
  - `lr_schedule=cosine`, `n=12000`: this claim -5.5%, mean |gap| 4.4% (5 runs)
  - `n=500`, `normalize=zscore`: this claim -5.0%, mean |gap| 4.7% (5 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `n=6000, normalize=minmax` (reported)
- `n=10000, normalize=minmax`
- `lr_schedule=cosine, n=120`

### History matching (every measured configuration, all claims together)
- 25 of 55 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `n, normalize`: n=6000, normalize=minmax (max I 0.34); n=10000, normalize=minmax (max I 0.7); n=500, normalize=zscore (max I 0.88); n=12000, normalize=minmax (max I 1.32); +1 more
  - `lr_schedule, n`: lr_schedule=cosine, n=10000 (max I 0.91); lr_schedule=cosine, n=12000 (max I 0.92); lr_schedule=cosine, n=120 (max I 1.52)
  - `class_weight, lr_schedule`: class_weight=balanced, lr_schedule=cosine (max I 2.06)
  - `lr_schedule`: lr_schedule=cosine (max I 2.15)
- 3 separate islands (no single-knob move joins them): lr_schedule=cosine, n=10000; lr_schedule=cosine, n=12000; lr_schedule=cosine, n=120 | n=6000, normalize=minmax; n=10000, normalize=minmax; n=500, normalize=zscore | class_weight=balanced, n=120; class_weight=balanced, n=12000; class_weight=balanced, n=600
- Equally good values: `n` in {6000, 10000, 12000}

Notes:
- configurations the target claim can't tell apart from the answer: n=6000, normalize=minmax; n=10000, normalize=minmax; lr_schedule=cosine, n=120
- equally good values within one noise band (measured): n in {6000, 10000, 12000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax`, `n=6000` | 5 | +0.7% | +1.6% | 1.2% |
| `normalize=minmax`, `n=10000` | 5 | +2.1% | +4.4% | 3.3% |
| `lr_schedule=cosine`, `n=12000` | 5 | -5.5% | +3.2% | 4.4% |
| `n=500`, `normalize=zscore` | 5 | -5.0% | +4.4% | 4.7% |
| `lr_schedule=cosine`, `n=10000` | 5 | -5.5% | +4.2% | 4.9% |

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
