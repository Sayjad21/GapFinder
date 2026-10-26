# Gap Report: test-v11-05

Artifact `mlbench` · generated 2026-10-23 17:52 · 200 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -26.9% | -2.3% | ±2.3% | `normalize=minmax`, `epochs=75` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Held-out claims outside noise:**
  - C2 (`balanced_accuracy`): paper 0.6732, measured 0.5387 (-20.0%, band ±2.1%)

## C1: test_accuracy (paper 0.7292)
**Fits but unsupported** · gap -26.9% → -2.3% · 53 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0120`, `B0134`, `B0161`, `B0162`, `B0163` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `epochs` naive `15`, changed to `75`
- Command:

  Replay: fork checkpoint `dd8105cc-54cb-489c-a8cf-f88d5675adb3` and run
  ```
  @ast:train.py:66:@mut.8.Call.xdiv2=0 @ast:train.py:66:@mut.8.Call.xmul2=0 @ast:train.py:68:@mut.37.num.add1=0 @ast:train.py:68:@mut.37.num.div2=0 @ast:train.py:68:@mut.37.num.mul2=0 @ast:train.py:68:@mut.37.num.sub1=0 RUN_TAG=68b46b1c8bef export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 75 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7, 0.7167, 0.7125, 0.7125, 0.7375; gap after -2.3%; result checkpoint `0a9cd608-f484-4bb5-9cfc-98205b506f52`
- Effect: candidate 0.7125 minus naive 0.5333 = +0.1792, 95% bootstrap interval [+0.1683, +0.2475] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.729 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7292 (headline claim)

### What did we measure?
- Naive median 0.5333 over 5 runs; repeats: 0.4833, 0.4667, 0.5333, 0.5333, 0.5417
- Spread: range 0.4667 to 0.5417, noise band ±0.0168 (2 x MAD), CV 6.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -26.9% (noise band ±2.3% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -28.3% (it comes back)
- PASS · Counterfactual (reversal test): without `epochs` the gap is -18.3% (it comes back)
- PASS · Held-out claim: C2: -20.0% to -3.1% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- FAIL · Evidence: `epochs=75`: no evidence mentions '75'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.1792 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (5.96 noise units, gap +13.1%); `lr_schedule=cosine` (4.46 noise units, gap -16.6%); `epochs=150` (2.98 noise units, gap -20.0%); `epochs=2` (1.24 noise units, gap -24.0%)
- Near alternatives (closest across all claims):
  - `lr_schedule=cosine`, `epochs=150`: this claim -2.3%, mean |gap| 2.5% (6 runs)
  - `epochs=750`, `lr_schedule=step`: this claim +3.4%, mean |gap| 5.0% (5 runs)
  - `lr_schedule=cosine`, `epochs=75`: this claim -8.6%, mean |gap| 5.5% (5 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `epochs=75, normalize=minmax` (reported)
- `epochs=750, lr_schedule=step`
- `epochs=150, lr_schedule=cosine`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting epochs=75, normalize=minmax | settings | 53% | 0.4 sigma (fits every claim) | run with epochs=75, normalize=minmax |
| 2 | the setting epochs=150, lr_schedule=cosine | settings | 17% | 0.4 sigma (fits every claim) | run with epochs=150, lr_schedule=cosine |
| 3 | the setting epochs=750, lr_schedule=step | settings | 16% | 0.7 sigma (fits every claim) | run with epochs=750, lr_schedule=step |

### History matching (every measured configuration, all claims together)
- 15 of 56 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `epochs, normalize`: epochs=75, normalize=minmax (max I 0.39); epochs=150, normalize=minmax (max I 1.58)
  - `epochs, lr_schedule`: epochs=150, lr_schedule=cosine (max I 0.43); epochs=750, lr_schedule=step (max I 0.66); epochs=75, lr_schedule=cosine (max I 1.41); epochs=750, lr_schedule=cosine (max I 2.07); +2 more
  - `lr_schedule`: lr_schedule=cosine (max I 2.44)
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 2.56)
- 4 separate islands (no single-knob move joins them): epochs=150, lr_schedule=cosine; epochs=750, lr_schedule=step; epochs=75, lr_schedule=cosine | epochs=75, normalize=minmax; epochs=150, normalize=minmax | class_weight=balanced, normalize=minmax; class_weight=balanced, normalize=zscore | epochs=2, normalize=zscore

Notes:
- configurations the target claim can't tell apart from the answer: epochs=75, normalize=minmax; epochs=750, lr_schedule=step; epochs=150, lr_schedule=cosine
- spec knobs no ledger assumption names (batch_size, data_seed, label_noise, lr, n, positive_rate, split, threshold, weight_decay) were screened too; no better answer
- value interval stopped early: run budget of 200 reached (wanted 1 more run(s) of {'normalize': 'minmax', 'epochs': '47'} for 'interval epochs=47')
- not identifiable from the paper's numbers: 1 configuration(s) of other knobs fit every claim as well as the answer (epochs=75, normalize=minmax: epochs=150, lr_schedule=cosine), and the paper reports no other condition that could separate them: the answer is one of them, not the identified cause

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=cosine`, `epochs=150` | 6 | -2.3% | +2.6% | 2.5% |
| `normalize=minmax`, `epochs=75` | 5 | -2.3% | -3.1% | 2.7% |
| `epochs=750`, `lr_schedule=step` | 5 | +3.4% | +6.6% | 5.0% |
| `lr_schedule=cosine`, `epochs=75` | 5 | -8.6% | -2.4% | 5.5% |
| `normalize=minmax`, `epochs=150` | 5 | +6.3% | +9.9% | 8.1% |

## Runtime trace (one dry run)
1 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`

## Provenance
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `1fd3d59022925491b04c41fd5e5ed48e25739b360d0d1093aefdff9298c5fcf4`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
