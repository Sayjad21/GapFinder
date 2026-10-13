# Gap Report: MC Dropout post-hoc, re-labelled from recorded runs

Artifact `mcd` · generated 2026-10-14 00:42 · 30 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_energy_rmse (energy_rmse) | Explains target, conflicts with held-out | -76.7% | +3.8% | ±2.8% | `epochx=10`, `hidden=1` |

## C_energy_rmse: energy_rmse (paper 1.66)
**Explains target, conflicts with held-out** · gap -76.7% → +3.8% · 0 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0026`, `B0030`, `B0027`, `B0028`, `B0029` (5 run(s) of the same config)
- Config: `epochx` naive `500`, changed to `10`
- Config: `hidden` naive `2`, changed to `1`
- Command: not recorded
- Output: `energy_rmse` 1.723, 1.723, 1.74, 1.782, 1.598; gap after +3.8%
- Effect: candidate 1.723 minus naive 0.3868 = +1.336, 95% bootstrap interval [+1.256, +1.379] (5 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `energy_rmse` = 1.66.

### What did we measure?
- Naive median 0.3868 over 5 runs; repeats: 0.3393, 0.3853, 0.4349, 0.4103, 0.3868
- Spread: range 0.3393 to 0.4349, noise band ±0.04699 (2 x MAD), CV 9.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -76.7% (noise band ±2.8% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is +1.336 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `tau_values.txt`, `n_hidden.txt`, `weight_decay_lambda`, `length_scale_l`, `dropout_placement`, `normalization`, `dropout_variant`, `RL_exploration_method`, `precision_tau`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives (closest across all claims):
  - `epochx=10`: this claim -65.5%, mean |gap| 49.6% (5 runs)
  - `epochx=1000`: this claim -78.4%, mean |gap| 54.4% (5 runs)
  - `hidden=4`: this claim -78.0%, mean |gap| 57.1% (5 runs)

### History matching (every measured configuration, all claims together)
- out-of-space suspected: 1 tested configuration(s) fit C_energy_rmse, and every other claim (C_yacht_rmse) fits some tested configuration, but none of the 5 tested configurations fits them all. The claims are mutually inconsistent under every tested condition, which points to a cause outside the exposed settings (code, data or evaluation)

Notes:
- stopped early: run budget of 30 reached (wanted 1 more run(s) of {'epochx': '2000'} for 'screen epochx=2000')
- {'epochx': '10', 'hidden': '1'} (gap +3.8%) was verified from existing runs and rejected: {'epochx': '10', 'hidden': '1'} closes this claim but makes held-out claims worse; rejected
- {'epochx': '10'} (gap -65.5%) was verified from existing runs and rejected: {'epochx': '10'} closes this claim but makes held-out claims worse; rejected
- {'hidden': '1'} (gap -73.5%) was verified from existing runs and rejected: {'hidden': '1'} closes this claim but makes held-out claims worse; rejected
- history matching: out-of-space suspected: 1 tested configuration(s) fit C_energy_rmse, and every other claim (C_yacht_rmse) fits some tested configuration, but none of the 5 tested configurations fits them all. The claims are mutually inconsistent under every tested condition, which points to a cause outside the exposed settings (code, data or evaluation)
- {'epochx': '10', 'hidden': '1'} matches C_energy_rmse (I=0.58) but breaks C_yacht_rmse (I=7.55); no tested condition matches all claims, so the rest of the gap probably lies in code, data or evaluation, which GapFinder doesn't change

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_energy_rmse | C_yacht_rmse | Mean |gap| |
|---|---|---|---|---|
| `epochx=10`, `hidden=1` | 5 | +3.8% | +79.0% | 41.4% |
| naive (reproduction as run) | 5 | -76.7% | -6.2% | 41.4% |
| `epochx=10` | 5 | -65.5% | +33.7% | 49.6% |
| `epochx=1000` | 5 | -78.4% | -30.4% | 54.4% |
| `hidden=4` | 5 | -78.0% | -36.2% | 57.1% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `tau_values.txt`, `n_hidden.txt`, `weight_decay_lambda`, `length_scale_l`, `dropout_placement`, `normalization`, `dropout_variant`, `RL_exploration_method`, `precision_tau`

## Provenance
- GapFinder commit: `9afd753ce82a8fb1fb0f044a1638177aeb5a7ad7` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `9b08a608c0e0b53ef533bc2ad6e693780cbfd14e89189a9d0b1c6f8e9a549cd5`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
