# Gap Report: test-v12-01

Artifact `mlbench` · generated 2026-10-23 17:56 · 200 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -23.8% | -0.4% | ±1.2% | `normalize=minmax`, `n=6000` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Held-out claims outside noise:**
  - C2 (`balanced_accuracy`): paper 0.6255, measured 0.5422 (-13.3%, band ±1.1%)
- **The paper states these, and this harness can't vary them** (they are part of what the number means):
  - `num_runs`: "Numbers are medians over 7 runs with different shuffling seeds." (p.1)

## C1: test_accuracy (paper 0.705)
**Fits but unsupported** · gap -23.8% → -0.4% · 101 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0098`, `B0102`, `B0103`, `B0104` (4 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `n` naive `1200`, changed to `6000`
- Command:

  Replay: fork checkpoint `83d1fe45-e656-4c9d-82da-4dd8073d2112` and run
  ```
  @ast:train.py:66:@mut.8.Call.xdiv2=0 @ast:train.py:66:@mut.8.Call.xmul2=0 RUN_TAG=75ab80feb57d export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; "${PYTHON:-python3}" train.py --n 6000 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7033, 0.7017, 0.6975, 0.7075; gap after -0.4%; result checkpoint `67dc974e-e943-4625-948f-ba1c0965e1f0`
- Effect: candidate 0.7025 minus naive 0.5375 = +0.165, 95% bootstrap interval [+0.1548, +0.1713] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.705 test accuracy.

- p. 1; value used: `test_accuracy` = 0.705 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5458, 0.5458, 0.5333, 0.5375, 0.5333
- Spread: range 0.5333 to 0.5458, noise band ±0.0084 (2 x MAD), CV 1.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -23.8% (noise band ±1.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -19.3% (it comes back)
- PASS · Counterfactual (reversal test): without `n` the gap is -15.5% (it comes back)
- PASS · Held-out claim: C2: -13.3% to -1.0% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- FAIL · Evidence: `n=6000`: no evidence mentions '6000'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.165 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `python_version`, `hardware`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `n=120` (10.42 noise units, gap -11.3%); `lr_schedule=cosine` (10.42 noise units, gap -11.3%); `n=24` (8.63 noise units, gap +13.5%); `normalize=zscore` (5.65 noise units, gap +17.0%); `n=240` (2.98 noise units, gap -20.2%) (and 2 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=cosine`, `n=12000`: this claim -5.3%, mean |gap| 4.3% (3 runs)
  - `lr_schedule=step`, `n=120`: this claim -11.3%, mean |gap| 6.8% (3 runs)
  - `normalize=minmax`, `n=12000`: this claim +4.9%, mean |gap| 7.5% (3 runs)

### Equally good configurations
The target claim can't tell these 2 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `n=6000, normalize=minmax` (reported)
- `n=240, normalize=zscore`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting n=6000, normalize=minmax | settings | 77% | 0.2 sigma (fits every claim) | run with n=6000, normalize=minmax |
| 2 | the setting lr_schedule=cosine, n=12000 | settings | 12% | 1.1 sigma (fits every claim) | run with lr_schedule=cosine, n=12000 |
| 3 | the setting n=12000, normalize=minmax | settings | 5% | 1.6 sigma (fits every claim) | run with n=12000, normalize=minmax |

### History matching (every measured configuration, all claims together)
- 10 of 98 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `n, normalize`: n=6000, normalize=minmax (max I 0.18); n=12000, normalize=minmax (max I 1.75); n=240, normalize=zscore (max I 2.84)
  - `lr_schedule, n`: lr_schedule=cosine, n=12000 (max I 1.07); lr_schedule=cosine, n=6000 (max I 2.18); lr_schedule=cosine, n=2400 (max I 2.92); lr_schedule=cosine, n=2000 (max I 2.94)
  - `lr_schedule`: lr_schedule=cosine (max I 2.69)
  - `class_weight, n`: class_weight=balanced, n=12000 (max I 2.72)
  - `class_weight, lr_schedule`: class_weight=balanced, lr_schedule=cosine (max I 2.92)
- 4 separate islands (no single-knob move joins them): lr_schedule=cosine, n=12000; lr_schedule=cosine, n=6000; lr_schedule=cosine | n=6000, normalize=minmax; n=12000, normalize=minmax | class_weight=balanced, n=12000 | n=240, normalize=zscore

Notes:
- configurations the target claim can't tell apart from the answer: n=6000, normalize=minmax; n=240, normalize=zscore
- spec knobs no ledger assumption names (batch_size, data_seed, epochs, label_noise, lr, positive_rate, split, threshold, weight_decay) were screened too; no better answer
- n: values from 3795 to 7135 fit every claim (a bisection, 3 runs a side, one run a value: approximate)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `n=6000`, `normalize=minmax` | 4 | -0.4% | -1.0% | 0.7% |
| `lr_schedule=cosine`, `n=12000` | 3 | -5.3% | +3.4% | 4.3% |
| `lr_schedule=step`, `n=120` | 3 | -11.3% | -2.2% | 6.8% |
| `normalize=minmax`, `n=12000` | 3 | +4.9% | +10.0% | 7.5% |
| `normalize=zscore`, `n=240` | 3 | -2.5% | +12.8% | 7.6% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `n=1`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Runtime trace (one dry run)
1 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `python_version`, `hardware`, `--out`

## Provenance
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `7be36dde35aa5fcbe1cffeee1216997d960b4211d0ed734a6433b1f16ca8950d`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
