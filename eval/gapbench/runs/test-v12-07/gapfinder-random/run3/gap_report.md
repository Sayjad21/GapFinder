# Gap Report: test-v12-07

Artifact `rlbench` · generated 2026-10-15 09:04 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +78.9% | -0.4% | ±8.7% | `lr=0.02` |

## C1: mean_reward (paper 98.685)
**Fits but unsupported** · gap +78.9% → -0.4% · 54 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0019`, `B0034`, `B0035`, `B0042`, `B0043`, `B0044` (6 run(s) of the same config)
- Config: `lr` naive `0.1`, changed to `0.02`
- Command:

  Replay: fork checkpoint `ace3b114-b224-4628-8fb4-4f844349038d` and run
  ```
  RUN_TAG=a9aef6f7ec30 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.02 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 103.7, 55.77, 109.2, 117.4, 89.36, 92.89; gap after -0.4%; result checkpoint `1a0f9efe-224c-42ec-b5bc-c31f412c71fd`
- Effect: candidate 98.28 minus naive 176.6 = -78.3, 95% bootstrap interval [-121.4, -64.99] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 98.7 steps, and that its worst seed still balances for 95.4.

- p. 1; value used: `mean_reward` = 98.685 steps (headline claim)

### What did we measure?
- Naive median 176.6 over 5 runs; repeats: 192, 176.6, 175.2, 200, 172.3
- Spread: range 172.3 to 200, noise band ±8.56 (2 x MAD), CV 6.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +78.9% (noise band ±8.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr` the gap is +78.9% (it comes back)
- PASS · Held-out claim: C2: -3.7% to -86.9% (not worse beyond noise)
- FAIL · Evidence: `lr=0.02`: no evidence mentions '0.02'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -78.3 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole physics constants (g, mc, mp, l, f, dt)`, `Discretization bounds (theta: -0.21 to 0.21, omega: -2.0 to 2.0)`, `CartPole masscart (mc) and masspole (mp) values`, `Reset state range (uniform -0.05 to 0.05 for 4 state vars)`, `Done thresholds (abs(x) > 2.4, abs(th) > 12*pi/180)`, `max_steps`, `RL_SEED_BASE`, `RUN_TAG`, `Python version / random module behavior`, `Reward per step (hardcoded 1.0)`, `Number of actions (hardcoded 2)`, `Epsilon decay timing (after each episode)`, `Evaluation policy (greedy, no epsilon)`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (8.82 noise units, gap -2.4%); `lr=0.5` (8.01 noise units, gap +9.4%); `lr=0.05` (7.21 noise units, gap +16.4%); `lr=0.01` (6.72 noise units, gap -20.6%); `lr=0.002` (6.53 noise units, gap -22.3%) (and 2 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`, `init_q=1.0`: this claim +55.3%, mean |gap| 42.3% (5 runs)
  - `lr_schedule=linear`, `lr=0.05`: this claim +26.4%, mean |gap| 45.2% (5 runs)
  - `lr_schedule=inv`, `lr=0.05`: this claim +4.3%, mean |gap| 45.9% (5 runs)

### History matching (every measured configuration, all claims together)
- 18 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr, lr_schedule`: lr=0.05, lr_schedule=inv (max I 1.67); lr=0.02, lr_schedule=linear (max I 2.16); lr=5, lr_schedule=inv (max I 2.16)
  - `init_q, lr`: init_q=1.0, lr=1 (max I 1.71); init_q=-1.0, lr=0.02 (max I 1.72); init_q=-1.0, lr=0.5 (max I 1.73); init_q=-1.0, lr=1 (max I 1.73); +1 more
  - `lr`: lr=1 (max I 1.8); lr=0.02 (max I 1.85)

Notes:
- skipped init_q='random small': knob value 'random small' has shell metacharacters
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'lr': '0.001', 'init_q': '1.0'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| naive (reproduction as run) | 5 | +78.9% | -3.7% | 41.3% |
| `lr_schedule=inv`, `init_q=1.0` | 5 | +55.3% | -29.2% | 42.3% |
| `lr=0.02` | 6 | -0.4% | -86.9% | 43.6% |
| `lr_schedule=linear`, `lr=0.05` | 5 | +26.4% | -64.0% | 45.2% |
| `lr_schedule=inv`, `lr=0.05` | 5 | +4.3% | -87.5% | 45.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole physics constants (g, mc, mp, l, f, dt)`, `Discretization bounds (theta: -0.21 to 0.21, omega: -2.0 to 2.0)`, `CartPole masscart (mc) and masspole (mp) values`, `Reset state range (uniform -0.05 to 0.05 for 4 state vars)`, `Done thresholds (abs(x) > 2.4, abs(th) > 12*pi/180)`, `max_steps`, `RL_SEED_BASE`, `RUN_TAG`, `Python version / random module behavior`, `Reward per step (hardcoded 1.0)`, `Number of actions (hardcoded 2)`, `Epsilon decay timing (after each episode)`, `Evaluation policy (greedy, no epsilon)`

## Provenance
- GapFinder commit: `f01fe3d9a0095f98d6304ad0543b917ca8e529eb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `f01046dd2f29515a730f43fce26caac555dcb0d94d0216bdeffa04fc793fd571`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
