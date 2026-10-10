# Gap Report: test-gen-08

Artifact `mlbench` · generated 2026-10-10 23:52 · 54 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Fits but unsupported | -5.6% | +0.0% | ±2.8% | `normalize=minmax` |

## C1: test_accuracy (paper 0.5958)
**Fits but unsupported** · gap -5.6% → +0.0% · 13 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0009`, `B0025`, `B0026`, `B0027`, `B0028` (5 run(s) of the same config)
- Config: `normalize` naive `none`, changed to `minmax`
- Command:

  Replay: fork checkpoint `fe9a111d-b2f7-4347-96a1-212fc4718559` and run
  ```
  RUN_TAG=9850192fa618 "${PYTHON:-python3}" train.py --n 1200 --positive_rate 0.3 --label_noise 0.05 --split 0.8 --normalize minmax --epochs 15 --batch_size 32 --lr 0.05 --lr_schedule const --weight_decay 0.0 --class_weight none --threshold 0.5 --data_seed 7 --out out/result.json
  ```
- Output: `test_accuracy` 0.5958, 0.5958, 0.5958, 0.5958, 0.5958; gap after +0.0%; result checkpoint `ad9185cc-0754-4ac4-9fa9-ebac392d12b8`
- Effect: candidate 0.5958 minus naive 0.5625 = +0.0333, 95% bootstrap interval [+0.02998, +0.08412] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.596 test accuracy.

- p. 1; value used: `test_accuracy` = 0.5958 (headline claim)

### What did we measure?
- Naive median 0.5625 over 5 runs; repeats: 0.5625, 0.5708, 0.4917, 0.5625, 0.5125
- Spread: range 0.4917 to 0.5708, noise band ±0.0166 (2 x MAD), CV 6.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -5.6% (noise band ±2.8% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `normalize` the gap is -5.6% (it comes back)
- PASS · Held-out claim: C2: +11.7% to +0.0% (not worse beyond noise)
- FAIL · Evidence: `normalize=minmax`: evidence gate off: no evidence was looked for
- PASS · Effect vs noise: candidate minus naive is +0.0333 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `SCALES`, `WEIGHTS`, `RUN_TAG`, `weight_init_scale`, `num_runs`, `aggregation`, `sigmoid_clamp`, `CPU`, `memory`, `OS`, `Python_version`, `random_module`, `floating_point`, `storage`, `network`, `virtualization`, `containerization`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives (closest across all claims):
  - `lr_schedule=cosine`, `normalize=minmax`: this claim +0.0%, mean |gap| 0.0% (5 runs)
  - `normalize=minmax`, `epochs=30`: this claim +2.1%, mean |gap| 2.8% (5 runs)
  - `class_weight=balanced`: this claim -8.4%, mean |gap| 9.0% (5 runs)

Notes:
- evidence gate off: no evidence was checked, so this cannot be labelled Explained

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax` | 5 | +0.0% | +0.0% | 0.0% |
| `lr_schedule=cosine`, `normalize=minmax` | 5 | +0.0% | +0.0% | 0.0% |
| `normalize=minmax`, `epochs=30` | 5 | +2.1% | +3.4% | 2.8% |
| naive (reproduction as run) | 5 | -5.6% | +11.7% | 8.6% |
| `class_weight=balanced` | 5 | -8.4% | +9.5% | 9.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `SCALES`, `WEIGHTS`, `RUN_TAG`, `weight_init_scale`, `num_runs`, `aggregation`, `sigmoid_clamp`, `CPU`, `memory`, `OS`, `Python_version`, `random_module`, `floating_point`, `storage`, `network`, `virtualization`, `containerization`

## Provenance
- GapFinder commit: `fb04d3a1ab0b0fec0acc5b342103e9444806727c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `81ad24a2c635c2279bd33ad3363ed7dfbe8e21683f613c866dc86e070854c074`
- Cost: Nemotron billed $0.0652, sandbox reported $0.0000 (total $0.0652; this search; ledger extraction is included only if it shared the search's router)
