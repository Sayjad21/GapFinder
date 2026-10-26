# Gap Report: test-v13-05

Artifact `mlbench` · generated 2026-10-23 18:08 · 149 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -31.6% | +6.4% | ±11.8% | `normalize=zscore` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Held-out claims outside noise:**
  - C2 (`balanced_accuracy`): paper 0.75, measured 0.5387 (-28.2%, band ±12.7%)
- **The paper states these, and this harness can't vary them** (they are part of what the number means):
  - `number_of_runs`: "Numbers are medians over 7 runs with different shuffling seeds." (p.1)
  - `aggregation_method`: "Numbers are medians over 7 runs with different shuffling seeds." (p.1)
  - `shuffling_seed_generation`: "different shuffling seeds" (p.1)

## C1: test_accuracy (paper 0.7792)
**Fits but unsupported** · gap -31.6% → +6.4% · 51 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0020`, `B0030`, `B0031`, `B0032`, `B0033`, `B0034` (6 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Command:

  Replay: fork checkpoint `e4b8b6ed-ba20-4abc-96a0-03b4c77b6a23` and run
  ```
  RUN_TAG=3f2971935eef export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.8292, 0.8292, 0.8292, 0.8292, 0.825, 0.8292; gap after +6.4%; result checkpoint `d0a3d218-54ae-464d-93fe-aa66ace38ff1`
- Effect: candidate 0.8292 minus naive 0.5333 = +0.2959, 95% bootstrap interval [+0.2542, +0.345] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.779 test accuracy and 0.750 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7792 (headline claim)

### What did we measure?
- Naive median 0.5333 over 5 runs; repeats: 0.5375, 0.4875, 0.4792, 0.5958, 0.5333
- Spread: range 0.4792 to 0.5958, noise band ±0.0916 (2 x MAD), CV 8.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -31.6% (noise band ±11.8% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -31.6% (it comes back)
- PASS · Held-out claim: C2: -28.2% to +8.0% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2959 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `number_of_runs`, `aggregation_method`, `SCALES`, `WEIGHTS`, `shuffling_seed_generation`, `out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives (closest across all claims):
  - `label_noise=0.905`, `normalize=zscore`: this claim +0.8%, mean |gap| 1.4% (6 runs)
  - `class_weight=balanced`, `normalize=zscore`: this claim +0.5%, mean |gap| 2.6% (6 runs)
  - `normalize=minmax`, `class_weight=balanced`: this claim -2.1%, mean |gap| 2.8% (6 runs)

### Equally good configurations
The target claim can't tell these 4 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `normalize=zscore` (reported)
- `class_weight=balanced, normalize=zscore`
- `label_noise=0.905, normalize=zscore`
- `class_weight=balanced, normalize=minmax`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting label_noise=0.905, normalize=zscore | settings | 19% | 0.3 sigma (fits every claim) | run with label_noise=0.905, normalize=zscore |
| 2 | the setting normalize=zscore | settings | 17% | 1.3 sigma (fits every claim) | run with normalize=zscore |
| 3 | the setting class_weight=balanced, normalize=minmax | settings | 16% | 0.5 sigma (fits every claim) | run with class_weight=balanced, normalize=minmax |

### History matching (every measured configuration, all claims together)
- 20 of 51 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `label_noise, normalize`: label_noise=0.905, normalize=zscore (max I 0.33); label_noise=0.1, normalize=zscore (max I 0.83)
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 0.52); class_weight=balanced, normalize=zscore (max I 0.77)
  - `epochs, normalize`: epochs=30, normalize=zscore (max I 1.17); epochs=150, normalize=zscore (max I 1.18); epochs=20, normalize=zscore (max I 1.19); epochs=2, normalize=zscore (max I 1.22)
  - `normalize`: normalize=zscore (max I 1.26)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.27)

Notes:
- its runs spread 0.1x the naive run's noise band (reported, not used to judge)
- configurations the target claim can't tell apart from the answer: normalize=zscore; class_weight=balanced, normalize=zscore; label_noise=0.905, normalize=zscore; class_weight=balanced, normalize=minmax
- spec knobs no ledger assumption names (batch_size, data_seed, lr, n, positive_rate, split, threshold, weight_decay) were screened too; no better answer
- not identifiable from the paper's numbers: 1 configuration(s) of other knobs fit every claim as well as the answer (normalize=zscore: class_weight=balanced, normalize=minmax), and the paper reports no other condition that could separate them: the answer is one of them, not the identified cause
- the paper states normalize = none ("Features are used raw, without any scaling."), but none leaves the gap at -31.6% (beyond noise); zscore closes it: the stated value is likely not the one behind the paper's numbers

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `label_noise=0.905`, `normalize=zscore` | 6 | +0.8% | +2.0% | 1.4% |
| `class_weight=balanced`, `normalize=zscore` | 6 | +0.5% | +4.7% | 2.6% |
| `normalize=minmax`, `class_weight=balanced` | 6 | -2.1% | +3.5% | 2.8% |
| `label_noise=0.1`, `normalize=zscore` | 6 | +4.0% | +5.3% | 4.6% |
| `normalize=zscore`, `epochs=30` | 6 | +5.9% | +7.6% | 6.7% |

## Runtime trace (one dry run)
1 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `number_of_runs`, `aggregation_method`, `SCALES`, `WEIGHTS`, `shuffling_seed_generation`, `out`

## Provenance
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `a5ee8e94932cc1397dd02c920427dbe9702911f36a6fbfee753b818e8d60994f`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
