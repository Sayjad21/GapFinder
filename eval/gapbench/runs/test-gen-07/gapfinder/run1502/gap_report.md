# Gap Report: test-gen-07

Artifact `mlbench` · generated 2026-10-15 19:15 · 26 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Unexplained | +13.9% | +13.9% | ±1.7% | — |

## C1: test_accuracy (paper 0.4938)
**Unexplained** · gap +13.9% → +13.9% · 13 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (13 hypotheses tested).

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.494 test accuracy.

- p. 1; value used: `test_accuracy` = 0.4938 (headline claim)

### What did we measure?
- Naive median 0.5625 over 5 runs; repeats: 0.5667, 0.5625, 0.5708, 0.5375, 0.5625
- Spread: range 0.5375 to 0.5708, noise band ±0.0084 (2 x MAD), CV 2.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +13.9% (noise band ±1.7% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `class_weight=balanced` (1.99 noise units, gap +10.5%); `lr_schedule=step` (1.49 noise units, gap +11.4%)
- Near alternatives (closest across all claims):
  - `class_weight=balanced`: this claim +9.7%, mean |gap| 11.1% (4 runs)
  - `class_weight=balanced`, `lr_schedule=step`: this claim +11.4%, mean |gap| 12.7% (3 runs)
  - `lr_schedule=step`: this claim +13.1%, mean |gap| 13.9% (4 runs)

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 2 configurations
  - `class_weight`: class_weight=balanced (max I 1.84)
  - `lr_schedule`: lr_schedule=step (max I 2.96)

Notes:
- no hypothesis moved the gap by more than 1 noise units
- history matching: the naive configuration is within noise of every claim

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `class_weight=balanced` | 4 | +9.7% | +12.5% | 11.1% |
| `class_weight=balanced`, `lr_schedule=step` | 3 | +11.4% | +14.1% | 12.7% |
| `lr_schedule=step` | 4 | +13.1% | +14.7% | 13.9% |
| naive (reproduction as run) | 5 | +13.9% | +15.6% | 14.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
