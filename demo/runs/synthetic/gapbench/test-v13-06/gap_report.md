# Gap Report: test-v13-06

Artifact `mlbench` · generated 2026-10-23 18:09 · 166 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -36.1% | +0.1% | ±0.6% | `normalize=zscore`, `n=12000` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Held-out claims outside noise:**
  - C2 (`balanced_accuracy`): paper 0.7277, measured 0.4786 (-34.2%, band ±0.7%)

## C1: test_accuracy (paper 0.7558)
**Fits but unsupported** · gap -36.1% → +0.1% · 62 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0108`, `B0109`, `B0110`, `B0111`, `B0112`, `B0113` (6 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Config: `n` naive `1200`, changed to `12000`
- Command:

  Replay: fork checkpoint `e5593aa3-5848-42b8-a2bd-d52237380b0c` and run
  ```
  @ast:train.py:66:@mut.8.Call.xdiv2=0 @ast:train.py:66:@mut.8.Call.xmul2=0 @ast:train.py:68:@mut.37.num.add1=0 @ast:train.py:68:@mut.37.num.div2=0 @ast:train.py:68:@mut.37.num.mul2=0 @ast:train.py:68:@mut.37.num.sub1=0 RUN_TAG=ede4b1faaa2a export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; "${PYTHON:-python3}" train.py --n 12000 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7604, 0.7562, 0.7562, 0.755, 0.7558, 0.7579; gap after +0.1%; result checkpoint `9878ff6f-3b79-4bb0-940f-760fd8b333c6`
- Effect: candidate 0.7562 minus naive 0.4833 = +0.2729, 95% bootstrap interval [+0.2104, +0.2751] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.756 test accuracy and 0.728 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7558 (headline claim)

### What did we measure?
- Naive median 0.4833 over 5 runs; repeats: 0.4833, 0.4833, 0.55, 0.4833, 0.5375
- Spread: range 0.4833 to 0.55, noise band ±0.004833 (2 x MAD), CV 6.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -36.1% (noise band ±0.6% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -37.9% (it comes back)
- PASS · Counterfactual (reversal test): without `n` the gap is +9.7% (it comes back)
- PASS · Held-out claim: C2: -34.2% to -0.0% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- FAIL · Evidence: `n=12000`: no evidence mentions '12000'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2729 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (30.19 noise units, gap -16.8%); `normalize=minmax` (23.28 noise units, gap -21.2%); `n=120` (20.69 noise units, gap -22.8%); `n=10000` (18.97 noise units, gap -23.9%); `lr=0.01` (16.39 noise units, gap -25.6%) (and 4 more in the JSON)
- Near alternatives (closest across all claims):
  - `n=10000`, `normalize=zscore`: this claim -0.8%, mean |gap| 0.6% (5 runs)
  - `normalize=zscore`, `n=6000`: this claim -0.8%, mean |gap| 1.0% (5 runs)
  - `normalize=zscore`, `n=600`: this claim -1.9%, mean |gap| 2.8% (5 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `n=12000, normalize=zscore` (reported)
- `n=10000, normalize=zscore`
- `n=600, normalize=zscore`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting n=12000, normalize=zscore | settings | 41% | 0.0 sigma (fits every claim) | run with n=12000, normalize=zscore |
| 2 | the setting n=10000, normalize=zscore | settings | 13% | 0.1 sigma (fits every claim) | run with n=10000, normalize=zscore |
| 3 | the setting n=6000, normalize=zscore | settings | 13% | 0.2 sigma (fits every claim) | run with n=6000, normalize=zscore |

### History matching (every measured configuration, all claims together)
- 27 of 63 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `n, normalize`: n=12000, normalize=zscore (max I 0.03); n=10000, normalize=zscore (max I 0.15); n=6000, normalize=zscore (max I 0.21); n=600, normalize=zscore (max I 0.63); +4 more
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 1.11); class_weight=balanced, normalize=zscore (max I 1.3)
- 2 separate islands (no single-knob move joins them): n=12000, normalize=zscore; n=10000, normalize=zscore; n=6000, normalize=zscore | class_weight=balanced, n=10000; class_weight=balanced, n=6000

Notes:
- configurations the target claim can't tell apart from the answer: n=12000, normalize=zscore; n=10000, normalize=zscore; n=600, normalize=zscore
- found after adding spec knobs no ledger assumption names (batch_size, data_seed, epochs, label_noise, lr, positive_rate, split, threshold, weight_decay)
- n: values from 11465 to >120000 fit every claim (a bisection, 3 runs a side, one run a value: approximate)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore`, `n=12000` | 6 | +0.1% | -0.0% | 0.0% |
| `n=10000`, `normalize=zscore` | 5 | -0.8% | -0.4% | 0.6% |
| `normalize=zscore`, `n=6000` | 5 | -0.8% | -1.2% | 1.0% |
| `normalize=zscore`, `n=600` | 5 | -1.9% | -3.8% | 2.8% |
| `class_weight=balanced`, `normalize=minmax` | 5 | -0.8% | +6.3% | 3.5% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `n=1`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Runtime trace (one dry run)
1 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `1fd3d59022925491b04c41fd5e5ed48e25739b360d0d1093aefdff9298c5fcf4`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
