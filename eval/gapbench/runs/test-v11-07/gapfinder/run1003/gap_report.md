# Gap Report: test-v11-07

Artifact `mlbench` · generated 2026-10-15 00:23 · 23 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Unexplained | -11.4% | -11.4% | ±3.1% | — |

## C1: test_accuracy (paper 0.5361)
**Unexplained** · gap -11.4% → -11.4% · 13 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (13 hypotheses tested).

### What did the paper report?
> A plain logistic-regression baseline reaches 0.536 test accuracy and 0.543 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.5361 (headline claim)

### What did we measure?
- Naive median 0.475 over 5 runs; repeats: 0.4875, 0.4667, 0.4875, 0.475, 0.4667
- Spread: range 0.4667 to 0.4875, noise band ±0.0166 (2 x MAD), CV 2.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -11.4% (noise band ±3.1% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `class_weight=balanced` (3.6 noise units, gap +0.3%)
- Near alternatives (closest across all claims):
  - `class_weight=balanced`: this claim +0.7%, mean |gap| 0.4% (4 runs)
  - `class_weight=balanced`, `lr_schedule=step`: this claim -8.3%, mean |gap| 8.9% (3 runs)

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 8 configurations
  - `class_weight`: class_weight=balanced (max I 0.64)
  - `class_weight, lr_schedule`: class_weight=balanced, lr_schedule=step (max I 1.57); class_weight=balanced, lr_schedule=cosine (max I 2.79)
  - `normalize`: normalize=minmax (max I 2.05)
  - `lr_schedule, normalize`: lr_schedule=step, normalize=minmax (max I 2.05); lr_schedule=cosine, normalize=minmax (max I 2.05)
  - `lr_schedule`: lr_schedule=step (max I 2.1); lr_schedule=cosine (max I 2.9)

Notes:
- closest configuration tried: {'class_weight': 'balanced', 'lr_schedule': 'step'} (gap -8.3%); it did not pass verification
- history matching: the naive configuration is within noise of every claim

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `class_weight=balanced` | 4 | +0.7% | +0.1% | 0.4% |
| `class_weight=balanced`, `lr_schedule=step` | 3 | -8.3% | -9.6% | 8.9% |
| naive (reproduction as run) | 5 | -11.4% | -13.4% | 12.4% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
