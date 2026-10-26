# Gap Report: test-v13-04

Artifact `mlbench` · generated 2026-10-23 18:07 · 165 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -37.7% | +0.0% | ±7.0% | `normalize=zscore` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Held-out claims outside noise:**
  - C2 (`balanced_accuracy`): paper 0.8102, measured 0.5132 (-36.7%, band ±8.5%)

## C1: test_accuracy (paper 0.8292)
**Fits but unsupported** · gap -37.7% → +0.0% · 90 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0008`, `B0013`, `B0014`, `B0015`, `B0016`, `B0017` (6 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Command:

  Replay: fork checkpoint `e9a3eee3-9299-4dbe-aa70-7f1c4ebcc2ce` and run
  ```
  RUN_TAG=d1178c2648f6 export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.8292, 0.8292, 0.825, 0.825, 0.8292, 0.8292; gap after +0.0%; result checkpoint `8230de06-fc8f-4f39-af38-d700d42c3d1c`
- Effect: candidate 0.8292 minus naive 0.5167 = +0.3125, 95% bootstrap interval [+0.2859, +0.3525] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.829 test accuracy.

- p. 1, Table 1; value used: `test_accuracy` = 0.8292 (headline claim)

### What did we measure?
- Naive median 0.5167 over 5 runs; repeats: 0.475, 0.5375, 0.475, 0.5458, 0.5167
- Spread: range 0.475 to 0.5458, noise band ±0.0582 (2 x MAD), CV 6.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -37.7% (noise band ±7.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -37.7% (it comes back)
- PASS · Held-out claim: C2: -36.7% to +0.0% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.3125 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `python_version`, `random_module`, `floating_point`, `os`, `cpu_arch`, `memory_size`, `disk_type`, `PYTHONHASHSEED`, `math_lib`, `cpu_cores`, `python_optimize`, `python_debug`, `PYTHONPATH`, `PYTHONHOME`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (1.79 noise units, gap -25.1%); `normalize=minmax` (1.36 noise units, gap -28.1%)
- Near alternatives (closest across all claims):
  - `normalize=zscore`, `lr_schedule=cosine`: this claim +0.0%, mean |gap| 0.0% (6 runs)
  - `normalize=zscore`, `lr_schedule=step`: this claim +0.0%, mean |gap| 0.0% (6 runs)
  - `normalize=zscore`, `batch_size=3`: this claim -0.3%, mean |gap| 0.2% (6 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `normalize=zscore` (reported)
- `lr_schedule=cosine, normalize=zscore`
- `lr_schedule=step, normalize=zscore`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting normalize=zscore | settings | 36% | 0.0 sigma (fits every claim) | run with normalize=zscore |
| 2 | the setting lr_schedule=cosine, normalize=zscore | settings | 12% | 0.0 sigma (fits every claim) | run with lr_schedule=cosine, normalize=zscore |
| 3 | the setting lr_schedule=step, normalize=zscore | settings | 12% | 0.0 sigma (fits every claim) | run with lr_schedule=step, normalize=zscore |

### History matching (every measured configuration, all claims together)
- 15 of 88 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 0); lr_schedule=step, normalize=zscore (max I 0.02)
  - `normalize`: normalize=zscore (max I 0.03)
  - `batch_size, normalize`: batch_size=3, normalize=zscore (max I 0.08); batch_size=320, normalize=zscore (max I 0.13)
  - `normalize, split`: normalize=zscore, split=0.7 (max I 0.86)
  - `class_weight, normalize`: class_weight=balanced, normalize=zscore (max I 0.96); class_weight=balanced, normalize=minmax (max I 1.27)
  - `n, normalize`: n=2000, normalize=zscore (max I 1.15); n=120, normalize=zscore (max I 1.42)
- 4 separate islands (no single-knob move joins them): lr_schedule=cosine, normalize=zscore; lr_schedule=step, normalize=zscore; normalize=zscore | lr_schedule=cosine, n=120 | batch_size=3, n=120 | batch_size=3, lr_schedule=cosine

Notes:
- its runs spread 0.1x the naive run's noise band (reported, not used to judge)
- configurations the target claim can't tell apart from the answer: normalize=zscore; lr_schedule=cosine, normalize=zscore; lr_schedule=step, normalize=zscore
- spec knobs no ledger assumption names (batch_size, data_seed, epochs, label_noise, lr, n, positive_rate, split, threshold, weight_decay) were screened too; no better answer

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore` | 6 | +0.0% | +0.0% | 0.0% |
| `normalize=zscore`, `lr_schedule=cosine` | 6 | +0.0% | +0.0% | 0.0% |
| `normalize=zscore`, `lr_schedule=step` | 6 | +0.0% | +0.0% | 0.0% |
| `normalize=zscore`, `batch_size=3` | 6 | -0.3% | -0.2% | 0.2% |
| `normalize=zscore`, `batch_size=320` | 6 | -0.5% | -0.7% | 0.6% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `split=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made
- `n=1`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Runtime trace (one dry run)
1 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `python_version`, `random_module`, `floating_point`, `os`, `cpu_arch`, `memory_size`, `disk_type`, `PYTHONHASHSEED`, `math_lib`, `cpu_cores`, `python_optimize`, `python_debug`, `PYTHONPATH`, `PYTHONHOME`, `--out`

## Provenance
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `a5ee8e94932cc1397dd02c920427dbe9702911f36a6fbfee753b818e8d60994f`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
