# Gap Report: test-gen-01

Artifact `mlbench` · generated 2026-10-13 00:01 · 37 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Unexplained | -29.3% | -29.3% | ±9.4% | — |

## C1: test_accuracy (paper 0.7069)
**Unexplained** · gap -29.3% → -29.3% · 8 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (8 hypotheses tested).

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.707 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7069 (headline claim)

### What did we measure?
- Naive median 0.5 over 5 runs; repeats: 0.5458, 0.475, 0.5, 0.4667, 0.5375
- Spread: range 0.4667 to 0.5458, noise band ±0.0666 (2 x MAD), CV 7.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -29.3% (noise band ±9.4% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (1.88 noise units, gap -11.6%); `normalize=minmax` (1.44 noise units, gap -15.7%); `normalize=zscore` (1.27 noise units, gap +17.3%)
- Near alternatives (closest across all claims):
  - `normalize=minmax`: this claim -15.7%, mean |gap| 18.7% (5 runs)
  - `lr_schedule=cosine`, `normalize=minmax`: this claim -15.7%, mean |gap| 18.7% (5 runs)
  - `lr_schedule=cosine`: this claim -11.6%, mean |gap| 31.5% (5 runs)

Notes:
- evidence gate off: no evidence was checked, so this cannot be labelled Explained
- {'normalize': 'minmax', 'class_weight': 'balanced'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'normalize': 'minmax', 'class_weight': 'balanced'} (gap +7.9%); it did not pass verification

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax` | 5 | -15.7% | +21.6% | 18.7% |
| `lr_schedule=cosine`, `normalize=minmax` | 5 | -15.7% | +21.6% | 18.7% |
| naive (reproduction as run) | 5 | -29.3% | +20.6% | 24.9% |
| `lr_schedule=cosine` | 5 | -11.6% | +51.4% | 31.5% |
| `lr_schedule=cosine`, `class_weight=balanced` | 5 | -15.7% | +47.4% | 31.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `2e9291c6be5f4b9ffe219d44dfe2904a7d2d6a9f` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `81ad24a2c635c2279bd33ad3363ed7dfbe8e21683f613c866dc86e070854c074`
- Cost: Nemotron billed $0.1806, sandbox reported $0.0000 (total $0.1806; this search; ledger extraction is included only if it shared the search's router)
