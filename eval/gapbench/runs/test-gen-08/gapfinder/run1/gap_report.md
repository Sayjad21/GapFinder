# Gap Report: test-gen-08

Artifact `mlbench` · generated 2026-10-10 21:23 · 7 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Unexplained | -10.5% | -10.5% | ±7.0% | — |

## C1: test_accuracy (paper 0.5958)
**Unexplained** · gap -10.5% → -10.5% · 2 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (2 hypotheses tested).

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.596 test accuracy.

- p. 1; value used: `test_accuracy` = 0.5958 (headline claim)

### What did we measure?
- Naive median 0.5333 over 5 runs; repeats: 0.475, 0.5333, 0.5375, 0.5542, 0.4875
- Spread: range 0.475 to 0.5542, noise band ±0.0418 (2 x MAD), CV 6.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -10.5% (noise band ±7.0% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `runs`, `aggregation`, `PYTHON_VERSION`, `OS`, `CPU`, `memory`, `storage`, `float_determinism`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives: none recorded

Notes:
- skipped normalize='"none"': knob value '"none"' has shell metacharacters
- skipped normalize='"zscore"': knob value '"zscore"' has shell metacharacters
- skipped lr_schedule='"const"': knob value '"const"' has shell metacharacters
- skipped lr_schedule='"step"': knob value '"step"' has shell metacharacters
- skipped class_weight='"none"': knob value '"none"' has shell metacharacters
- skipped class_weight='"balanced"': knob value '"balanced"' has shell metacharacters
- no hypothesis moved the gap by more than 1 noise units

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| naive (reproduction as run) | 5 | -10.5% | +7.7% | 9.1% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `runs`, `aggregation`, `PYTHON_VERSION`, `OS`, `CPU`, `memory`, `storage`, `float_determinism`, `--out`

## Provenance
- GapFinder commit: `fb04d3a1ab0b0fec0acc5b342103e9444806727c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `81ad24a2c635c2279bd33ad3363ed7dfbe8e21683f613c866dc86e070854c074`
- Cost: Nemotron billed $0.0521, sandbox reported $0.0000 (total $0.0521; this search; ledger extraction is included only if it shared the search's router)
