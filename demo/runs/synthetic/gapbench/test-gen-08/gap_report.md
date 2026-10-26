# Gap Report: test-gen-08

Artifact `mlbench` · generated 2026-10-23 17:47 · 191 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -9.8% | +0.0% | ±7.0% | `normalize=minmax` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Held-out claims outside noise:**
  - C2 (`balanced_accuracy`): paper 0.5, measured 0.5422 (+8.4%, band ±5.0%)
- **The paper states these, and this harness can't vary them** (they are part of what the number means):
  - `num_runs`: "Numbers are medians over 7 runs with different shuffling seeds." (p.1)
  - `train_test_split_order`: "The first 80% of rows are used for training and the rest for testing (data seed 7)." (p.1)

## C1: test_accuracy (paper 0.5958)
**Fits but unsupported** · gap -9.8% → +0.0% · 53 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0017`, `B0037`, `B0038`, `B0049`, `B0050`, `B0051` (6 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Command:

  Replay: fork checkpoint `34c6d97d-0cdd-475f-b918-0420aa89857f` and run
  ```
  RUN_TAG=b49978d54ef6 export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.5958, 0.5958, 0.5958, 0.5958, 0.5958, 0.5958; gap after +0.0%; result checkpoint `be83004c-dd14-4c00-ad99-cb6a02ff6319`
- Effect: candidate 0.5958 minus naive 0.5375 = +0.0583, 95% bootstrap interval [+0.04, +0.1258] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.596 test accuracy.

- p. 1; value used: `test_accuracy` = 0.5958 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5458, 0.5375, 0.4667, 0.475, 0.5583
- Spread: range 0.4667 to 0.5583, noise band ±0.0416 (2 x MAD), CV 8.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -9.8% (noise band ±7.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -9.8% (it comes back)
- PASS · Held-out claim: C2: +8.4% to +0.0% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.0583 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `SCALES`, `WEIGHTS`, `RUN_TAG`, `num_runs`, `train_test_split_order`, `python_version`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `epochs=750` (1.1 noise units, gap +2.1%); `epochs=10` (1 noise units, gap -2.8%); `lr_schedule=cosine` (1 noise units, gap +2.8%)
- Near alternatives (closest across all claims):
  - `epochs=10`, `normalize=minmax`: this claim +0.0%, mean |gap| 0.0% (6 runs)
  - `normalize=minmax`, `lr_schedule=cosine`: this claim +0.0%, mean |gap| 0.0% (6 runs)
  - `epochs=20`, `normalize=minmax`: this claim +0.0%, mean |gap| 0.0% (6 runs)

### Equally good configurations
The target claim can't tell these 6 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `normalize=minmax` (reported)
- `lr_schedule=cosine, normalize=minmax`
- `lr_schedule=step, normalize=minmax`
- `epochs=20, normalize=minmax`
- `epochs=10, normalize=minmax`
- `epochs=8, normalize=minmax`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting normalize=minmax | settings | 30% | 0.0 sigma (fits every claim) | run with normalize=minmax |
| 2 | the setting lr_schedule=cosine, normalize=minmax | settings | 10% | 0.0 sigma (fits every claim) | run with lr_schedule=cosine, normalize=minmax |
| 3 | the setting lr_schedule=step, normalize=minmax | settings | 10% | 0.0 sigma (fits every claim) | run with lr_schedule=step, normalize=minmax |

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `normalize`: normalize=minmax (max I 0)
  - `epochs, normalize`: epochs=10, normalize=minmax (max I 0); epochs=20, normalize=minmax (max I 0); epochs=8, normalize=minmax (max I 0); epochs=30, normalize=minmax (max I 0.63)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=minmax (max I 0); lr_schedule=step, normalize=minmax (max I 0)
  - `class_weight, epochs`: class_weight=balanced, epochs=8 (max I 0.9); class_weight=balanced, epochs=750 (max I 0.97)
  - `epochs`: epochs=10 (max I 1.32)

Notes:
- its runs spread 0.1x the naive run's noise band (reported, not used to judge)
- configurations the target claim can't tell apart from the answer: normalize=minmax; lr_schedule=cosine, normalize=minmax; lr_schedule=step, normalize=minmax; epochs=20, normalize=minmax; epochs=10, normalize=minmax; epochs=8, normalize=minmax
- spec knobs no ledger assumption names (batch_size, data_seed, label_noise, lr, n, positive_rate, split, threshold, weight_decay) were screened too; no better answer

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax` | 6 | +0.0% | +0.0% | 0.0% |
| `epochs=10`, `normalize=minmax` | 6 | +0.0% | +0.0% | 0.0% |
| `normalize=minmax`, `lr_schedule=cosine` | 6 | +0.0% | +0.0% | 0.0% |
| `epochs=20`, `normalize=minmax` | 6 | +0.0% | +0.0% | 0.0% |
| `normalize=minmax`, `epochs=8` | 6 | +0.0% | +0.0% | 0.0% |

## Runtime trace (one dry run)
1 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `SCALES`, `WEIGHTS`, `RUN_TAG`, `num_runs`, `train_test_split_order`, `python_version`

## Provenance
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `a5ee8e94932cc1397dd02c920427dbe9702911f36a6fbfee753b818e8d60994f`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
