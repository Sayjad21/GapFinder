# Gap Report: test-gen-05

Artifact `rlbench` · generated 2026-10-14 00:29 · 43 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +974.9% | +91.6% | ±36.1% | `eps_start=0.1` |

## C1: mean_reward (paper 17.31)
**Fits but unsupported** · gap +974.9% → +91.6% · 12 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0009`, `B0023`, `B0024`, `B0025` (4 run(s) of the same config)
- Config: `eps_start` naive `1.0`, changed to `0.1`
- Command:

  Replay: fork checkpoint `e26d01cb-995d-417a-97ce-e24ca128afad` and run
  ```
  RUN_TAG=e7e74c71a05a "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 0.1 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 47.33, 23.42, 42.92, 13.04; gap after +91.6%; result checkpoint `f4565fc8-ebbd-451b-aa5b-ad8cf82d8083`
- Effect: candidate 33.17 minus naive 186.1 = -152.9, 95% bootstrap interval [-174.9, -140.1] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 17.3 steps, and that its worst seed still balances for 9.1.

- p. 1; value used: `mean_reward` = 17.31 steps (headline claim)

### What did we measure?
- Naive median 186.1 over 5 runs; repeats: 179.4, 186.1, 182.9, 186.1, 193.9
- Spread: range 179.4 to 193.9, noise band ±6.25 (2 x MAD), CV 2.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +974.9% (noise band ±36.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `eps_start` the gap is +974.9% (it comes back)
- PASS · Held-out claim: C2: +772.5% to +1.9% (not worse beyond noise)
- FAIL · Evidence: `eps_start=0.1`: no evidence mentions '0.1'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -152.9 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole dynamics constants (g, mc, mp, l, f, dt)`, `discretization bounds (theta clip, omega clip)`, `CartPole step physics implementation (force, cos/sin, equations)`, `reset state range`, `done thresholds (x threshold, theta threshold)`, `force magnitude (self.f)`, `RUN_TAG`, `CartPole mass/cart parameters (mc, mp, l)`, `RL_SEED_BASE`, `time step (dt)`, `gravity (g)`, `seed generation logic (base + i)`, `Q-table default for unseen states during eval (q.get(s, [0.0, 0.0]))`, `reward scaling (scale = 1.0 / max_steps if reward_norm == "on")`, `action selection tie-breaking (qs[0] >= qs[1] -> action 0)`, `evaluation policy (greedy vs epsilon-greedy)`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.02` (25.8 noise units, gap -43.5%); `eps_start=0.5` (9.46 noise units, gap +633.3%); `lr_schedule=inv` (7.24 noise units, gap +713.5%); `lr_schedule=linear` (2.42 noise units, gap +887.7%); `eps_start=50` (2.25 noise units, gap +893.8%)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`, `eps_start=0.1`: this claim -2.4%, mean |gap| 1.7% (3 runs)
  - `lr_schedule=linear`, `eps_start=0.02`: this claim +16.2%, mean |gap| 8.4% (3 runs)
  - `eps_start=0.02`: this claim -28.5%, mean |gap| 14.5% (4 runs)

Notes:
- equally good values within one noise band (measured): eps_start in {0.02, 0.1}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv`, `eps_start=0.1` | 3 | -2.4% | +1.1% | 1.7% |
| `lr_schedule=linear`, `eps_start=0.02` | 3 | +16.2% | +0.5% | 8.4% |
| `eps_start=0.02` | 4 | -28.5% | +0.5% | 14.5% |
| `lr_schedule=linear`, `eps_start=0.1` | 3 | +34.4% | -0.5% | 17.5% |
| `lr_schedule=inv`, `eps_start=0.02` | 3 | -41.7% | -0.5% | 21.1% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole dynamics constants (g, mc, mp, l, f, dt)`, `discretization bounds (theta clip, omega clip)`, `CartPole step physics implementation (force, cos/sin, equations)`, `reset state range`, `done thresholds (x threshold, theta threshold)`, `force magnitude (self.f)`, `RUN_TAG`, `CartPole mass/cart parameters (mc, mp, l)`, `RL_SEED_BASE`, `time step (dt)`, `gravity (g)`, `seed generation logic (base + i)`, `Q-table default for unseen states during eval (q.get(s, [0.0, 0.0]))`, `reward scaling (scale = 1.0 / max_steps if reward_norm == "on")`, `action selection tie-breaking (qs[0] >= qs[1] -> action 0)`, `evaluation policy (greedy vs epsilon-greedy)`

## Provenance
- GapFinder commit: `037cdf1603d6771de8f0101af7838abc1a610293` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `fedcbdf1b57461a1273eeb81ccb09c30931e58de34a306249ffd0422bbf51ae6`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
