# Gap Report: mcd

Artifact `mcd` · generated 2026-10-12 23:18 · 30 branch runs (1 build/load setups) · sandbox $733.0623

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_energy_rmse (energy_rmse) | Unexplained | -76.7% | -76.7% | ±2.8% | — |

## C_energy_rmse: energy_rmse (paper 1.66)
**Unexplained** · gap -76.7% → -76.7% · 5 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (5 hypotheses tested).

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `energy_rmse` = 1.66.

### What did we measure?
- Naive median 0.3868 over 5 runs; repeats: 0.3393, 0.3868, 0.3853, 0.4103, 0.4349
- Spread: range 0.3393 to 0.4349, noise band ±0.04699 (2 x MAD), CV 9.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -76.7% (noise band ±2.8% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `tau_values.txt`, `n_hidden.txt`, `weight_decay_lambda`, `length_scale_l`, `dropout_placement`, `normalization`, `dropout_variant`, `RL_exploration_method`, `precision_tau`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `epochx=10` (3.97 noise units, gap -65.5%); `hidden=1` (1.01 noise units, gap -73.8%)
- Near alternatives (closest across all claims):
  - `epochx=10`, `hidden=1`: this claim +3.8%, mean |gap| 41.4% (5 runs)
  - `epochx=10`: this claim -65.5%, mean |gap| 49.6% (5 runs)
  - `epochx=1000`: this claim -78.4%, mean |gap| 54.4% (5 runs)

Notes:
- {'epochx': '10', 'hidden': '1'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'epochx': '10', 'hidden': '1'} (gap +3.8%); it did not pass verification

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
- GapFinder commit: `56779a9cc2cef642dbf91ede59da97a848c305cd` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `ba8391a105883d412eb8a18ac545f3f8adf5b9bdb0e5903e196fd26c52f845ef`
- Cost: Nemotron billed $0.0000, sandbox reported $733.0623 (total $733.0623; this search; ledger extraction is included only if it shared the search's router)
