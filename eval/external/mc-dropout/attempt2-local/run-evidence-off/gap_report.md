# Gap Report: mcd

Artifact `mcd` · generated 2026-10-12 15:22 · 26 branch runs (1 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_energy_rmse (energy_rmse) | Unexplained | -78.2% | -78.2% | ±2.0% | — |

## C_energy_rmse: energy_rmse (paper 1.66)
**Unexplained** · gap -78.2% → -78.2% · 5 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (5 hypotheses tested).

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `energy_rmse` = 1.66.

### What did we measure?
- Naive median 0.3611 over 5 runs; repeats: 0.3437, 0.3442, 0.4436, 0.3744, 0.3611
- Spread: range 0.3437 to 0.4436, noise band ±0.0337 (2 x MAD), CV 11.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -78.2% (noise band ±2.0% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `tau_values.txt`, `n_hidden.txt`, `weight_decay_lambda`, `length_scale_l`, `dropout_placement`, `normalization`, `dropout_variant`, `RL_exploration_method`, `precision_tau`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives (closest across all claims):
  - `hidden=5`: this claim -75.5%, mean |gap| 47.7% (5 runs)
  - `hidden=4`: this claim -79.3%, mean |gap| 56.0% (5 runs)
  - `epochx=1000`: this claim -76.8%, mean |gap| 62.6% (5 runs)

Notes:
- no hypothesis moved the gap by more than 1 noise units

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_energy_rmse | C_yacht_rmse | Mean |gap| |
|---|---|---|---|---|
| naive (reproduction as run) | 5 | -78.2% | +2.0% | 40.1% |
| `hidden=5` | 5 | -75.5% | -19.9% | 47.7% |
| `hidden=4` | 5 | -79.3% | -32.7% | 56.0% |
| `epochx=1000` | 5 | -76.8% | -48.5% | 62.6% |
| `epochx=2000` | 5 | -78.3% | -56.0% | 67.1% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `tau_values.txt`, `n_hidden.txt`, `weight_decay_lambda`, `length_scale_l`, `dropout_placement`, `normalization`, `dropout_variant`, `RL_exploration_method`, `precision_tau`

## Provenance
- GapFinder commit: not recorded (no git checkout)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `de04a283f3f32a1ff75d2b668f5625c9735cb493c869f6f6a3fc68088ce3d13d`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
