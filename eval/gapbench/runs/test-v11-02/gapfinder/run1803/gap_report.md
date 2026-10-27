# Gap Report: test-v11-02

Artifact `mlbench` · generated 2026-10-15 19:42 · 33 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Unexplained | -18.7% | -18.7% | ±1.2% | — |

## C1: test_accuracy (paper 0.6666)
**Unexplained** · gap -18.7% → -18.7% · 13 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (13 hypotheses tested).

### What did the paper report?
> A plain logistic-regression baseline reaches 0.667 test accuracy and 0.485 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.6666 (headline claim)

### What did we measure?
- Naive median 0.5417 over 5 runs; repeats: 0.5417, 0.5458, 0.5458, 0.5375, 0.4875
- Spread: range 0.4875 to 0.5458, noise band ±0.0082 (2 x MAD), CV 4.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -18.7% (noise band ±1.2% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (8.63 noise units, gap -8.1%); `normalize=minmax` (6.6 noise units, gap -10.6%)
- Near alternatives (closest across all claims):
  - `normalize=minmax`: this claim -10.6%, mean |gap| 6.9% (4 runs)
  - `normalize=minmax`, `lr_schedule=cosine`: this claim -10.6%, mean |gap| 6.9% (3 runs)
  - `normalize=minmax`, `lr_schedule=step`: this claim -10.6%, mean |gap| 6.9% (3 runs)

### History matching (every measured configuration, all claims together)
- 5 of 13 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 5 configurations
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=minmax (max I 1.86); lr_schedule=step, normalize=minmax (max I 1.86)
  - `normalize`: normalize=minmax (max I 1.89)
  - `class_weight`: class_weight=balanced (max I 2.89)
  - `lr_schedule`: lr_schedule=step (max I 2.99)
- 2 separate islands (no single-knob move joins them): lr_schedule=cosine, normalize=minmax; lr_schedule=step, normalize=minmax; normalize=minmax | class_weight=balanced

Notes:
- {'lr_schedule': 'cosine'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'lr_schedule': 'cosine'} (gap -8.4%); it did not pass verification
- history matching: 5 of 13 tested configurations fit every claim within 3 sigma

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax` | 4 | -10.6% | +3.1% | 6.9% |
| `normalize=minmax`, `lr_schedule=cosine` | 3 | -10.6% | +3.1% | 6.9% |
| `normalize=minmax`, `lr_schedule=step` | 3 | -10.6% | +3.1% | 6.9% |
| naive (reproduction as run) | 5 | -18.7% | +12.2% | 15.5% |
| `lr_schedule=cosine` | 4 | -8.4% | +25.8% | 17.1% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `--out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
