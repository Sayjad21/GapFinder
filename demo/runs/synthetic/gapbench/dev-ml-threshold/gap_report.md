# Gap Report: dev-ml-threshold

Artifact `mlbench` · generated 2026-10-23 17:37 · 176 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -29.1% | +0.0% | ±0.7% | `normalize=zscore`, `threshold=0.3` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Held-out claims outside noise:**
  - C2 (`balanced_accuracy`): paper 0.7839, measured 0.5422 (-30.8%, band ±0.7%)

## C1: test_accuracy (paper 0.7583)
**Fits but unsupported** · gap -29.1% → +0.0% · 86 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0071`, `B0077`, `B0078`, `B0079` (4 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Config: `threshold` naive `0.5`, changed to `0.3`
- Command:

  Replay: fork checkpoint `43264293-e798-4f3a-97b8-08acd6b39ffe` and run
  ```
  @ast:train.py:66:@mut.8.Call.xdiv2=0 @ast:train.py:66:@mut.8.Call.xmul2=0 @ast:train.py:68:@mut.37.num.add1=0 @ast:train.py:68:@mut.37.num.div2=0 @ast:train.py:68:@mut.37.num.mul2=0 @ast:train.py:68:@mut.37.num.sub1=0 RUN_TAG=df5f261e6a35 export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.3 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7583, 0.7583, 0.7583, 0.7583; gap after +0.0%; result checkpoint `428f98ab-c760-40a5-9c6c-b16b10d60d5e`
- Effect: candidate 0.7583 minus naive 0.5375 = +0.2208, 95% bootstrap interval [+0.2174, +0.2608] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> On imbalanced screening data, accuracy depends as much on the decision rule as on the model.

- p. 1; value used: `test_accuracy` = 0.7583 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5375, 0.4875, 0.5417, 0.5375, 0.5375
- Spread: range 0.4875 to 0.5417, noise band ±0.005375 (2 x MAD), CV 4.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -29.1% (noise band ±0.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -33.2% (it comes back)
- PASS · Counterfactual (reversal test): without `threshold` the gap is +8.8% (it comes back)
- PASS · Held-out claim: C2: -30.8% to +0.0% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- FAIL · Evidence: `threshold=0.3`: no evidence mentions '0.3'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2208 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (15.5 noise units, gap -18.1%); `normalize=minmax` (10.85 noise units, gap -21.4%); `threshold=0.75` (5.43 noise units, gap -25.3%); `lr_schedule=step` (3.11 noise units, gap -26.9%); `threshold=0.1` (3.11 noise units, gap -26.9%)
- Near alternatives (closest across all claims):
  - `normalize=minmax`, `class_weight=balanced`: this claim +1.6%, mean |gap| 1.1% (3 runs)
  - `normalize=zscore`, `class_weight=balanced`: this claim +3.9%, mean |gap| 2.2% (3 runs)
  - `normalize=zscore`: this claim +8.8%, mean |gap| 5.9% (4 runs)

### Equally good configurations
The target claim can't tell these 2 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `normalize=zscore, threshold=0.3` (reported)
- `class_weight=balanced, normalize=minmax`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting normalize=zscore, threshold=0.3 | settings | 52% | 0.0 sigma (fits every claim) | run with normalize=zscore, threshold=0.3 |
| 2 | the setting class_weight=balanced, normalize=minmax | settings | 16% | 0.3 sigma (fits every claim) | run with class_weight=balanced, normalize=minmax |
| 3 | the setting class_weight=balanced, normalize=zscore | settings | 13% | 0.7 sigma (fits every claim) | run with class_weight=balanced, normalize=zscore |

### History matching (every measured configuration, all claims together)
- 7 of 87 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 7 configurations
  - `normalize, threshold`: normalize=zscore, threshold=0.3 (max I 0); normalize=zscore, threshold=0.25 (max I 0.82)
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 0.27); class_weight=balanced, normalize=zscore (max I 0.7)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.56); lr_schedule=step, normalize=zscore (max I 1.56)
  - `normalize`: normalize=zscore (max I 1.65)

Notes:
- configurations the target claim can't tell apart from the answer: normalize=zscore, threshold=0.3; class_weight=balanced, normalize=minmax
- spec knobs no ledger assumption names (batch_size, data_seed, epochs, label_noise, lr, n, positive_rate, split, weight_decay) were screened too; no better answer
- threshold: values from 0.3 to 0.3 fit every claim (a bisection, 3 runs a side, one run a value: approximate)
- not identifiable from the paper's numbers: 1 configuration(s) of other knobs fit every claim as well as the answer (normalize=zscore, threshold=0.3: class_weight=balanced, normalize=minmax), and the paper reports no other condition that could separate them: the answer is one of them, not the identified cause

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore`, `threshold=0.3` | 4 | +0.0% | +0.0% | 0.0% |
| `normalize=minmax`, `class_weight=balanced` | 3 | +1.6% | -0.6% | 1.1% |
| `normalize=zscore`, `class_weight=balanced` | 3 | +3.9% | +0.6% | 2.2% |
| `normalize=zscore` | 4 | +8.8% | +2.9% | 5.9% |
| `lr_schedule=cosine` | 3 | -18.1% | -21.3% | 19.7% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `threshold=auto`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

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
