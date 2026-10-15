# Gap Report: test-v13-05

Artifact `mlbench` · generated 2026-10-16 00:11 · 151 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -31.0% | +6.1% | ±2.1% | `normalize=zscore` |

## C1: test_accuracy (paper 0.7792)
**Fits but unsupported** · gap -31.0% → +6.1% · 29 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0020`, `B0058`, `B0059`, `B0089`, `B0090`, `B0091` (6 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `zscore`
- Command:

  Replay: fork checkpoint `6c889b4e-bb1f-40a5-96a5-f3c237278d0a` and run
  ```
  RUN_TAG=fc7883d71e1b "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize zscore --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.825, 0.825, 0.8292, 0.8292, 0.8292, 0.825; gap after +6.1%; result checkpoint `574b2e40-e23d-4944-bdbd-aa6df56ff7c1`
- Effect: candidate 0.8271 minus naive 0.5375 = +0.2896, 95% bootstrap interval [+0.2809, +0.34] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.779 test accuracy and 0.750 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7792 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5458, 0.5375, 0.5208, 0.5458, 0.4792
- Spread: range 0.4792 to 0.5458, noise band ±0.0166 (2 x MAD), CV 5.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -31.0% (noise band ±2.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -31.0% (it comes back)
- PASS · Held-out claim: C2: -27.7% to +7.8% (not worse beyond noise)
- FAIL · Evidence: `normalize=zscore`: no evidence mentions 'zscore'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +0.2896 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `epochs=750` (10.04 noise units, gap -9.6%); `lr_schedule=cosine` (4.52 noise units, gap -21.4%); `normalize=minmax` (3.51 noise units, gap -23.5%); `weight_decay=1e-4` (2.01 noise units, gap -26.7%); `class_weight=balanced` (1.51 noise units, gap -27.8%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=cosine`: this claim -21.4%, mean |gap| 20.2% (3 runs)
  - `normalize=minmax`: this claim -23.5%, mean |gap| 28.4% (3 runs)
  - `epochs=30`: this claim -30.2%, mean |gap| 28.7% (6 runs)

### History matching (every measured configuration, all claims together)
- 1 of 28 tested configurations fit every claim within 3 sigma

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore` | 6 | +6.1% | +7.8% | 7.0% |
| `lr_schedule=cosine` | 3 | -21.4% | -19.1% | 20.2% |
| `normalize=minmax` | 3 | -23.5% | -33.3% | 28.4% |
| `epochs=30` | 6 | -30.2% | -27.1% | 28.7% |
| `epochs=1` | 6 | -30.5% | -27.5% | 29.0% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `weight_decay=none`: invalid_value, The training script expects a numeric float for --weight_decay, but received the string 'none', which is not a valid float, causing argument parsing to fail; retried as `weight_decay=0.000001`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`

## Provenance
- GapFinder commit: `e9c31fd1405f5c8aae4bd880eadcdc8d491fad02` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0398, sandbox reported $0.0000 (total $0.0398; this search; ledger extraction is included only if it shared the search's router)
