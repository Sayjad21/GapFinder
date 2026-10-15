# Gap Report: test-v12-07

Artifact `rlbench` · generated 2026-10-15 09:03 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +81.7% | -11.7% | ±18.3% | `lr=1` |

## C1: mean_reward (paper 98.685)
**Fits but unsupported** · gap +81.7% → -11.7% · 54 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0011`, `B0026`, `B0027`, `B0036`, `B0037`, `B0038` (6 run(s) of the same config)
- Config: `lr` naive `0.1`, changed to `1`
- Command:

  Replay: fork checkpoint `397b3781-801b-43d8-9d2c-13a76ebb12a2` and run
  ```
  RUN_TAG=941ed0490761 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 79.86, 87.49, 97.6, 63.09, 106.4, 86.78; gap after -11.7%; result checkpoint `7a7b48a2-779f-4f27-8645-9bf6982e1752`
- Effect: candidate 87.13 minus naive 179.3 = -92.21, 95% bootstrap interval [-112.5, -72.08] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 98.7 steps, and that its worst seed still balances for 95.4.

- p. 1; value used: `mean_reward` = 98.685 steps (headline claim)

### What did we measure?
- Naive median 179.3 over 5 runs; repeats: 179.3, 173, 190.6, 188.4, 165.8
- Spread: range 165.8 to 190.6, noise band ±18.06 (2 x MAD), CV 5.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +81.7% (noise band ±18.3% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr` the gap is +81.7% (it comes back)
- PASS · Held-out claim: C2: -31.0% to -87.3% (not worse beyond noise)
- FAIL · Evidence: `lr=1`: no evidence mentions '1'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -92.21 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole physics constants (g, mc, mp, l, f, dt)`, `Discretization bounds (theta: -0.21 to 0.21, omega: -2.0 to 2.0)`, `CartPole masscart (mc) and masspole (mp) values`, `Reset state range (uniform -0.05 to 0.05 for 4 state vars)`, `Done thresholds (abs(x) > 2.4, abs(th) > 12*pi/180)`, `max_steps`, `RL_SEED_BASE`, `RUN_TAG`, `Python version / random module behavior`, `Reward per step (hardcoded 1.0)`, `Number of actions (hardcoded 2)`, `Epsilon decay timing (after each episode)`, `Evaluation policy (greedy, no epsilon)`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr=0.002` (4.15 noise units, gap -5.8%); `lr=0.01` (3.88 noise units, gap -10.7%); `lr=0.05` (3.82 noise units, gap +11.9%); `lr=0.02` (2.73 noise units, gap -31.8%); `lr_schedule=inv` (2.62 noise units, gap +33.7%) (and 2 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`: this claim +31.0%, mean |gap| 40.8% (5 runs)
  - `lr=0.05`, `lr_schedule=inv`: this claim -4.0%, mean |gap| 44.5% (5 runs)
  - `init_q=-1.0`, `lr=1`: this claim -2.3%, mean |gap| 44.8% (5 runs)

### History matching (every measured configuration, all claims together)
- 17 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr`: lr=0.05 (max I 2.24)
  - `init_q, lr`: init_q=-1.0, lr=0.05 (max I 2.39); init_q=-1.0, lr=1 (max I 2.52); init_q=-1.0, lr=0.5 (max I 2.55); init_q=1.0, lr=1 (max I 2.68)
  - `lr, lr_schedule`: lr=0.05, lr_schedule=linear (max I 2.47); lr=0.05, lr_schedule=inv (max I 2.54); lr=0.02, lr_schedule=linear (max I 2.65); lr=5, lr_schedule=inv (max I 2.7); +1 more

Notes:
- skipped init_q='random small': knob value 'random small' has shell metacharacters
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'lr_schedule': 'linear', 'init_q': '1.0'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv` | 5 | +31.0% | -50.6% | 40.8% |
| `lr=0.05`, `lr_schedule=inv` | 5 | -4.0% | -85.1% | 44.5% |
| `init_q=-1.0`, `lr=1` | 5 | -2.3% | -87.3% | 44.8% |
| `init_q=-1.0`, `lr_schedule=inv` | 5 | +26.9% | -63.8% | 45.4% |
| `lr=0.05`, `init_q=-1.0` | 5 | +14.8% | -82.4% | 48.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole physics constants (g, mc, mp, l, f, dt)`, `Discretization bounds (theta: -0.21 to 0.21, omega: -2.0 to 2.0)`, `CartPole masscart (mc) and masspole (mp) values`, `Reset state range (uniform -0.05 to 0.05 for 4 state vars)`, `Done thresholds (abs(x) > 2.4, abs(th) > 12*pi/180)`, `max_steps`, `RL_SEED_BASE`, `RUN_TAG`, `Python version / random module behavior`, `Reward per step (hardcoded 1.0)`, `Number of actions (hardcoded 2)`, `Epsilon decay timing (after each episode)`, `Evaluation policy (greedy, no epsilon)`

## Provenance
- GapFinder commit: `f01fe3d9a0095f98d6304ad0543b917ca8e529eb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `f01046dd2f29515a730f43fce26caac555dcb0d94d0216bdeffa04fc793fd571`
- Cost: Nemotron billed $0.0373, sandbox reported $0.0000 (total $0.0373; this search; ledger extraction is included only if it shared the search's router)
