# Gap Report: test-gen-06

Artifact `mlbench` · generated 2026-10-10 23:03 · 62 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Partially explained | -34.3% | -16.3% | ±5.6% | `lr_schedule=cosine` |

## C1: test_accuracy (paper 0.7417)
**Partially explained** · gap -34.3% → -16.3% · 13 hypotheses tested
> Plausible explanation (fits but unsupported): it closes only part of the gap, or the paper's own value was not tested

### Which experiment changed it?
- Branch: `B0009`, `B0025`, `B0026`, `B0027`, `B0028` (5 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `cosine`
- Command:

  Replay: fork checkpoint `2c009672-2a4c-4167-ab94-23161cc892b2` and run
  ```
  RUN_TAG=3b2f996725bb "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize none --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule cosine --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.625, 0.6208, 0.6083, 0.6125, 0.6417; gap after -16.3%; result checkpoint `390fb84e-a8c8-4a87-9894-9c55917afa56`
- Effect: candidate 0.6208 minus naive 0.4875 = +0.1333, 95% bootstrap interval [+0.08166, +0.1483] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.742 test accuracy and 0.700 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7417 (headline claim)

### What did we measure?
- Naive median 0.4875 over 5 runs; repeats: 0.475, 0.4667, 0.5333, 0.4875, 0.5625
- Spread: range 0.4667 to 0.5625, noise band ±0.0416 (2 x MAD), CV 8.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -34.3% (noise band ±5.6% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is +0.1333 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `Python random module`, `Hardware CPU`, `Python version`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (4.01 noise units, gap +11.8%); `normalize=minmax` (2.6 noise units, gap -19.7%); `n=5000` (1.77 noise units, gap -24.4%); `class_weight=balanced` (1.2 noise units, gap -27.5%); `lr_schedule=step` (1.1 noise units, gap -28.1%)
- Near alternatives (closest across all claims):
  - `n=5000`, `normalize=zscore`: this claim +1.8%, mean |gap| 3.3% (5 runs)
  - `class_weight=balanced`, `normalize=zscore`: this claim +5.6%, mean |gap| 8.8% (5 runs)
  - `n=5000`, `lr_schedule=cosine`: this claim -14.9%, mean |gap| 12.9% (5 runs)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `n=5000`, `normalize=zscore` | 5 | +1.8% | +4.9% | 3.3% |
| `class_weight=balanced`, `normalize=zscore` | 5 | +5.6% | +12.1% | 8.8% |
| `n=5000`, `lr_schedule=cosine` | 5 | -14.9% | -10.9% | 12.9% |
| `normalize=zscore` | 5 | +11.8% | +15.7% | 13.7% |
| `normalize=zscore`, `lr_schedule=cosine` | 5 | +11.8% | +15.7% | 13.7% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `Python random module`, `Hardware CPU`, `Python version`, `--out`

## Provenance
- GapFinder commit: `fb04d3a1ab0b0fec0acc5b342103e9444806727c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `81ad24a2c635c2279bd33ad3363ed7dfbe8e21683f613c866dc86e070854c074`
- Cost: Nemotron billed $0.0437, sandbox reported $0.0000 (total $0.0437; this search; ledger extraction is included only if it shared the search's router)
