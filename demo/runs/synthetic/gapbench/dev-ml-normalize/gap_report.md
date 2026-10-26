# Gap Report: dev-ml-normalize

Artifact `mlbench` · generated 2026-10-23 17:37 · 156 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -35.7% | -0.5% | ±1.0% | `normalize=zscore` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Held-out claims outside noise:**
  - C2 (`balanced_accuracy`): paper 0.8102, measured 0.5387 (-33.5%, band ±0.9%)
- **The paper states these, and this harness can't vary them** (they are part of what the number means):
  - `median aggregation over runs`: "All numbers are medians over seven runs with different shuffling seeds" (p.1)
  - `shuffling seed per run`: "medians over seven runs with different shuffling seeds" (p.1)

## C1: test_accuracy (paper 0.8292)
**Fits but unsupported** · gap -35.7% → -0.5% · 69 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0008`, `B0013`, `B0014`, `B0023`, `B0024`, `B0025` (6 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Command:

  Replay: fork checkpoint `6a8d2f18-08cd-4251-b9c7-c47e541973cf` and run
  ```
  RUN_TAG=415dac617ac8 export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.8292, 0.825, 0.825, 0.825, 0.825, 0.825; gap after -0.5%; result checkpoint `fa549b8d-581c-4fa4-b7d3-54a32446d83d`
- Effect: candidate 0.825 minus naive 0.5333 = +0.2917, 95% bootstrap interval [+0.2875, +0.3583] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic credit-screening dataset and show it reaches 0.829 test accuracy, competitive with far larger models.

- p. 1; value used: `test_accuracy` = 0.8292 accuracy (headline claim)

### What did we measure?
- Naive median 0.5333 over 5 runs; repeats: 0.4667, 0.4667, 0.5375, 0.5333, 0.5375
- Spread: range 0.4667 to 0.5375, noise band ±0.0084 (2 x MAD), CV 7.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -35.7% (noise band ±1.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -35.7% (it comes back)
- PASS · Held-out claim: C2: -33.5% to -0.4% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2917 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `median aggregation over runs`, `shuffling seed per run`, `SCALES`, `WEIGHTS`, `hardware`, `OS`, `Python version`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (10.92 noise units, gap -24.6%); `normalize=minmax` (7.44 noise units, gap -28.1%); `lr_schedule=step` (3.48 noise units, gap -32.2%); `class_weight=balanced` (3.48 noise units, gap -32.2%)
- Near alternatives (closest across all claims):
  - `lr_schedule=cosine`, `normalize=zscore`: this claim +0.0%, mean |gap| 0.0% (6 runs)
  - `lr_schedule=step`, `normalize=zscore`: this claim +0.0%, mean |gap| 0.0% (6 runs)
  - `class_weight=balanced`, `normalize=zscore`: this claim -5.0%, mean |gap| 3.9% (5 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `normalize=zscore` (reported)
- `lr_schedule=cosine, normalize=zscore`
- `lr_schedule=step, normalize=zscore`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting normalize=zscore | settings | 50% | 0.1 sigma (fits every claim) | run with normalize=zscore |
| 2 | the setting lr_schedule=cosine, normalize=zscore | settings | 17% | 0.0 sigma (fits every claim) | run with lr_schedule=cosine, normalize=zscore |
| 3 | the setting lr_schedule=step, normalize=zscore | settings | 17% | 0.0 sigma (fits every claim) | run with lr_schedule=step, normalize=zscore |

### History matching (every measured configuration, all claims together)
- 5 of 66 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 5 configurations
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 0); lr_schedule=step, normalize=zscore (max I 0)
  - `normalize`: normalize=zscore (max I 0.07)
  - `class_weight, normalize`: class_weight=balanced, normalize=zscore (max I 0.88); class_weight=balanced, normalize=minmax (max I 0.92)

Notes:
- configurations the target claim can't tell apart from the answer: normalize=zscore; lr_schedule=cosine, normalize=zscore; lr_schedule=step, normalize=zscore
- spec knobs no ledger assumption names (batch_size, data_seed, epochs, label_noise, lr, n, positive_rate, split, threshold, weight_decay) were screened too; no better answer

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=cosine`, `normalize=zscore` | 6 | +0.0% | +0.0% | 0.0% |
| `lr_schedule=step`, `normalize=zscore` | 6 | +0.0% | +0.0% | 0.0% |
| `normalize=zscore` | 6 | -0.5% | -0.4% | 0.5% |
| `class_weight=balanced`, `normalize=zscore` | 5 | -5.0% | -2.7% | 3.9% |
| `lr_schedule=cosine` | 6 | -25.4% | -23.8% | 24.6% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `n=1`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made
- `positive_rate=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made
- `split=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Runtime trace (one dry run)
1 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `median aggregation over runs`, `shuffling seed per run`, `SCALES`, `WEIGHTS`, `hardware`, `OS`, `Python version`, `--out`

## Provenance
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `a5ee8e94932cc1397dd02c920427dbe9702911f36a6fbfee753b818e8d60994f`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
