# Gap Report: test-gen-08

Artifact `mlbench` · generated 2026-10-13 00:16 · 15 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Unexplained | -18.2% | -18.2% | ±7.0% | — |

## C1: test_accuracy (paper 0.5958)
**Unexplained** · gap -18.2% → -18.2% · 2 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (2 hypotheses tested).

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.596 test accuracy.

- p. 1; value used: `test_accuracy` = 0.5958 fraction (headline claim)

### What did we measure?
- Naive median 0.4875 over 5 runs; repeats: 0.5375, 0.4875, 0.5458, 0.4667, 0.4667
- Spread: range 0.4667 to 0.5458, noise band ±0.0416 (2 x MAD), CV 7.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -18.2% (noise band ±7.0% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `SCALES`, `WEIGHTS`, `RUN_TAG`, `median_aggregation`, `hardware_cpu`, `os`, `python_version`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `epochs=20` (1.2 noise units, gap -9.8%)
- Near alternatives (closest across all claims):
  - `epochs=10`: this claim -16.1%, mean |gap| 8.4% (5 runs)
  - `epochs=20`: this claim -9.8%, mean |gap| 9.1% (5 runs)

Notes:
- skipped normalize='"none"': knob value '"none"' has shell metacharacters
- skipped normalize='"zscore"': knob value '"zscore"' has shell metacharacters
- skipped lr_schedule='"const"': knob value '"const"' has shell metacharacters
- skipped lr_schedule='"step"': knob value '"step"' has shell metacharacters
- skipped class_weight='"none"': knob value '"none"' has shell metacharacters
- skipped class_weight='"balanced"': knob value '"balanced"' has shell metacharacters
- evidence gate off: no evidence was checked, so this cannot be labelled Explained
- closest configuration tried: {'epochs': '20'} (gap -9.8%); it did not pass verification

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `epochs=10` | 5 | -16.1% | -0.8% | 8.4% |
| `epochs=20` | 5 | -9.8% | +8.4% | 9.1% |
| naive (reproduction as run) | 5 | -18.2% | -3.3% | 10.7% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `SCALES`, `WEIGHTS`, `RUN_TAG`, `median_aggregation`, `hardware_cpu`, `os`, `python_version`, `--out`

## Provenance
- GapFinder commit: `2e9291c6be5f4b9ffe219d44dfe2904a7d2d6a9f` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `81ad24a2c635c2279bd33ad3363ed7dfbe8e21683f613c866dc86e070854c074`
- Cost: Nemotron billed $0.0366, sandbox reported $0.0000 (total $0.0366; this search; ledger extraction is included only if it shared the search's router)
