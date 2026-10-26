# Gap Report: test-gen-07

Artifact `mlbench` · generated 2026-10-23 17:46 · 184 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | +8.8% | -0.3% | ±1.1% | `n=1000` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Held-out claims outside noise:**
  - C2 (`balanced_accuracy`): paper 0.4845, measured 0.5422 (+11.9%, band ±1.1%)
- **The paper states these, and this harness can't vary them** (they are part of what the number means):
  - `num_runs_aggregation`: "Numbers are medians over 7 runs with different shuffling seeds." (p.1)

## C1: test_accuracy (paper 0.4938)
**Fits but unsupported** · gap +8.8% → -0.3% · 92 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0061`, `B0091`, `B0092`, `B0110` (4 run(s) of the same config)
- Config: `n` naive `1200`, changed to `1000`
- Command:

  Replay: fork checkpoint `f2c4ac8e-4700-4ef5-a499-ceca0b49b92e` and run
  ```
  RUN_TAG=b1fc60cf6c0b export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; "${PYTHON:-python3}" train.py --n 1000 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize none --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.525, 0.49, 0.495, 0.49; gap after -0.3%; result checkpoint `d173d502-43fe-47cc-9450-4c175ff4068a`
- Effect: candidate 0.4925 minus naive 0.5375 = -0.045, 95% bootstrap interval [-0.0558, -0.0425] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.494 test accuracy.

- p. 1; value used: `test_accuracy` = 0.4938 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5458, 0.5458, 0.5375, 0.5375, 0.5375
- Spread: range 0.5375 to 0.5458, noise band ±0.005375 (2 x MAD), CV 0.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +8.8% (noise band ±1.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `n` the gap is +8.8% (it comes back)
- PASS · Held-out claim: C2: +11.9% to +3.6% (not worse beyond noise)
- FAIL · Evidence: `n=1000`: no evidence mentions '1000'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -0.045 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs_aggregation`, `run_seeds`, `init_scale`, `splitting_method`, `python_version`, `os`, `hardware`, `gauss_algorithm`, `random_algorithm`, `normalizer_scope`, `shuffle_per_epoch`, `loss_function`, `gradient_calculation`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `label_noise=0.025` (7.74 noise units, gap -0.4%); `label_noise=0.02` (6.98 noise units, gap +1.3%); `threshold=0.3` (6.96 noise units, gap -1.3%); `lr=0.1` (6.96 noise units, gap -1.3%); `positive_rate=0.15` (6.96 noise units, gap -1.3%) (and 15 more in the JSON)
- Near alternatives (closest across all claims):
  - `threshold=0.3`: this claim -1.3%, mean |gap| 0.7% (4 runs)
  - `label_noise=0.025`: this claim -1.3%, mean |gap| 0.9% (4 runs)
  - `positive_rate=0.1`, `lr=0.0`: this claim +0.4%, mean |gap| 1.0% (3 runs)

### Equally good configurations
The target claim can't tell these 18 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `n=1000` (reported)
- `positive_rate=0.03`
- `label_noise=0.025`
- `label_noise=0.02`
- `epochs=1`
- `split=0.08`
- `positive_rate=0.1`
- `split=0.7`
- `label_noise=0.025, positive_rate=0.1`
- `label_noise=0.02, threshold=0.3`
- `positive_rate=0.15, threshold=0.3`
- `label_noise=0.02, positive_rate=0.1`
- `lr=0.0, positive_rate=0.1`
- `label_noise=0.02, lr=0.1`
- `label_noise=0.02, lr=0.0`
- `lr=0.1, positive_rate=0.1`
- `label_noise=0.025, threshold=0.3`
- `label_noise=0.025, lr=0.0`

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting n=1000 | settings | 32% | 0.7 sigma (fits every claim) | run with n=1000 |
| 2 | the setting epochs=1 | settings | 11% | 0.4 sigma (fits every claim) | run with epochs=1 |
| 3 | the setting label_noise=0.025 | settings | 11% | 0.2 sigma (fits every claim) | run with label_noise=0.025 |

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `label_noise, threshold`: label_noise=0.02, threshold=0.3 (max I 0.25)
  - `lr, positive_rate`: lr=0.0, positive_rate=0.1 (max I 0.25)
  - `lr`: lr=0.0 (max I 0.31)
  - `label_noise`: label_noise=0.025 (max I 0.31)
  - `positive_rate`: positive_rate=0.03 (max I 0.33); positive_rate=0.15 (max I 0.41)
  - `threshold`: threshold=0.3 (max I 0.34)
  - `positive_rate, threshold`: positive_rate=0.15, threshold=0.3 (max I 0.34)
  - `epochs`: epochs=1 (max I 0.5)
  - `label_noise, lr`: label_noise=0.02, lr=0.1 (max I 0.64)
- 2 separate islands (no single-knob move joins them): label_noise=0.02, threshold=0.3; lr=0.0, positive_rate=0.1; lr=0.0 | epochs=1, label_noise=0.025, n=1000, positive_rate=0.03, split=0.7

Notes:
- configurations the target claim can't tell apart from the answer: n=1000; positive_rate=0.03; label_noise=0.025; label_noise=0.02; epochs=1; split=0.08; positive_rate=0.1; split=0.7; label_noise=0.025, positive_rate=0.1; label_noise=0.02, threshold=0.3; positive_rate=0.15, threshold=0.3; label_noise=0.02, positive_rate=0.1; lr=0.0, positive_rate=0.1; label_noise=0.02, lr=0.1; label_noise=0.02, lr=0.0; lr=0.1, positive_rate=0.1; label_noise=0.025, threshold=0.3; label_noise=0.025, lr=0.0
- found after adding spec knobs no ledger assumption names (batch_size, data_seed, epochs, label_noise, lr, n, positive_rate, split, threshold, weight_decay)
- n: values from 1000 to 1000 fit every claim (a bisection, 3 runs a side, one run a value: approximate)
- not identifiable from the paper's numbers: 10 configuration(s) of other knobs fit every claim as well as the answer (n=1000: epochs=1; label_noise=0.02, lr=0.1; label_noise=0.02, positive_rate=0.1; label_noise=0.02, threshold=0.3; label_noise=0.025; lr=0.0, positive_rate=0.1), and the paper reports no other condition that could separate them: the answer is one of them, not the identified cause
- the paper states n = 1200 ("1,200 rows"), but 1200 leaves the gap at +8.8% (beyond noise); 1000 closes it: the stated value is likely not the one behind the paper's numbers

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `threshold=0.3` | 4 | -1.3% | -0.2% | 0.7% |
| `label_noise=0.025` | 4 | -1.3% | -0.4% | 0.9% |
| `positive_rate=0.1`, `lr=0.0` | 3 | +0.4% | -1.7% | 1.0% |
| `positive_rate=0.15` | 4 | +1.7% | +1.5% | 1.6% |
| `positive_rate=0.15`, `threshold=0.3` | 3 | -1.3% | -1.9% | 1.6% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `split=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made
- `positive_rate=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made
- `n=1`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Runtime trace (one dry run)
1 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs_aggregation`, `run_seeds`, `init_scale`, `splitting_method`, `python_version`, `os`, `hardware`, `gauss_algorithm`, `random_algorithm`, `normalizer_scope`, `shuffle_per_epoch`, `loss_function`, `gradient_calculation`, `--out`

## Provenance
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `a5ee8e94932cc1397dd02c920427dbe9702911f36a6fbfee753b818e8d60994f`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
