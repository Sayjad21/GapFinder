# Gap Report: test-v13-08

Artifact `mlbench` · generated 2026-10-16 02:07 · 23 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Inconclusive | +9.0% | +9.0% | ±1.1% | — |

## C1: test_accuracy (paper 0.4931)
**Inconclusive** · naive gap +9.0% is inside the noise band ±1.1%, but the band is too wide to call it a reproduction.

### Which experiment changed it?
- None could be tested: the noise band is too wide to tell values apart.

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.493 test accuracy.

- p. 1; value used: `test_accuracy` = 0.4931 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.575, 0.5375, 0.5375, 0.4875, 0.5375
- Spread: range 0.4875 to 0.575, noise band ±0.005375 (2 x MAD), CV 5.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +9.0% (noise band ±1.1% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `class_weight=balanced` (7.22 noise units, gap -1.1%)
- Near alternatives (closest across all claims):
  - `class_weight=balanced`: this claim +4.4%, mean |gap| 3.2% (6 runs)

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 8 configurations
  - `class_weight`: class_weight=balanced (max I 0.8)
  - `class_weight, lr_schedule`: class_weight=balanced, lr_schedule=step (max I 1.15); class_weight=balanced, lr_schedule=cosine (max I 2.72)
  - `lr_schedule`: lr_schedule=step (max I 2.03); lr_schedule=cosine (max I 2.43)
  - `normalize`: normalize=minmax (max I 2.43)
  - `lr_schedule, normalize`: lr_schedule=step, normalize=minmax (max I 2.43); lr_schedule=cosine, normalize=minmax (max I 2.43)

Notes:
- no hypothesis moved the gap by more than 1 noise units
- the gap (+9.0%) is below the minimum detectable effect (±12.8% with 5 runs per configuration at 80% power): even a setting that closed it couldn't have been confirmed, so 'nothing explains it' can't be claimed either

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `class_weight=balanced` | 6 | +4.4% | -2.0% | 3.2% |
| naive (reproduction as run) | 5 | +9.0% | +3.1% | 6.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
