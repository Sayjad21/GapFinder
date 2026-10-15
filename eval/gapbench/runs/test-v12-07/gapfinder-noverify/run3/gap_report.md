# Gap Report: test-v12-07

Artifact `rlbench` · generated 2026-10-15 09:03 · 199 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Explained | +90.3% | -0.8% | ±17.3% | `lr=0.02` |

## C1: mean_reward (paper 98.685)
**Explained** · gap +90.3% → -0.8% · 54 hypotheses tested
> Confirmed cause: reverting it brings the gap back, held-out claims hold, and the value has evidence

### Which experiment changed it?
- Branch: `B0013`, `B0032`, `B0033`, `B0042`, `B0043`, `B0044` (6 run(s) of the same config)
- Config: `lr` naive `0.1`, changed to `0.02`
- Command:

  Replay: fork checkpoint `732dad33-9552-4eef-8f66-c4f1832d6e31` and run
  ```
  RUN_TAG=9d51fb17daf4 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.02 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 116.1, 101.6, 97.54, 72.31, 95.59, 98.33; gap after -0.8%; result checkpoint `933aa5b8-ae55-40c6-a110-1477e9bbcf9b`
- Effect: candidate 97.94 minus naive 187.8 = -89.84, 95% bootstrap interval [-111.8, -62.89] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 98.7 steps, and that its worst seed still balances for 95.4.

- p. 1; value used: `mean_reward` = 98.685 steps (headline claim)

### What did we measure?
- Naive median 187.8 over 5 runs; repeats: 196.3, 190, 173.3, 187.8, 152.5
- Spread: range 152.5 to 196.3, noise band ±17.05 (2 x MAD), CV 9.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +90.3% (noise band ±17.3% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is -89.84 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole physics constants (g, mc, mp, l, f, dt)`, `Discretization bounds (theta: -0.21 to 0.21, omega: -2.0 to 2.0)`, `CartPole masscart (mc) and masspole (mp) values`, `Reset state range (uniform -0.05 to 0.05 for 4 state vars)`, `Done thresholds (abs(x) > 2.4, abs(th) > 12*pi/180)`, `max_steps`, `RL_SEED_BASE`, `RUN_TAG`, `Python version / random module behavior`, `Reward per step (hardcoded 1.0)`, `Number of actions (hardcoded 2)`, `Epsilon decay timing (after each episode)`, `Evaluation policy (greedy, no epsilon)`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr=0.01` (5.2 noise units, gap -0.4%); `lr=1` (4.84 noise units, gap +6.6%); `lr=0.5` (4.75 noise units, gap -8.1%); `lr=0.002` (4.58 noise units, gap -11.1%); `lr=0.05` (4.09 noise units, gap +19.7%) (and 5 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr=1`, `init_q=1.0`: this claim -3.2%, mean |gap| 44.1% (5 runs)
  - `init_q=-1.0`, `lr=0.02`: this claim -2.6%, mean |gap| 44.6% (5 runs)
  - `lr_schedule=linear`, `lr=0.05`: this claim +23.0%, mean |gap| 44.9% (5 runs)

### History matching (every measured configuration, all claims together)
- 28 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr, lr_schedule`: lr=5, lr_schedule=inv (max I 1.26); lr=0.05, lr_schedule=linear (max I 1.86); lr=0.02, lr_schedule=inv (max I 1.93); lr=0.01, lr_schedule=inv (max I 2.01)
  - `lr`: lr=0.05 (max I 1.54); lr=0.001 (max I 1.9); lr=0.5 (max I 2.01)
  - `init_q, lr`: init_q=1.0, lr=0.5 (max I 1.74); init_q=1.0, lr=1 (max I 1.87); init_q=-1.0, lr=0.05 (max I 1.91)

Notes:
- skipped init_q='random small': knob value 'random small' has shell metacharacters
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'lr_schedule': 'linear', 'init_q': '-1.0'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr=0.02` | 6 | -0.8% | -86.4% | 43.6% |
| `lr=1`, `init_q=1.0` | 5 | -3.2% | -85.1% | 44.1% |
| `init_q=-1.0`, `lr=0.02` | 5 | -2.6% | -86.5% | 44.6% |
| `lr_schedule=linear`, `lr=0.05` | 5 | +23.0% | -66.9% | 44.9% |
| `lr=0.05` | 3 | +20.6% | -71.4% | 46.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole physics constants (g, mc, mp, l, f, dt)`, `Discretization bounds (theta: -0.21 to 0.21, omega: -2.0 to 2.0)`, `CartPole masscart (mc) and masspole (mp) values`, `Reset state range (uniform -0.05 to 0.05 for 4 state vars)`, `Done thresholds (abs(x) > 2.4, abs(th) > 12*pi/180)`, `max_steps`, `RL_SEED_BASE`, `RUN_TAG`, `Python version / random module behavior`, `Reward per step (hardcoded 1.0)`, `Number of actions (hardcoded 2)`, `Epsilon decay timing (after each episode)`, `Evaluation policy (greedy, no epsilon)`

## Provenance
- GapFinder commit: `f01fe3d9a0095f98d6304ad0543b917ca8e529eb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `f01046dd2f29515a730f43fce26caac555dcb0d94d0216bdeffa04fc793fd571`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
