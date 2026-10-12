# Gap Report: test-gen-01

Artifact `mlbench` · generated 2026-10-12 23:07 · 27 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Partially explained | -24.0% | +9.0% | ±1.2% | `normalize=minmax`, `class_weight=balanced` |

## C1: test_accuracy (paper 0.7069)
**Partially explained** · gap -24.0% → +9.0% · 8 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0021`, `B0026`, `B0027` (3 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Config: `class_weight` naive `none`, changed to `balanced`
- Command:

  Replay: fork checkpoint `41aaf73e-61b5-4413-8119-f461e2a881d9` and run
  ```
  RUN_TAG=c6a9334f79c5 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight balanced --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.7708, 0.7708, 0.7708; gap after +9.0%; result checkpoint `35e96978-b6de-4b4d-aca9-9ed243fb613b`
- Effect: candidate 0.7708 minus naive 0.5375 = +0.2333, 95% bootstrap interval [+0.22, +0.235] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.707 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7069 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5375, 0.5583, 0.5458, 0.5375, 0.5333
- Spread: range 0.5333 to 0.5583, noise band ±0.0084 (2 x MAD), CV 1.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -24.0% (noise band ±1.2% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is +0.2333 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `shuffling_seeds`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `python_version`, `os`, `cpu_architecture`, `memory_size`, `disk_type`, `math_library`, `float_precision`, `random_module_implementation`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (10.92 noise units, gap -11.0%); `normalize=zscore` (5.61 noise units, gap +17.3%); `lr_schedule=step` (1.49 noise units, gap -22.2%)
- Near alternatives (closest across all claims):
  - `normalize=minmax`: this claim -15.7%, mean |gap| 18.7% (3 runs)
  - `normalize=minmax`, `lr_schedule=cosine`: this claim -15.7%, mean |gap| 18.7% (3 runs)
  - `lr_schedule=step`: this claim -22.2%, mean |gap| 27.7% (3 runs)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax` | 3 | -15.7% | +21.6% | 18.7% |
| `normalize=minmax`, `lr_schedule=cosine` | 3 | -15.7% | +21.6% | 18.7% |
| `lr_schedule=step` | 3 | -22.2% | +33.3% | 27.7% |
| naive (reproduction as run) | 5 | -24.0% | +31.9% | 27.9% |
| `class_weight=balanced`, `lr_schedule=cosine` | 3 | -15.1% | +47.1% | 31.1% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `shuffling_seeds`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `python_version`, `os`, `cpu_architecture`, `memory_size`, `disk_type`, `math_library`, `float_precision`, `random_module_implementation`, `--out`

## Provenance
- GapFinder commit: `56779a9cc2cef642dbf91ede59da97a848c305cd` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `81ad24a2c635c2279bd33ad3363ed7dfbe8e21683f613c866dc86e070854c074`
- Cost: Nemotron billed $0.1524, sandbox reported $0.0000 (total $0.1524; this search; ledger extraction is included only if it shared the search's router)
