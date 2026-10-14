# Gap Report: test-v11-03

Artifact `mlbench` · generated 2026-10-14 11:11 · 198 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Unexplained | -31.9% | -31.9% | ±1.1% | — |

## C1: test_accuracy (paper 0.7833)
**Unexplained** · gap -31.9% → -31.9% · 64 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (64 hypotheses tested).

### What did the paper report?
> A plain logistic-regression baseline reaches 0.783 test accuracy and 0.752 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7833 (headline claim)

### What did we measure?
- Naive median 0.5333 over 5 runs; repeats: 0.4667, 0.5375, 0.5375, 0.5333, 0.4833
- Spread: range 0.4667 to 0.5375, noise band ±0.0084 (2 x MAD), CV 6.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -31.9% (noise band ±1.1% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `NUM_RUNS`, `AGGREGATION_METHOD`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (24.8 noise units, gap +5.3%); `lr_schedule=cosine` (8.93 noise units, gap -22.3%); `normalize=minmax` (7.44 noise units, gap -23.9%); `positive_rate=0.1` (4.96 noise units, gap -26.6%); `label_noise=0.025` (1 noise units, gap -30.8%)
- Near alternatives (closest across all claims):
  - `label_noise=0.1`, `normalize=zscore`: this claim +3.2%, mean |gap| 4.0% (5 runs)
  - `label_noise=0.025`, `normalize=zscore`: this claim +5.9%, mean |gap| 6.8% (5 runs)
  - `normalize=zscore`: this claim +5.9%, mean |gap| 6.8% (6 runs)

### History matching (every measured configuration, all claims together)
- 12 of 63 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `batch_size, normalize`: batch_size=3, normalize=minmax (max I 0.77); batch_size=3, normalize=zscore (max I 0.8); batch_size=64, normalize=zscore (max I 1.28)
  - `label_noise, normalize`: label_noise=0.1, normalize=zscore (max I 0.85); label_noise=0.025, normalize=zscore (max I 1.27)
  - `normalize, positive_rate`: normalize=zscore, positive_rate=0.15 (max I 1.26)
  - `normalize`: normalize=zscore (max I 1.27)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 1.28); lr_schedule=step, normalize=zscore (max I 1.28)
  - `batch_size, lr_schedule`: batch_size=3, lr_schedule=cosine (max I 1.69)
- 3 separate islands (no single-knob move joins them): batch_size=3, normalize=minmax; batch_size=3, normalize=zscore; label_noise=0.1, normalize=zscore | lr_schedule=cosine, positive_rate=0.1; lr_schedule=cosine, positive_rate=0.15 | batch_size=3, lr_schedule=cosine

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'normalize': 'zscore', 'batch_size': '3'} for 'confirm-combo')
- closest configuration not verified: {'positive_rate': '0.1', 'normalize': 'minmax'} (gap +0.0%, 1 of 5 confirmation runs); the budget ran out first, so no attribution is made
- history matching: 12 of 63 tested configurations fit every claim within 3 sigma

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `label_noise=0.1`, `normalize=zscore` | 5 | +3.2% | +4.8% | 4.0% |
| `label_noise=0.025`, `normalize=zscore` | 5 | +5.9% | +7.7% | 6.8% |
| `normalize=zscore` | 6 | +5.9% | +7.8% | 6.8% |
| `lr_schedule=cosine`, `normalize=zscore` | 5 | +5.9% | +7.8% | 6.8% |
| `lr_schedule=step`, `normalize=zscore` | 5 | +5.9% | +7.8% | 6.8% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: invalid_value, The code computes math.log(positive_rate / (1 - positive_rate)), which requires the argument to be >0. Setting positive_rate to 0.0 makes the argument zero, causing a math domain error. A small positive value like 0.001 preserves the intent of a low positive rate while keeping the expression defined; retried as `positive_rate=0.001`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `NUM_RUNS`, `AGGREGATION_METHOD`

## Provenance
- GapFinder commit: `b05f7288e1a4df8af69bb0b5e7633827b4cb46c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0007, sandbox reported $0.0000 (total $0.0007; this search; ledger extraction is included only if it shared the search's router)
