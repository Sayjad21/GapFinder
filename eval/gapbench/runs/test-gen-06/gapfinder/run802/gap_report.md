# Gap Report: test-gen-06

Artifact `mlbench` · generated 2026-10-14 23:28 · 195 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -26.4% | -1.0% | ±4.5% | `n=12000`, `normalize=minmax` |

## C1: test_accuracy (paper 0.7417)
**Fits but unsupported** · gap -26.4% → -1.0% · 54 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0072`, `B0184`, `B0185`, `B0186`, `B0187` (5 run(s) of the same config)
- Config: `n` naive `1200`, changed to `12000`
- Config: `normalize` naive `none`, changed to `minmax`
- Command:

  Replay: fork checkpoint `ce10f1b2-34be-4bf1-a2c3-c6ab552a231a` and run
  ```
  RUN_TAG=0be6b163cf7a "${PYTHON:-python3}" train.py --n 12000 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7371, 0.7317, 0.7346, 0.7367, 0.7175; gap after -1.0%; result checkpoint `ba1b63d5-e349-4e3f-84a2-4d2224037ffe`
- Effect: candidate 0.7346 minus naive 0.5458 = +0.1888, 95% bootstrap interval [+0.1662, +0.2368] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.742 test accuracy and 0.700 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7417 (headline claim)

### What did we measure?
- Naive median 0.5458 over 5 runs; repeats: 0.5042, 0.4875, 0.5625, 0.5458, 0.5625
- Spread: range 0.4875 to 0.5625, noise band ±0.0334 (2 x MAD), CV 6.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -26.4% (noise band ±4.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `n` the gap is -19.7% (it comes back)
- PASS · Counterfactual (reversal test): without `normalize` the gap is -37.0% (it comes back)
- PASS · Held-out claim: C2: -21.6% to -3.2% (not worse beyond noise)
- FAIL · Evidence: `n=12000`: no evidence mentions '12000'; it fits, but nothing says the authors used it
- FAIL · Evidence: `normalize=minmax`: no evidence mentions 'minmax'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.1888 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `hardware`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `n=120` (3.62 noise units, gap -10.1%); `normalize=zscore` (3.25 noise units, gap +11.8%); `lr_schedule=cosine` (2.25 noise units, gap -16.3%)
- Near alternatives (closest across all claims):
  - `normalize=zscore`, `n=2400`: this claim -4.2%, mean |gap| 2.5% (5 runs)
  - `normalize=zscore`, `lr_schedule=cosine`, `n=120`: this claim -4.5%, mean |gap| 2.9% (5 runs)
  - `normalize=zscore`, `n=12000`: this claim +2.1%, mean |gap| 3.1% (5 runs)

### Equally good configurations
The target claim can't tell these 5 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `n=12000, normalize=minmax` (reported)
- `n=120, normalize=zscore`
- `n=5000, normalize=zscore`
- `n=12000, normalize=zscore`
- `lr_schedule=cosine, n=120, normalize=zscore`

### History matching (every measured configuration, all claims together)
- 18 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr_schedule, n, normalize`: lr_schedule=cosine, n=120, normalize=zscore (max I 0.62)
  - `n, normalize`: n=12000, normalize=minmax (max I 0.66); n=12000, normalize=zscore (max I 0.67); n=2400, normalize=zscore (max I 0.71); n=120, normalize=zscore (max I 0.76); +4 more
  - `lr_schedule, n`: lr_schedule=cosine, n=12000 (max I 1.69)
- Equally good values: `n` in {5000, 12000}; `normalize` in {minmax, zscore}

Notes:
- configurations the target claim can't tell apart from the answer: n=12000, normalize=minmax; n=120, normalize=zscore; n=5000, normalize=zscore; n=12000, normalize=zscore; lr_schedule=cosine, n=120, normalize=zscore
- equally good values within one noise band (measured): n in {5000, 12000}; normalize in {minmax, zscore}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax`, `n=12000` | 5 | -1.0% | -3.2% | 2.1% |
| `normalize=zscore`, `n=2400` | 5 | -4.2% | -0.7% | 2.5% |
| `normalize=zscore`, `lr_schedule=cosine`, `n=120` | 5 | -4.5% | +1.3% | 2.9% |
| `normalize=zscore`, `n=12000` | 5 | +2.1% | +4.2% | 3.1% |
| `normalize=zscore`, `n=5000` | 5 | +1.8% | +4.8% | 3.3% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `n=1`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `hardware`

## Provenance
- GapFinder commit: `efb2f63a257a40b9982099a274f2e882f272b80c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
