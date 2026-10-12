# Gap Report: mcd

Artifact `mcd` · generated 2026-10-12 21:42 · 22 branch runs (1 build/load setups) · sandbox $1043.0258

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_energy_rmse (energy_rmse) | Unexplained | -76.9% | -76.9% | ±1.4% | — |

## C_energy_rmse: energy_rmse (paper 1.66)
**Unexplained** · gap -76.9% → -76.9% · 9 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (9 hypotheses tested).

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `energy_rmse` = 1.66.

### What did we measure?
- Naive median 0.3828 over 5 runs; repeats: 0.358, 0.3828, 0.394, 0.394, 0.3807
- Spread: range 0.358 to 0.394, noise band ±0.02245 (2 x MAD), CV 3.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -76.9% (noise band ±1.4% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: `n_splits=30`
- Not settable with this harness: `dropout_rate`, `tau`, `n_hidden.txt`, `MC_samples_T`, `nonlinearity`, `dropout_placement`, `data_preprocessing`, `weight_decay_lambda`, `length_scale_l`, `loss_function`, `hardware_environment`, `epochs_multiplier`, `num_hidden_layers`, `MC_log_likelihood_estimation`, `KL_objective_approximation`, `predictive_variance_formula`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `hidden=4` (4.19 noise units, gap -71.3%); `hidden=5` (4.02 noise units, gap -71.5%)
- Near alternatives (closest across all claims):
  - `n_splits=10`: this claim -78.1%, mean |gap| 43.0% (3 runs)
  - `hidden=4`: this claim -74.0%, mean |gap| 52.6% (3 runs)
  - `epochx=2000`: this claim -79.2%, mean |gap| 54.4% (3 runs)

Notes:
- evidence gate off: no evidence was checked, so this cannot be labelled Explained
- {'hidden': '4'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'hidden': '4'} (gap -74.0%); it did not pass verification

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_energy_rmse | C_yacht_rmse | Mean |gap| |
|---|---|---|---|---|
| `n_splits=10` | 3 | -78.1% | -7.9% | 43.0% |
| naive (reproduction as run) | 5 | -76.9% | -10.5% | 43.7% |
| `hidden=4` | 3 | -74.0% | -31.3% | 52.6% |
| `epochx=2000` | 3 | -79.2% | -29.5% | 54.4% |
| `hidden=5` | 3 | -78.4% | -45.3% | 61.9% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `epochx=1000000`: invalid_value, The value 1000000 for epochx exceeds the maximum allowed epochs for the training script, causing the program to reject it as an invalid value; suggested `2000`, already measured
- `n_splits=20`: invalid_value, The program rejected the value n_splits='20', indicating it is not a valid setting for the benchmark script, likely because only certain integers are accepted for cross‑validation splits. This is an invalid value error rather than a crash, timeout, or infrastructure issue. To preserve the user’s intent of using a larger number of splits than the default while staying within the allowed range, a reasonable alternative is 10 splits, which is higher than the default 3 and closer to the requested 20 without being rejected. If the tool only accepts small integers (e.g., 2‑5), then 5 would be the closest valid choice; however, assuming typical cross‑validation accepts up to at least 10, we suggest 10

## Not testable within the budget
Candidate values above the harness spec's cost limits (e.g. the paper's full scale). A gap that only these could close stays Unexplained here: `n_splits=30`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `dropout_rate`, `tau`, `n_hidden.txt`, `MC_samples_T`, `nonlinearity`, `dropout_placement`, `data_preprocessing`, `weight_decay_lambda`, `length_scale_l`, `loss_function`, `hardware_environment`, `epochs_multiplier`, `num_hidden_layers`, `MC_log_likelihood_estimation`, `KL_objective_approximation`, `predictive_variance_formula`

## Provenance
- GapFinder commit: `7c103057f622b7175731d31bb1941906178b10a2` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `ba8391a105883d412eb8a18ac545f3f8adf5b9bdb0e5903e196fd26c52f845ef`
- Cost: Nemotron billed $0.0009, sandbox reported $1043.0258 (total $1043.0267; this search; ledger extraction is included only if it shared the search's router)
