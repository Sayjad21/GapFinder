# Gap Report: test-gen-01

Artifact `mlbench` · generated 2026-10-15 00:44 · 47 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Explains target, conflicts with held-out | -24.0% | -14.5% | ±1.2% | `class_weight=balanced`, `lr_schedule=cosine` |

## C1: test_accuracy (paper 0.7069)
**Explains target, conflicts with held-out** · gap -24.0% → -14.5% · 17 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0023`, `B0036`, `B0037` (3 run(s) of the same config)
- Config: `class_weight` naive `none`, changed to `balanced`
- Config: `lr_schedule` naive `const`, changed to `cosine`
- Command: not recorded
- Output: `test_accuracy` 0.6, 0.6042, 0.6167; gap after -14.5%
- Effect: candidate 0.6042 minus naive 0.5375 = +0.0667, 95% bootstrap interval [+0.04834, +0.0784] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> We revisit logistic regression trained with mini-batch SGD on a synthetic screening dataset and show that it reaches 0.707 test accuracy.

- p. 1; value used: `test_accuracy` = 0.7069 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5625, 0.5333, 0.5375, 0.5333, 0.5458
- Spread: range 0.5333 to 0.5625, noise band ±0.0084 (2 x MAD), CV 2.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -24.0% (noise band ±1.2% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is +0.0667 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `median_aggregation (workflow)`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `normalize=minmax` (6.94 noise units, gap -15.7%); `normalize=zscore` (5.61 noise units, gap +17.3%)
- Near alternatives (closest across all claims):
  - `normalize=minmax`: this claim -15.7%, mean |gap| 18.7% (4 runs)
  - `normalize=minmax`, `lr_schedule=cosine`: this claim -15.7%, mean |gap| 18.7% (3 runs)
  - `normalize=minmax`, `lr_schedule=step`: this claim -15.7%, mean |gap| 18.7% (3 runs)

### History matching (every measured configuration, all claims together)
- out-of-space suspected: 4 tested configuration(s) fit C1, and every other claim (C2) fits some tested configuration, but none of the 13 tested configurations fits them all. The claims are mutually inconsistent under every tested condition, which points to a cause outside the exposed settings (code, data or evaluation)
- Fit C1 alone (4; worst claim's implausibility in brackets, lowest is the least inconsistent): class_weight=balanced, lr_schedule=cosine (9.42); lr_schedule=cosine (9.46); class_weight=balanced, normalize=minmax (16.93); class_weight=balanced, normalize=zscore (17.29)

Notes:
- {'normalize': 'minmax', 'class_weight': 'balanced'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'normalize': 'minmax', 'class_weight': 'balanced'} (gap +8.5%); it did not pass verification
- history matching: out-of-space suspected: 4 tested configuration(s) fit C1, and every other claim (C2) fits some tested configuration, but none of the 13 tested configurations fits them all. The claims are mutually inconsistent under every tested condition, which points to a cause outside the exposed settings (code, data or evaluation)
- {'class_weight': 'balanced', 'lr_schedule': 'cosine'} matches C1 (I=2.74) but breaks C2 (I=9.42); no tested condition matches all claims, so the rest of the gap probably lies in code, data or evaluation, which GapFinder doesn't change

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax` | 4 | -15.7% | +21.6% | 18.7% |
| `normalize=minmax`, `lr_schedule=cosine` | 3 | -15.7% | +21.6% | 18.7% |
| `normalize=minmax`, `lr_schedule=step` | 3 | -15.7% | +21.6% | 18.7% |
| naive (reproduction as run) | 5 | -24.0% | +31.9% | 27.9% |
| `lr_schedule=step`, `class_weight=balanced` | 3 | -24.0% | +31.9% | 27.9% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `lr_schedule=constant`: other, triage failed: super: not in cache and GF_CACHE_ONLY=1, so no paid call was made

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `median_aggregation (workflow)`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
