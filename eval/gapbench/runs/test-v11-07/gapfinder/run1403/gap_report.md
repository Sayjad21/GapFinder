# Gap Report: test-v11-07

Artifact `mlbench` · generated 2026-10-15 18:58 · 5 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Reproduced | -0.5% | n/a | ±7.8% | — |

## C1: test_accuracy (paper 0.5361)
**Reproduced**: naive gap -0.5% is inside the noise band ±7.8%.

### Which experiment changed it?
- None was needed: the naive run is inside the noise band of the paper's value.

### What did the paper report?
> A plain logistic-regression baseline reaches 0.536 test accuracy and 0.543 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.5361 (headline claim)

### What did we measure?
- Naive median 0.5333 over 5 runs; repeats: 0.5333, 0.5542, 0.475, 0.5375, 0.4833
- Spread: range 0.475 to 0.5542, noise band ±0.0418 (2 x MAD), CV 6.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -0.5% (noise band ±7.8% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives: none recorded

Notes:
- naive run is within the noise band of the paper's value

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| naive (reproduction as run) | 5 | -0.5% | -0.7% | 0.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
