# Gap Report: test-gen-06

Artifact `mlbench` · generated 2026-10-12 23:34 · 11 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Unexplained | -35.4% | -35.4% | ±2.2% | — |

## C1: test_accuracy (paper 0.7417)
**Unexplained** · gap -35.4% → -35.4% · 2 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (2 hypotheses tested).

### What did the paper report?
> A plain logistic-regression baseline reaches 0.742 test accuracy and 0.700 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7417 (headline claim)

### What did we measure?
- Naive median 0.4792 over 5 runs; repeats: 0.4792, 0.5, 0.4667, 0.4875, 0.475
- Spread: range 0.4667 to 0.5, noise band ±0.0166 (2 x MAD), CV 2.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -35.4% (noise band ±2.2% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `n=2000` (2.61 noise units, gap -29.6%)
- Near alternatives (closest across all claims):
  - `n=2000`: this claim -28.5%, mean |gap| 25.9% (3 runs)
  - `n=5000`: this claim -37.8%, mean |gap| 36.3% (3 runs)

Notes:
- skipped normalize='"none"': knob value '"none"' has shell metacharacters
- skipped normalize='"zscore"': knob value '"zscore"' has shell metacharacters
- skipped class_weight='"none"': knob value '"none"' has shell metacharacters
- skipped class_weight='"balanced"': knob value '"balanced"' has shell metacharacters
- skipped lr_schedule='"const"': knob value '"const"' has shell metacharacters
- skipped lr_schedule='"step"': knob value '"step"' has shell metacharacters
- closest configuration tried: {'n': '2000'} (gap -28.5%); it did not pass verification

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `n=2000` | 3 | -28.5% | -23.3% | 25.9% |
| naive (reproduction as run) | 5 | -35.4% | -32.2% | 33.8% |
| `n=5000` | 3 | -37.8% | -34.9% | 36.3% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`

## Provenance
- GapFinder commit: `441160eee0dbc476a0c6ade0ba048870e1946da1` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `81ad24a2c635c2279bd33ad3363ed7dfbe8e21683f613c866dc86e070854c074`
- Cost: Nemotron billed $0.0494, sandbox reported $0.0000 (total $0.0494; this search; ledger extraction is included only if it shared the search's router)
