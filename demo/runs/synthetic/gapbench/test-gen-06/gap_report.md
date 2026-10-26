# Gap Report: test-gen-06

Artifact `mlbench` · generated 2026-10-23 17:45 · 169 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -28.1% | +0.0% | ±1.1% | `normalize=zscore`, `n=600` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Held-out claims outside noise:**
  - C2 (`balanced_accuracy`): paper 0.7004, measured 0.5387 (-23.1%, band ±1.0%)

## C1: test_accuracy (paper 0.7417)
**Fits but unsupported** · gap -28.1% → +0.0% · 86 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0095`, `B0096`, `B0097`, `B0098` (4 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Config: `n` naive `1200`, changed to `600`
- Command:

  Replay: fork checkpoint `8ae35478-ed32-4086-9cd7-4fdd405463d7` and run
  ```
  @ast:train.py:66:@mut.8.Call.xdiv2=0 @ast:train.py:66:@mut.8.Call.xmul2=0 RUN_TAG=2f71bf67eeda export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; "${PYTHON:-python3}" train.py --n 600 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7417, 0.7417, 0.7417, 0.7417; gap after +0.0%; result checkpoint `80ca1c48-af9f-4854-b424-cb1d3d03d994`
- Effect: candidate 0.7417 minus naive 0.5333 = +0.2084, 95% bootstrap interval [+0.2042, +0.245] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.742 test accuracy and 0.700 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7417 accuracy (headline claim)

### What did we measure?
- Naive median 0.5333 over 5 runs; repeats: 0.5375, 0.4875, 0.5375, 0.5333, 0.5333
- Spread: range 0.4875 to 0.5375, noise band ±0.0084 (2 x MAD), CV 4.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -28.1% (noise band ±1.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -24.7% (it comes back)
- PASS · Counterfactual (reversal test): without `n` the gap is +11.8% (it comes back)
- PASS · Held-out claim: C2: -23.1% to +0.0% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- FAIL · Evidence: `n=600`: no evidence mentions '600'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2084 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `NUM_RUNS`, `CPU_MODEL`, `PYTHON_VERSION`, `LIBM_VERSION`, `OS_VERSION`, `ROUNDING_PRECISION`, `MEMORY_SIZE`, `STORAGE_DEVICE`, `CPU_CORES`, `ULIMIT_SETTINGS`, `FILESYSTEM`, `PYTHONHASHSEED`, `RANDOM_MODULE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (11.9 noise units, gap -14.6%); `n=6000` (7.74 noise units, gap -19.3%); `normalize=minmax` (7.44 noise units, gap -19.7%); `n=120` (5.95 noise units, gap -21.4%); `n=2400` (3.73 noise units, gap -23.9%) (and 3 more in the JSON)
- Near alternatives (closest across all claims):
  - `n=12000`, `normalize=minmax`: this claim -0.3%, mean |gap| 1.0% (3 runs)
  - `normalize=zscore`, `n=6000`: this claim +1.0%, mean |gap| 1.8% (3 runs)
  - `normalize=zscore`, `n=2400`: this claim -4.2%, mean |gap| 2.5% (3 runs)

### Equally good configurations
The target claim can't tell these 6 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `n=600, normalize=zscore` (reported)
- `n=12000, normalize=minmax`
- `n=6000, normalize=zscore`
- `n=120, normalize=zscore`
- `class_weight=balanced, normalize=minmax`
- `n=12000, normalize=zscore`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting n=600, normalize=zscore | settings | 39% | 0.0 sigma (fits every claim) | run with n=600, normalize=zscore |
| 2 | the setting n=12000, normalize=minmax | settings | 12% | 0.4 sigma (fits every claim) | run with n=12000, normalize=minmax |
| 3 | the setting n=6000, normalize=zscore | settings | 11% | 0.4 sigma (fits every claim) | run with n=6000, normalize=zscore |

### History matching (every measured configuration, all claims together)
- 21 of 83 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `n, normalize`: n=600, normalize=zscore (max I 0); n=12000, normalize=minmax (max I 0.41); n=6000, normalize=zscore (max I 0.44); n=12000, normalize=zscore (max I 0.67); +5 more
  - `lr_schedule, n`: lr_schedule=cosine, n=12000 (max I 1.67)
- Equally good values: `n` in {600, 6000}

Notes:
- configurations the target claim can't tell apart from the answer: n=600, normalize=zscore; n=12000, normalize=minmax; n=6000, normalize=zscore; n=120, normalize=zscore; class_weight=balanced, normalize=minmax; n=12000, normalize=zscore
- equally good values within one noise band (measured): n in {600, 6000}
- spec knobs no ledger assumption names (batch_size, data_seed, epochs, label_noise, lr, positive_rate, split, threshold, weight_decay) were screened too; no better answer
- n: values from 600 to 600 fit every claim (a bisection, 3 runs a side, one run a value: approximate)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore`, `n=600` | 4 | +0.0% | +0.0% | 0.0% |
| `n=12000`, `normalize=minmax` | 3 | -0.3% | -1.6% | 1.0% |
| `normalize=zscore`, `n=6000` | 3 | +1.0% | +2.6% | 1.8% |
| `normalize=zscore`, `n=2400` | 3 | -4.2% | -0.7% | 2.5% |
| `normalize=zscore`, `n=12000` | 3 | +1.7% | +3.6% | 2.7% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `n=1`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Runtime trace (one dry run)
1 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `NUM_RUNS`, `CPU_MODEL`, `PYTHON_VERSION`, `LIBM_VERSION`, `OS_VERSION`, `ROUNDING_PRECISION`, `MEMORY_SIZE`, `STORAGE_DEVICE`, `CPU_CORES`, `ULIMIT_SETTINGS`, `FILESYSTEM`, `PYTHONHASHSEED`, `RANDOM_MODULE`, `--out`

## Provenance
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `7be36dde35aa5fcbe1cffeee1216997d960b4211d0ed734a6433b1f16ca8950d`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
