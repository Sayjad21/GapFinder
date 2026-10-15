# Gap Report: test-v13-02

Artifact `mlbench` · generated 2026-10-16 00:35 · 29 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Unexplained | -38.7% | -38.7% | ±6.0% | — |

## C1: test_accuracy (paper 0.8292)
**Unexplained** · gap -38.7% → -38.7% · 5 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (5 hypotheses tested).

### What did the paper report?
> A plain logistic-regression baseline reaches 0.829 test accuracy and 0.810 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.8292 (headline claim)

### What did we measure?
- Naive median 0.5083 over 5 runs; repeats: 0.4875, 0.4833, 0.5375, 0.5083, 0.5708
- Spread: range 0.4833 to 0.5708, noise band ±0.05 (2 x MAD), CV 7.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -38.7% (noise band ±6.0% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `--normalize`, `python_version`, `os`, `cpu_arch`, `random_module`, `memory_size`, `disk_type`, `math_module`, `floating_point_precision`, `PYTHONHASHSEED`, `OMP_NUM_THREADS`, `MKL_NUM_THREADS`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (2.83 noise units, gap -21.6%); `class_weight=balanced` (1 noise units, gap -32.7%)
- Near alternatives (closest across all claims):
  - `lr_schedule=cosine`: this claim -24.9%, mean |gap| 24.1% (6 runs)
  - `lr_schedule=cosine`, `class_weight=balanced`: this claim -27.6%, mean |gap| 26.3% (5 runs)
  - `lr_schedule=step`: this claim -33.2%, mean |gap| 32.4% (6 runs)

### History matching (every measured configuration, all claims together)
- out-of-space likely: no tested configuration comes within 3 sigma of C1, C2, among 5 tested

Notes:
- closest configuration tried: {'lr_schedule': 'cosine'} (gap -24.9%); it did not pass verification
- history matching: out-of-space likely: no tested configuration comes within 3 sigma of C1, C2, among 5 tested

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=cosine` | 6 | -24.9% | -23.4% | 24.1% |
| `lr_schedule=cosine`, `class_weight=balanced` | 5 | -27.6% | -25.0% | 26.3% |
| `lr_schedule=step` | 6 | -33.2% | -31.6% | 32.4% |
| `class_weight=balanced` | 6 | -33.9% | -32.3% | 33.1% |
| naive (reproduction as run) | 5 | -38.7% | -37.7% | 38.2% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `--normalize`, `python_version`, `os`, `cpu_arch`, `random_module`, `memory_size`, `disk_type`, `math_module`, `floating_point_precision`, `PYTHONHASHSEED`, `OMP_NUM_THREADS`, `MKL_NUM_THREADS`, `--out`

## Provenance
- GapFinder commit: `e9c31fd1405f5c8aae4bd880eadcdc8d491fad02` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `460f2b20cfc37f744e9659681610940370212e103b69f68e976ce9617f6797c2`
- Cost: Nemotron billed $0.1557, sandbox reported $0.0000 (total $0.1557; this search; ledger extraction is included only if it shared the search's router)
