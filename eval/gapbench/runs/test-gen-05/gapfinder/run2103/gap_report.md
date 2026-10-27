# Gap Report: test-gen-05

Artifact `rlbench` · generated 2026-10-15 20:55 · 87 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +946.3% | +47.7% | ±46.4% | `eps_start=0.0` |

## C1: mean_reward (paper 17.31)
**Fits but unsupported** · gap +946.3% → +47.7% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0011`, `B0028`, `B0029`, `B0036` (4 run(s) of the same config)
- Config: `eps_start` naive `1.0`, changed to `0.0`
- Command:

  Replay: fork checkpoint `6d14b841-e70c-4887-b3ab-733f4c7c96a7` and run
  ```
  RUN_TAG=f187d5aca30c "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 0.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 31.48, 19.66, 9.94, 36.56; gap after +47.7%; result checkpoint `4047d9c1-7b6d-4c04-86a8-229f2fb6601f`
- Effect: candidate 25.57 minus naive 181.1 = -155.6, 95% bootstrap interval [-176.9, -143] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 17.3 steps, and that its worst seed still balances for 9.1.

- p. 1; value used: `mean_reward` = 17.31 steps (headline claim)

### What did we measure?
- Naive median 181.1 over 5 runs; repeats: 191.4, 175.4, 180.4, 185.1, 181.1
- Spread: range 175.4 to 191.4, noise band ±8.03 (2 x MAD), CV 3.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +946.3% (noise band ±46.4% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `eps_start` the gap is +946.3% (it comes back)
- PASS · Held-out claim: C2: +464.3% to +1.4% (not worse beyond noise)
- FAIL · Evidence: `eps_start=0.0`: no evidence mentions '0.0'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -155.6 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole dynamics constants (g, mc, mp, l, f, dt)`, `discretization bounds (theta clip, omega clip)`, `CartPole step physics implementation (force, cos/sin, equations)`, `reset state range`, `done thresholds (x threshold, theta threshold)`, `force magnitude (self.f)`, `RUN_TAG`, `CartPole mass/cart parameters (mc, mp, l)`, `RL_SEED_BASE`, `time step (dt)`, `gravity (g)`, `seed generation logic (base + i)`, `Q-table default for unseen states during eval (q.get(s, [0.0, 0.0]))`, `reward scaling (scale = 1.0 / max_steps if reward_norm == "on")`, `action selection tie-breaking (qs[0] >= qs[1] -> action 0)`, `evaluation policy (greedy vs epsilon-greedy)`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.1` (19.87 noise units, gap +24.6%); `eps_start=0.02` (19.47 noise units, gap +43.1%); `eps_start=0.01` (19 noise units, gap +65.0%); `eps_start=0.2` (17.45 noise units, gap +136.6%); `eps_start=0.5` (6.9 noise units, gap +626.1%) (and 3 more in the JSON)
- Near alternatives (closest across all claims):
  - `eps_start=0.02`, `lr_schedule=inv`: this claim -1.2%, mean |gap| 0.9% (3 runs)
  - `eps_start=0.01`, `lr_schedule=linear`: this claim -8.9%, mean |gap| 4.7% (3 runs)
  - `eps_start=0.1`, `lr_schedule=linear`: this claim +8.8%, mean |gap| 5.2% (3 runs)

### Equally good configurations
The target claim can't tell these 11 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `eps_start=0.0` (reported)
- `eps_start=0.01`
- `eps_start=0.02`
- `eps_start=0.1`
- `eps_start=0.01, lr_schedule=linear`
- `eps_start=0.1, lr_schedule=linear`
- `eps_start=0.0, lr_schedule=inv`
- `eps_start=0.02, lr_schedule=inv`
- `eps_start=0.02, lr_schedule=linear`
- `eps_start=0.1, lr_schedule=inv`
- `eps_start=0.2, lr_schedule=inv`

### History matching (every measured configuration, all claims together)
- 10 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `eps_start, lr_schedule`: eps_start=0.1, lr_schedule=linear (max I 0.13); eps_start=0.02, lr_schedule=inv (max I 0.21); eps_start=0.01, lr_schedule=linear (max I 0.41); eps_start=0.0, lr_schedule=inv (max I 0.83); +4 more
  - `eps_start`: eps_start=0.0 (max I 1.69); eps_start=0.01 (max I 2.73)
- Equally good values: `eps_start` in {0.0, 0.01, 0.1}

Notes:
- configurations the target claim can't tell apart from the answer: eps_start=0.0; eps_start=0.01; eps_start=0.02; eps_start=0.1; eps_start=0.01, lr_schedule=linear; eps_start=0.1, lr_schedule=linear; eps_start=0.0, lr_schedule=inv; eps_start=0.02, lr_schedule=inv; eps_start=0.02, lr_schedule=linear; eps_start=0.1, lr_schedule=inv; eps_start=0.2, lr_schedule=inv
- equally good values within one noise band (measured): eps_start in {0.0, 0.01, 0.1}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `eps_start=0.02`, `lr_schedule=inv` | 3 | -1.2% | +0.5% | 0.9% |
| `eps_start=0.01`, `lr_schedule=linear` | 3 | -8.9% | -0.5% | 4.7% |
| `eps_start=0.1`, `lr_schedule=linear` | 3 | +8.8% | -1.6% | 5.2% |
| `eps_start=0.02`, `lr_schedule=linear` | 3 | -42.4% | -0.5% | 21.5% |
| `lr_schedule=linear`, `eps_start=0.0` | 3 | -43.9% | +0.0% | 21.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole dynamics constants (g, mc, mp, l, f, dt)`, `discretization bounds (theta clip, omega clip)`, `CartPole step physics implementation (force, cos/sin, equations)`, `reset state range`, `done thresholds (x threshold, theta threshold)`, `force magnitude (self.f)`, `RUN_TAG`, `CartPole mass/cart parameters (mc, mp, l)`, `RL_SEED_BASE`, `time step (dt)`, `gravity (g)`, `seed generation logic (base + i)`, `Q-table default for unseen states during eval (q.get(s, [0.0, 0.0]))`, `reward scaling (scale = 1.0 / max_steps if reward_norm == "on")`, `action selection tie-breaking (qs[0] >= qs[1] -> action 0)`, `evaluation policy (greedy vs epsilon-greedy)`

## Provenance
- GapFinder commit: `cd8c8af2b9d079dd9a57443ed501c0dd8a467d34` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
