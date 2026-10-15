# Gap Report: test-v12-07

Artifact `rlbench` · generated 2026-10-15 09:04 · 199 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +84.7% | +1.6% | ±15.9% | `lr=1` |

## C1: mean_reward (paper 98.685)
**Fits but unsupported** · gap +84.7% → +1.6% · 54 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0011`, `B0026`, `B0027`, `B0039`, `B0040`, `B0041` (6 run(s) of the same config)
- Config: `lr` naive `0.1`, changed to `1`
- Command:

  Replay: fork checkpoint `b8148e4a-9262-4f37-b895-1369c4948efe` and run
  ```
  RUN_TAG=98a62552861a "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 115.2, 120.7, 90.02, 69.24, 90.08, 110.4; gap after +1.6%; result checkpoint `f28cca20-627d-4817-a810-ef8e31249b17`
- Effect: candidate 100.2 minus naive 182.2 = -82.01, 95% bootstrap interval [-106.3, -54.67] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 98.7 steps, and that its worst seed still balances for 95.4.

- p. 1; value used: `mean_reward` = 98.685 steps (headline claim)

### What did we measure?
- Naive median 182.2 over 5 runs; repeats: 151.1, 172.1, 189, 182.2, 190.1
- Spread: range 151.1 to 190.1, noise band ±15.66 (2 x MAD), CV 9.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +84.7% (noise band ±15.9% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr` the gap is +84.7% (it comes back)
- PASS · Held-out claim: C2: +9.1% to -85.4% (not worse beyond noise)
- FAIL · Evidence: `lr=1`: evidence gate off: no evidence was looked for
- PASS · Effect vs noise: candidate minus naive is -82.01 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole physics constants (g, mc, mp, l, f, dt)`, `Discretization bounds (theta: -0.21 to 0.21, omega: -2.0 to 2.0)`, `CartPole masscart (mc) and masspole (mp) values`, `Reset state range (uniform -0.05 to 0.05 for 4 state vars)`, `Done thresholds (abs(x) > 2.4, abs(th) > 12*pi/180)`, `max_steps`, `RL_SEED_BASE`, `RUN_TAG`, `Python version / random module behavior`, `Reward per step (hardcoded 1.0)`, `Number of actions (hardcoded 2)`, `Epsilon decay timing (after each episode)`, `Evaluation policy (greedy, no epsilon)`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (4.84 noise units, gap +7.8%); `lr=0.05` (4.42 noise units, gap +14.5%); `lr=0.5` (3.59 noise units, gap -27.7%); `lr=0.01` (3.56 noise units, gap -28.2%); `lr=0.002` (2.92 noise units, gap -38.4%) (and 2 more in the JSON)
- Near alternatives (closest across all claims):
  - `init_q=1.0`, `lr=0.05`: this claim +16.0%, mean |gap| 39.1% (5 runs)
  - `lr_schedule=inv`: this claim +37.4%, mean |gap| 39.5% (6 runs)
  - `lr_schedule=linear`, `lr=0.05`: this claim +3.2%, mean |gap| 42.6% (5 runs)

### History matching (every measured configuration, all claims together)
- 28 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr, lr_schedule`: lr=0.05, lr_schedule=linear (max I 2); lr=0.02, lr_schedule=linear (max I 2.14); lr=0.05, lr_schedule=inv (max I 2.19)
  - `init_q, lr`: init_q=-1.0, lr=0.05 (max I 2.12); init_q=-1.0, lr=0.5 (max I 2.2); init_q=-1.0, lr=0.02 (max I 2.2); init_q=-1.0, lr=1 (max I 2.28)
  - `lr`: lr=0.01 (max I 2.17); lr=0.05 (max I 2.21); lr=0.5 (max I 2.24)
- 2 separate islands (no single-knob move joins them): lr=0.05, lr_schedule=linear; init_q=-1.0, lr=0.05; lr=0.02, lr_schedule=linear | init_q=1.0, lr_schedule=linear

Notes:
- skipped init_q='random small': knob value 'random small' has shell metacharacters
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'lr': '0.2', 'init_q': '-1.0'} for 'confirm-combo')
- evidence gate off: no evidence was checked, so this cannot be labelled Explained
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `init_q=1.0`, `lr=0.05` | 5 | +16.0% | -62.2% | 39.1% |
| `lr_schedule=inv` | 6 | +37.4% | -41.6% | 39.5% |
| `lr_schedule=linear`, `lr=0.05` | 5 | +3.2% | -82.0% | 42.6% |
| `lr=1` | 6 | +1.6% | -85.4% | 43.5% |
| `init_q=-1.0`, `lr=0.05` | 5 | +5.8% | -82.0% | 43.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole physics constants (g, mc, mp, l, f, dt)`, `Discretization bounds (theta: -0.21 to 0.21, omega: -2.0 to 2.0)`, `CartPole masscart (mc) and masspole (mp) values`, `Reset state range (uniform -0.05 to 0.05 for 4 state vars)`, `Done thresholds (abs(x) > 2.4, abs(th) > 12*pi/180)`, `max_steps`, `RL_SEED_BASE`, `RUN_TAG`, `Python version / random module behavior`, `Reward per step (hardcoded 1.0)`, `Number of actions (hardcoded 2)`, `Epsilon decay timing (after each episode)`, `Evaluation policy (greedy, no epsilon)`

## Provenance
- GapFinder commit: `f01fe3d9a0095f98d6304ad0543b917ca8e529eb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `f01046dd2f29515a730f43fce26caac555dcb0d94d0216bdeffa04fc793fd571`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
