# Gap Report: test-gen-07

Artifact `mlbench` · generated 2026-10-15 19:39 · 30 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Unexplained | +8.0% | +8.0% | ±3.4% | — |

## C1: test_accuracy (paper 0.4938)
**Unexplained** · gap +8.0% → +8.0% · 13 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (13 hypotheses tested).

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.494 test accuracy.

- p. 1; value used: `test_accuracy` = 0.4938 (headline claim)

### What did we measure?
- Naive median 0.5333 over 5 runs; repeats: 0.5333, 0.5333, 0.5167, 0.5417, 0.5208
- Spread: range 0.5167 to 0.5417, noise band ±0.0168 (2 x MAD), CV 1.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +8.0% (noise band ±3.4% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `median_over_runs`, `SCALES`, `WEIGHTS`, `feature_count`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives (closest across all claims):
  - `normalize=minmax`: this claim +20.7%, mean |gap| 11.9% (4 runs)
  - `lr_schedule=step`: this claim +12.2%, mean |gap| 13.3% (4 runs)
  - `lr_schedule=cosine`: this claim +24.9%, mean |gap| 25.9% (4 runs)

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 2 configurations
  - `lr_schedule`: lr_schedule=step (max I 2.73)
  - `class_weight`: class_weight=balanced (max I 3)

Notes:
- no hypothesis moved the gap by more than 1 noise units
- history matching: the naive configuration is within noise of every claim

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| naive (reproduction as run) | 5 | +8.0% | +11.2% | 9.6% |
| `normalize=minmax` | 4 | +20.7% | +3.2% | 11.9% |
| `lr_schedule=step` | 4 | +12.2% | +14.3% | 13.3% |
| `lr_schedule=cosine` | 4 | +24.9% | +27.0% | 25.9% |
| `normalize=zscore` | 4 | +67.5% | +66.9% | 67.2% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `median_over_runs`, `SCALES`, `WEIGHTS`, `feature_count`, `--out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
