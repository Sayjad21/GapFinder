# Gap Report: test-v11-05

Artifact `mlbench` · generated 2026-10-14 23:33 · 197 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Unexplained | -26.3% | -26.3% | ±3.4% | — |

## C1: test_accuracy (paper 0.7292)
**Unexplained** · gap -26.3% → -26.3% · 53 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (53 hypotheses tested).

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.729 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7292 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5625, 0.5375, 0.4833, 0.5375, 0.55
- Spread: range 0.4833 to 0.5625, noise band ±0.025 (2 x MAD), CV 5.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -26.3% (noise band ±3.4% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `os`, `evaluation_metric`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (3.67 noise units, gap +13.7%); `lr_schedule=cosine` (3.33 noise units, gap -14.9%); `normalize=minmax` (2.33 noise units, gap -18.3%)
- Near alternatives (closest across all claims):
  - `lr_schedule=cosine`, `epochs=30`: this claim -14.3%, mean |gap| 10.9% (5 runs)
  - `lr_schedule=cosine`: this claim -15.4%, mean |gap| 12.3% (3 runs)
  - `epochs=10`, `lr_schedule=cosine`: this claim -16.6%, mean |gap| 13.4% (5 runs)

### History matching (every measured configuration, all claims together)
- 9 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 9 configurations
  - `epochs, normalize`: epochs=75, normalize=minmax (max I 0.42)
  - `epochs, lr_schedule`: epochs=75, lr_schedule=cosine (max I 1.35); epochs=75, lr_schedule=step (max I 2.11); epochs=30, lr_schedule=cosine (max I 2.46); epochs=10, lr_schedule=cosine (max I 2.96)
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 2.08); class_weight=balanced, normalize=zscore (max I 2.26)
  - `class_weight, lr_schedule`: class_weight=balanced, lr_schedule=cosine (max I 2.44)
  - `lr_schedule`: lr_schedule=cosine (max I 2.59)
- 3 separate islands (no single-knob move joins them): epochs=75, lr_schedule=cosine; epochs=75, lr_schedule=step; class_weight=balanced, lr_schedule=cosine | class_weight=balanced, normalize=minmax; class_weight=balanced, normalize=zscore | epochs=75, normalize=minmax

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'lr_schedule': 'cosine', 'epochs': '75'} for 'confirm-combo')
- closest configuration not verified: {'epochs': '75', 'normalize': 'minmax'} (gap +2.3%, 1 of 5 confirmation runs); the budget ran out first, so no attribution is made
- history matching: 9 of 53 tested configurations fit every claim within 3 sigma

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=cosine`, `epochs=30` | 5 | -14.3% | -7.6% | 10.9% |
| `lr_schedule=cosine` | 3 | -15.4% | -9.1% | 12.3% |
| `epochs=10`, `lr_schedule=cosine` | 5 | -16.6% | -10.1% | 13.4% |
| `epochs=8`, `lr_schedule=cosine` | 5 | -17.7% | -12.2% | 14.9% |
| `normalize=zscore` | 6 | +13.1% | +19.8% | 16.5% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `num_runs`, `aggregation`, `SCALES`, `WEIGHTS`, `os`, `evaluation_metric`

## Provenance
- GapFinder commit: `efb2f63a257a40b9982099a274f2e882f272b80c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
