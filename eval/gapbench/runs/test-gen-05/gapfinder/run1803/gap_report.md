# Gap Report: test-gen-05

Artifact `rlbench` · generated 2026-10-15 19:38 · 108 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +949.5% | -13.8% | ±126.1% | `eps_start=0.01` |

## C1: mean_reward (paper 17.31)
**Fits but unsupported** · gap +949.5% → -13.8% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0017`, `B0032`, `B0033`, `B0034`, `B0035`, `B0036` (6 run(s) of the same config)
- Config: `eps_start` naive `1.0`, changed to `0.01`
- Command:

  Replay: fork checkpoint `6c7451bc-d9a7-4218-8db4-f05895cf81ad` and run
  ```
  RUN_TAG=19850574ed98 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 0.01 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 28.86, 10.21, 13.01, 9.835, 18.07, 16.82; gap after -13.8%; result checkpoint `ac189a4e-5221-48ee-b092-23abec0ce71a`
- Effect: candidate 14.92 minus naive 181.7 = -166.8, 95% bootstrap interval [-181, -156.4] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 17.3 steps, and that its worst seed still balances for 9.1.

- p. 1; value used: `mean_reward` = 17.31 steps (headline claim)

### What did we measure?
- Naive median 181.7 over 5 runs; repeats: 193.8, 171.7, 193.7, 181.7, 170.8
- Spread: range 170.8 to 193.8, noise band ±21.83 (2 x MAD), CV 6.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +949.5% (noise band ±126.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `eps_start` the gap is +949.5% (it comes back)
- PASS · Held-out claim: C2: +1067.0% to +0.3% (not worse beyond noise)
- FAIL · Evidence: `eps_start=0.01`: no evidence mentions '0.01'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -166.8 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole dynamics constants (g, mc, mp, l, f, dt)`, `discretization bounds (theta clip, omega clip)`, `CartPole step physics implementation (force, cos/sin, equations)`, `reset state range`, `done thresholds (x threshold, theta threshold)`, `force magnitude (self.f)`, `RUN_TAG`, `CartPole mass/cart parameters (mc, mp, l)`, `RL_SEED_BASE`, `time step (dt)`, `gravity (g)`, `seed generation logic (base + i)`, `Q-table default for unseen states during eval (q.get(s, [0.0, 0.0]))`, `reward scaling (scale = 1.0 / max_steps if reward_norm == "on")`, `action selection tie-breaking (qs[0] >= qs[1] -> action 0)`, `evaluation policy (greedy vs epsilon-greedy)`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.02` (7.35 noise units, gap +22.1%); `eps_start=0.0` (7.2 noise units, gap -41.7%); `eps_start=0.1` (5.54 noise units, gap +251.4%); `eps_start=0.2` (5.43 noise units, gap +264.6%); `lr_schedule=inv` (4 noise units, gap +445.1%) (and 2 more in the JSON)
- Near alternatives (closest across all claims):
  - `eps_start=0.02`, `lr_schedule=linear`: this claim -10.1%, mean |gap| 5.3% (5 runs)
  - `eps_start=0.0`: this claim -23.4%, mean |gap| 12.1% (6 runs)
  - `eps_start=0.01`, `lr_schedule=linear`: this claim -24.5%, mean |gap| 12.5% (5 runs)

### Equally good configurations
The target claim can't tell these 7 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `eps_start=0.01` (reported)
- `eps_start=0.0`
- `eps_start=0.02`
- `eps_start=0.02, lr_schedule=linear`
- `eps_start=0.01, lr_schedule=linear`
- `eps_start=0.1, lr_schedule=inv`
- `eps_start=0.01, lr_schedule=inv`

### History matching (every measured configuration, all claims together)
- 13 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `eps_start`: eps_start=0.01 (max I 0.17); eps_start=0.0 (max I 0.5)
  - `eps_start, lr_schedule`: eps_start=0.02, lr_schedule=linear (max I 0.27); eps_start=0.01, lr_schedule=linear (max I 0.29); eps_start=0.1, lr_schedule=inv (max I 0.41); eps_start=0.01, lr_schedule=inv (max I 0.72); +4 more
- Equally good values: `eps_start` in {0.0, 0.01, 0.02}

Notes:
- configurations the target claim can't tell apart from the answer: eps_start=0.01; eps_start=0.0; eps_start=0.02; eps_start=0.02, lr_schedule=linear; eps_start=0.01, lr_schedule=linear; eps_start=0.1, lr_schedule=inv; eps_start=0.01, lr_schedule=inv
- equally good values within one noise band (measured): eps_start in {0.0, 0.01, 0.02}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `eps_start=0.02`, `lr_schedule=linear` | 5 | -10.1% | -0.5% | 5.3% |
| `eps_start=0.01` | 6 | -13.8% | +0.3% | 7.0% |
| `eps_start=0.0` | 6 | -23.4% | +0.8% | 12.1% |
| `eps_start=0.01`, `lr_schedule=linear` | 5 | -24.5% | +0.5% | 12.5% |
| `eps_start=0.02` | 6 | +27.2% | +1.1% | 14.1% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole dynamics constants (g, mc, mp, l, f, dt)`, `discretization bounds (theta clip, omega clip)`, `CartPole step physics implementation (force, cos/sin, equations)`, `reset state range`, `done thresholds (x threshold, theta threshold)`, `force magnitude (self.f)`, `RUN_TAG`, `CartPole mass/cart parameters (mc, mp, l)`, `RL_SEED_BASE`, `time step (dt)`, `gravity (g)`, `seed generation logic (base + i)`, `Q-table default for unseen states during eval (q.get(s, [0.0, 0.0]))`, `reward scaling (scale = 1.0 / max_steps if reward_norm == "on")`, `action selection tie-breaking (qs[0] >= qs[1] -> action 0)`, `evaluation policy (greedy vs epsilon-greedy)`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
