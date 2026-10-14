# Gap Report: test-v11-03

Artifact `mlbench` · generated 2026-10-14 11:44 · 198 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -31.4% | +0.0% | ±1.1% | `label_noise=0.905`, `normalize=zscore` |

## C1: test_accuracy (paper 0.7833)
**Fits but unsupported** · gap -31.4% → +0.0% · 64 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0139`, `B0191`, `B0192`, `B0193`, `B0194` (5 run(s) of the same config)
- Config: `label_noise` naive `0.05`, changed to `0.905`
- Config: `normalize` naive `none`, changed to `zscore`
- Command:

  Replay: fork checkpoint `6cde7572-2311-4c13-84bd-3a2b20609b6b` and run
  ```
  RUN_TAG=125aed7e199d "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.905 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7833, 0.7833, 0.7833, 0.7833, 0.7833; gap after +0.0%; result checkpoint `e5a8994b-12e5-414f-8603-ad9b29a0f3ca`
- Effect: candidate 0.7833 minus naive 0.5375 = +0.2458, 95% bootstrap interval [+0.2424, +0.3133] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.783 test accuracy and 0.752 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7833 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.4667, 0.5417, 0.4833, 0.5375, 0.5375
- Spread: range 0.4667 to 0.5417, noise band ±0.0084 (2 x MAD), CV 6.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -31.4% (noise band ±1.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `label_noise` the gap is +5.3% (it comes back)
- PASS · Counterfactual (reversal test): without `normalize` the gap is -30.8% (it comes back)
- PASS · Held-out claim: C2: -27.9% to +1.5% (not worse beyond noise)
- FAIL · Evidence: `label_noise=0.905`: evidence gate off: no evidence was looked for
- FAIL · Evidence: `normalize=zscore`: evidence gate off: no evidence was looked for
- PASS · Effect vs noise: candidate minus naive is +0.2458 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `aggregation_method`, `run_tag_seeds`, `cpu`, `memory`, `os`, `python_version`, `random_module`, `disk`, `network`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (10.92 noise units, gap -19.7%); `normalize=minmax` (6.94 noise units, gap -23.9%); `batch_size=3` (3.48 noise units, gap -27.7%); `positive_rate=0.15` (1.99 noise units, gap -29.2%); `label_noise=0.0` (1.99 noise units, gap -29.2%)
- Near alternatives (closest across all claims):
  - `normalize=zscore`, `positive_rate=0.15`: this claim -0.5%, mean |gap| 5.1% (5 runs)
  - `batch_size=3`, `normalize=zscore`: this claim +5.3%, mean |gap| 6.2% (5 runs)
  - `normalize=zscore`: this claim +5.3%, mean |gap| 6.3% (6 runs)

### History matching (every measured configuration, all claims together)
- 12 of 63 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `batch_size, normalize`: batch_size=3, normalize=minmax (max I 0.03); batch_size=320, normalize=zscore (max I 1.15); batch_size=3, normalize=zscore (max I 1.16)
  - `label_noise, normalize`: label_noise=0.905, normalize=zscore (max I 0.25); label_noise=0.0, normalize=zscore (max I 1.32)
  - `lr_schedule, normalize`: lr_schedule=step, normalize=zscore (max I 1); lr_schedule=cosine, normalize=zscore (max I 1.27)
  - `normalize`: normalize=zscore (max I 1.23)
  - `normalize, positive_rate`: normalize=zscore, positive_rate=0.15 (max I 1.64)
  - `batch_size, lr_schedule`: batch_size=3, lr_schedule=cosine (max I 1.88)
- 4 separate islands (no single-knob move joins them): batch_size=3, normalize=minmax; label_noise=0.905, normalize=zscore; lr_schedule=step, normalize=zscore | batch_size=3, lr_schedule=cosine | lr_schedule=cosine, positive_rate=0.15 | label_noise=0.0, lr_schedule=cosine

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'normalize': 'zscore', 'positive_rate': '0.001'} for 'confirm-combo')
- evidence gate off: no evidence was checked, so this cannot be labelled Explained
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `label_noise=0.905`, `normalize=zscore` | 5 | +0.0% | +1.5% | 0.8% |
| `normalize=zscore`, `positive_rate=0.15` | 5 | -0.5% | -9.6% | 5.1% |
| `batch_size=3`, `normalize=zscore` | 5 | +5.3% | +7.1% | 6.2% |
| `normalize=zscore` | 6 | +5.3% | +7.3% | 6.3% |
| `batch_size=320`, `normalize=zscore` | 5 | +5.3% | +7.3% | 6.3% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: invalid_value, Setting positive_rate to 0.0 causes a math domain error when computing log(positive_rate/(1-positive_rate)) because log(0) is undefined. A small positive value like 0.001 preserves the intent of a near-zero positive rate while avoiding the domain error; retried as `positive_rate=0.001`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `aggregation_method`, `run_tag_seeds`, `cpu`, `memory`, `os`, `python_version`, `random_module`, `disk`, `network`

## Provenance
- GapFinder commit: `b05f7288e1a4df8af69bb0b5e7633827b4cb46c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0006, sandbox reported $0.0000 (total $0.0006; this search; ledger extraction is included only if it shared the search's router)
