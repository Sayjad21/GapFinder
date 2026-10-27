# Gap Report: test-v11-10

Artifact `rlbench` · generated 2026-10-14 22:20 · 128 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Unexplained | +88.4% | +88.4% | ±11.1% | — |

## C1: mean_reward (paper 94.93)
**Unexplained** · gap +88.4% → +88.4% · 32 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (32 hypotheses tested).

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 94.9 steps, and that its worst seed still balances for 63.9.

- p. 1; value used: `mean_reward` = 94.93 steps (headline claim)

### What did we measure?
- Naive median 178.8 over 5 runs; repeats: 173.6, 195, 197.4, 178.4, 178.8
- Spread: range 173.6 to 197.4, noise band ±10.51 (2 x MAD), CV 5.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +88.4% (noise band ±11.1% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `cartpole_physics`, `discretization_bounds`, `done_thresholds`, `reset_distribution`, `force_magnitude`, `RL_SEED_BASE`, `RUN_TAG`, `timestep_dt`, `discretization_formula`, `pole_length`, `mass_cart`, `mass_pole`, `action_tiebreak`, `epsilon_decay_timing`, `q_lazy_init`, `evaluation_policy`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=100` (7.64 noise units, gap +3.9%); `lr_schedule=inv` (4.43 noise units, gap +39.4%); `max_steps=40` (2.76 noise units, gap -57.9%); `max_steps=2000` (1.86 noise units, gap +67.7%)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `lr_schedule=linear`: this claim +3.1%, mean |gap| 25.1% (5 runs)
  - `max_steps=100`: this claim +4.5%, mean |gap| 26.4% (6 runs)
  - `lr_schedule=inv`, `max_steps=100`: this claim -11.2%, mean |gap| 32.7% (5 runs)

### History matching (every measured configuration, all claims together)
- 3 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.6); lr_schedule=inv, max_steps=100 (max I 1.45)
  - `max_steps`: max_steps=100 (max I 0.73)

Notes:
- {'max_steps': '100'} closes this claim but makes held-out claims worse; rejected
- lr_schedule dropped: with repeats, {'max_steps': '100', 'lr_schedule': 'linear'} fits {'max_steps': '100'}'s gap by less than one noise band, so it is not needed
- closest configuration tried: {'max_steps': '100'} (gap +4.5%); it did not pass verification
- history matching: 3 of 32 tested configurations fit every claim within 3 sigma

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100`, `lr_schedule=linear` | 5 | +3.1% | +47.1% | 25.1% |
| `max_steps=100` | 6 | +4.5% | +48.4% | 26.4% |
| `lr_schedule=inv`, `max_steps=100` | 5 | -11.2% | -54.2% | 32.7% |
| `lr_schedule=inv` | 6 | +28.9% | -46.8% | 37.9% |
| `lr_schedule=inv`, `max_steps=10000` | 5 | +50.3% | -43.2% | 46.7% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `cartpole_physics`, `discretization_bounds`, `done_thresholds`, `reset_distribution`, `force_magnitude`, `RL_SEED_BASE`, `RUN_TAG`, `timestep_dt`, `discretization_formula`, `pole_length`, `mass_cart`, `mass_pole`, `action_tiebreak`, `epsilon_decay_timing`, `q_lazy_init`, `evaluation_policy`

## Provenance
- GapFinder commit: `e0f13d101585ad1609a15fbf67b70128f4cfffc8` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
