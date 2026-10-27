# Gap Report: test-gen-01

Artifact `mlbench` · generated 2026-10-15 00:44 · 41 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Explains target, conflicts with held-out | -23.4% | -15.7% | ±2.4% | `lr_schedule=cosine`, `normalize=minmax` |

## C1: test_accuracy (paper 0.7069)
**Explains target, conflicts with held-out** · gap -23.4% → -15.7% · 13 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0020`, `B0028`, `B0029` (3 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `cosine`
- Config: `normalize` naive `none`, changed to `minmax`
- Command: not recorded
- Output: `test_accuracy` 0.5958, 0.5958, 0.5958; gap after -15.7%
- Effect: candidate 0.5958 minus naive 0.5417 = +0.0541, 95% bootstrap interval [+0.03162, +0.0625] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.707 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7069 (headline claim)

### What did we measure?
- Naive median 0.5417 over 5 runs; repeats: 0.5667, 0.5333, 0.5417, 0.5625, 0.5333
- Spread: range 0.5333 to 0.5667, noise band ±0.0168 (2 x MAD), CV 2.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -23.4% (noise band ±2.4% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is +0.0541 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `SCALES`, `WEIGHTS`, `aggregation_method`, `num_runs`, `shuffling_seed_source`, `feature_count`, `out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=zscore` (2.55 noise units, gap +17.3%)
- Near alternatives (closest across all claims):
  - `normalize=minmax`: this claim -15.7%, mean |gap| 18.7% (4 runs)
  - `normalize=minmax`, `lr_schedule=step`: this claim -15.7%, mean |gap| 18.7% (3 runs)
  - `lr_schedule=cosine`: this claim -11.6%, mean |gap| 31.5% (4 runs)

### History matching (every measured configuration, all claims together)
- out-of-space suspected: 7 tested configuration(s) fit C1, and every other claim (C2) fits some tested configuration, but none of the 13 tested configurations fits them all. The claims are mutually inconsistent under every tested condition, which points to a cause outside the exposed settings (code, data or evaluation)
- Fit C1 alone (7; worst claim's implausibility in brackets, lowest is the least inconsistent): lr_schedule=cosine, normalize=minmax (3.92); lr_schedule=step, normalize=minmax (3.92); normalize=minmax (3.98); class_weight=balanced, lr_schedule=cosine (9.17); lr_schedule=cosine (9.43); class_weight=balanced, normalize=minmax (15.94)
- Equally good values: `lr_schedule` in {cosine, step}

Notes:
- {'normalize': 'minmax', 'class_weight': 'balanced'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'normalize': 'minmax', 'class_weight': 'balanced'} (gap +6.1%); it did not pass verification
- history matching: out-of-space suspected: 7 tested configuration(s) fit C1, and every other claim (C2) fits some tested configuration, but none of the 13 tested configurations fits them all. The claims are mutually inconsistent under every tested condition, which points to a cause outside the exposed settings (code, data or evaluation)
- {'lr_schedule': 'cosine', 'normalize': 'minmax'} matches C1 (I=2.98) but breaks C2 (I=3.92); no tested condition matches all claims, so the rest of the gap probably lies in code, data or evaluation, which GapFinder doesn't change

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax` | 4 | -15.7% | +21.6% | 18.7% |
| `lr_schedule=cosine`, `normalize=minmax` | 3 | -15.7% | +21.6% | 18.7% |
| `normalize=minmax`, `lr_schedule=step` | 3 | -15.7% | +21.6% | 18.7% |
| naive (reproduction as run) | 5 | -23.4% | +32.4% | 27.9% |
| `lr_schedule=cosine` | 4 | -11.6% | +51.4% | 31.5% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `SCALES`, `WEIGHTS`, `aggregation_method`, `num_runs`, `shuffling_seed_source`, `feature_count`, `out`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
