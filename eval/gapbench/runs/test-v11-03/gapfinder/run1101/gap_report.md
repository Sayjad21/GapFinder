# Gap Report: test-v11-03

Artifact `mlbench` · generated 2026-10-15 00:34 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Unexplained | -28.2% | -28.2% | ±4.3% | — |

## C1: test_accuracy (paper 0.7833)
**Unexplained** · gap -28.2% → -28.2% · 35 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (35 hypotheses tested).

### What did the paper report?
> A plain logistic-regression baseline reaches 0.783 test accuracy and 0.752 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.7833 (headline claim)

### What did we measure?
- Naive median 0.5625 over 5 runs; repeats: 0.4667, 0.5625, 0.5625, 0.5792, 0.5333
- Spread: range 0.4667 to 0.5792, noise band ±0.0334 (2 x MAD), CV 8.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -28.2% (noise band ±4.3% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `NUM_RUNS`, `AGGREGATION_METHOD`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (5.36 noise units, gap +5.3%); `lr_schedule=cosine` (1.62 noise units, gap -21.3%); `normalize=minmax` (1 noise units, gap -23.9%)
- Near alternatives (closest across all claims):
  - `normalize=zscore`: this claim +5.9%, mean |gap| 6.8% (6 runs)
  - `lr_schedule=cosine`: this claim -21.8%, mean |gap| 20.1% (3 runs)
  - `positive_rate=0.006`: this claim -35.6%, mean |gap| 28.2% (6 runs)

### History matching (every measured configuration, all claims together)
- 8 of 42 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 8 configurations
  - `batch_size, normalize`: batch_size=16, normalize=zscore (max I 0.8); batch_size=64, normalize=zscore (max I 0.93)
  - `normalize, positive_rate`: normalize=zscore, positive_rate=0.65 (max I 0.88); normalize=zscore, positive_rate=0.15 (max I 1.16)
  - `label_noise, normalize`: label_noise=0.0, normalize=zscore (max I 0.92)
  - `lr_schedule, normalize`: lr_schedule=cosine, normalize=zscore (max I 0.93); lr_schedule=step, normalize=zscore (max I 0.93)
  - `normalize`: normalize=zscore (max I 1.21)

Notes:
- stopped early: run budget of 200 reached (wanted 1 more run(s) of {'normalize': 'minmax', 'lr_schedule': 'cosine'} for 'combine')
- closest configuration not verified: {'positive_rate': '0.15', 'normalize': 'zscore'} (gap -0.5%, 1 of 5 confirmation runs); the budget ran out first, so no attribution is made
- history matching: 8 of 42 tested configurations fit every claim within 3 sigma

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=zscore` | 6 | +5.9% | +7.8% | 6.8% |
| `lr_schedule=cosine` | 3 | -21.8% | -18.4% | 20.1% |
| naive (reproduction as run) | 5 | -28.2% | -25.3% | 26.7% |
| `positive_rate=0.006` | 6 | -35.6% | -20.8% | 28.2% |
| `batch_size=1` | 6 | -30.0% | -26.9% | 28.5% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `positive_rate=0.0`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `NUM_RUNS`, `AGGREGATION_METHOD`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
