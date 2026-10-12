# Gap Report: mcd

Artifact `mcd` · generated 2026-10-12 04:25 · 26 branch runs (1 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C_energy_rmse (energy_rmse) | Unexplained | -77.8% | -77.8% | ±3.4% | — |

## C_energy_rmse: energy_rmse (paper 1.66)
**Unexplained** · gap -77.8% → -77.8% · 5 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (5 hypotheses tested).

### What did the paper report?
- Quote not recorded (the report has no linked ledger claim); the value used was `energy_rmse` = 1.66.

### What did we measure?
- Naive median 0.3692 over 5 runs; repeats: 0.3532, 0.3692, 0.3976, 0.4551, 0.3318
- Spread: range 0.3318 to 0.4551, noise band ±0.05687 (2 x MAD), CV 12.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -77.8% (noise band ±3.4% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `tau_values.txt`, `n_hidden.txt`, `weight_decay_lambda`, `length_scale_l`, `dropout_placement`, `normalization`, `dropout_variant`, `RL_exploration_method`, `precision_tau`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives (closest across all claims):
  - `hidden=5`: this claim -76.0%, mean |gap| 43.2% (5 runs)
  - `hidden=4`: this claim -78.5%, mean |gap| 55.9% (5 runs)
  - `epochx=1000`: this claim -76.6%, mean |gap| 62.8% (5 runs)

Notes:
- no hypothesis moved the gap by more than 1 noise units

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C_energy_rmse | C_yacht_rmse | Mean |gap| |
|---|---|---|---|---|
| `hidden=5` | 5 | -76.0% | -10.3% | 43.2% |
| naive (reproduction as run) | 5 | -77.8% | -14.6% | 46.2% |
| `hidden=4` | 5 | -78.5% | -33.3% | 55.9% |
| `epochx=1000` | 5 | -76.6% | -49.0% | 62.8% |
| `epochx=2000` | 5 | -78.6% | -48.5% | 63.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `tau_values.txt`, `n_hidden.txt`, `weight_decay_lambda`, `length_scale_l`, `dropout_placement`, `normalization`, `dropout_variant`, `RL_exploration_method`, `precision_tau`

## Provenance
- GapFinder commit: `13bfb34923b1a085c8304dee5b96924f47e9f6e2` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `de04a283f3f32a1ff75d2b668f5625c9735cb493c869f6f6a3fc68088ce3d13d`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
