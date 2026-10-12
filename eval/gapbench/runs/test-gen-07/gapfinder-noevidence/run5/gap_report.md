# Gap Report: test-gen-07

Artifact `mlbench` · generated 2026-10-13 00:13 · 23 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Unexplained | +8.0% | +8.0% | ±5.1% | — |

## C1: test_accuracy (paper 0.4938)
**Unexplained** · gap +8.0% → +8.0% · 8 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (8 hypotheses tested).

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.494 test accuracy.

- p. 1; value used: `test_accuracy` = 0.4938 (headline claim)

### What did we measure?
- Naive median 0.5333 over 5 runs; repeats: 0.5375, 0.5208, 0.5333, 0.4875, 0.5458
- Spread: range 0.4875 to 0.5458, noise band ±0.025 (2 x MAD), CV 4.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +8.0% (noise band ±5.1% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives (closest across all claims):
  - `class_weight=balanced`: this claim -0.4%, mean |gap| 0.7% (3 runs)
  - `normalize=minmax`: this claim +20.7%, mean |gap| 11.9% (3 runs)
  - `lr_schedule=step`: this claim +13.9%, mean |gap| 15.1% (3 runs)

Notes:
- no hypothesis moved the gap by more than 1 noise units

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `class_weight=balanced` | 3 | -0.4% | +0.9% | 0.7% |
| naive (reproduction as run) | 5 | +8.0% | +8.5% | 8.2% |
| `normalize=minmax` | 3 | +20.7% | +3.2% | 11.9% |
| `lr_schedule=step` | 3 | +13.9% | +16.2% | 15.1% |
| `lr_schedule=cosine` | 3 | +28.3% | +30.2% | 29.2% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `2e9291c6be5f4b9ffe219d44dfe2904a7d2d6a9f` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `81ad24a2c635c2279bd33ad3363ed7dfbe8e21683f613c866dc86e070854c074`
- Cost: Nemotron billed $0.0466, sandbox reported $0.0000 (total $0.0466; this search; ledger extraction is included only if it shared the search's router)
