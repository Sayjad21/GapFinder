# Gap Report: mcd

Artifact `mcd` · generated 2026-10-16 03:31 · 200 branch runs (1 build/load setups) · sandbox $3487.1544

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_energy_rmse (energy_rmse) | Explains target, conflicts with held-out | -78.9% | +2.8% | ±1.9% | `epochx=10`, `hidden=1` |

## C_energy_rmse: energy_rmse (paper 1.66)
**Explains target, conflicts with held-out** · gap -78.9% → +2.8% · 53 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0095`, `B0126`, `B0157`, `B0158`, `B0159` (5 run(s) of the same config)
- Config: `epochx` naive `500`, changed to `10`
- Config: `hidden` naive `2`, changed to `1`
- Command: not recorded
- Output: `energy_rmse` 1.707, 1.69, 1.602, 1.858, 1.838; gap after +2.8%
- Effect: candidate 1.707 minus naive 0.3499 = +1.357, 95% bootstrap interval [+1.262, +1.505] (5 candidate runs vs 5 naive runs)

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `energy_rmse` = 1.66.

### What did we measure?
- Naive median 0.3499 over 5 runs; repeats: 0.3499, 0.372, 0.3928, 0.3417, 0.3339
- Spread: range 0.3339 to 0.3928, noise band ±0.03199 (2 x MAD), CV 6.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -78.9% (noise band ±1.9% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is +1.357 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `tau_values.txt`, `n_hidden.txt`, `weight_decay_lambda`, `length_scale_l`, `dropout_placement`, `normalization`, `dropout_variant`, `RL_exploration_method`, `precision_tau`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `epochx=2` (36.44 noise units, gap +8.7%); `epochx=5` (11.14 noise units, gap -57.5%); `epochx=1` (3.93 noise units, gap +71.3%); `epochx=100` (3.87 noise units, gap -71.5%); `epochx=50` (2.18 noise units, gap -74.7%)
- Near alternatives (closest across all claims):
  - `epochx=100`: this claim -71.1%, mean |gap| 37.3% (6 runs)
  - `epochx=100`, `hidden=5`: this claim -71.4%, mean |gap| 38.3% (2 runs)
  - `epochx=50`: this claim -73.6%, mean |gap| 38.4% (6 runs)

### History matching (every measured configuration, all claims together)
- out-of-space suspected: 5 tested configuration(s) fit C_energy_rmse, and every other claim (C_yacht_rmse) fits some tested configuration, but none of the 42 tested configurations fits them all. The claims are mutually inconsistent under every tested condition, which points to a cause outside the exposed settings (code, data or evaluation)
- Fit C_energy_rmse alone (5; worst claim's implausibility in brackets, lowest is the least inconsistent): epochx=10, hidden=1 (10.03); epochx=1, hidden=10 (11.59); epochx=1, hidden=5 (15.47); epochx=1, hidden=20 (17.39); epochx=2 (23.45)
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
- {'epochx': '1', 'hidden': '5'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'epochx': '1', 'hidden': '5'} (gap -1.9%); it did not pass verification
- history matching: out-of-space suspected: 5 tested configuration(s) fit C_energy_rmse, and every other claim (C_yacht_rmse) fits some tested configuration, but none of the 42 tested configurations fits them all. The claims are mutually inconsistent under every tested condition, which points to a cause outside the exposed settings (code, data or evaluation)
- {'epochx': '10', 'hidden': '1'} matches C_energy_rmse (I=0.91) but breaks C_yacht_rmse (I=10.03); no tested condition matches all claims, so the rest of the gap probably lies in code, data or evaluation, which GapFinder doesn't change
- patch round stopped early: run budget of 200 reached (wanted 1 more run(s) of {'epochx': '10', 'hidden': '1', '@ast:net/net.py:70:batch_size': '32'} for 'patch screen')

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_energy_rmse | C_yacht_rmse | Mean |gap| |
|---|---|---|---|---|
| `epochx=100` | 6 | -71.1% | +3.4% | 37.3% |
| `epochx=100`, `hidden=5` | 2 | -71.4% | +5.2% | 38.3% |
| `epochx=50` | 6 | -73.6% | -3.2% | 38.4% |
| `epochx=250` | 6 | -77.3% | +0.1% | 38.7% |
| `epochx=100`, `hidden=10` | 2 | -68.4% | +10.6% | 39.5% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `epochx=5000`: other, The program likely enforces an upper bound on epochx (e.g., ≤1000) and rejected the value 5000 as exceeding that limit. [not taken as invalid_value: the log shows no rejection]
- `hidden=20`: other, The program likely restricts hidden layer size to certain values (e.g., powers of two) and rejected 20 as invalid. [not taken as invalid_value: the log shows no rejection]
- `hidden=100`: crash, The script executed but encountered a RecursionError when computing gradients, indicating that the hidden=100 setting caused excessive recursion depth (likely due to an overly large network), leading to a crash
- `hidden=200`: crash, Setting hidden=200 creates a neural network with 200 hidden units, causing the gradient computation to generate a computation graph so deep that Python's recursion limit is exceeded, resulting in a RecursionError and crash.

The stack trace shows repeated calls to `account_for` in theano/gradient.py, indicating infinite recursion while traversing the graph, which ultimately triggers the RecursionError and aborts the experiment.

This is a runtime crash due to excessive resource usage, not a validation rejection of the parameter value itself

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `tau_values.txt`, `n_hidden.txt`, `weight_decay_lambda`, `length_scale_l`, `dropout_placement`, `normalization`, `dropout_variant`, `RL_exploration_method`, `precision_tau`

## Provenance
- GapFinder commit: `d24d2e96ac2da532fd5818afdacdf17c8429ec48` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `4ff27834659b7f90ab6b862ba0484645dfa28660e76e6c87e7f0f79b17480a92`
- Cost: Nemotron billed $0.0000, sandbox reported $3487.1544 (total $3487.1544; this search; ledger extraction is included only if it shared the search's router)
