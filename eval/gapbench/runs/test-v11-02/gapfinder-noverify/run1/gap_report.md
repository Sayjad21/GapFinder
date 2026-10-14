# Gap Report: test-v11-02

Artifact `mlbench` · generated 2026-10-14 11:08 · 39 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Partially explained | -20.0% | -8.4% | ±1.3% | `lr_schedule=cosine` |

## C1: test_accuracy (paper 0.6666)
**Partially explained** · gap -20.0% → -8.4% · 13 hypotheses tested
> Plausible explanation (fits but unsupported): it closes only part of the gap, or the paper's own value was not tested

### Which experiment changed it?
- Branch: `B0008`, `B0014`, `B0015`, `B0016` (4 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `cosine`
- Command:

  Replay: fork checkpoint `d79f5734-b20b-4885-9292-d01aaa94aba4` and run
  ```
  RUN_TAG=a2eaa81ba10f "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize none --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule cosine --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.625, 0.6083, 0.6083, 0.6125; gap after -8.4%; result checkpoint `5b736137-e3b5-46f6-8d94-9647cec6e4af`
- Effect: candidate 0.6104 minus naive 0.5333 = +0.0771, 95% bootstrap interval [+0.07164, +0.0889] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.667 test accuracy and 0.485 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.6666 (headline claim)

### What did we measure?
- Naive median 0.5333 over 5 runs; repeats: 0.5375, 0.5208, 0.5375, 0.5208, 0.5333
- Spread: range 0.5208 to 0.5375, noise band ±0.0084 (2 x MAD), CV 1.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -20.0% (noise band ±1.3% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is +0.0771 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `CPU`, `memory`, `OS`, `Python_version`, `random_module`, `math_module`, `floating_point`, `disk`, `network`, `system_load`, `--out`, `thread_count`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=minmax` (7.44 noise units, gap -10.6%); `lr_schedule=step` (1 noise units, gap -18.7%)
- Near alternatives (closest across all claims):
  - `normalize=minmax`: this claim -10.6%, mean |gap| 6.9% (4 runs)
  - `normalize=minmax`, `lr_schedule=cosine`: this claim -10.6%, mean |gap| 6.9% (3 runs)
  - `normalize=minmax`, `lr_schedule=step`: this claim -10.6%, mean |gap| 6.9% (3 runs)

### History matching (every measured configuration, all claims together)
- 3 of 13 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `normalize`: normalize=minmax (max I 2.09)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=minmax (max I 2.09); lr_schedule=step, normalize=minmax (max I 2.09)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax` | 4 | -10.6% | +3.1% | 6.9% |
| `normalize=minmax`, `lr_schedule=cosine` | 3 | -10.6% | +3.1% | 6.9% |
| `normalize=minmax`, `lr_schedule=step` | 3 | -10.6% | +3.1% | 6.9% |
| `lr_schedule=step`, `class_weight=balanced` | 3 | -19.4% | +11.5% | 15.4% |
| naive (reproduction as run) | 5 | -20.0% | +11.1% | 15.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `CPU`, `memory`, `OS`, `Python_version`, `random_module`, `math_module`, `floating_point`, `disk`, `network`, `system_load`, `--out`, `thread_count`

## Provenance
- GapFinder commit: `b05f7288e1a4df8af69bb0b5e7633827b4cb46c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
