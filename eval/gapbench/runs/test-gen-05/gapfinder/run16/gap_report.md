# Gap Report: test-gen-05

Artifact `rlbench` · generated 2026-10-14 00:52 · 90 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +948.9% | +44.6% | ±133.9% | `eps_start=0.0` |

## C1: mean_reward (paper 17.31)
**Fits but unsupported** · gap +948.9% → +44.6% · 20 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0011`, `B0029`, `B0030`, `B0031`, `B0032`, `B0033` (6 run(s) of the same config)
- Config: `eps_start` naive `1.0`, changed to `0.0`
- Command:

  Replay: fork checkpoint `5885fad4-fed4-4427-a33d-71c2a53a62d9` and run
  ```
  RUN_TAG=2e1701676bbf "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 0.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 22.94, 14.77, 41.88, 31.05, 23.57, 26.49; gap after +44.6%; result checkpoint `d5324f76-6c26-48be-acc2-af4e9c749ad0`
- Effect: candidate 25.03 minus naive 181.6 = -156.5, 95% bootstrap interval [-165.8, -132.7] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 17.3 steps, and that its worst seed still balances for 9.1.

- p. 1; value used: `mean_reward` = 17.31 steps (headline claim)

### What did we measure?
- Naive median 181.6 over 5 runs; repeats: 181.6, 193.2, 182.3, 158.6, 168.6
- Spread: range 158.6 to 193.2, noise band ±23.17 (2 x MAD), CV 7.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +948.9% (noise band ±133.9% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `eps_start` the gap is +948.9% (it comes back)
- PASS · Held-out claim: C2: +861.0% to +1.1% (not worse beyond noise)
- FAIL · Evidence: `eps_start=0.0`: no evidence mentions '0.0'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -156.5 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole dynamics constants (g, mc, mp, l, f, dt)`, `discretization bounds (theta clip, omega clip)`, `CartPole step physics implementation (force, cos/sin, equations)`, `reset state range`, `done thresholds (x threshold, theta threshold)`, `force magnitude (self.f)`, `RUN_TAG`, `CartPole mass/cart parameters (mc, mp, l)`, `RL_SEED_BASE`, `time step (dt)`, `gravity (g)`, `seed generation logic (base + i)`, `Q-table default for unseen states during eval (q.get(s, [0.0, 0.0]))`, `reward scaling (scale = 1.0 / max_steps if reward_norm == "on")`, `action selection tie-breaking (qs[0] >= qs[1] -> action 0)`, `evaluation policy (greedy vs epsilon-greedy)`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.1` (6.96 noise units, gap +17.3%); `eps_start=0.02` (6.66 noise units, gap +57.8%); `eps_start=0.5` (2.28 noise units, gap +643.4%); `lr_schedule=inv` (1.21 noise units, gap +786.9%)
- Near alternatives (closest across all claims):
  - `eps_start=0.02`: this claim +13.3%, mean |gap| 6.8% (6 runs)
  - `lr_schedule=inv`, `eps_start=0.1`: this claim +21.4%, mean |gap| 11.0% (5 runs)
  - `lr_schedule=inv`, `eps_start=0.0`: this claim -30.9%, mean |gap| 15.4% (5 runs)

### History matching (every measured configuration, all claims together)
- 8 of 20 tested configurations fit every claim within 3 sigma
- Equally good values: `eps_start` in {0.0, 0.02}

Notes:
- equally good values within one noise band (measured): eps_start in {0.0, 0.02}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `eps_start=0.02` | 6 | +13.3% | +0.3% | 6.8% |
| `lr_schedule=inv`, `eps_start=0.1` | 5 | +21.4% | +0.5% | 11.0% |
| `lr_schedule=inv`, `eps_start=0.0` | 5 | -30.9% | +0.0% | 15.4% |
| `eps_start=0.02`, `lr_schedule=inv` | 5 | -43.6% | +0.0% | 21.8% |
| `lr_schedule=linear`, `eps_start=0.02` | 5 | -44.3% | +0.0% | 22.1% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole dynamics constants (g, mc, mp, l, f, dt)`, `discretization bounds (theta clip, omega clip)`, `CartPole step physics implementation (force, cos/sin, equations)`, `reset state range`, `done thresholds (x threshold, theta threshold)`, `force magnitude (self.f)`, `RUN_TAG`, `CartPole mass/cart parameters (mc, mp, l)`, `RL_SEED_BASE`, `time step (dt)`, `gravity (g)`, `seed generation logic (base + i)`, `Q-table default for unseen states during eval (q.get(s, [0.0, 0.0]))`, `reward scaling (scale = 1.0 / max_steps if reward_norm == "on")`, `action selection tie-breaking (qs[0] >= qs[1] -> action 0)`, `evaluation policy (greedy vs epsilon-greedy)`

## Provenance
- GapFinder commit: `e89cebde86417c8c65704c51b94620ddb20a97ce` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `fedcbdf1b57461a1273eeb81ccb09c30931e58de34a306249ffd0422bbf51ae6`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
