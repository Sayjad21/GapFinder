# Gap Report: test-v12-07

Artifact `rlbench` · generated 2026-10-16 02:00 · 177 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +77.2% | +3.3% | ±17.1% | `lr=0.02` |

## C1: mean_reward (paper 98.685)
**Fits but unsupported** · gap +77.2% → +3.3% · 54 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0015`, `B0030`, `B0031`, `B0041`, `B0042`, `B0043` (6 run(s) of the same config)
- Config: `lr` naive `0.1`, changed to `0.02`
- Command:

  Replay: fork checkpoint `b3e29da8-2078-4235-946f-b827f09a04f0` and run
  ```
  RUN_TAG=dc8d62122e7b "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.02 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 106.3, 102.8, 101.2, 62.73, 127.7, 82.52; gap after +3.3%; result checkpoint `4d485f65-31ce-4343-b8bd-dfa4d8fc2090`
- Effect: candidate 102 minus naive 174.9 = -72.91, 95% bootstrap interval [-110.1, -44.92] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 98.7 steps, and that its worst seed still balances for 95.4.

- p. 1; value used: `mean_reward` = 98.685 steps (headline claim)

### What did we measure?
- Naive median 174.9 over 5 runs; repeats: 169.9, 141.8, 174.9, 194.6, 183.3
- Spread: range 141.8 to 194.6, noise band ±16.9 (2 x MAD), CV 11.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +77.2% (noise band ±17.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr` the gap is +77.2% (it comes back)
- PASS · Held-out claim: C2: -51.7% to -87.9% (not worse beyond noise)
- FAIL · Evidence: `lr=0.02`: no evidence mentions '0.02'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -72.91 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole physics constants (g, mc, mp, l, f, dt)`, `Discretization bounds (theta: -0.21 to 0.21, omega: -2.0 to 2.0)`, `CartPole masscart (mc) and masspole (mp) values`, `Reset state range (uniform -0.05 to 0.05 for 4 state vars)`, `Done thresholds (abs(x) > 2.4, abs(th) > 12*pi/180)`, `max_steps`, `RL_SEED_BASE`, `RUN_TAG`, `Python version / random module behavior`, `Reward per step (hardcoded 1.0)`, `Number of actions (hardcoded 2)`, `Epsilon decay timing (after each episode)`, `Evaluation policy (greedy, no epsilon)`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr=0.001` (3.65 noise units, gap -14.6%); `lr=0.5` (3.52 noise units, gap +17.0%); `lr=1` (3.47 noise units, gap -17.8%); `lr_schedule=inv` (3.41 noise units, gap +18.8%); `lr=0.01` (3.41 noise units, gap -18.8%) (and 3 more in the JSON)
- Near alternatives (closest across all claims):
  - `init_q=-1.0`, `lr_schedule=inv`: this claim +54.0%, mean |gap| 31.9% (2 runs)
  - `lr=0.5`, `init_q=-1.0`: this claim +42.2%, mean |gap| 38.4% (2 runs)
  - `init_q=1.0`, `lr_schedule=inv`: this claim +20.8%, mean |gap| 42.3% (5 runs)

### Equally good configurations
The target claim can't tell these 15 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `lr=0.02` (reported)
- `lr=0.05`
- `lr=1`
- `lr=0.001`
- `init_q=-1.0, lr=1`
- `lr=0.05, lr_schedule=inv`
- `lr=0.02, lr_schedule=inv`
- `lr=0.02, lr_schedule=linear`
- `init_q=-1.0, lr=0.02`
- `lr=0.05, lr_schedule=linear`
- `init_q=1.0, lr=1`
- `lr=0.001, lr_schedule=inv`
- `lr=5, lr_schedule=inv`
- `init_q=-1.0, lr=0.01`
- `init_q=1.0, lr=0.05`

### History matching (every measured configuration, all claims together)
- 34 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr, lr_schedule`: lr=0.05, lr_schedule=linear (max I 1.54); lr=0.05, lr_schedule=inv (max I 1.9); lr=0.02, lr_schedule=linear (max I 1.92)
  - `lr_schedule`: lr_schedule=inv (max I 1.62)
  - `init_q, lr`: init_q=1.0, lr=0.05 (max I 1.78); init_q=-1.0, lr=1 (max I 1.91)
  - `init_q, lr_schedule`: init_q=1.0, lr_schedule=inv (max I 1.79)
  - `lr`: lr=0.05 (max I 1.8); lr=0.02 (max I 1.9); lr=1 (max I 1.92)
- Equally good values: `lr` in {0.02, 0.05, 1}

Notes:
- skipped init_q='random small': knob value 'random small' has shell metacharacters
- configurations the target claim can't tell apart from the answer: lr=0.02; lr=0.05; lr=1; lr=0.001; init_q=-1.0, lr=1; lr=0.05, lr_schedule=inv; lr=0.02, lr_schedule=inv; lr=0.02, lr_schedule=linear; init_q=-1.0, lr=0.02; lr=0.05, lr_schedule=linear; init_q=1.0, lr=1; lr=0.001, lr_schedule=inv; lr=5, lr_schedule=inv; init_q=-1.0, lr=0.01; init_q=1.0, lr=0.05
- equally good values within one noise band (measured): lr in {0.02, 0.05, 1}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `init_q=-1.0`, `lr_schedule=inv` | 2 | +54.0% | +9.8% | 31.9% |
| `lr=0.5`, `init_q=-1.0` | 2 | +42.2% | -34.6% | 38.4% |
| `init_q=1.0`, `lr_schedule=inv` | 5 | +20.8% | -63.8% | 42.3% |
| `lr=1`, `init_q=1.0` | 5 | -1.6% | -86.7% | 44.2% |
| `lr=0.02` | 6 | +3.3% | -87.9% | 45.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole physics constants (g, mc, mp, l, f, dt)`, `Discretization bounds (theta: -0.21 to 0.21, omega: -2.0 to 2.0)`, `CartPole masscart (mc) and masspole (mp) values`, `Reset state range (uniform -0.05 to 0.05 for 4 state vars)`, `Done thresholds (abs(x) > 2.4, abs(th) > 12*pi/180)`, `max_steps`, `RL_SEED_BASE`, `RUN_TAG`, `Python version / random module behavior`, `Reward per step (hardcoded 1.0)`, `Number of actions (hardcoded 2)`, `Epsilon decay timing (after each episode)`, `Evaluation policy (greedy, no epsilon)`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `f01046dd2f29515a730f43fce26caac555dcb0d94d0216bdeffa04fc793fd571`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
