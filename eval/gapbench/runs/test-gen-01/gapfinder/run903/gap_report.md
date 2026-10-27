# Gap Report: test-gen-01

Artifact `mlbench` · generated 2026-10-14 23:40 · 56 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Unexplained | -24.6% | -24.6% | ±8.3% | — |

## C1: test_accuracy (paper 0.7069)
**Unexplained** · gap -24.6% → -24.6% · 17 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (17 hypotheses tested).

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.707 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7069 (headline claim)

### What did we measure?
- Naive median 0.5333 over 5 runs; repeats: 0.5583, 0.5333, 0.5625, 0.4833, 0.4875
- Spread: range 0.4833 to 0.5625, noise band ±0.0584 (2 x MAD), CV 7.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -24.6% (noise band ±8.3% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `median_aggregation (workflow)`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (1.71 noise units, gap -10.4%); `normalize=minmax` (1.07 noise units, gap -15.7%)
- Near alternatives (closest across all claims):
  - `normalize=minmax`: this claim -15.7%, mean |gap| 18.7% (6 runs)
  - `lr_schedule=cosine`, `normalize=minmax`: this claim -15.7%, mean |gap| 18.7% (5 runs)
  - `lr_schedule=step`, `normalize=minmax`: this claim -15.7%, mean |gap| 18.7% (5 runs)

### History matching (every measured configuration, all claims together)
- 3 of 13 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=minmax (max I 2.69); lr_schedule=step, normalize=minmax (max I 2.69)
  - `normalize`: normalize=minmax (max I 2.75)

Notes:
- {'lr_schedule': 'cosine'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'lr_schedule': 'cosine'} (gap -10.4%); it did not pass verification
- history matching: 3 of 13 tested configurations fit every claim within 3 sigma

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax` | 6 | -15.7% | +21.6% | 18.7% |
| `lr_schedule=cosine`, `normalize=minmax` | 5 | -15.7% | +21.6% | 18.7% |
| `lr_schedule=step`, `normalize=minmax` | 5 | -15.7% | +21.6% | 18.7% |
| naive (reproduction as run) | 5 | -24.6% | +31.0% | 27.8% |
| `lr_schedule=cosine` | 6 | -10.4% | +53.3% | 31.8% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `lr_schedule=constant`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `median_aggregation (workflow)`

## Provenance
- GapFinder commit: `efb2f63a257a40b9982099a274f2e882f272b80c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
