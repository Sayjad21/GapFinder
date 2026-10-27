# Gap Report: test-v12-07

Artifact `rlbench` · generated 2026-10-15 19:06 · 199 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +94.7% | -18.0% | ±1.9% | `lr=1` |

## C1: mean_reward (paper 98.685)
**Fits but unsupported** · gap +94.7% → -18.0% · 54 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0011`, `B0030`, `B0031`, `B0048`, `B0049`, `B0050` (6 run(s) of the same config)
- Config: `lr` naive `0.1`, changed to `1`
- Command:

  Replay: fork checkpoint `310411d7-e5ef-4d01-80fc-8ebd7a53f4f7` and run
  ```
  RUN_TAG=ffe76e981de4 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 90.73, 117.8, 64.87, 71.08, 66.84, 96.1; gap after -18.0%; result checkpoint `09ebc3eb-b489-42b2-9b1e-9c16119c377f`
- Effect: candidate 80.91 minus naive 192.1 = -111.2, 95% bootstrap interval [-127.9, -69.31] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 98.7 steps, and that its worst seed still balances for 95.4.

- p. 1; value used: `mean_reward` = 98.685 steps (headline claim)

### What did we measure?
- Naive median 192.1 over 5 runs; repeats: 192, 196.9, 192.4, 192.1, 157.9
- Spread: range 157.9 to 196.9, noise band ±1.921 (2 x MAD), CV 8.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +94.7% (noise band ±1.9% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr` the gap is +94.7% (it comes back)
- PASS · Held-out claim: C2: +62.5% to -87.1% (not worse beyond noise)
- FAIL · Evidence: `lr=1`: no evidence mentions '1'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -111.2 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole physics constants (g, mc, mp, l, f, dt)`, `Discretization bounds (theta: -0.21 to 0.21, omega: -2.0 to 2.0)`, `CartPole masscart (mc) and masspole (mp) values`, `Reset state range (uniform -0.05 to 0.05 for 4 state vars)`, `Done thresholds (abs(x) > 2.4, abs(th) > 12*pi/180)`, `max_steps`, `RL_SEED_BASE`, `RUN_TAG`, `Python version / random module behavior`, `Reward per step (hardcoded 1.0)`, `Number of actions (hardcoded 2)`, `Epsilon decay timing (after each episode)`, `Evaluation policy (greedy, no epsilon)`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr=0.02` (41.06 noise units, gap -14.7%); `lr=0.001` (38.53 noise units, gap -19.7%); `lr=0.05` (35.49 noise units, gap +25.6%); `lr_schedule=inv` (31.17 noise units, gap +34.0%); `lr=0.002` (30.41 noise units, gap -35.5%) (and 8 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `init_q=-1.0`: this claim +57.7%, mean |gap| 29.6% (2 runs)
  - `lr_schedule=inv`: this claim +38.5%, mean |gap| 34.7% (6 runs)
  - `init_q=-1.0`, `lr_schedule=inv`: this claim +54.6%, mean |gap| 34.8% (2 runs)

### History matching (every measured configuration, all claims together)
- 27 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr, lr_schedule`: lr=0.05, lr_schedule=linear (max I 1.8); lr=0.02, lr_schedule=linear (max I 1.98); lr=0.05, lr_schedule=inv (max I 2); lr=5, lr_schedule=inv (max I 2)
  - `init_q, lr`: init_q=1.0, lr=1 (max I 1.83); init_q=-1.0, lr=1 (max I 1.85); init_q=1.0, lr=0.5 (max I 1.9); init_q=-1.0, lr=0.05 (max I 1.96); +2 more

Notes:
- skipped init_q='random small': knob value 'random small' has shell metacharacters
- stopped early: run budget of 200 reached (wanted 3 more run(s) of {'lr': '0.02', 'lr_schedule': 'inv'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=linear`, `init_q=-1.0` | 2 | +57.7% | +1.5% | 29.6% |
| `lr_schedule=inv` | 6 | +38.5% | -30.9% | 34.7% |
| `init_q=-1.0`, `lr_schedule=inv` | 2 | +54.6% | -14.9% | 34.8% |
| `lr=0.2` | 3 | +59.6% | -13.5% | 36.5% |
| `init_q=1.0`, `lr=0.2` | 2 | +82.8% | -0.8% | 41.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole physics constants (g, mc, mp, l, f, dt)`, `Discretization bounds (theta: -0.21 to 0.21, omega: -2.0 to 2.0)`, `CartPole masscart (mc) and masspole (mp) values`, `Reset state range (uniform -0.05 to 0.05 for 4 state vars)`, `Done thresholds (abs(x) > 2.4, abs(th) > 12*pi/180)`, `max_steps`, `RL_SEED_BASE`, `RUN_TAG`, `Python version / random module behavior`, `Reward per step (hardcoded 1.0)`, `Number of actions (hardcoded 2)`, `Epsilon decay timing (after each episode)`, `Evaluation policy (greedy, no epsilon)`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `f01046dd2f29515a730f43fce26caac555dcb0d94d0216bdeffa04fc793fd571`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
