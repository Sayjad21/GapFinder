# Gap Report: test-v13-10

Artifact `mlbench` · generated 2026-10-16 01:38 · 23 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Unexplained | -41.2% | -41.2% | ±5.0% | — |

## C1: test_accuracy (paper 0.8292)
**Unexplained** · gap -41.2% → -41.2% · 5 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (5 hypotheses tested).

### What did the paper report?
> A plain logistic-regression baseline reaches 0.829 test accuracy and 0.810 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.8292 (headline claim)

### What did we measure?
- Naive median 0.4875 over 5 runs; repeats: 0.4875, 0.4833, 0.5458, 0.4667, 0.5458
- Spread: range 0.4667 to 0.5458, noise band ±0.0416 (2 x MAD), CV 7.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -41.2% (noise band ±5.0% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--normalize`, `PYTHON_VERSION`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (2.81 noise units, gap -27.1%)
- Near alternatives (closest across all claims):
  - `lr_schedule=cosine`, `class_weight=balanced`: this claim -25.6%, mean |gap| 24.3% (5 runs)
  - `lr_schedule=cosine`: this claim -25.6%, mean |gap| 24.8% (6 runs)
  - `lr_schedule=step`, `class_weight=balanced`: this claim -34.7%, mean |gap| 33.7% (5 runs)

### History matching (every measured configuration, all claims together)
- out-of-space likely: no tested configuration comes within 3 sigma of C1, C2, among 5 tested

Notes:
- class_weight dropped: with repeats, {'lr_schedule': 'cosine', 'class_weight': 'balanced'} fits {'lr_schedule': 'cosine'}'s gap by less than one noise band, so it is not needed
- closest configuration tried: {'lr_schedule': 'cosine'} (gap -25.6%); it did not pass verification
- history matching: out-of-space likely: no tested configuration comes within 3 sigma of C1, C2, among 5 tested

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=cosine`, `class_weight=balanced` | 5 | -25.6% | -23.0% | 24.3% |
| `lr_schedule=cosine` | 6 | -25.6% | -24.1% | 24.8% |
| `lr_schedule=step`, `class_weight=balanced` | 5 | -34.7% | -32.6% | 33.7% |
| naive (reproduction as run) | 5 | -41.2% | -40.5% | 40.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--normalize`, `PYTHON_VERSION`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `460f2b20cfc37f744e9659681610940370212e103b69f68e976ce9617f6797c2`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
