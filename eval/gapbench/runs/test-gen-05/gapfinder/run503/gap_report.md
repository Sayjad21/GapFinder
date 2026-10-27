# Gap Report: test-gen-05

Artifact `rlbench` · generated 2026-10-14 22:15 · 168 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +966.6% | -8.3% | ±49.2% | `eps_start=0.0` |

## C1: mean_reward (paper 17.31)
**Fits but unsupported** · gap +966.6% → -8.3% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0011`, `B0043`, `B0044`, `B0045`, `B0046`, `B0047` (6 run(s) of the same config)
- Config: `eps_start` naive `1.0`, changed to `0.0`
- Command:

  Replay: fork checkpoint `d984a231-d907-4ee5-a102-f52a5e2d249e` and run
  ```
  RUN_TAG=fdd62c56526b "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 0.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 22.07, 10.66, 10.62, 32.12, 12.81, 18.95; gap after -8.3%; result checkpoint `e32278f4-8b96-4516-860c-dff3a616e618`
- Effect: candidate 15.88 minus naive 184.6 = -168.8, 95% bootstrap interval [-180.2, -151.1] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 17.3 steps, and that its worst seed still balances for 9.1.

- p. 1; value used: `mean_reward` = 17.31 steps (headline claim)

### What did we measure?
- Naive median 184.6 over 5 runs; repeats: 188.7, 196.4, 184.6, 180.4, 168.7
- Spread: range 168.7 to 196.4, noise band ±8.51 (2 x MAD), CV 5.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +966.6% (noise band ±49.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `eps_start` the gap is +966.6% (it comes back)
- PASS · Held-out claim: C2: +1379.1% to +0.5% (not worse beyond noise)
- FAIL · Evidence: `eps_start=0.0`: no evidence mentions '0.0'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -168.8 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole dynamics constants (g, mc, mp, l, f, dt)`, `discretization bounds (theta clip, omega clip)`, `CartPole step physics implementation (force, cos/sin, equations)`, `reset state range`, `done thresholds (x threshold, theta threshold)`, `force magnitude (self.f)`, `RUN_TAG`, `CartPole mass/cart parameters (mc, mp, l)`, `RL_SEED_BASE`, `time step (dt)`, `gravity (g)`, `seed generation logic (base + i)`, `Q-table default for unseen states during eval (q.get(s, [0.0, 0.0]))`, `reward scaling (scale = 1.0 / max_steps if reward_norm == "on")`, `action selection tie-breaking (qs[0] >= qs[1] -> action 0)`, `evaluation policy (greedy vs epsilon-greedy)`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.02` (18.85 noise units, gap -40.0%); `eps_start=0.01` (18.53 noise units, gap +55.4%); `eps_start=0.1` (16.24 noise units, gap +168.0%); `eps_start=0.2` (15.99 noise units, gap +180.3%); `eps_start=0.5` (11.4 noise units, gap +405.9%) (and 5 more in the JSON)
- Near alternatives (closest across all claims):
  - `eps_start=0.1`, `lr_schedule=linear`: this claim -12.6%, mean |gap| 6.8% (5 runs)
  - `lr_schedule=linear`, `eps_start=0.02`: this claim -14.2%, mean |gap| 7.4% (5 runs)
  - `lr_schedule=inv`, `eps_start=0.1`: this claim -28.2%, mean |gap| 14.4% (5 runs)

### Equally good configurations
The target claim can't tell these 13 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `eps_start=0.0` (reported)
- `eps_start=0.01`
- `eps_start=0.02`
- `eps_start=0.1`
- `eps_start=0.02, lr_schedule=linear`
- `eps_start=0.1, lr_schedule=inv`
- `eps_start=0.1, lr_schedule=linear`
- `eps_start=0.0, lr_schedule=inv`
- `eps_start=0.01, lr_schedule=inv`
- `eps_start=0.01, lr_schedule=linear`
- `eps_start=0.0, lr_schedule=linear`
- `eps_start=0.02, lr_schedule=inv`
- `eps_start=0.2, lr_schedule=inv`

### History matching (every measured configuration, all claims together)
- 13 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `eps_start, lr_schedule`: eps_start=0.01, lr_schedule=linear (max I 0.05); eps_start=0.02, lr_schedule=linear (max I 0.14); eps_start=0.1, lr_schedule=linear (max I 0.44); eps_start=0.1, lr_schedule=inv (max I 0.48); +5 more
  - `eps_start`: eps_start=0.0 (max I 0.09)

Notes:
- configurations the target claim can't tell apart from the answer: eps_start=0.0; eps_start=0.01; eps_start=0.02; eps_start=0.1; eps_start=0.02, lr_schedule=linear; eps_start=0.1, lr_schedule=inv; eps_start=0.1, lr_schedule=linear; eps_start=0.0, lr_schedule=inv; eps_start=0.01, lr_schedule=inv; eps_start=0.01, lr_schedule=linear; eps_start=0.0, lr_schedule=linear; eps_start=0.02, lr_schedule=inv; eps_start=0.2, lr_schedule=inv

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `eps_start=0.0` | 6 | -8.3% | +0.5% | 4.4% |
| `eps_start=0.1`, `lr_schedule=linear` | 5 | -12.6% | +1.1% | 6.8% |
| `lr_schedule=linear`, `eps_start=0.02` | 5 | -14.2% | +0.5% | 7.4% |
| `lr_schedule=inv`, `eps_start=0.1` | 5 | -28.2% | +0.5% | 14.4% |
| `lr_schedule=inv`, `eps_start=0.02` | 5 | -31.7% | -0.5% | 16.1% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole dynamics constants (g, mc, mp, l, f, dt)`, `discretization bounds (theta clip, omega clip)`, `CartPole step physics implementation (force, cos/sin, equations)`, `reset state range`, `done thresholds (x threshold, theta threshold)`, `force magnitude (self.f)`, `RUN_TAG`, `CartPole mass/cart parameters (mc, mp, l)`, `RL_SEED_BASE`, `time step (dt)`, `gravity (g)`, `seed generation logic (base + i)`, `Q-table default for unseen states during eval (q.get(s, [0.0, 0.0]))`, `reward scaling (scale = 1.0 / max_steps if reward_norm == "on")`, `action selection tie-breaking (qs[0] >= qs[1] -> action 0)`, `evaluation policy (greedy vs epsilon-greedy)`

## Provenance
- GapFinder commit: `e0f13d101585ad1609a15fbf67b70128f4cfffc8` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
