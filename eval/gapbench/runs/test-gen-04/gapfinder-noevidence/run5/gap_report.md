# Gap Report: test-gen-04

Artifact `mlbench` · generated 2026-10-13 00:07 · 37 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -38.4% | +0.5% | ±10.1% | `normalize=zscore` |

## C1: test_accuracy (paper 0.825)
**Fits but unsupported** · gap -38.4% → +0.5% · 8 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0006`, `B0011`, `B0012`, `B0013`, `B0014` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Command:

  Replay: fork checkpoint `2c8b6fca-9a82-4d91-bd62-77accc33fd56` and run
  ```
  RUN_TAG=0fed09af698e "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.825, 0.8292, 0.8292, 0.8292, 0.8292; gap after +0.5%; result checkpoint `45abd30f-61b8-4c14-8cf6-8559c6fbdceb`
- Effect: candidate 0.8292 minus naive 0.5083 = +0.3209, 95% bootstrap interval [+0.2942, +0.3533] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.825 test accuracy and 0.807 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.825 (headline claim)

### What did we measure?
- Naive median 0.5083 over 5 runs; repeats: 0.4667, 0.4667, 0.5375, 0.5083, 0.55
- Spread: range 0.4667 to 0.55, noise band ±0.0832 (2 x MAD), CV 7.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -38.4% (noise band ±10.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -38.4% (it comes back)
- PASS · Held-out claim: C2: -37.5% to +0.4% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: evidence gate off: no evidence was looked for
- PASS · Effect vs noise: candidate minus naive is +0.3209 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `aggregation_method`, `SCALES`, `WEIGHTS`, `label_noise_application`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (1.4 noise units, gap -24.2%); `normalize=minmax` (1.05 noise units, gap -27.8%)
- Near alternatives (closest across all claims):
  - `lr_schedule=cosine`, `normalize=zscore`: this claim +0.5%, mean |gap| 0.5% (5 runs)
  - `class_weight=balanced`, `normalize=zscore`: this claim -5.1%, mean |gap| 4.0% (5 runs)
  - `lr_schedule=cosine`: this claim -24.2%, mean |gap| 23.6% (5 runs)

Notes:
- evidence gate off: no evidence was checked, so this cannot be labelled Explained

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore` | 5 | +0.5% | +0.4% | 0.5% |
| `lr_schedule=cosine`, `normalize=zscore` | 5 | +0.5% | +0.4% | 0.5% |
| `class_weight=balanced`, `normalize=zscore` | 5 | -5.1% | -2.9% | 4.0% |
| `lr_schedule=cosine` | 5 | -24.2% | -22.9% | 23.6% |
| `class_weight=balanced`, `lr_schedule=cosine` | 5 | -26.3% | -24.0% | 25.1% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `aggregation_method`, `SCALES`, `WEIGHTS`, `label_noise_application`

## Provenance
- GapFinder commit: `2e9291c6be5f4b9ffe219d44dfe2904a7d2d6a9f` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `81ad24a2c635c2279bd33ad3363ed7dfbe8e21683f613c866dc86e070854c074`
- Cost: Nemotron billed $0.0439, sandbox reported $0.0000 (total $0.0439; this search; ledger extraction is included only if it shared the search's router)
