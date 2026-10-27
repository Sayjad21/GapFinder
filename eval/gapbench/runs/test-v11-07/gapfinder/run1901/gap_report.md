# Gap Report: test-v11-07

Artifact `mlbench` · generated 2026-10-15 19:46 · 23 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Inconclusive | -9.1% | -9.1% | ±7.8% | — |

## C1: test_accuracy (paper 0.5361)
**Inconclusive** · naive gap -9.1% is inside the noise band ±7.8%, but the band is too wide to call it a reproduction.

### Which experiment changed it?
- None could be tested: the noise band is too wide to tell values apart.

### What did the paper report?
> A plain logistic-regression baseline reaches 0.536 test accuracy and 0.543 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.5361 (headline claim)

### What did we measure?
- Naive median 0.4875 over 5 runs; repeats: 0.4833, 0.4667, 0.5792, 0.5875, 0.4875
- Spread: range 0.4667 to 0.5875, noise band ±0.0416 (2 x MAD), CV 11.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -9.1% (noise band ±7.8% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `class_weight=balanced` (1.13 noise units, gap +0.3%)
- Near alternatives (closest across all claims):
  - `class_weight=balanced`: this claim +0.3%, mean |gap| 0.2% (6 runs)

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 8 configurations
  - `class_weight`: class_weight=balanced (max I 0.18)
  - `class_weight, lr_schedule`: class_weight=balanced, lr_schedule=step (max I 0.2); class_weight=balanced, lr_schedule=cosine (max I 0.97)
  - `lr_schedule`: lr_schedule=step (max I 0.79); lr_schedule=cosine (max I 1.41)
  - `normalize`: normalize=minmax (max I 0.86)
  - `lr_schedule, normalize`: lr_schedule=step, normalize=minmax (max I 0.86); lr_schedule=cosine, normalize=minmax (max I 0.86)

Notes:
- no hypothesis moved the gap by more than 1 noise units
- the gap (-9.1%) is below the minimum detectable effect (±21.7% with 5 runs per configuration at 80% power): even a setting that closed it couldn't have been confirmed, so 'nothing explains it' can't be claimed either

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `class_weight=balanced` | 6 | +0.3% | -0.1% | 0.2% |
| naive (reproduction as run) | 5 | -9.1% | -10.9% | 10.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
