# Gap Report: test-v13-10

Artifact `mlbench` · generated 2026-10-16 02:08 · 33 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Unexplained | -41.2% | -41.2% | ±0.6% | — |

## C1: test_accuracy (paper 0.8292)
**Unexplained** · gap -41.2% → -41.2% · 5 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (5 hypotheses tested).

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `test_accuracy` = 0.8292.

### What did we measure?
- Naive median 0.4875 over 5 runs; repeats: 0.5458, 0.4875, 0.4875, 0.5375, 0.4875
- Spread: range 0.4875 to 0.5458, noise band ±0.004875 (2 x MAD), CV 5.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -41.2% (noise band ±0.6% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--normalize`, `SCALES`, `WEIGHTS`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (24.78 noise units, gap -26.6%); `lr_schedule=step` (10.26 noise units, gap -35.2%); `class_weight=balanced` (9.39 noise units, gap -35.7%)
- Near alternatives (closest across all claims):
  - `lr_schedule=cosine`: this claim -24.1%, mean |gap| 23.4% (6 runs)
  - `lr_schedule=cosine`, `class_weight=balanced`: this claim -26.6%, mean |gap| 25.2% (5 runs)
  - `class_weight=balanced`, `lr_schedule=step`: this claim -34.7%, mean |gap| 33.7% (5 runs)

### History matching (every measured configuration, all claims together)
- out-of-space likely: no tested configuration comes within 3 sigma of C1, C2, among 5 tested

Notes:
- closest configuration tried: {'lr_schedule': 'cosine'} (gap -24.1%); it did not pass verification
- history matching: out-of-space likely: no tested configuration comes within 3 sigma of C1, C2, among 5 tested

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=cosine` | 6 | -24.1% | -22.8% | 23.4% |
| `lr_schedule=cosine`, `class_weight=balanced` | 5 | -26.6% | -23.7% | 25.2% |
| `class_weight=balanced`, `lr_schedule=step` | 5 | -34.7% | -32.6% | 33.7% |
| `lr_schedule=step` | 6 | -34.9% | -33.0% | 33.9% |
| `class_weight=balanced` | 6 | -35.7% | -33.5% | 34.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--normalize`, `SCALES`, `WEIGHTS`, `--out`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `460f2b20cfc37f744e9659681610940370212e103b69f68e976ce9617f6797c2`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
