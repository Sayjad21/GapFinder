# Gap Report: test-gen-06

Artifact `mlbench` · generated 2026-10-10 21:20 · 22 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Unexplained | -36.0% | -36.0% | ±2.2% | — |

## C1: test_accuracy (paper 0.7417)
**Unexplained** · gap -36.0% → -36.0% · 5 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (5 hypotheses tested).

### What did the paper report?
> A plain logistic-regression baseline reaches 0.742 test accuracy and 0.700 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7417 (headline claim)

### What did we measure?
- Naive median 0.475 over 5 runs; repeats: 0.5375, 0.475, 0.475, 0.4667, 0.5792
- Spread: range 0.4667 to 0.5792, noise band ±0.0166 (2 x MAD), CV 9.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -36.0% (noise band ±2.2% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `weight_init_std`, `rounding_precision`, `median_aggregation`, `python_random_module`, `logit_bias`, `sigmoid_clamping`, `floating_point_determinism`, `balanced_accuracy_formula`, `hardware_cpu`, `os`, `memory_size`, `storage_device`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `n=2000` (3.01 noise units, gap -29.2%)
- Near alternatives (closest across all claims):
  - `n=2000`, `split=0.7`: this claim -24.9%, mean |gap| 22.5% (5 runs)
  - `n=2000`: this claim -29.2%, mean |gap| 26.6% (5 runs)
  - `n=1000`: this claim -33.3%, mean |gap| 30.6% (5 runs)

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
| `n=2000`, `split=0.7` | 5 | -24.9% | -20.0% | 22.5% |
| `n=2000` | 5 | -29.2% | -24.0% | 26.6% |
| `n=1000` | 5 | -33.3% | -27.9% | 30.6% |
| naive (reproduction as run) | 5 | -36.0% | -32.9% | 34.4% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `weight_init_std`, `rounding_precision`, `median_aggregation`, `python_random_module`, `logit_bias`, `sigmoid_clamping`, `floating_point_determinism`, `balanced_accuracy_formula`, `hardware_cpu`, `os`, `memory_size`, `storage_device`, `--out`

## Provenance
- GapFinder commit: `fb04d3a1ab0b0fec0acc5b342103e9444806727c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `81ad24a2c635c2279bd33ad3363ed7dfbe8e21683f613c866dc86e070854c074`
- Cost: Nemotron billed $0.0506, sandbox reported $0.0000 (total $0.0506; this search; ledger extraction is included only if it shared the search's router)
