# Gap Report: test-v11-10

Artifact `rlbench` · generated 2026-10-14 21:26 · 120 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Unexplained | +72.1% | +72.1% | ±15.1% | — |

## C1: mean_reward (paper 94.93)
**Unexplained** · gap +72.1% → +72.1% · 32 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (32 hypotheses tested).

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 94.9 steps, and that its worst seed still balances for 63.9.

- p. 1; value used: `mean_reward` = 94.93 steps (headline claim)

### What did we measure?
- Naive median 163.4 over 5 runs; repeats: 198.6, 156.2, 163.4, 186.1, 157
- Spread: range 156.2 to 198.6, noise band ±14.34 (2 x MAD), CV 11.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +72.1% (noise band ±15.1% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `cartpole_physics`, `discretization_bounds`, `done_thresholds`, `reset_distribution`, `force_magnitude`, `RL_SEED_BASE`, `RUN_TAG`, `timestep_dt`, `discretization_formula`, `pole_length`, `mass_cart`, `mass_pole`, `action_tiebreak`, `epsilon_decay_timing`, `q_lazy_init`, `evaluation_policy`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=100` (4.5 noise units, gap +4.2%); `lr_schedule=inv` (1.02 noise units, gap +56.8%)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `lr_schedule=linear`: this claim +2.4%, mean |gap| 23.4% (5 runs)
  - `max_steps=100`: this claim +4.3%, mean |gap| 26.6% (6 runs)
  - `max_steps=100`, `lr_schedule=inv`: this claim -11.5%, mean |gap| 31.1% (5 runs)

### History matching (every measured configuration, all claims together)
- 6 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 6 configurations
  - `max_steps`: max_steps=100 (max I 0.5)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.58); lr_schedule=inv, max_steps=100 (max I 0.88); lr_schedule=linear, max_steps=40 (max I 2.6); lr_schedule=inv, max_steps=40 (max I 2.63)
  - `lr_schedule`: lr_schedule=inv (max I 2.9)

Notes:
- {'max_steps': '100'} closes this claim but makes held-out claims worse; rejected
- lr_schedule dropped: reverting it did not bring the gap back, and {'max_steps': '100'} fits better than {'max_steps': '100', 'lr_schedule': 'inv'}
- closest configuration tried: {'max_steps': '100'} (gap +4.3%); it did not pass verification
- history matching: 6 of 32 tested configurations fit every claim within 3 sigma

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100`, `lr_schedule=linear` | 5 | +2.4% | +44.4% | 23.4% |
| `max_steps=100` | 6 | +4.3% | +48.8% | 26.6% |
| `max_steps=100`, `lr_schedule=inv` | 5 | -11.5% | -50.6% | 31.1% |
| `lr_schedule=inv`, `max_steps=400` | 5 | +57.4% | -20.5% | 39.0% |
| `lr_schedule=inv`, `max_steps=2000` | 5 | +56.2% | -21.8% | 39.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `cartpole_physics`, `discretization_bounds`, `done_thresholds`, `reset_distribution`, `force_magnitude`, `RL_SEED_BASE`, `RUN_TAG`, `timestep_dt`, `discretization_formula`, `pole_length`, `mass_cart`, `mass_pole`, `action_tiebreak`, `epsilon_decay_timing`, `q_lazy_init`, `evaluation_policy`

## Provenance
- GapFinder commit: `634d827f07d6659ff82f6ea0924c8ba487e9d02a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
