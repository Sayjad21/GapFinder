# Gap Report: test-v11-09

Artifact `mlbench` · generated 2026-10-15 00:58 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Unexplained | -29.3% | -29.3% | ±7.7% | — |

## C1: test_accuracy (paper 0.7542)
**Unexplained** · gap -29.3% → -29.3% · 61 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (61 hypotheses tested).

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.754 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7542 (headline claim)

### What did we measure?
- Naive median 0.5333 over 5 runs; repeats: 0.5583, 0.4875, 0.5333, 0.4667, 0.5625
- Spread: range 0.4667 to 0.5625, noise band ±0.0584 (2 x MAD), CV 8.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -29.3% (noise band ±7.7% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `aggregation`, `CPU`, `memory`, `OS`, `Python_version`, `random_module`, `floating_point`, `num_features`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (2.5 noise units, gap +9.9%); `lr_schedule=cosine` (1.5 noise units, gap -17.7%); `normalize=minmax` (1.07 noise units, gap -21.0%)
- Near alternatives (closest across all claims):
  - `lr=0.0005`, `normalize=zscore`: this claim +5.0%, mean |gap| 5.7% (5 runs)
  - `class_weight=balanced`, `normalize=zscore`: this claim +4.4%, mean |gap| 6.8% (5 runs)
  - `lr=0.1`, `normalize=zscore`: this claim +9.4%, mean |gap| 10.5% (5 runs)

### History matching (every measured configuration, all claims together)
- 25 of 61 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr, normalize`: lr=0.25, normalize=minmax (max I 0.18); lr=0.001, normalize=zscore (max I 0.47); lr=0.0005, normalize=zscore (max I 0.95); lr=2.5, normalize=zscore (max I 1.04); +4 more
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 0.72); class_weight=balanced, normalize=zscore (max I 1.42)

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'lr_schedule': 'cosine', 'lr': '0.01'} for 'confirm-combo')
- closest configuration not verified: {'lr': '0.25', 'normalize': 'minmax'} (gap +0.5%, 1 of 5 confirmation runs); the budget ran out first, so no attribution is made
- history matching: 25 of 61 tested configurations fit every claim within 3 sigma

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr=0.0005`, `normalize=zscore` | 5 | +5.0% | +6.4% | 5.7% |
| `class_weight=balanced`, `normalize=zscore` | 5 | +4.4% | +9.2% | 6.8% |
| `lr=0.1`, `normalize=zscore` | 5 | +9.4% | +11.7% | 10.5% |
| `lr=0.25`, `normalize=zscore` | 5 | +9.4% | +11.7% | 10.5% |
| `normalize=zscore` | 6 | +9.9% | +12.2% | 11.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `num_runs`, `aggregation`, `CPU`, `memory`, `OS`, `Python_version`, `random_module`, `floating_point`, `num_features`, `--out`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
