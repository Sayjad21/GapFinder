# Gap Report: test-v11-08

Artifact `mlbench` · generated 2026-10-23 17:53 · 169 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -9.8% | +0.0% | ±1.4% | `normalize=minmax` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Held-out claims outside noise:**
  - C2 (`balanced_accuracy`): paper 0.5, measured 0.5387 (+7.7%, band ±1.4%)

## C1: test_accuracy (paper 0.5958)
**Fits but unsupported** · gap -9.8% → +0.0% · 102 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0009`, `B0013`, `B0014`, `B0015` (4 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Command:

  Replay: fork checkpoint `652bbf54-cff9-4621-9272-4a41a79065cb` and run
  ```
  RUN_TAG=fa80a1571983 export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.5958, 0.5958, 0.5958, 0.5958; gap after +0.0%; result checkpoint `e05bf3bd-819d-4fec-998e-cf7a81a238b8`
- Effect: candidate 0.5958 minus naive 0.5375 = +0.0583, 95% bootstrap interval [+0.05166, +0.0983] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.596 test accuracy and 0.500 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.5958 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5458, 0.5333, 0.5375, 0.5375, 0.4875
- Spread: range 0.4875 to 0.5458, noise band ±0.0084 (2 x MAD), CV 4.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -9.8% (noise band ±1.4% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -9.8% (it comes back)
- PASS · Held-out claim: C2: +7.7% to +0.0% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.0583 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (3.96 noise units, gap +4.2%)
- Near alternatives (closest across all claims):
  - `lr_schedule=cosine`, `normalize=minmax`: this claim +0.0%, mean |gap| 0.0% (4 runs)
  - `lr_schedule=step`, `normalize=minmax`: this claim +0.0%, mean |gap| 0.0% (4 runs)
  - `batch_size=320`, `normalize=minmax`: this claim +0.0%, mean |gap| 0.0% (4 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `normalize=minmax` (reported)
- `lr_schedule=cosine, normalize=minmax`
- `lr_schedule=step, normalize=minmax`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting normalize=minmax | settings | 37% | 0.0 sigma (fits every claim) | run with normalize=minmax |
| 2 | the setting lr_schedule=cosine, normalize=minmax | settings | 12% | 0.0 sigma (fits every claim) | run with lr_schedule=cosine, normalize=minmax |
| 3 | the setting lr_schedule=step, normalize=minmax | settings | 12% | 0.0 sigma (fits every claim) | run with lr_schedule=step, normalize=minmax |

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `normalize`: normalize=minmax (max I 0)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=minmax (max I 0); lr_schedule=step, normalize=minmax (max I 0)
  - `batch_size, normalize`: batch_size=320, normalize=minmax (max I 0)
  - `n, normalize`: n=2000, normalize=minmax (max I 0.6)
  - `data_seed, normalize`: data_seed=4, normalize=minmax (max I 1.17)
  - `data_seed`: data_seed=14 (max I 1.27)
  - `batch_size, lr_schedule`: batch_size=320, lr_schedule=step (max I 1.27)
  - `threshold`: threshold=0.7 (max I 1.32)
  - `label_noise`: label_noise=0.905 (max I 1.36)

Notes:
- configurations the target claim can't tell apart from the answer: normalize=minmax; lr_schedule=cosine, normalize=minmax; lr_schedule=step, normalize=minmax
- spec knobs no ledger assumption names (batch_size, data_seed, epochs, label_noise, lr, n, positive_rate, split, threshold, weight_decay) were screened too; no better answer

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax` | 4 | +0.0% | +0.0% | 0.0% |
| `lr_schedule=cosine`, `normalize=minmax` | 4 | +0.0% | +0.0% | 0.0% |
| `lr_schedule=step`, `normalize=minmax` | 4 | +0.0% | +0.0% | 0.0% |
| `batch_size=320`, `normalize=minmax` | 4 | +0.0% | +0.0% | 0.0% |
| `n=2000`, `normalize=minmax` | 3 | +2.8% | +3.1% | 3.0% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `n=1`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made
- `positive_rate=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made
- `split=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Runtime trace (one dry run)
1 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `a5ee8e94932cc1397dd02c920427dbe9702911f36a6fbfee753b818e8d60994f`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
