# Gap Report: test-v12-07

Artifact `rlbench` · generated 2026-10-15 19:53 · 139 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +62.6% | +2.0% | ±29.7% | `lr=0.5` |

## C1: mean_reward (paper 98.685)
**Fits but unsupported** · gap +62.6% → +2.0% · 54 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0014`, `B0028`, `B0029`, `B0032`, `B0033`, `B0034` (6 run(s) of the same config)
- Config: `lr` naive `0.1`, changed to `0.5`
- Command:

  Replay: fork checkpoint `18747c1a-d988-4f49-bb0b-58f93d0a489f` and run
  ```
  RUN_TAG=2601faaba3c2 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.5 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 100.1, 121.7, 78.6, 93.28, 106.6, 101.2; gap after +2.0%; result checkpoint `3322a81b-0099-412b-9862-8ef8b02c4009`
- Effect: candidate 100.7 minus naive 160.4 = -59.73, 95% bootstrap interval [-87.12, -41.99] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 98.7 steps, and that its worst seed still balances for 95.4.

- p. 1; value used: `mean_reward` = 98.685 steps (headline claim)

### What did we measure?
- Naive median 160.4 over 5 runs; repeats: 178.1, 157.3, 178, 145.8, 160.4
- Spread: range 145.8 to 178.1, noise band ±29.31 (2 x MAD), CV 8.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +62.6% (noise band ±29.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr` the gap is +62.6% (it comes back)
- PASS · Held-out claim: C2: -51.7% to -81.1% (not worse beyond noise)
- FAIL · Evidence: `lr=0.5`: no evidence mentions '0.5'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -59.73 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole physics constants (g, mc, mp, l, f, dt)`, `Discretization bounds (theta: -0.21 to 0.21, omega: -2.0 to 2.0)`, `CartPole masscart (mc) and masspole (mp) values`, `Reset state range (uniform -0.05 to 0.05 for 4 state vars)`, `Done thresholds (abs(x) > 2.4, abs(th) > 12*pi/180)`, `max_steps`, `RL_SEED_BASE`, `RUN_TAG`, `Python version / random module behavior`, `Reward per step (hardcoded 1.0)`, `Number of actions (hardcoded 2)`, `Epsilon decay timing (after each episode)`, `Evaluation policy (greedy, no epsilon)`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr=0.05` (1.99 noise units, gap +3.5%); `lr=0.01` (1.65 noise units, gap -13.4%); `lr=1` (1.6 noise units, gap +15.0%); `lr=0.002` (1.4 noise units, gap -21.0%); `lr_schedule=inv` (1.37 noise units, gap +21.9%)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `lr=0.02`: this claim +3.0%, mean |gap| 35.1% (5 runs)
  - `lr_schedule=inv`: this claim +21.9%, mean |gap| 39.2% (3 runs)
  - `init_q=-1.0`, `lr=1`: this claim +0.0%, mean |gap| 43.2% (5 runs)

### Equally good configurations
The target claim can't tell these 13 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `lr=0.5` (reported)
- `lr=1`
- `lr=0.01`
- `lr=0.05, lr_schedule=linear`
- `lr=0.05, lr_schedule=inv`
- `init_q=-1.0, lr=1`
- `lr=0.02, lr_schedule=linear`
- `lr=0.01, lr_schedule=inv`
- `lr=0.02, lr_schedule=inv`
- `init_q=1.0, lr=1`
- `init_q=1.0, lr=0.02`
- `lr=5, lr_schedule=inv`
- `init_q=1.0, lr=0.01`

### History matching (every measured configuration, all claims together)
- 16 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `init_q, lr_schedule`: init_q=1.0, lr_schedule=inv (max I 2.07)
  - `init_q, lr`: init_q=-1.0, lr=0.02 (max I 2.08); init_q=-1.0, lr=0.05 (max I 2.5); init_q=-1.0, lr=0.01 (max I 2.51); init_q=1.0, lr=0.002 (max I 2.51)
  - `lr_schedule`: lr_schedule=inv (max I 2.22)
  - `lr, lr_schedule`: lr=0.001, lr_schedule=linear (max I 2.51); lr=0.01, lr_schedule=linear (max I 2.52); lr=0.002, lr_schedule=inv (max I 2.63); lr=0.02, lr_schedule=linear (max I 2.64)
- 2 separate islands (no single-knob move joins them): init_q=1.0, lr_schedule=inv; init_q=-1.0, lr=0.02; lr_schedule=inv | init_q=1.0, lr=0.002; init_q=1.0, lr=0.001; init_q=1.0, lr=0.5
- Equally good values: `lr` in {0.01, 0.05, 0.5, 1}

Notes:
- skipped init_q='random small': knob value 'random small' has shell metacharacters
- configurations the target claim can't tell apart from the answer: lr=0.5; lr=1; lr=0.01; lr=0.05, lr_schedule=linear; lr=0.05, lr_schedule=inv; init_q=-1.0, lr=1; lr=0.02, lr_schedule=linear; lr=0.01, lr_schedule=inv; lr=0.02, lr_schedule=inv; init_q=1.0, lr=1; init_q=1.0, lr=0.02; lr=5, lr_schedule=inv; init_q=1.0, lr=0.01
- equally good values within one noise band (measured): lr in {0.01, 0.05, 0.5, 1}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=linear`, `lr=0.02` | 5 | +3.0% | -67.2% | 35.1% |
| `lr_schedule=inv` | 3 | +21.9% | -56.6% | 39.2% |
| `lr=0.5` | 6 | +2.0% | -81.1% | 41.6% |
| `init_q=-1.0`, `lr=1` | 5 | +0.0% | -86.4% | 43.2% |
| `lr=0.05` | 6 | +22.1% | -65.7% | 43.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole physics constants (g, mc, mp, l, f, dt)`, `Discretization bounds (theta: -0.21 to 0.21, omega: -2.0 to 2.0)`, `CartPole masscart (mc) and masspole (mp) values`, `Reset state range (uniform -0.05 to 0.05 for 4 state vars)`, `Done thresholds (abs(x) > 2.4, abs(th) > 12*pi/180)`, `max_steps`, `RL_SEED_BASE`, `RUN_TAG`, `Python version / random module behavior`, `Reward per step (hardcoded 1.0)`, `Number of actions (hardcoded 2)`, `Epsilon decay timing (after each episode)`, `Evaluation policy (greedy, no epsilon)`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `f01046dd2f29515a730f43fce26caac555dcb0d94d0216bdeffa04fc793fd571`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
