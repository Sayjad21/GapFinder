# Gap Report: test-gen-04

Artifact `mlbench` · generated 2026-10-13 00:08 · 41 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -40.9% | +0.0% | ±5.0% | `normalize=zscore` |

## C1: test_accuracy (paper 0.825)
**Fits but unsupported** · gap -40.9% → +0.0% · 8 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0006`, `B0011`, `B0012`, `B0013`, `B0014` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Command:

  Replay: fork checkpoint `b655afd5-1c99-47a5-87f5-95042711e9be` and run
  ```
  RUN_TAG=048d3ae7cbb5 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.825, 0.8292, 0.825, 0.825, 0.825; gap after +0.0%; result checkpoint `232391b6-ea8a-4fce-b6da-52be2cbbd083`
- Effect: candidate 0.825 minus naive 0.4875 = +0.3375, 95% bootstrap interval [+0.29, +0.3508] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.825 test accuracy and 0.807 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.825 (headline claim)

### What did we measure?
- Naive median 0.4875 over 5 runs; repeats: 0.55, 0.5458, 0.4875, 0.475, 0.4667
- Spread: range 0.4667 to 0.55, noise band ±0.0416 (2 x MAD), CV 7.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -40.9% (noise band ±5.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -40.9% (it comes back)
- PASS · Held-out claim: C2: -40.0% to +0.0% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: evidence gate off: no evidence was looked for
- PASS · Effect vs noise: candidate minus naive is +0.3375 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `normalisation_method`, `RUN_TAG`, `SCALES`, `WEIGHTS`, `aggregation_method`, `shuffling_seed_source`, `cpu_architecture`, `os`, `python_version`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (2.81 noise units, gap -26.8%); `normalize=minmax` (2.6 noise units, gap -27.8%); `lr_schedule=step` (1.3 noise units, gap -34.3%)
- Near alternatives (closest across all claims):
  - `lr_schedule=cosine`, `normalize=zscore`: this claim +0.5%, mean |gap| 0.5% (5 runs)
  - `normalize=zscore`, `class_weight=balanced`: this claim -4.5%, mean |gap| 3.4% (5 runs)
  - `lr_schedule=cosine`: this claim -24.8%, mean |gap| 24.1% (5 runs)

Notes:
- evidence gate off: no evidence was checked, so this cannot be labelled Explained

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore` | 5 | +0.0% | +0.0% | 0.0% |
| `lr_schedule=cosine`, `normalize=zscore` | 5 | +0.5% | +0.4% | 0.5% |
| `normalize=zscore`, `class_weight=balanced` | 5 | -4.5% | -2.3% | 3.4% |
| `lr_schedule=cosine` | 5 | -24.8% | -23.5% | 24.1% |
| `lr_schedule=cosine`, `class_weight=balanced` | 5 | -27.8% | -24.9% | 26.3% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `normalisation_method`, `RUN_TAG`, `SCALES`, `WEIGHTS`, `aggregation_method`, `shuffling_seed_source`, `cpu_architecture`, `os`, `python_version`, `--out`

## Provenance
- GapFinder commit: `2e9291c6be5f4b9ffe219d44dfe2904a7d2d6a9f` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `81ad24a2c635c2279bd33ad3363ed7dfbe8e21683f613c866dc86e070854c074`
- Cost: Nemotron billed $0.0438, sandbox reported $0.0000 (total $0.0438; this search; ledger extraction is included only if it shared the search's router)
