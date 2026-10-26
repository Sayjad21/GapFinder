# Gap Report: test-v11-03

Artifact `mlbench` · generated 2026-10-23 17:49 · 146 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -39.4% | +5.6% | ±2.1% | `normalize=zscore` |

## Audit of the reproduction
What a matching number doesn't show. The protocol tests below were run; the rest is static.
- **Held-out claims outside noise:**
  - C2 (`balanced_accuracy`): paper 0.7519, measured 0.4699 (-37.5%, band ±2.3%)
- **The paper states these, and this harness can't vary them** (they are part of what the number means):
  - `NUM_RUNS`: "Numbers are medians over 7 runs with different shuffling seeds." (p.1)
  - `AGGREGATION_METHOD`: "Numbers are medians over 7 runs with different shuffling seeds." (p.1)

## C1: test_accuracy (paper 0.7833)
**Fits but unsupported** · gap -39.4% → +5.6% · 35 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0022`, `B0049`, `B0050`, `B0115` (4 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Command:

  Replay: fork checkpoint `2560acb3-bca2-4af5-a027-b2c1516f675c` and run
  ```
  @ast:train.py:66:@mut.8.Call.xdiv2=0 @ast:train.py:66:@mut.8.Call.xmul2=0 @ast:train.py:68:@mut.37.num.add1=0 @ast:train.py:68:@mut.37.num.div2=0 @ast:train.py:68:@mut.37.num.mul2=0 @ast:train.py:68:@mut.37.num.sub1=0 RUN_TAG=0bb48d1868e7 export PYTHONPATH="${PYTHONPATH:+$PYTHONPATH${GF_PATHSEP:-:}}${WORK:-$PWD}/.gf_runtime"; "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.825, 0.825, 0.8292, 0.8292; gap after +5.6%; result checkpoint `e4dc9923-dffc-43ab-b322-ee07eb349a12`
- Effect: candidate 0.8271 minus naive 0.475 = +0.3521, 95% bootstrap interval [+0.3439, +0.3625] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.783 test accuracy and 0.752 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7833 (headline claim)

### What did we measure?
- Naive median 0.475 over 5 runs; repeats: 0.4833, 0.4792, 0.475, 0.4667, 0.4667
- Spread: range 0.4667 to 0.4833, noise band ±0.0166 (2 x MAD), CV 1.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -39.4% (noise band ±2.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -39.4% (it comes back)
- PASS · Held-out claim: C2: -37.5% to +7.5% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.3521 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `NUM_RUNS`, `AGGREGATION_METHOD`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (8.78 noise units, gap -20.7%); `normalize=minmax` (7.28 noise units, gap -23.9%); `batch_size=16` (5.77 noise units, gap -27.1%); `batch_size=128` (4.27 noise units, gap -30.3%); `batch_size=320` (4.27 noise units, gap -30.3%) (and 17 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=cosine`: this claim -19.7%, mean |gap| 18.3% (3 runs)
  - `batch_size=1`: this claim -26.3%, mean |gap| 25.2% (4 runs)
  - `normalize=minmax`: this claim -23.9%, mean |gap| 28.7% (3 runs)

### Differential diagnosis (every class on one scale: the likelihood of all the claims)
| rank | explanation | class | posterior | worst claim | how to check |
|---|---|---|---|---|---|
| 1 | the setting normalize=zscore | settings | 98% | 1.5 sigma (fits every claim) | run with normalize=zscore |
| 2 | a cause outside every class tested | outside | 2% |  | look for code, data or evaluation differences the classes don't cover |
| 3 | no difference in reporting: the numbers as printed at the end of the run | settings | 0% | 7.8 sigma | the settings search and the other classes |

### History matching (every measured configuration, all claims together)
- 1 of 37 tested configurations fit every claim within 3 sigma

Notes:
- spec knobs no ledger assumption names (data_seed, epochs, lr, n, split, threshold, weight_decay) were screened too; no better answer
- the paper states normalize = none ("Features are used raw, without any scaling."), but none leaves the gap at -39.4% (beyond noise); zscore closes it: the stated value is likely not the one behind the paper's numbers

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore` | 4 | +5.6% | +7.5% | 6.6% |
| `lr_schedule=cosine` | 3 | -19.7% | -17.0% | 18.3% |
| `batch_size=1` | 4 | -26.3% | -24.0% | 25.2% |
| `normalize=minmax` | 3 | -23.9% | -33.5% | 28.7% |
| `batch_size=320` | 4 | -30.9% | -27.5% | 29.2% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Runtime trace (one dry run)
1 process(es) traced. Each role comes from the sink the knob's value reached, not from its name.

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `NUM_RUNS`, `AGGREGATION_METHOD`

## Provenance
- GapFinder commit: `deea98f13b20d8fc0dab22dbabfc6925648c1a6d` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `c3eb66989927b367ea581a7b15e2a10cce28685eb22df703c39223b64c3dacea`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `1fd3d59022925491b04c41fd5e5ed48e25739b360d0d1093aefdff9298c5fcf4`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
