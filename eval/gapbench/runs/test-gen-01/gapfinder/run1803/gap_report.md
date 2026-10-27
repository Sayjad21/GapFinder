# Gap Report: test-gen-01

Artifact `mlbench` · generated 2026-10-15 19:35 · 46 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Unexplained | -24.0% | -24.0% | ±0.8% | — |

## C1: test_accuracy (paper 0.7069)
**Unexplained** · gap -24.0% → -24.0% · 17 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (17 hypotheses tested).

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.707 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7069 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5375, 0.5375, 0.5375, 0.4958, 0.4875
- Spread: range 0.4875 to 0.5375, noise band ±0.005375 (2 x MAD), CV 4.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -24.0% (noise band ±0.8% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `median_aggregation (workflow)`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=step` (13.17 noise units, gap -13.9%); `lr_schedule=cosine` (13.17 noise units, gap -13.9%); `normalize=minmax` (10.85 noise units, gap -15.7%); `normalize=zscore` (8.76 noise units, gap +17.3%)
- Near alternatives (closest across all claims):
  - `normalize=minmax`: this claim -15.7%, mean |gap| 18.7% (4 runs)
  - `normalize=minmax`, `lr_schedule=cosine`: this claim -15.7%, mean |gap| 18.7% (3 runs)
  - `lr_schedule=step`, `normalize=minmax`: this claim -15.7%, mean |gap| 18.7% (2 runs)

### History matching (every measured configuration, all claims together)
- 2 of 13 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 2 configurations
  - `lr_schedule, normalize`: lr_schedule=step, normalize=minmax (max I 2.72); lr_schedule=cosine, normalize=minmax (max I 2.94)

Notes:
- {'normalize': 'minmax', 'class_weight': 'balanced'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'normalize': 'minmax', 'class_weight': 'balanced'} (gap +9.0%); it did not pass verification
- history matching: 2 of 13 tested configurations fit every claim within 3 sigma

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax` | 4 | -15.7% | +21.6% | 18.7% |
| `normalize=minmax`, `lr_schedule=cosine` | 3 | -15.7% | +21.6% | 18.7% |
| `lr_schedule=step`, `normalize=minmax` | 2 | -15.7% | +21.6% | 18.7% |
| `lr_schedule=step` | 4 | -27.5% | +24.8% | 26.1% |
| naive (reproduction as run) | 5 | -24.0% | +31.9% | 27.9% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `lr_schedule=constant`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `median_aggregation (workflow)`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
