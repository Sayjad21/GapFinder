# Gap Report: test-v11-09

Artifact `mlbench` · generated 2026-10-14 12:52 · 144 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -29.3% | +3.9% | ±1.1% | `normalize=minmax`, `lr=0.905` |

## C1: test_accuracy (paper 0.7542)
**Fits but unsupported** · gap -29.3% → +3.9% · 50 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0066`, `B0121`, `B0122` (3 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `lr` naive `0.05`, changed to `0.905`
- Command:

  Replay: fork checkpoint `24ed5deb-a3e3-4398-8780-d1acc58038af` and run
  ```
  RUN_TAG=53f684f8999e "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.905 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7833, 0.8, 0.6667; gap after +3.9%; result checkpoint `9fd4eeb9-6c03-4ff0-af17-049625aae51a`
- Effect: candidate 0.7833 minus naive 0.5333 = +0.25, 95% bootstrap interval [+0.1276, +0.2717] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.754 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7542 (headline claim)

### What did we measure?
- Naive median 0.5333 over 5 runs; repeats: 0.5333, 0.5458, 0.5375, 0.5208, 0.5333
- Spread: range 0.5208 to 0.5458, noise band ±0.0084 (2 x MAD), CV 1.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -29.3% (noise band ±1.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -32.0% (it comes back)
- PASS · Counterfactual (reversal test): without `lr` the gap is -21.0% (it comes back)
- PASS · Held-out claim: C2: -25.4% to +2.5% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: evidence gate off: no evidence was looked for
- FAIL · Evidence: `lr=0.905`: evidence gate off: no evidence was looked for
- PASS · Effect vs noise: candidate minus naive is +0.25 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `aggregation`, `CPU`, `memory`, `OS`, `Python_version`, `random_module`, `floating_point`, `num_features`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (17.87 noise units, gap +9.4%); `lr_schedule=cosine` (9.93 noise units, gap -18.2%); `class_weight=balanced` (1.49 noise units, gap -27.6%)
- Near alternatives (closest across all claims):
  - `normalize=minmax`, `class_weight=balanced`: this claim +2.2%, mean |gap| 4.7% (3 runs)
  - `normalize=zscore`, `class_weight=balanced`: this claim +3.9%, mean |gap| 6.3% (3 runs)
  - `lr=0.01`, `normalize=zscore`, `lr_schedule=cosine`: this claim +8.8%, mean |gap| 9.8% (3 runs)

### History matching (every measured configuration, all claims together)
- 12 of 50 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr, normalize`: lr=0.905, normalize=minmax (max I 0.35); lr=0.905, normalize=zscore (max I 2.05); lr=0.005, normalize=zscore (max I 2.18); lr=0.1, normalize=zscore (max I 2.21); +1 more
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 1.46); class_weight=balanced, normalize=zscore (max I 1.66)
  - `lr, lr_schedule, normalize`: lr=0.01, lr_schedule=cosine, normalize=zscore (max I 2.08)
  - `normalize`: normalize=zscore (max I 2.34)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 2.35)

Notes:
- evidence gate off: no evidence was checked, so this cannot be labelled Explained

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax`, `lr=0.905` | 3 | +3.9% | +2.5% | 3.2% |
| `normalize=minmax`, `class_weight=balanced` | 3 | +2.2% | +7.2% | 4.7% |
| `normalize=zscore`, `class_weight=balanced` | 3 | +3.9% | +8.7% | 6.3% |
| `lr=0.01`, `normalize=zscore`, `lr_schedule=cosine` | 3 | +8.8% | +10.7% | 9.8% |
| `normalize=zscore`, `lr=0.905` | 3 | +9.4% | +10.5% | 10.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `aggregation`, `CPU`, `memory`, `OS`, `Python_version`, `random_module`, `floating_point`, `num_features`, `--out`

## Provenance
- GapFinder commit: `b05f7288e1a4df8af69bb0b5e7633827b4cb46c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
