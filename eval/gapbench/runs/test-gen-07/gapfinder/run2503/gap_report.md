# Gap Report: test-gen-07

Artifact `mlbench` · generated 2026-10-16 01:47 · 43 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Inconclusive | +10.5% | +10.5% | ±6.8% | — |

## C1: test_accuracy (paper 0.4938)
**Inconclusive** · naive gap +10.5% is inside the noise band ±6.8%, but the band is too wide to call it a reproduction.

### Which experiment changed it?
- None could be tested: the noise band is too wide to tell values apart.

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.494 test accuracy.

- p. 1; value used: `test_accuracy` = 0.4938 (headline claim)

### What did we measure?
- Naive median 0.5458 over 5 runs; repeats: 0.4833, 0.5458, 0.5375, 0.5625, 0.5708
- Spread: range 0.4833 to 0.5708, noise band ±0.0334 (2 x MAD), CV 6.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +10.5% (noise band ±6.8% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `median_over_runs`, `SCALES`, `WEIGHTS`, `feature_count`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `class_weight=balanced` (1.24 noise units, gap -2.1%)
- Near alternatives (closest across all claims):
  - `class_weight=balanced`: this claim -0.9%, mean |gap| 0.5% (6 runs)
  - `lr_schedule=step`: this claim +4.2%, mean |gap| 5.2% (6 runs)
  - `normalize=minmax`: this claim +20.7%, mean |gap| 11.9% (6 runs)

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 6 configurations
  - `class_weight`: class_weight=balanced (max I 0.51)
  - `lr_schedule`: lr_schedule=step (max I 1.13)
  - `class_weight, lr_schedule`: class_weight=balanced, lr_schedule=step (max I 2.23); class_weight=balanced, lr_schedule=cosine (max I 2.86)
  - `lr_schedule, normalize`: lr_schedule=step, normalize=minmax (max I 2.25); lr_schedule=cosine, normalize=minmax (max I 2.25)

Notes:
- no hypothesis moved the gap by more than 1 noise units
- the gap (+10.5%) is below the minimum detectable effect (±14.0% with 5 runs per configuration at 80% power): even a setting that closed it couldn't have been confirmed, so 'nothing explains it' can't be claimed either

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `class_weight=balanced` | 6 | -0.9% | +0.2% | 0.5% |
| `lr_schedule=step` | 6 | +4.2% | +6.2% | 5.2% |
| naive (reproduction as run) | 5 | +10.5% | +13.0% | 11.8% |
| `normalize=minmax` | 6 | +20.7% | +3.2% | 11.9% |
| `lr_schedule=cosine` | 6 | +24.5% | +26.8% | 25.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `median_over_runs`, `SCALES`, `WEIGHTS`, `feature_count`, `--out`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
