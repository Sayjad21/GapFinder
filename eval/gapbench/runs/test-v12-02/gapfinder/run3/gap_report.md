# Gap Report: test-v12-02

Artifact `mlbench` · generated 2026-10-15 08:49 · 36 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (test_accuracy) | Explains target, conflicts with held-out | -19.4% | -10.6% | ±1.3% | `lr_schedule=cosine`, `normalize=minmax` |

## C1: test_accuracy (paper 0.6666)
**Explains target, conflicts with held-out** · gap -19.4% → -10.6% · 13 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0017`, `B0025`, `B0026` (3 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `cosine`
- Config: `normalize` naive `none`, changed to `minmax`
- Command: not recorded
- Output: `test_accuracy` 0.5958, 0.5958, 0.5958; gap after -10.6%
- Effect: candidate 0.5958 minus naive 0.5375 = +0.0583, 95% bootstrap interval [+0.04166, +0.06082] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> A plain logistic-regression baseline reaches 0.667 test accuracy and 0.431 balanced accuracy on a synthetic screening task.

- p. 1; value used: `test_accuracy` = 0.6666 (headline claim)

### What did we measure?
- Naive median 0.5375 over 5 runs; repeats: 0.5375, 0.5375, 0.5583, 0.5583, 0.5333
- Spread: range 0.5333 to 0.5583, noise band ±0.0084 (2 x MAD), CV 2.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -19.4% (noise band ±1.3% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is +0.0583 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives (closest across all claims):
  - `normalize=minmax`: this claim -10.6%, mean |gap| 13.3% (4 runs)
  - `lr_schedule=step`, `normalize=minmax`: this claim -10.6%, mean |gap| 13.3% (3 runs)
  - `lr_schedule=step`, `class_weight=balanced`: this claim -19.4%, mean |gap| 22.6% (3 runs)

### History matching (every measured configuration, all claims together)
- out-of-space suspected: 6 tested configuration(s) fit C1, and every other claim (C2) fits some tested configuration, but none of the 13 tested configurations fits them all. The claims are mutually inconsistent under every tested condition, which points to a cause outside the exposed settings (code, data or evaluation)
- Fit C1 alone (6; worst claim's implausibility in brackets, lowest is the least inconsistent): lr_schedule=cosine, normalize=minmax (3.09); lr_schedule=step, normalize=minmax (3.09); normalize=minmax (3.11); lr_schedule=cosine (8.29); class_weight=balanced, lr_schedule=cosine (8.4); class_weight=balanced, normalize=minmax (15.53)
- Equally good values: `lr_schedule` in {cosine, step}

Notes:
- {'lr_schedule': 'cosine'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'lr_schedule': 'cosine'} (gap -7.8%); it did not pass verification
- history matching: out-of-space suspected: 6 tested configuration(s) fit C1, and every other claim (C2) fits some tested configuration, but none of the 13 tested configurations fits them all. The claims are mutually inconsistent under every tested condition, which points to a cause outside the exposed settings (code, data or evaluation)
- {'lr_schedule': 'cosine', 'normalize': 'minmax'} matches C1 (I=2.05) but breaks C2 (I=3.09); no tested condition matches all claims, so the rest of the gap probably lies in code, data or evaluation, which GapFinder doesn't change

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `normalize=minmax` | 4 | -10.6% | +16.0% | 13.3% |
| `normalize=minmax`, `lr_schedule=cosine` | 3 | -10.6% | +16.0% | 13.3% |
| `lr_schedule=step`, `normalize=minmax` | 3 | -10.6% | +16.0% | 13.3% |
| naive (reproduction as run) | 5 | -19.4% | +25.8% | 22.6% |
| `lr_schedule=step`, `class_weight=balanced` | 3 | -19.4% | +25.8% | 22.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `f01fe3d9a0095f98d6304ad0543b917ca8e529eb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `d40af83ac9e7d490c83a7c14873dd0bfa078dcbe3144d8e4646b0d9ed4967432`
- Cost: Nemotron billed $0.1461, sandbox reported $0.0000 (total $0.1461; this search; ledger extraction is included only if it shared the search's router)
