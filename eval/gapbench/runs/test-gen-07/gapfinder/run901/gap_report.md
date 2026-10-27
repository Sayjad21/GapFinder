# Gap Report: test-gen-07

Artifact `mlbench` · generated 2026-10-14 23:42 · 27 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Inconclusive | +9.7% | +9.7% | ±3.4% | — |

## C1: test_accuracy (paper 0.4938)
**Inconclusive** · naive gap +9.7% is inside the noise band ±3.4%, but the band is too wide to call it a reproduction.

### Which experiment changed it?
- None could be tested: the noise band is too wide to tell values apart.

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.494 test accuracy.

- p. 1; value used: `test_accuracy` = 0.4938 (headline claim)

### What did we measure?
- Naive median 0.5417 over 5 runs; repeats: 0.4833, 0.5417, 0.55, 0.4792, 0.5417
- Spread: range 0.4792 to 0.55, noise band ±0.0166 (2 x MAD), CV 6.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +9.7% (noise band ±3.4% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs_aggregation`, `run_seeds`, `init_scale`, `splitting_method`, `python_version`, `os`, `hardware`, `gauss_algorithm`, `random_algorithm`, `normalizer_scope`, `shuffle_per_epoch`, `loss_function`, `gradient_calculation`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `class_weight=balanced` (2.51 noise units, gap -1.3%)
- Near alternatives (closest across all claims):
  - `lr_schedule=step`, `class_weight=balanced`: this claim +8.8%, mean |gap| 10.2% (5 runs)
  - `class_weight=balanced`: this claim +8.8%, mean |gap| 10.4% (6 runs)

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 8 configurations
  - `class_weight, lr_schedule`: class_weight=balanced, lr_schedule=step (max I 1.34); class_weight=balanced, lr_schedule=cosine (max I 2.81)
  - `class_weight`: class_weight=balanced (max I 1.35)
  - `lr_schedule`: lr_schedule=step (max I 1.79); lr_schedule=cosine (max I 2.69)
  - `normalize`: normalize=minmax (max I 2.23)
  - `lr_schedule, normalize`: lr_schedule=step, normalize=minmax (max I 2.23); lr_schedule=cosine, normalize=minmax (max I 2.23)

Notes:
- no hypothesis moved the gap by more than 1 noise units
- the gap (+9.7%) is below the minimum detectable effect (±14.2% with 5 runs per configuration at 80% power): even a setting that closed it couldn't have been confirmed, so 'nothing explains it' can't be claimed either

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=step`, `class_weight=balanced` | 5 | +8.8% | +11.6% | 10.2% |
| `class_weight=balanced` | 6 | +8.8% | +11.9% | 10.4% |
| naive (reproduction as run) | 5 | +9.7% | +12.0% | 10.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs_aggregation`, `run_seeds`, `init_scale`, `splitting_method`, `python_version`, `os`, `hardware`, `gauss_algorithm`, `random_algorithm`, `normalizer_scope`, `shuffle_per_epoch`, `loss_function`, `gradient_calculation`, `--out`

## Provenance
- GapFinder commit: `efb2f63a257a40b9982099a274f2e882f272b80c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
