# Gap Report: test-v11-05

Artifact `mlbench` · generated 2026-10-15 00:35 · 199 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Unexplained | -33.1% | -33.1% | ±3.4% | — |

## C1: test_accuracy (paper 0.7292)
**Unexplained** · gap -33.1% → -33.1% · 53 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (53 hypotheses tested).

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.729 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7292 (headline claim)

### What did we measure?
- Naive median 0.4875 over 5 runs; repeats: 0.4875, 0.5375, 0.4792, 0.5625, 0.475
- Spread: range 0.475 to 0.5625, noise band ±0.025 (2 x MAD), CV 7.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -33.1% (noise band ±3.4% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (5.67 noise units, gap +13.7%); `lr_schedule=cosine` (4.83 noise units, gap -16.6%); `normalize=minmax` (4.33 noise units, gap -18.3%); `epochs=3` (2.67 noise units, gap -24.0%); `epochs=750` (2.5 noise units, gap -24.6%) (and 5 more in the JSON)
- Near alternatives (closest across all claims):
  - `epochs=750`, `lr_schedule=cosine`: this claim +8.6%, mean |gap| 10.6% (5 runs)
  - `epochs=20`, `lr_schedule=cosine`: this claim -14.3%, mean |gap| 10.7% (5 runs)
  - `lr_schedule=cosine`: this claim -16.6%, mean |gap| 13.2% (3 runs)

### History matching (every measured configuration, all claims together)
- 16 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `epochs, lr_schedule`: epochs=750, lr_schedule=step (max I 0.53); epochs=750, lr_schedule=cosine (max I 2.02); epochs=20, lr_schedule=cosine (max I 2.17); epochs=2, lr_schedule=step (max I 2.79)
  - `class_weight, normalize`: class_weight=balanced, normalize=minmax (max I 1.63); class_weight=balanced, normalize=zscore (max I 1.86)
  - `class_weight, lr_schedule`: class_weight=balanced, lr_schedule=cosine (max I 2.2); class_weight=balanced, lr_schedule=step (max I 2.5)
  - `class_weight, epochs`: class_weight=balanced, epochs=750 (max I 2.28)
  - `lr_schedule`: lr_schedule=cosine (max I 2.55)
- 4 separate islands (no single-knob move joins them): epochs=750, lr_schedule=step; epochs=750, lr_schedule=cosine; epochs=20, lr_schedule=cosine | class_weight=balanced, normalize=minmax; class_weight=balanced, normalize=zscore; normalize=zscore | class_weight=balanced, epochs=750; class_weight=balanced, epochs=10 | epochs=750, normalize=minmax

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'normalize': 'minmax', 'epochs': '20'} for 'confirm-combo')
- closest configuration not verified: {'lr_schedule': 'step', 'epochs': '750'} (gap +1.1%, 1 of 5 confirmation runs); the budget ran out first, so no attribution is made
- history matching: 16 of 53 tested configurations fit every claim within 3 sigma

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `epochs=750`, `lr_schedule=cosine` | 5 | +8.6% | +12.7% | 10.6% |
| `epochs=20`, `lr_schedule=cosine` | 5 | -14.3% | -7.1% | 10.7% |
| `lr_schedule=cosine` | 3 | -16.6% | -9.9% | 13.2% |
| `epochs=10`, `lr_schedule=cosine` | 5 | -18.3% | -11.9% | 15.1% |
| `epochs=8`, `lr_schedule=cosine` | 5 | -18.3% | -13.2% | 15.7% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
