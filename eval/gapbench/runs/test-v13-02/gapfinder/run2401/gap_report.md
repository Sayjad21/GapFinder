# Gap Report: test-v13-02

Artifact `mlbench` · generated 2026-10-16 01:33 · 19 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Unexplained | -35.2% | -35.2% | ±7.0% | — |

## C1: test_accuracy (paper 0.8292)
**Unexplained** · gap -35.2% → -35.2% · 5 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (5 hypotheses tested).

### What did the paper report?
> A plain logistic-regression baseline reaches 0.829 test accuracy and 0.810 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.8292 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.4792, 0.5375, 0.4667, 0.5667, 0.5375
- Spread: range 0.4667 to 0.5667, noise band ±0.0584 (2 x MAD), CV 8.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -35.2% (noise band ±7.0% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `num_runs (implicit)`, `--normalize`, `median_aggregation_external (implicit)`, `SCALES (hardcoded)`, `WEIGHTS (hardcoded)`, `weight_init_stddev (hardcoded)`, `sigmoid_clip_bound (hardcoded)`, `data_generation_intercept_formula (hardcoded)`, `batch_gradient_averaging (hardcoded)`, `shuffle_each_epoch (hardcoded)`, `python_random_module`, `bias_init_zero (hardcoded)`, `RUN_TAG_hex_parsing`, `hardware`, `random_Random_implementation`, `feature_order_fixed (SCALES/WEIGHTS order)`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (1.64 noise units, gap -23.6%)
- Near alternatives (closest across all claims):
  - `lr_schedule=cosine`: this claim -24.9%, mean |gap| 23.9% (6 runs)
  - `lr_schedule=cosine`, `class_weight=balanced`: this claim -27.1%, mean |gap| 25.8% (5 runs)

### History matching (every measured configuration, all claims together)
- out-of-space likely: no tested configuration comes within 3 sigma of C1, C2, among 5 tested

Notes:
- closest configuration tried: {'lr_schedule': 'cosine'} (gap -24.9%); it did not pass verification
- history matching: out-of-space likely: no tested configuration comes within 3 sigma of C1, C2, among 5 tested

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=cosine` | 6 | -24.9% | -23.0% | 23.9% |
| `lr_schedule=cosine`, `class_weight=balanced` | 5 | -27.1% | -24.5% | 25.8% |
| naive (reproduction as run) | 5 | -35.2% | -33.1% | 34.1% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `num_runs (implicit)`, `--normalize`, `median_aggregation_external (implicit)`, `SCALES (hardcoded)`, `WEIGHTS (hardcoded)`, `weight_init_stddev (hardcoded)`, `sigmoid_clip_bound (hardcoded)`, `data_generation_intercept_formula (hardcoded)`, `batch_gradient_averaging (hardcoded)`, `shuffle_each_epoch (hardcoded)`, `python_random_module`, `bias_init_zero (hardcoded)`, `RUN_TAG_hex_parsing`, `hardware`, `random_Random_implementation`, `feature_order_fixed (SCALES/WEIGHTS order)`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `460f2b20cfc37f744e9659681610940370212e103b69f68e976ce9617f6797c2`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
