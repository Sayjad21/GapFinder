# Gap Report: test-v11-10

Artifact `rlbench` · generated 2026-10-15 01:16 · 146 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Partially explained | +94.3% | +4.5% | ±3.9% | `max_steps=100` |

## C1: mean_reward (paper 94.93)
**Partially explained** · gap +94.3% → +4.5% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it closes only part of the gap, or the paper's own value was not tested

### Which experiment changed it?
- Branch: `B0006`, `B0018`, `B0019`, `B0054`, `B0055`, `B0056` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `5402dc08-5654-4c32-a4a2-ab8f68e275db` and run
  ```
  RUN_TAG=9540bdefa00d "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 98.33, 99.44, 99.94, 98.98, 98.77, 99.53; gap after +4.5%; result checkpoint `3a25fb89-1a2e-418c-9c02-fe84ea91c2c7`
- Effect: candidate 99.21 minus naive 184.5 = -85.25, 95% bootstrap interval [-94.54, -72.16] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 94.9 steps, and that its worst seed still balances for 63.9.

- p. 1; value used: `mean_reward` = 94.93 steps (headline claim)

### What did we measure?
- Naive median 184.5 over 5 runs; repeats: 168.2, 196.4, 184.5, 182.6, 184.8
- Spread: range 168.2 to 196.4, noise band ±3.68 (2 x MAD), CV 5.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +94.3% (noise band ±3.9% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +94.3% (it comes back)
- PASS · Held-out claim: C2: +11.8% to +49.0% (not worse beyond noise)
- PASS · Evidence: `max_steps=100`: paper states '100'
- PASS · Effect vs noise: candidate minus naive is -85.25 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `cartpole_physics`, `discretization_bounds`, `done_thresholds`, `reset_distribution`, `force_magnitude`, `RL_SEED_BASE`, `RUN_TAG`, `timestep_dt`, `discretization_formula`, `pole_length`, `mass_cart`, `mass_pole`, `action_tiebreak`, `epsilon_decay_timing`, `q_lazy_init`, `evaluation_policy`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (21.54 noise units, gap +10.8%); `max_steps=40` (9.4 noise units, gap -57.9%); `lr_schedule=linear` (4.95 noise units, gap +75.1%); `max_steps=20` (3.97 noise units, gap -78.9%)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `lr_schedule=inv`: this claim -2.0%, mean |gap| 9.3% (5 runs)
  - `max_steps=100`, `lr_schedule=linear`: this claim +2.8%, mean |gap| 24.7% (5 runs)
  - `lr_schedule=inv`, `max_steps=2000`: this claim +40.2%, mean |gap| 38.0% (5 runs)

### Equally good configurations
The target claim can't tell these 4 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `lr_schedule=inv`
- `lr_schedule=inv, max_steps=100`
- `lr_schedule=linear, max_steps=100`

### History matching (every measured configuration, all claims together)
- 3 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `lr_schedule, max_steps`: lr_schedule=inv, max_steps=100 (max I 0.53); lr_schedule=linear, max_steps=100 (max I 0.82)
  - `max_steps`: max_steps=100 (max I 0.93)

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=100; lr_schedule=inv; lr_schedule=inv, max_steps=100; lr_schedule=linear, max_steps=100

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100`, `lr_schedule=inv` | 5 | -2.0% | -16.6% | 9.3% |
| `max_steps=100`, `lr_schedule=linear` | 5 | +2.8% | +46.5% | 24.7% |
| `max_steps=100` | 6 | +4.5% | +49.0% | 26.7% |
| `lr_schedule=inv`, `max_steps=2000` | 5 | +40.2% | -35.9% | 38.0% |
| `lr_schedule=inv` | 6 | +37.8% | -42.4% | 40.1% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `cartpole_physics`, `discretization_bounds`, `done_thresholds`, `reset_distribution`, `force_magnitude`, `RL_SEED_BASE`, `RUN_TAG`, `timestep_dt`, `discretization_formula`, `pole_length`, `mass_cart`, `mass_pole`, `action_tiebreak`, `epsilon_decay_timing`, `q_lazy_init`, `evaluation_policy`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
