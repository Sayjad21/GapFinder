# Gap Report: test-v12-03

Artifact `mlbench` · generated 2026-10-16 01:58 · 112 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Unexplained | -25.6% | -25.6% | ±8.3% | — |

## C1: test_accuracy (paper 0.7)
**Unexplained** · gap -25.6% → -25.6% · 37 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (37 hypotheses tested).

### What did the paper report?
> A plain logistic-regression baseline reaches 0.700 test accuracy and 0.500 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7 (headline claim)

### What did we measure?
- Naive median 0.5208 over 5 runs; repeats: 0.5208, 0.55, 0.4667, 0.5208, 0.4875
- Spread: range 0.4667 to 0.55, noise band ±0.0584 (2 x MAD), CV 6.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -25.6% (noise band ±8.3% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=minmax` (1.28 noise units, gap -14.9%); `lr_schedule=cosine` (1.21 noise units, gap -15.5%)
- Near alternatives (closest across all claims):
  - `normalize=minmax`, `positive_rate=0.1`: this claim +11.9%, mean |gap| 6.0% (5 runs)
  - `normalize=minmax`: this claim -14.9%, mean |gap| 7.4% (5 runs)
  - `normalize=minmax`, `lr_schedule=cosine`: this claim -14.9%, mean |gap| 7.4% (2 runs)

### History matching (every measured configuration, all claims together)
- 12 of 37 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `normalize, positive_rate`: normalize=minmax, positive_rate=0.1 (max I 2.04); normalize=minmax, positive_rate=0.93 (max I 2.49); normalize=zscore, positive_rate=0.1 (max I 2.8); normalize=zscore, positive_rate=0.93 (max I 2.83)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=minmax (max I 2.34); lr_schedule=step, normalize=minmax (max I 2.34)
  - `lr_schedule, positive_rate`: lr_schedule=step, positive_rate=0.1 (max I 2.41); lr_schedule=cosine, positive_rate=0.1 (max I 2.52)
  - `normalize`: normalize=minmax (max I 2.55)
  - `class_weight, lr_schedule`: class_weight=balanced, lr_schedule=cosine (max I 2.82)
- 3 separate islands (no single-knob move joins them): normalize=minmax, positive_rate=0.1; lr_schedule=cosine, normalize=minmax; lr_schedule=step, normalize=minmax | lr_schedule=step, positive_rate=0.1; lr_schedule=cosine, positive_rate=0.1; lr_schedule=cosine, positive_rate=0.03 | class_weight=balanced, lr_schedule=cosine; class_weight=balanced, lr_schedule=step

Notes:
- {'lr_schedule': 'cosine'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'lr_schedule': 'cosine'} (gap -12.2%); it did not pass verification
- history matching: 12 of 37 tested configurations fit every claim within 3 sigma

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax`, `positive_rate=0.1` | 5 | +11.9% | +0.0% | 6.0% |
| `normalize=minmax` | 5 | -14.9% | +0.0% | 7.4% |
| `normalize=minmax`, `lr_schedule=cosine` | 2 | -14.9% | +0.0% | 7.4% |
| `normalize=minmax`, `lr_schedule=step` | 2 | -14.9% | +0.0% | 7.4% |
| `positive_rate=0.03`, `lr_schedule=cosine` | 5 | +18.5% | +0.3% | 9.4% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
