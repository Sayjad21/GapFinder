# Gap Report: test-v12-02

Artifact `mlbench` · generated 2026-10-15 21:07 · 60 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Unexplained | -28.7% | -28.7% | ±2.5% | — |

## C1: test_accuracy (paper 0.6666)
**Unexplained** · gap -28.7% → -28.7% · 13 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (13 hypotheses tested).

### What did the paper report?
> Logistic regression (ours) | 0.667 | 0.431

- p. 1, Table 1; value used: `test_accuracy` = 0.6666 (headline claim)

### What did we measure?
- Naive median 0.475 over 5 runs; repeats: 0.475, 0.4667, 0.575, 0.4833, 0.4667
- Spread: range 0.4667 to 0.575, noise band ±0.0166 (2 x MAD), CV 9.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -28.7% (noise band ±2.5% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (9.29 noise units, gap -5.6%); `normalize=minmax` (7.28 noise units, gap -10.6%); `class_weight=balanced` (3.77 noise units, gap -19.4%); `lr_schedule=step` (3.77 noise units, gap -19.4%); `normalize=zscore` (1.75 noise units, gap +24.4%)
- Near alternatives (closest across all claims):
  - `normalize=minmax`: this claim -10.6%, mean |gap| 13.3% (6 runs)
  - `lr_schedule=cosine`, `normalize=minmax`: this claim -10.6%, mean |gap| 13.3% (5 runs)
  - `lr_schedule=step`, `normalize=minmax`: this claim -10.6%, mean |gap| 13.3% (5 runs)

### History matching (every measured configuration, all claims together)
- 4 of 13 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 4 configurations
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=minmax (max I 1.86); lr_schedule=step, normalize=minmax (max I 1.86)
  - `normalize`: normalize=minmax (max I 1.91)
  - `class_weight, lr_schedule`: class_weight=balanced, lr_schedule=step (max I 2.59)
- 2 separate islands (no single-knob move joins them): lr_schedule=cosine, normalize=minmax; lr_schedule=step, normalize=minmax; normalize=minmax | class_weight=balanced, lr_schedule=step

Notes:
- {'lr_schedule': 'cosine'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'lr_schedule': 'cosine'} (gap -6.2%); it did not pass verification
- history matching: 4 of 13 tested configurations fit every claim within 3 sigma

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax` | 6 | -10.6% | +16.0% | 13.3% |
| `lr_schedule=cosine`, `normalize=minmax` | 5 | -10.6% | +16.0% | 13.3% |
| `lr_schedule=step`, `normalize=minmax` | 5 | -10.6% | +16.0% | 13.3% |
| naive (reproduction as run) | 5 | -28.7% | +9.0% | 18.9% |
| `lr_schedule=step` | 6 | -22.8% | +19.3% | 21.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`

## Provenance
- GapFinder commit: `cd8c8af2b9d079dd9a57443ed501c0dd8a467d34` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
