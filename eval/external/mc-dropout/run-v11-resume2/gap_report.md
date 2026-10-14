# Gap Report: mcd

Artifact `mcd` · generated 2026-10-14 10:37 · 147 branch runs (1 build/load setups) · sandbox $182.1775

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_energy_rmse (energy_rmse) | Explains target, conflicts with held-out | -78.0% | +11.5% | ±1.5% | `epochx=1`, `hidden=10` |

## C_energy_rmse: energy_rmse (paper 1.66)
**Explains target, conflicts with held-out** · gap -78.0% → +11.5% · 48 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0075`, `B0036`, `B0037`, `B0038`, `B0039` (5 run(s) of the same config)
- Config: `epochx` naive `500`, changed to `1`
- Config: `hidden` naive `2`, changed to `10`
- Command: not recorded
- Output: `energy_rmse` 1.657, 1.653, 1.85, 1.851, 1.852; gap after +11.5%
- Effect: candidate 1.85 minus naive 0.3659 = +1.485, 95% bootstrap interval [+1.273, +1.498] (5 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `energy_rmse` = 1.66.

### What did we measure?
- Naive median 0.3659 over 5 runs; repeats: 0.4277, 0.3659, 0.3532, 0.3479, 0.377
- Spread: range 0.3479 to 0.4277, noise band ±0.02541 (2 x MAD), CV 8.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -78.0% (noise band ±1.5% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is +1.485 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `tau_values.txt`, `n_hidden.txt`, `weight_decay_lambda`, `length_scale_l`, `dropout_placement`, `normalization`, `dropout_variant`, `RL_exploration_method`, `precision_tau`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `epochx=2` (41.38 noise units, gap +14.6%); `epochx=5` (13.19 noise units, gap -57.8%); `epochx=10` (8.13 noise units, gap -65.5%); `hidden=1` (2.51 noise units, gap -74.1%); `hidden=5` (2.12 noise units, gap -74.7%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `epochx=1000`: this claim -77.9%, mean |gap| 40.5% (6 runs)
  - `hidden=4`: this claim -74.7%, mean |gap| 46.3% (6 runs)
  - `hidden=5`: this claim -74.7%, mean |gap| 49.8% (6 runs)

### History matching (every measured configuration, all claims together)
- out-of-space suspected: 5 tested configuration(s) fit C_energy_rmse, and every other claim (C_yacht_rmse) fits some tested configuration, but none of the 40 tested configurations fits them all. The claims are mutually inconsistent under every tested condition, which points to a cause outside the exposed settings (code, data or evaluation)
- Leads outside the settings (static code checks, nothing run; check these first):
  - selection in code: the code selects best_ll, best_network, best_tau, best_dropout by comparing ll > best_ll over split in range(int(n_splits)); dropout_rate in dropout_rates; tau in tau_values: a tuning protocol the paper may describe differently (e.g. a different search, grid or budget) (`experiment.py:163`)
  - unexposed setting: `batch_size = 128` is fixed in the code; no flag sets it (`net/net.py:70`)
  - unexposed setting: `lengthscale = 0.01` is fixed in the code; no flag sets it (`net/net.py:71`)
  - fixed seed: random seed fixed to 1 (`experiment.py:87`)
  - split fraction: `num_training_examples` uses a fixed fraction 0.8; no flag sets it (`experiment.py:132`)
  - unexposed setting: `predict(..., batch_size=500)`: fixed in evaluation; no flag sets it (`net/net.py:122`)
  - unexposed setting: `T = 10000` is fixed in the code; no flag sets it (`net/net.py:126`)
  - unexposed setting: `predict(..., batch_size=500)`: fixed in evaluation; no flag sets it (`net/net.py:128`)

Notes:
- stopped early: run budget of 150 reached (wanted 4 more run(s) of {'epochx': '1', 'hidden': '1'} for 'confirm-combo')
- closest configuration not verified: {'epochx': '1', 'hidden': '20'} (gap +3.8%, 1 of 5 confirmation runs); the budget ran out first, so no attribution is made
- history matching: out-of-space suspected: 5 tested configuration(s) fit C_energy_rmse, and every other claim (C_yacht_rmse) fits some tested configuration, but none of the 40 tested configurations fits them all. The claims are mutually inconsistent under every tested condition, which points to a cause outside the exposed settings (code, data or evaluation)
- {'epochx': '1', 'hidden': '10'} matches C_energy_rmse (I=1.25) but breaks C_yacht_rmse (I=9); no tested condition matches all claims, so the rest of the gap probably lies in code, data or evaluation, which GapFinder doesn't change

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_energy_rmse | C_yacht_rmse | Mean |gap| |
|---|---|---|---|---|
| `epochx=1000` | 6 | -77.9% | -3.1% | 40.5% |
| `hidden=4` | 6 | -74.7% | -17.9% | 46.3% |
| naive (reproduction as run) | 5 | -78.0% | -21.4% | 49.7% |
| `hidden=5` | 6 | -74.7% | -24.9% | 49.8% |
| `epochx=2000` | 6 | -79.4% | -26.1% | 52.8% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `hidden=20`: other, The program likely restricts hidden layer size to certain values (e.g., powers of two) and rejected 20 as invalid. [not taken as invalid_value: the log shows no rejection]
- `hidden=100`: crash, The script executed but encountered a RecursionError when computing gradients, indicating that the hidden=100 setting caused excessive recursion depth (likely due to an overly large network), leading to a crash

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `tau_values.txt`, `n_hidden.txt`, `weight_decay_lambda`, `length_scale_l`, `dropout_placement`, `normalization`, `dropout_variant`, `RL_exploration_method`, `precision_tau`

## Provenance
- GapFinder commit: `3f82ad6ddcfec38f5e6a68eb4f22d5b314b3d4b3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `3d8d6228b7be5a02cf5921a394c4d80c83bd00bf55bf5b99463b3388de6d8ffd`
- Cost: Nemotron billed $0.0000, sandbox reported $182.1775 (total $182.1775; this search; ledger extraction is included only if it shared the search's router)
