# Gap Report: test-v12-07

Artifact `rlbench` · generated 2026-10-15 19:54 · 165 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +85.5% | -4.5% | ±19.4% | `lr=0.05`, `lr_schedule=inv` |

## C1: mean_reward (paper 98.685)
**Fits but unsupported** · gap +85.5% → -4.5% · 54 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0064`, `B0098`, `B0147`, `B0148`, `B0149` (5 run(s) of the same config)
- Config: `lr` naive `0.1`, changed to `0.05`
- Config: `lr_schedule` naive `const`, changed to `inv`
- Command:

  Replay: fork checkpoint `5ebce4ae-c9aa-4cfb-b323-3b723bc098a5` and run
  ```
  RUN_TAG=8731d8f384b1 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.05 --lr_schedule inv --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 118, 125.2, 66.94, 94.27, 54.15; gap after -4.5%; result checkpoint `a7db0914-7879-4ea1-8563-8225681c2967`
- Effect: candidate 94.27 minus naive 183.1 = -88.8, 95% bootstrap interval [-122.6, -54.34] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 98.7 steps, and that its worst seed still balances for 95.4.

- p. 1; value used: `mean_reward` = 98.685 steps (headline claim)

### What did we measure?
- Naive median 183.1 over 5 runs; repeats: 162.7, 183.1, 168.3, 189.9, 192.6
- Spread: range 162.7 to 192.6, noise band ±19.13 (2 x MAD), CV 7.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +85.5% (noise band ±19.4% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr` the gap is +37.9% (it comes back)
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is +35.4% (it comes back)
- PASS · Held-out claim: C2: +3.5% to -86.1% (not worse beyond noise)
- FAIL · Evidence: `lr=0.05`: no evidence mentions '0.05'; it fits, but nothing says the authors used it
- FAIL · Evidence: `lr_schedule=inv`: no evidence mentions 'inv'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -88.8 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole physics constants (g, mc, mp, l, f, dt)`, `Discretization bounds (theta: -0.21 to 0.21, omega: -2.0 to 2.0)`, `CartPole masscart (mc) and masspole (mp) values`, `Reset state range (uniform -0.05 to 0.05 for 4 state vars)`, `Done thresholds (abs(x) > 2.4, abs(th) > 12*pi/180)`, `max_steps`, `RL_SEED_BASE`, `RUN_TAG`, `Python version / random module behavior`, `Reward per step (hardcoded 1.0)`, `Number of actions (hardcoded 2)`, `Epsilon decay timing (after each episode)`, `Evaluation policy (greedy, no epsilon)`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr=0.5` (4.19 noise units, gap -4.2%); `lr=1` (3.33 noise units, gap -20.9%); `lr=0.02` (3.03 noise units, gap +26.8%); `lr=0.001` (2.89 noise units, gap -29.6%); `lr=0.01` (2.39 noise units, gap -39.2%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `init_q=1.0`, `lr_schedule=linear`: this claim +61.6%, mean |gap| 31.2% (2 runs)
  - `init_q=1.0`, `lr=0.2`: this claim +60.2%, mean |gap| 41.2% (2 runs)
  - `init_q=-1.0`, `lr=1`: this claim -12.3%, mean |gap| 46.9% (5 runs)

### Equally good configurations
The target claim can't tell these 13 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `lr=0.05, lr_schedule=inv` (reported)
- `lr=0.02`
- `lr=0.002`
- `lr=0.001`
- `lr=0.05, lr_schedule=linear`
- `init_q=-1.0, lr=1`
- `init_q=1.0, lr=0.5`
- `init_q=-1.0, lr=0.02`
- `init_q=1.0, lr=1`
- `init_q=-1.0, lr=0.05`
- `lr=5, lr_schedule=inv`
- `init_q=-1.0, lr_schedule=inv`
- `lr=0.02, lr_schedule=inv`

### History matching (every measured configuration, all claims together)
- 24 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `init_q, lr`: init_q=1.0, lr=0.5 (max I 1.99); init_q=-1.0, lr=1 (max I 2.04); init_q=-1.0, lr=0.05 (max I 2.05); init_q=-1.0, lr=0.5 (max I 2.08); +3 more
  - `lr`: lr=1 (max I 2.1)
  - `init_q, lr_schedule`: init_q=-1.0, lr_schedule=inv (max I 2.16)
  - `lr, lr_schedule`: lr=0.05, lr_schedule=linear (max I 2.18)
- 2 separate islands (no single-knob move joins them): init_q=1.0, lr=0.5; init_q=-1.0, lr=1; init_q=-1.0, lr=0.05 | init_q=-1.0, lr_schedule=inv
- Equally good values: `lr` in {0.01, 0.02, 0.05, 5}; `lr_schedule` in {inv, linear}

Notes:
- skipped init_q='random small': knob value 'random small' has shell metacharacters
- configurations the target claim can't tell apart from the answer: lr=0.05, lr_schedule=inv; lr=0.02; lr=0.002; lr=0.001; lr=0.05, lr_schedule=linear; init_q=-1.0, lr=1; init_q=1.0, lr=0.5; init_q=-1.0, lr=0.02; init_q=1.0, lr=1; init_q=-1.0, lr=0.05; lr=5, lr_schedule=inv; init_q=-1.0, lr_schedule=inv; lr=0.02, lr_schedule=inv
- equally good values within one noise band (measured): lr in {0.01, 0.02, 0.05, 5}; lr_schedule in {inv, linear}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `init_q=1.0`, `lr_schedule=linear` | 2 | +61.6% | -0.8% | 31.2% |
| `init_q=1.0`, `lr=0.2` | 2 | +60.2% | -22.2% | 41.2% |
| naive (reproduction as run) | 5 | +85.5% | +3.5% | 44.5% |
| `lr=0.05`, `lr_schedule=inv` | 5 | -4.5% | -86.1% | 45.3% |
| `init_q=-1.0`, `lr=1` | 5 | -12.3% | -81.5% | 46.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole physics constants (g, mc, mp, l, f, dt)`, `Discretization bounds (theta: -0.21 to 0.21, omega: -2.0 to 2.0)`, `CartPole masscart (mc) and masspole (mp) values`, `Reset state range (uniform -0.05 to 0.05 for 4 state vars)`, `Done thresholds (abs(x) > 2.4, abs(th) > 12*pi/180)`, `max_steps`, `RL_SEED_BASE`, `RUN_TAG`, `Python version / random module behavior`, `Reward per step (hardcoded 1.0)`, `Number of actions (hardcoded 2)`, `Epsilon decay timing (after each episode)`, `Evaluation policy (greedy, no epsilon)`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `f01046dd2f29515a730f43fce26caac555dcb0d94d0216bdeffa04fc793fd571`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
