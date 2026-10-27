# Gap Report: test-v11-10

Artifact `rlbench` · generated 2026-10-15 19:49 · 139 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Paper-artifact inconsistency | +99.9% | +0.6% | ±2.0% | `max_steps=100` |

## C1: mean_reward (paper 94.93)
**Paper-artifact inconsistency** · gap +99.9% → +0.6% · 32 hypotheses tested
> Confirmed cause: reverting it brings the gap back, held-out claims hold, and the value has evidence

### Which experiment changed it?
- Branch: `B0006`, `B0018`, `B0019`, `B0042`, `B0043`, `B0044` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `2375338a-efc3-44cb-9613-d44acffe42c6` and run
  ```
  RUN_TAG=a7620bf5ebbb "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 94.89, 94.15, 99.96, 96.14, 94.7, 96.19; gap after +0.6%; result checkpoint `ec7fdf5a-e839-4d49-a906-69808e182260`
- Effect: candidate 95.52 minus naive 189.7 = -94.22, 95% bootstrap interval [-95.25, -66.92] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 94.9 steps, and that its worst seed still balances for 63.9.

- p. 1; value used: `mean_reward` = 94.93 steps (headline claim)

### What did we measure?
- Naive median 189.7 over 5 runs; repeats: 189.7, 190.4, 156.4, 190.1, 179.6
- Spread: range 156.4 to 190.4, noise band ±1.897 (2 x MAD), CV 8.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +99.9% (noise band ±2.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +99.9% (it comes back)
- PASS · Held-out claim: C2: +80.4% to -1.5% (not worse beyond noise)
- PASS · Evidence: `max_steps=100`: paper states '100'
- PASS · Effect vs noise: candidate minus naive is -94.22 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `cartpole_physics`, `discretization_bounds`, `done_thresholds`, `reset_distribution`, `force_magnitude`, `RL_SEED_BASE`, `RUN_TAG`, `timestep_dt`, `discretization_formula`, `pole_length`, `mass_cart`, `mass_pole`, `action_tiebreak`, `epsilon_decay_timing`, `q_lazy_init`, `evaluation_policy`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (23.06 noise units, gap +53.8%); `max_steps=40` (21.02 noise units, gap -57.9%); `lr_schedule=linear` (11.88 noise units, gap +76.1%); `max_steps=20` (10.48 noise units, gap -78.9%); `max_steps=4` (2.04 noise units, gap -95.8%)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `max_steps=100`: this claim +2.4%, mean |gap| 25.1% (5 runs)
  - `max_steps=2000`, `lr_schedule=inv`: this claim +43.0%, mean |gap| 32.5% (5 runs)
  - `max_steps=10000`, `lr_schedule=inv`: this claim +50.7%, mean |gap| 34.4% (5 runs)

### Equally good configurations
The target claim can't tell these 2 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `lr_schedule=linear, max_steps=100`

### History matching (every measured configuration, all claims together)
- 3 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `max_steps`: max_steps=100 (max I 0.13)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.39); lr_schedule=inv, max_steps=100 (max I 1.25)

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=100; lr_schedule=linear, max_steps=100

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 6 | +0.6% | -1.5% | 1.1% |
| `lr_schedule=linear`, `max_steps=100` | 5 | +2.4% | +47.9% | 25.1% |
| `max_steps=2000`, `lr_schedule=inv` | 5 | +43.0% | -22.1% | 32.5% |
| `max_steps=10000`, `lr_schedule=inv` | 5 | +50.7% | -18.1% | 34.4% |
| `lr_schedule=inv` | 6 | +36.3% | -35.7% | 36.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `cartpole_physics`, `discretization_bounds`, `done_thresholds`, `reset_distribution`, `force_magnitude`, `RL_SEED_BASE`, `RUN_TAG`, `timestep_dt`, `discretization_formula`, `pole_length`, `mass_cart`, `mass_pole`, `action_tiebreak`, `epsilon_decay_timing`, `q_lazy_init`, `evaluation_policy`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
