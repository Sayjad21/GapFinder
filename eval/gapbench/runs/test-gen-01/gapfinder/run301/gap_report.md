# Gap Report: test-gen-01

Artifact `mlbench` · generated 2026-10-14 21:41 · 35 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Unexplained | -20.4% | -20.4% | ±5.9% | — |

## C1: test_accuracy (paper 0.7069)
**Unexplained** · gap -20.4% → -20.4% · 13 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (13 hypotheses tested).

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.707 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7069 (headline claim)

### What did we measure?
- Naive median 0.5625 over 5 runs; repeats: 0.4875, 0.5792, 0.5833, 0.5625, 0.5
- Spread: range 0.4875 to 0.5833, noise band ±0.0416 (2 x MAD), CV 8.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -20.4% (noise band ±5.9% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `aggregation`, `SCALES`, `WEIGHTS`, `num_runs`, `weight_init_std`, `sigmoid_clamp`, `CPU`, `OS`, `Python_version`, `random_module`, `floating_point_precision`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (1.3 noise units, gap -12.8%)
- Near alternatives (closest across all claims):
  - `lr_schedule=cosine`: this claim -12.5%, mean |gap| 31.1% (6 runs)
  - `class_weight=balanced`, `lr_schedule=cosine`: this claim -14.5%, mean |gap| 31.4% (5 runs)
  - `class_weight=balanced`, `normalize=minmax`: this claim +9.0%, mean |gap| 49.1% (5 runs)

### History matching (every measured configuration, all claims together)
- 5 of 13 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 5 configurations
  - `normalize`: normalize=minmax (max I 1.81)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=minmax (max I 1.81); lr_schedule=step, normalize=minmax (max I 1.81)
  - `lr_schedule`: lr_schedule=step (max I 2.69)
  - `class_weight, lr_schedule`: class_weight=balanced, lr_schedule=step (max I 2.76)

Notes:
- {'normalize': 'minmax', 'class_weight': 'balanced'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'normalize': 'minmax', 'class_weight': 'balanced'} (gap +9.0%); it did not pass verification
- history matching: 5 of 13 tested configurations fit every claim within 3 sigma

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| naive (reproduction as run) | 5 | -20.4% | +36.6% | 28.5% |
| `lr_schedule=cosine` | 6 | -12.5% | +49.7% | 31.1% |
| `class_weight=balanced`, `lr_schedule=cosine` | 5 | -14.5% | +48.3% | 31.4% |
| `class_weight=balanced`, `normalize=minmax` | 5 | +9.0% | +89.2% | 49.1% |
| `class_weight=balanced`, `normalize=zscore` | 5 | +10.8% | +91.0% | 50.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `aggregation`, `SCALES`, `WEIGHTS`, `num_runs`, `weight_init_std`, `sigmoid_clamp`, `CPU`, `OS`, `Python_version`, `random_module`, `floating_point_precision`, `--out`

## Provenance
- GapFinder commit: `634d827f07d6659ff82f6ea0924c8ba487e9d02a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
