# Gap Report: test-v11-10

Artifact `rlbench` · generated 2026-10-16 01:56 · 116 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Partially explained | +86.9% | +3.4% | ±21.9% | `max_steps=100` |

## C1: mean_reward (paper 94.93)
**Partially explained** · gap +86.9% → +3.4% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it closes only part of the gap, or the paper's own value was not tested

### Which experiment changed it?
- Branch: `B0006`, `B0018`, `B0019`, `B0040`, `B0041`, `B0042` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `41324fa6-ec0f-44c9-8e8a-fef5858d1403` and run
  ```
  RUN_TAG=a53b01a9d00b "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 99.17, 97.19, 95.84, 88.31, 99.72, 99.61; gap after +3.4%; result checkpoint `a3c689c3-7097-4da7-a307-45aec79fb52a`
- Effect: candidate 98.18 minus naive 177.4 = -79.25, 95% bootstrap interval [-101.3, -67.31] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 94.9 steps, and that its worst seed still balances for 63.9.

- p. 1; value used: `mean_reward` = 94.93 steps (headline claim)

### What did we measure?
- Naive median 177.4 over 5 runs; repeats: 177.4, 200, 167.1, 162.3, 181.9
- Spread: range 162.3 to 200, noise band ±20.75 (2 x MAD), CV 8.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +86.9% (noise band ±21.9% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +86.9% (it comes back)
- PASS · Held-out claim: C2: -22.1% to +36.7% (not worse beyond noise)
- PASS · Evidence: `max_steps=100`: paper states '100'
- PASS · Effect vs noise: candidate minus naive is -79.25 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `cartpole_physics`, `discretization_bounds`, `done_thresholds`, `reset_distribution`, `force_magnitude`, `RL_SEED_BASE`, `RUN_TAG`, `timestep_dt`, `discretization_formula`, `pole_length`, `mass_cart`, `mass_pole`, `action_tiebreak`, `epsilon_decay_timing`, `q_lazy_init`, `evaluation_policy`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (2.85 noise units, gap +24.5%); `max_steps=40` (1.33 noise units, gap -57.9%)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `lr_schedule=inv`: this claim -5.4%, mean |gap| 23.5% (5 runs)
  - `max_steps=100`, `lr_schedule=linear`: this claim +3.5%, mean |gap| 25.3% (5 runs)
  - `lr_schedule=inv`: this claim +36.3%, mean |gap| 36.6% (6 runs)

### History matching (every measured configuration, all claims together)
- 3 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `max_steps`: max_steps=100 (max I 0.41)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.6); lr_schedule=inv, max_steps=100 (max I 0.76)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 6 | +3.4% | +36.7% | 20.0% |
| `max_steps=100`, `lr_schedule=inv` | 5 | -5.4% | -41.6% | 23.5% |
| `max_steps=100`, `lr_schedule=linear` | 5 | +3.5% | +47.0% | 25.3% |
| `lr_schedule=inv` | 6 | +36.3% | -37.0% | 36.6% |
| `max_steps=400`, `lr_schedule=inv` | 5 | +46.5% | -29.7% | 38.1% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `cartpole_physics`, `discretization_bounds`, `done_thresholds`, `reset_distribution`, `force_magnitude`, `RL_SEED_BASE`, `RUN_TAG`, `timestep_dt`, `discretization_formula`, `pole_length`, `mass_cart`, `mass_pole`, `action_tiebreak`, `epsilon_decay_timing`, `q_lazy_init`, `evaluation_policy`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
