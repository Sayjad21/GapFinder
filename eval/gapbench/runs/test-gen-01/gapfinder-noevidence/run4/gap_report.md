# Gap Report: test-gen-01

Artifact `mlbench` · generated 2026-10-12 23:59 · 56 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Unexplained | -24.0% | -24.0% | ±1.2% | — |

## C1: test_accuracy (paper 0.7069)
**Unexplained** · gap -24.0% → -24.0% · 15 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (15 hypotheses tested).

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.707 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7069 accuracy (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5375, 0.5417, 0.5375, 0.5792, 0.4875
- Spread: range 0.4875 to 0.5792, noise band ±0.0084 (2 x MAD), CV 6.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -24.0% (noise band ±1.2% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `number_of_runs`, `RUN_TAG`, `SCALES`, `WEIGHTS`, `aggregation_method`, `data_generation_formula`, `train_test_split_method`, `output_rounding`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=cosine` (9.92 noise units, gap -12.2%); `normalize=minmax` (6.94 noise units, gap -15.7%); `normalize=zscore` (5.61 noise units, gap +17.3%); `split=0.9` (4.46 noise units, gap -18.7%); `lr=0.1` (3.48 noise units, gap -19.8%)
- Near alternatives (closest across all claims):
  - `normalize=minmax`: this claim -15.7%, mean |gap| 18.7% (5 runs)
  - `normalize=minmax`, `lr_schedule=cosine`: this claim -15.7%, mean |gap| 18.7% (5 runs)
  - `normalize=minmax`, `lr=0.1`: this claim -13.4%, mean |gap| 20.2% (5 runs)

Notes:
- evidence gate off: no evidence was checked, so this cannot be labelled Explained
- {'lr_schedule': 'cosine'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'lr_schedule': 'cosine'} (gap -12.2%); it did not pass verification

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax` | 5 | -15.7% | +21.6% | 18.7% |
| `normalize=minmax`, `lr_schedule=cosine` | 5 | -15.7% | +21.6% | 18.7% |
| `normalize=minmax`, `lr=0.1` | 5 | -13.4% | +27.0% | 20.2% |
| `normalize=minmax`, `split=0.9` | 5 | -19.8% | +21.6% | 20.7% |
| `split=0.9` | 5 | -32.8% | +15.2% | 24.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `number_of_runs`, `RUN_TAG`, `SCALES`, `WEIGHTS`, `aggregation_method`, `data_generation_formula`, `train_test_split_method`, `output_rounding`

## Provenance
- GapFinder commit: `2e9291c6be5f4b9ffe219d44dfe2904a7d2d6a9f` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `81ad24a2c635c2279bd33ad3363ed7dfbe8e21683f613c866dc86e070854c074`
- Cost: Nemotron billed $0.0473, sandbox reported $0.0000 (total $0.0473; this search; ledger extraction is included only if it shared the search's router)
