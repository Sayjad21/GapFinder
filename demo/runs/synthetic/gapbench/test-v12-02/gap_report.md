# Gap Report: test-v12-02

Artifact `mlbench` · generated 2026-10-23 17:56 · 179 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -17.5% | -6.2% | ±2.5% | `split=0.98`, `normalize=minmax` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Held-out claims outside noise:**
  - C2 (`balanced_accuracy`): paper 0.431, measured 0.5494 (+27.5%, band ±2.5%)
- **The paper states these, and this harness can't vary them** (they are part of what the number means):
  - `RUN_TAG`: "Numbers are medians over 7 runs with different shuffling seeds." (p.1)

## C1: test_accuracy (paper 0.6666)
**Fits but unsupported** · gap -17.5% → -6.2% · 101 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0114`, `B0149`, `B0163` (3 run(s) of the same config)
- Config: `split` naive `0.8`, changed to `0.98`
- Config: `normalize` naive `none`, changed to `minmax`
- Command:

  Replay: fork checkpoint `75235665-782b-4dc5-9fa1-eeb8c8193a9f` and run
  ```
  @ast:train.py:66:@mut.8.Call.xdiv2=0 @ast:train.py:66:@mut.8.Call.xmul2=0 RUN_TAG=72882d42d72e export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.98 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.625, 0.625, 0.625; gap after -6.2%; result checkpoint `8a5905ea-06df-4c7d-8088-b6243fe83187`
- Effect: candidate 0.625 minus naive 0.55 = +0.075, 95% bootstrap interval [+0.06164, +0.105] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> Logistic regression (ours) | 0.667 | 0.431

- p. 1, Table 1; value used: `test_accuracy` = 0.6666 (headline claim)

### What did we measure?
- Naive median 0.55 over 5 runs; repeats: 0.5583, 0.5417, 0.5125, 0.5667, 0.55
- Spread: range 0.5125 to 0.5667, noise band ±0.0166 (2 x MAD), CV 3.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -17.5% (noise band ±2.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `split` the gap is -10.6% (it comes back)
- PASS · Counterfactual (reversal test): without `normalize` the gap is -9.4% (it comes back)
- PASS · Held-out claim: C2: +27.5% to +16.0% (not worse beyond noise)
- FAIL · Evidence: `split=0.98`: no evidence mentions '0.98'; it fits, but nothing says the authors used it
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.075 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (3.77 noise units, gap -8.1%); `n=2000` (1.81 noise units, gap -13.0%); `split=0.9` (1.51 noise units, gap -13.7%); `batch_size=3` (1.51 noise units, gap -13.7%); `data_seed=4` (1.51 noise units, gap -13.7%) (and 3 more in the JSON)
- Near alternatives (closest across all claims):
  - `n=600`, `normalize=minmax`: this claim -5.0%, mean |gap| 10.5% (3 runs)
  - `normalize=minmax`: this claim -10.6%, mean |gap| 13.3% (4 runs)
  - `normalize=minmax`, `lr_schedule=cosine`: this claim -10.6%, mean |gap| 13.3% (3 runs)

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting normalize=minmax, split=0.98 | settings | 40% | 2.5 sigma (fits every claim) | run with normalize=minmax, split=0.98 |
| 2 | a cause outside every class tested | outside | 32% |  | look for code, data or evaluation differences the classes don't cover |
| 3 | the setting n=600, normalize=minmax | settings | 17% | 2.5 sigma (fits every claim) | run with n=600, normalize=minmax |

### History matching (every measured configuration, all claims together)
- 6 of 96 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 6 configurations
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=minmax (max I 2.53); lr_schedule=step, normalize=minmax (max I 2.53)
  - `normalize, split`: normalize=minmax, split=0.98 (max I 2.53); normalize=minmax, split=0.9 (max I 2.65)
  - `n, normalize`: n=600, normalize=minmax (max I 2.53)
  - `normalize`: normalize=minmax (max I 2.6)

Notes:
- found after adding spec knobs no ledger assumption names (batch_size, data_seed, epochs, label_noise, lr, n, positive_rate, split, threshold, weight_decay)
- split: values from 0.98 to 0.98 fit every claim (a bisection, 3 runs a side, one run a value: approximate)
- the paper states split = 0.8 ("The first 80% of rows are used for training and the rest for testing"), but 0.8 leaves the gap at -17.5% (beyond noise); 0.98 closes it: the stated value is likely not the one behind the paper's numbers
- the paper states normalize = none ("Features are used raw, without any scaling."), but none leaves the gap at -17.5% (beyond noise); minmax closes it: the stated value is likely not the one behind the paper's numbers

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `n=600`, `normalize=minmax` | 3 | -5.0% | +16.0% | 10.5% |
| `split=0.98`, `normalize=minmax` | 3 | -6.2% | +16.0% | 11.1% |
| `normalize=minmax` | 4 | -10.6% | +16.0% | 13.3% |
| `normalize=minmax`, `lr_schedule=cosine` | 3 | -10.6% | +16.0% | 13.3% |
| `lr_schedule=step`, `normalize=minmax` | 3 | -10.6% | +16.0% | 13.3% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made
- `split=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made
- `n=1`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Runtime trace (one dry run)
1 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`

## Provenance
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `7be36dde35aa5fcbe1cffeee1216997d960b4211d0ed734a6433b1f16ca8950d`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
