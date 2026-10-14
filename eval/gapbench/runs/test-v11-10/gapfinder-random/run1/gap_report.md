# Gap Report: test-v11-10

Artifact `rlbench` · generated 2026-10-14 11:30 · 57 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +98.9% | -1.3% | ±6.3% | `max_steps=100`, `lr_schedule=linear` |

## C1: mean_reward (paper 94.93)
**Fits but unsupported** · gap +98.9% → -1.3% · 20 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0027`, `B0040`, `B0041` (3 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Config: `lr_schedule` naive `const`, changed to `linear`
- Command:

  Replay: fork checkpoint `91154915-483f-422a-8fdc-4c4100bd6647` and run
  ```
  RUN_TAG=c6834380eab0 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule linear --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 93, 93.74, 97.19; gap after -1.3%; result checkpoint `38c57720-a3aa-4336-95b5-e77e535df91f`
- Effect: candidate 93.74 minus naive 188.8 = -95.07, 95% bootstrap interval [-96.88, -83.55] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 94.9 steps, and that its worst seed still balances for 63.9.

- p. 1; value used: `mean_reward` = 94.93 steps (headline claim)

### What did we measure?
- Naive median 188.8 over 5 runs; repeats: 188.8, 189.1, 175.7, 191.8, 184.9
- Spread: range 175.7 to 191.8, noise band ±5.95 (2 x MAD), CV 3.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +98.9% (noise band ±6.3% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +72.8% (it comes back)
- FAIL · Counterfactual (reversal test): without `lr_schedule` the gap is -4.1% (it did NOT come back)
- PASS · Held-out claim: C2: +88.9% to -9.2% (not worse beyond noise)
- PASS · Evidence: `max_steps=100`: paper states '100'
- FAIL · Evidence: `lr_schedule=linear`: no evidence mentions 'linear'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -95.07 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `cartpole_physics`, `discretization_bounds`, `done_thresholds`, `reset_distribution`, `force_magnitude`, `RL_SEED_BASE`, `RUN_TAG`, `timestep_dt`, `discretization_formula`, `pole_length`, `mass_cart`, `mass_pole`, `action_tiebreak`, `epsilon_decay_timing`, `q_lazy_init`, `evaluation_policy`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (11.14 noise units, gap +29.1%); `max_steps=20` (3.18 noise units, gap -78.9%)
- Near alternatives (closest across all claims):
  - `max_steps=100`: this claim -4.1%, mean |gap| 20.0% (4 runs)
  - `lr_schedule=inv`, `max_steps=100`: this claim -19.3%, mean |gap| 33.4% (3 runs)
  - `lr_schedule=inv`: this claim +21.4%, mean |gap| 35.6% (4 runs)

### History matching (every measured configuration, all claims together)
- 3 of 20 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.21); lr_schedule=inv, max_steps=100 (max I 2.19)
  - `max_steps`: max_steps=100 (max I 0.82)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=linear`, `max_steps=100` | 3 | -1.3% | -9.2% | 5.2% |
| `max_steps=100` | 4 | -4.1% | -35.8% | 20.0% |
| `lr_schedule=inv`, `max_steps=100` | 3 | -19.3% | -47.5% | 33.4% |
| `lr_schedule=inv` | 4 | +21.4% | -49.8% | 35.6% |
| `max_steps=500`, `lr_schedule=inv` | 3 | +48.5% | -63.2% | 55.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `cartpole_physics`, `discretization_bounds`, `done_thresholds`, `reset_distribution`, `force_magnitude`, `RL_SEED_BASE`, `RUN_TAG`, `timestep_dt`, `discretization_formula`, `pole_length`, `mass_cart`, `mass_pole`, `action_tiebreak`, `epsilon_decay_timing`, `q_lazy_init`, `evaluation_policy`

## Provenance
- GapFinder commit: `b05f7288e1a4df8af69bb0b5e7633827b4cb46c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
