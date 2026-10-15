# Gap Report: mcd

Artifact `mcd` · generated 2026-10-15 15:01 · 147 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_energy_rmse (energy_rmse) | Unexplained | -76.6% | -76.6% | ±2.5% | — |

## C_energy_rmse: energy_rmse (paper 1.66)
**Unexplained** · gap -76.6% → -76.6% · 0 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (0 hypotheses tested).

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `energy_rmse` = 1.66.

### What did we measure?
- Naive median 0.3877 over 5 runs; repeats: 0.3579, 0.3559, 0.3877, 0.4086, 0.4045
- Spread: range 0.3559 to 0.4086, noise band ±0.0418 (2 x MAD), CV 6.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -76.6% (noise band ±2.5% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `tau_values.txt`, `n_hidden.txt`, `weight_decay_lambda`, `length_scale_l`, `dropout_placement`, `normalization`, `dropout_variant`, `RL_exploration_method`, `precision_tau`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives (closest across all claims):
  - `hidden=10`: this claim -71.5%, mean |gap| 37.4% (6 runs)
  - `epochx=100`: this claim -75.1%, mean |gap| 41.3% (6 runs)
  - `epochx=250`: this claim -76.3%, mean |gap| 41.5% (6 runs)

### History matching (every measured configuration, all claims together)
- out-of-space suspected: 4 tested configuration(s) fit C_energy_rmse, and every other claim (C_yacht_rmse) fits some tested configuration, but none of the 42 tested configurations fits them all. The claims are mutually inconsistent under every tested condition, which points to a cause outside the exposed settings (code, data or evaluation)
- Fit C_energy_rmse alone (4; worst claim's implausibility in brackets, lowest is the least inconsistent): epochx=1, hidden=10 (5.83); epochx=10, hidden=1 (8.71); epochx=1, hidden=5 (9.5); epochx=2 (24.18)
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
- stopped early: run budget of 147 reached (wanted 1 more run(s) of {'epochx': '5000'} for 'screen epochx=5000')
- closest configuration not verified: {'epochx': '10', 'hidden': '1'} (gap +1.3%, 1 of 5 confirmation runs); the budget ran out first, so no attribution is made
- history matching: out-of-space suspected: 4 tested configuration(s) fit C_energy_rmse, and every other claim (C_yacht_rmse) fits some tested configuration, but none of the 42 tested configurations fits them all. The claims are mutually inconsistent under every tested condition, which points to a cause outside the exposed settings (code, data or evaluation)
- history matching: the most consistent fits have a single run, so none is named; unconfirmed leads: {'epochx': '1', 'hidden': '10'} (worst I 5.83, 1 run(s)); {'epochx': '10', 'hidden': '1'} (worst I 8.71, 1 run(s)); {'epochx': '1', 'hidden': '5'} (worst I 9.5, 1 run(s))

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_energy_rmse | C_yacht_rmse | Mean |gap| |
|---|---|---|---|---|
| `hidden=10` | 6 | -71.5% | +3.4% | 37.4% |
| `epochx=100` | 6 | -75.1% | +7.6% | 41.3% |
| `epochx=250` | 6 | -76.3% | -6.7% | 41.5% |
| naive (reproduction as run) | 5 | -76.6% | -7.5% | 42.1% |
| `epochx=50` | 6 | -70.5% | +20.6% | 45.5% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `tau_values.txt`, `n_hidden.txt`, `weight_decay_lambda`, `length_scale_l`, `dropout_placement`, `normalization`, `dropout_variant`, `RL_exploration_method`, `precision_tau`

## Provenance
- GapFinder commit: `e10b678164c150d7029345557f037e6c4da3fdf6` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `629f0ecbd266686b4065a2a19bce295b6b107a7ead9900092d6d91a083b7a3c7`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
