# Gap Report: test-gen-07

Artifact `mlbench` · generated 2026-10-14 00:29 · 38 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Unexplained | +10.5% | +10.5% | ±3.4% | — |

## C1: test_accuracy (paper 0.4938)
**Unexplained** · gap +10.5% → +10.5% · 13 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (13 hypotheses tested).

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.494 test accuracy.

- p. 1; value used: `test_accuracy` = 0.4938 (headline claim)

### What did we measure?
- Naive median 0.5458 over 5 runs; repeats: 0.4958, 0.5458, 0.4667, 0.5458, 0.5542
- Spread: range 0.4667 to 0.5542, noise band ±0.0168 (2 x MAD), CV 7.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +10.5% (noise band ±3.4% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `median_over_runs`, `SCALES`, `WEIGHTS`, `feature_count`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=step` (2.47 noise units, gap -2.1%)
- Near alternatives (closest across all claims):
  - `lr_schedule=step`: this claim +8.8%, mean |gap| 10.4% (6 runs)
  - `normalize=minmax`: this claim +20.7%, mean |gap| 11.9% (6 runs)
  - `lr_schedule=cosine`: this claim +24.9%, mean |gap| 25.7% (6 runs)

Notes:
- no hypothesis moved the gap by more than 1 noise units

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=step` | 6 | +8.8% | +11.9% | 10.4% |
| naive (reproduction as run) | 5 | +10.5% | +13.0% | 11.8% |
| `normalize=minmax` | 6 | +20.7% | +3.2% | 11.9% |
| `lr_schedule=cosine` | 6 | +24.9% | +26.5% | 25.7% |
| `normalize=zscore` | 6 | +67.9% | +67.2% | 67.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `median_over_runs`, `SCALES`, `WEIGHTS`, `feature_count`, `--out`

## Provenance
- GapFinder commit: `037cdf1603d6771de8f0101af7838abc1a610293` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `bfdd41b8caf786503bc4ee736dca20ece1be6a7c560eb6cb028e538e361e4388`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
