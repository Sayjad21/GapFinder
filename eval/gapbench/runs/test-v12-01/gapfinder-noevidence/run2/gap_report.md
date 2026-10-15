# Gap Report: test-v12-01

Artifact `mlbench` · generated 2026-10-15 08:01 · 143 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -23.8% | +1.1% | ±1.2% | `n=2400`, `normalize=zscore` |

## C1: test_accuracy (paper 0.705)
**Fits but unsupported** · gap -23.8% → +1.1% · 54 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0061`, `B0110`, `B0111` (3 run(s) of the same config)
- Config: `n` naive `1200`, changed to `2400`
- Config: `normalize` naive `none`, changed to `zscore`
- Command:

  Replay: fork checkpoint `9cf438c0-d803-46bc-b266-ee4a42eb3fe7` and run
  ```
  RUN_TAG=77f33fca83b4 "${PYTHON:-python3}" train.py --n 2400 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7125, 0.7104, 0.7146; gap after +1.1%; result checkpoint `11a2ad1e-40d1-4c88-90c0-5cf4c2adbb56`
- Effect: candidate 0.7125 minus naive 0.5375 = +0.175, 95% bootstrap interval [+0.1542, +0.1788] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.705 test accuracy.

- p. 1; value used: `test_accuracy` = 0.705 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5375, 0.5625, 0.5333, 0.5375, 0.5417
- Spread: range 0.5333 to 0.5625, noise band ±0.0084 (2 x MAD), CV 2.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -23.8% (noise band ±1.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `n` the gap is +17.3% (it comes back)
- PASS · Counterfactual (reversal test): without `normalize` the gap is -19.9% (it comes back)
- PASS · Held-out claim: C2: -13.3% to +11.5% (not worse beyond noise)
- FAIL · Evidence: `n=2400`: evidence gate off: no evidence was looked for
- FAIL · Evidence: `normalize=zscore`: evidence gate off: no evidence was looked for
- PASS · Effect vs noise: candidate minus naive is +0.175 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `python_version`, `hardware`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `n=6000` (10.51 noise units, gap -11.2%); `lr_schedule=cosine` (10.42 noise units, gap -11.3%); `n=12000` (7.44 noise units, gap -14.9%); `n=24` (7.44 noise units, gap -14.9%); `normalize=minmax` (6.94 noise units, gap -15.5%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `normalize=minmax`, `n=6000`: this claim +0.2%, mean |gap| 0.4% (3 runs)
  - `lr_schedule=cosine`, `n=12000`: this claim -5.0%, mean |gap| 4.2% (3 runs)
  - `lr_schedule=cosine`, `n=120`: this claim -5.4%, mean |gap| 5.3% (3 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `n=2400, normalize=zscore` (reported)
- `n=6000, normalize=minmax`
- `n=120, normalize=zscore`

### History matching (every measured configuration, all claims together)
- 14 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `n, normalize`: n=6000, normalize=minmax (max I 0.06); n=12000, normalize=minmax (max I 1.57); n=2400, normalize=zscore (max I 2.26); n=24, normalize=minmax (max I 2.62)
  - `lr_schedule, n`: lr_schedule=cosine, n=12000 (max I 0.97); lr_schedule=cosine, n=120 (max I 1.44); lr_schedule=step, n=120 (max I 1.82); lr_schedule=cosine, n=6000 (max I 2.21); +1 more
  - `lr_schedule`: lr_schedule=cosine (max I 2.17)
- 2 separate islands (no single-knob move joins them): lr_schedule=cosine, n=12000; lr_schedule=cosine, n=120; lr_schedule=step, n=120 | n=6000, normalize=minmax; n=12000, normalize=minmax; n=2400, normalize=zscore
- Equally good values: `n` in {120, 2400}

Notes:
- evidence gate off: no evidence was checked, so this cannot be labelled Explained
- configurations the target claim can't tell apart from the answer: n=2400, normalize=zscore; n=6000, normalize=minmax; n=120, normalize=zscore
- equally good values within one noise band (measured): n in {120, 2400}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax`, `n=6000` | 3 | +0.2% | +0.5% | 0.4% |
| `lr_schedule=cosine`, `n=12000` | 3 | -5.0% | +3.5% | 4.2% |
| `lr_schedule=cosine`, `n=120` | 3 | -5.4% | +5.1% | 5.3% |
| `lr_schedule=step`, `n=120` | 3 | -5.4% | +5.1% | 5.3% |
| `lr_schedule=cosine` | 3 | -11.3% | -0.2% | 5.8% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `n=1`: invalid_value, The value n=1 is too small, resulting in an empty training subset after the data split, which causes an IndexError when the code tries to access Xtr[0]. A larger value is needed to retain at least one batch of data; retried as `n=32`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `python_version`, `hardware`, `--out`

## Provenance
- GapFinder commit: `f01fe3d9a0095f98d6304ad0543b917ca8e529eb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0009, sandbox reported $0.0000 (total $0.0009; this search; ledger extraction is included only if it shared the search's router)
