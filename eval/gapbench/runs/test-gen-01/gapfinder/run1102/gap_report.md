# Gap Report: test-gen-01

Artifact `mlbench` · generated 2026-10-15 00:28 · 65 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Unexplained | -24.0% | -24.0% | ±2.3% | — |

## C1: test_accuracy (paper 0.7069)
**Unexplained** · gap -24.0% → -24.0% · 13 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (13 hypotheses tested).

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.707 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7069 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.4875, 0.5833, 0.5458, 0.5375, 0.5333
- Spread: range 0.4875 to 0.5833, noise band ±0.0166 (2 x MAD), CV 6.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -24.0% (noise band ±2.3% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `aggregation_method`, `num_runs`, `shuffling_seed_source`, `feature_count`, `out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (4.77 noise units, gap -12.8%); `normalize=minmax` (3.51 noise units, gap -15.7%); `normalize=zscore` (2.84 noise units, gap +17.3%)
- Near alternatives (closest across all claims):
  - `normalize=minmax`: this claim -15.7%, mean |gap| 18.7% (6 runs)
  - `lr_schedule=cosine`, `normalize=minmax`: this claim -15.7%, mean |gap| 18.7% (5 runs)
  - `normalize=minmax`, `lr_schedule=step`: this claim -15.7%, mean |gap| 18.7% (5 runs)

### History matching (every measured configuration, all claims together)
- out-of-space likely: no tested configuration comes within 3 sigma of C2, among 13 tested
- Fit C1 alone (10; worst claim's implausibility in brackets, lowest is the least inconsistent): lr_schedule=cosine, normalize=minmax (3.03); lr_schedule=step, normalize=minmax (3.03); normalize=minmax (3.09); class_weight=balanced, lr_schedule=cosine (6.82); lr_schedule=cosine (7.1); class_weight=balanced, normalize=minmax (12.59)

Notes:
- {'normalize': 'minmax', 'class_weight': 'balanced'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'normalize': 'minmax', 'class_weight': 'balanced'} (gap +9.0%); it did not pass verification
- history matching: out-of-space likely: no tested configuration comes within 3 sigma of C2, among 13 tested

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax` | 6 | -15.7% | +21.6% | 18.7% |
| `lr_schedule=cosine`, `normalize=minmax` | 5 | -15.7% | +21.6% | 18.7% |
| `normalize=minmax`, `lr_schedule=step` | 5 | -15.7% | +21.6% | 18.7% |
| naive (reproduction as run) | 5 | -24.0% | +31.9% | 27.9% |
| `lr_schedule=step`, `class_weight=balanced` | 5 | -23.4% | +32.7% | 28.1% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `aggregation_method`, `num_runs`, `shuffling_seed_source`, `feature_count`, `out`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
