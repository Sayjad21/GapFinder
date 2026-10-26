# Gap Report: test-gen-04

Artifact `mlbench` · generated 2026-10-23 17:43 · 50 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Paper-artifact inconsistency | -33.8% | +0.5% | ±4.0% | `normalize=zscore` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Held-out claims outside noise:**
  - C2 (`balanced_accuracy`): paper 0.8067, measured 0.5492 (-31.9%, band ±1.8%)
- **The paper states these, and this harness can't vary them** (they are part of what the number means):
  - `num_runs`: "Numbers are medians over 7 runs with different shuffling seeds." (p.1)

## C1: test_accuracy (paper 0.825)
**Paper-artifact inconsistency** · gap -33.8% → +0.5% · 13 hypotheses tested
> Confirmed cause: reverting it brings the gap back, held-out claims hold, and the value has evidence

### Which experiment changed it?
- Branch: `B0008`, `B0013`, `B0014`, `B0015`, `B0016`, `B0017` (6 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Command:

  Replay: fork checkpoint `8a7cdcc1-7dd6-44b0-9582-f87b1df673bd` and run
  ```
  RUN_TAG=83f655865f2b export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.8292, 0.8292, 0.825, 0.8292, 0.8292, 0.8292; gap after +0.5%; result checkpoint `fbb665bd-a222-4c89-b6f5-971d2aca2c7b`
- Effect: candidate 0.8292 minus naive 0.5458 = +0.2834, 95% bootstrap interval [+0.2709, +0.3458] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.825 test accuracy and 0.807 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.825 (headline claim)

### What did we measure?
- Naive median 0.5458 over 5 runs; repeats: 0.5458, 0.475, 0.55, 0.5625, 0.4875
- Spread: range 0.475 to 0.5625, noise band ±0.0334 (2 x MAD), CV 7.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -33.8% (noise band ±4.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -33.8% (it comes back)
- PASS · Held-out claim: C2: -31.9% to +0.4% (not worse beyond noise)
- PASS · Evidence: `normalize=zscore`: paper states 'zscore'
- PASS · Effect vs noise: candidate minus naive is +0.2834 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `python_version`, `os`, `cpu`, `memory`, `disk`, `PYTHONHASHSEED`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (2.25 noise units, gap -24.8%); `normalize=minmax` (1.5 noise units, gap -27.8%)
- Near alternatives (closest across all claims):
  - `lr_schedule=cosine`, `normalize=zscore`: this claim +0.5%, mean |gap| 0.5% (6 runs)
  - `normalize=zscore`, `lr_schedule=step`: this claim +0.5%, mean |gap| 0.5% (6 runs)
  - `normalize=zscore`, `class_weight=balanced`: this claim -5.1%, mean |gap| 3.9% (5 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `normalize=zscore` (reported)
- `lr_schedule=step, normalize=zscore`
- `lr_schedule=cosine, normalize=zscore`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting normalize=zscore | settings | 50% | 0.1 sigma (fits every claim) | run with normalize=zscore |
| 2 | the setting lr_schedule=step, normalize=zscore | settings | 17% | 0.1 sigma (fits every claim) | run with lr_schedule=step, normalize=zscore |
| 3 | the setting lr_schedule=cosine, normalize=zscore | settings | 17% | 0.1 sigma (fits every claim) | run with lr_schedule=cosine, normalize=zscore |

### History matching (every measured configuration, all claims together)
- 5 of 13 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 5 configurations
  - `normalize`: normalize=zscore (max I 0.07)
  - `lr_schedule, normalize`: lr_schedule=step, normalize=zscore (max I 0.07); lr_schedule=cosine, normalize=zscore (max I 0.09)
  - `class_weight, normalize`: class_weight=balanced, normalize=zscore (max I 0.84); class_weight=balanced, normalize=minmax (max I 0.97)

Notes:
- its runs spread 0.2x the naive run's noise band (reported, not used to judge)
- configurations the target claim can't tell apart from the answer: normalize=zscore; lr_schedule=step, normalize=zscore; lr_schedule=cosine, normalize=zscore

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore` | 6 | +0.5% | +0.4% | 0.5% |
| `lr_schedule=cosine`, `normalize=zscore` | 6 | +0.5% | +0.4% | 0.5% |
| `normalize=zscore`, `lr_schedule=step` | 6 | +0.5% | +0.4% | 0.5% |
| `normalize=zscore`, `class_weight=balanced` | 5 | -5.1% | -2.7% | 3.9% |
| `lr_schedule=cosine` | 6 | -24.8% | -23.3% | 24.0% |

## Runtime trace (one dry run)
1 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `python_version`, `os`, `cpu`, `memory`, `disk`, `PYTHONHASHSEED`, `--out`

## Provenance
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `a5ee8e94932cc1397dd02c920427dbe9702911f36a6fbfee753b818e8d60994f`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
