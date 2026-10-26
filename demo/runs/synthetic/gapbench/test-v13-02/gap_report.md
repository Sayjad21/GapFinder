# Gap Report: test-v13-02

Artifact `mlbench` · generated 2026-10-23 18:05 · 198 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -35.2% | -13.1% | ±1.0% | `lr_schedule=cosine`, `batch_size=1` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Held-out claims outside noise:**
  - C2 (`balanced_accuracy`): paper 0.8102, measured 0.5422 (-33.1%, band ±0.9%)
- **The paper states these, and this harness can't vary them** (they are part of what the number means):
  - `num_runs (implicit)`: "Numbers are medians over 7 runs with different shuffling seeds." (p.1)
  - `median_aggregation_external (implicit)`: "Numbers are medians over 7 runs with different shuffling seeds." (p.1)

## C1: test_accuracy (paper 0.8292)
**Fits but unsupported** · gap -35.2% → -13.1% · 89 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0115`, `B0145`, `B0165`, `B0166`, `B0167` (5 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `cosine`
- Config: `batch_size` naive `32`, changed to `1`
- Command:

  Replay: fork checkpoint `0f60a40f-0115-4515-b24f-f040a6b8046b` and run
  ```
  @ast:train.py:66:@mut.8.Call.xdiv2=0 @ast:train.py:66:@mut.8.Call.xmul2=0 @ast:train.py:68:@mut.37.num.add1=0 @ast:train.py:68:@mut.37.num.div2=0 @ast:train.py:68:@mut.37.num.mul2=0 @ast:train.py:68:@mut.37.num.sub1=0 RUN_TAG=27315d7b1940 export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --epochs 15 --batch_size 1 --lr 0.05 --lr_schedule cosine --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7167, 0.7208, 0.7292, 0.7292, 0.7083; gap after -13.1%; result checkpoint `7eb05176-a126-481f-98c2-a79070b3d423`
- Effect: candidate 0.7208 minus naive 0.5375 = +0.1833, 95% bootstrap interval [+0.1725, +0.2408] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.829 test accuracy and 0.810 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.8292 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.4667, 0.5458, 0.5375, 0.5375, 0.5333
- Spread: range 0.4667 to 0.5458, noise band ±0.0084 (2 x MAD), CV 6.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -35.2% (noise band ±1.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is -37.4% (it comes back)
- PASS · Counterfactual (reversal test): without `batch_size` the gap is -25.4% (it comes back)
- PASS · Held-out claim: C2: -33.1% to -13.7% (not worse beyond noise)
- PASS · Evidence: `lr_schedule=cosine`: code evidence at train.py:84: 'elif a.lr_schedule == "cosine":\n                lr = a.lr * 0.5 * (1 + math.cos(math.pi * step / steps))'
- FAIL · Evidence: `batch_size=1`: no evidence mentions '1'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.1833 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `num_runs (implicit)`, `--normalize`, `median_aggregation_external (implicit)`, `SCALES (hardcoded)`, `WEIGHTS (hardcoded)`, `weight_init_stddev (hardcoded)`, `sigmoid_clip_bound (hardcoded)`, `data_generation_intercept_formula (hardcoded)`, `batch_gradient_averaging (hardcoded)`, `shuffle_each_epoch (hardcoded)`, `python_random_module`, `bias_init_zero (hardcoded)`, `RUN_TAG_hex_parsing`, `hardware`, `random_Random_implementation`, `feature_order_fixed (SCALES/WEIGHTS order)`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `split=0.9` (4.46 noise units, gap -30.7%); `data_seed=123` (4.46 noise units, gap -30.7%); `lr=0.5` (3.96 noise units, gap -31.2%); `weight_decay=1e-3` (3.48 noise units, gap -31.7%); `n=12000` (3.32 noise units, gap -31.8%) (and 3 more in the JSON)
- Near alternatives (closest across all claims):
  - `data_seed=123`, `split=0.98`: this claim -24.6%, mean |gap| 18.0% (5 runs)
  - `batch_size=16`, `lr_schedule=cosine`: this claim -23.1%, mean |gap| 22.4% (5 runs)
  - `lr_schedule=cosine`: this claim -25.4%, mean |gap| 24.5% (6 runs)

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | a cause outside every class tested | outside | 60% |  | look for code, data or evaluation differences the classes don't cover |
| 2 | the setting batch_size=1, lr_schedule=cosine | settings | 40% | 2.4 sigma (fits every claim) | run with batch_size=1, lr_schedule=cosine |
| 3 | no difference in reporting: the numbers as printed at the end of the run | settings | 0% | 6.6 sigma | the settings search and the other classes |

### History matching (every measured configuration, all claims together)
- 1 of 89 tested configurations fit every claim within 3 sigma

Notes:
- found after adding spec knobs no ledger assumption names (batch_size, data_seed, epochs, label_noise, lr, n, positive_rate, split, threshold, weight_decay)
- batch_size: values from 1 to 1 fit every claim (a bisection, 3 runs a side, one run a value: approximate)
- the paper states batch_size = 32 ("batch size 32"), but 32 leaves the gap at -35.2% (beyond noise); 1 closes it: the stated value is likely not the one behind the paper's numbers

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `batch_size=1`, `lr_schedule=cosine` | 5 | -13.1% | -13.7% | 13.4% |
| `data_seed=123`, `split=0.98` | 5 | -24.6% | -11.3% | 18.0% |
| `batch_size=16`, `lr_schedule=cosine` | 5 | -23.1% | -21.7% | 22.4% |
| `lr_schedule=cosine` | 6 | -25.4% | -23.6% | 24.5% |
| `data_seed=123`, `split=0.9` | 5 | -25.6% | -24.2% | 24.9% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `n=1`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made
- `positive_rate=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made
- `split=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Runtime trace (one dry run)
1 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `num_runs (implicit)`, `--normalize`, `median_aggregation_external (implicit)`, `SCALES (hardcoded)`, `WEIGHTS (hardcoded)`, `weight_init_stddev (hardcoded)`, `sigmoid_clip_bound (hardcoded)`, `data_generation_intercept_formula (hardcoded)`, `batch_gradient_averaging (hardcoded)`, `shuffle_each_epoch (hardcoded)`, `python_random_module`, `bias_init_zero (hardcoded)`, `RUN_TAG_hex_parsing`, `hardware`, `random_Random_implementation`, `feature_order_fixed (SCALES/WEIGHTS order)`

## Provenance
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `0f039fdc282711cf8fae8046ee483f168c2fd2a36c2cd699ff6da459b9236b95`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
