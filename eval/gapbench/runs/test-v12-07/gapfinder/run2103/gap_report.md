# Gap Report: test-v12-07

Artifact `rlbench` · generated 2026-10-15 21:10 · 132 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +91.3% | +2.9% | ±6.9% | `lr=0.02` |

## C1: mean_reward (paper 98.685)
**Fits but unsupported** · gap +91.3% → +2.9% · 54 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0015`, `B0030`, `B0031`, `B0038` (4 run(s) of the same config)
- Config: `lr` naive `0.1`, changed to `0.02`
- Command:

  Replay: fork checkpoint `95311428-58f0-4a1b-be5f-f0d10ec1ac6a` and run
  ```
  RUN_TAG=d521399177e9 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.02 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 120.6, 82.46, 151, 62.2; gap after +2.9%; result checkpoint `b4dd4141-46e9-4b5f-9984-8753da5e0187`
- Effect: candidate 101.5 minus naive 188.8 = -87.24, 95% bootstrap interval [-130.1, -36.41] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 98.7 steps, and that its worst seed still balances for 95.4.

- p. 1; value used: `mean_reward` = 98.685 steps (headline claim)

### What did we measure?
- Naive median 188.8 over 5 runs; repeats: 188.8, 185.4, 188, 193.6, 192.8
- Spread: range 185.4 to 193.6, noise band ±6.82 (2 x MAD), CV 1.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +91.3% (noise band ±6.9% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr` the gap is +91.3% (it comes back)
- PASS · Held-out claim: C2: +72.4% to -76.9% (not worse beyond noise)
- FAIL · Evidence: `lr=0.02`: no evidence mentions '0.02'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -87.24 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole physics constants (g, mc, mp, l, f, dt)`, `Discretization bounds (theta: -0.21 to 0.21, omega: -2.0 to 2.0)`, `CartPole masscart (mc) and masspole (mp) values`, `Reset state range (uniform -0.05 to 0.05 for 4 state vars)`, `Done thresholds (abs(x) > 2.4, abs(th) > 12*pi/180)`, `max_steps`, `RL_SEED_BASE`, `RUN_TAG`, `Python version / random module behavior`, `Reward per step (hardcoded 1.0)`, `Number of actions (hardcoded 2)`, `Epsilon decay timing (after each episode)`, `Evaluation policy (greedy, no epsilon)`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr=1` (11.97 noise units, gap -8.6%); `lr=0.5` (10.61 noise units, gap +18.0%); `lr_schedule=inv` (10.49 noise units, gap +18.8%); `lr=0.002` (9.57 noise units, gap -25.2%); `lr=0.01` (8.84 noise units, gap -30.2%) (and 3 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `init_q=-1.0`: this claim +61.8%, mean |gap| 31.3% (2 runs)
  - `lr_schedule=inv`, `init_q=-1.0`: this claim +46.4%, mean |gap| 35.4% (2 runs)
  - `lr_schedule=inv`: this claim +51.7%, mean |gap| 36.2% (3 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `lr=0.02` (reported)
- `lr=0.05`
- `init_q=-1.0, lr=0.05`

### History matching (every measured configuration, all claims together)
- out-of-space suspected: 7 tested configuration(s) fit C1, and every other claim (C2) fits some tested configuration, but none of the 54 tested configurations fits them all. The claims are mutually inconsistent under every tested condition, which points to a cause outside the exposed settings (code, data or evaluation)
- Fit C1 alone (7; worst claim's implausibility in brackets, lowest is the least inconsistent): lr=0.02 (4.29); init_q=-1.0, lr=0.05 (4.56); lr=0.02, lr_schedule=linear (4.76); lr=0.05, lr_schedule=linear (4.88); init_q=-1.0, lr=1 (5.08); init_q=1.0, lr=0.02 (5.18)

Notes:
- skipped init_q='random small': knob value 'random small' has shell metacharacters
- configurations the target claim can't tell apart from the answer: lr=0.02; lr=0.05; init_q=-1.0, lr=0.05

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=linear`, `init_q=-1.0` | 2 | +61.8% | -0.8% | 31.3% |
| `lr_schedule=inv`, `init_q=-1.0` | 2 | +46.4% | -24.3% | 35.4% |
| `lr_schedule=inv` | 3 | +51.7% | -20.6% | 36.2% |
| `lr=0.02` | 4 | +2.9% | -76.9% | 39.9% |
| `lr_schedule=inv`, `init_q=1.0` | 2 | +41.6% | -45.3% | 43.4% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole physics constants (g, mc, mp, l, f, dt)`, `Discretization bounds (theta: -0.21 to 0.21, omega: -2.0 to 2.0)`, `CartPole masscart (mc) and masspole (mp) values`, `Reset state range (uniform -0.05 to 0.05 for 4 state vars)`, `Done thresholds (abs(x) > 2.4, abs(th) > 12*pi/180)`, `max_steps`, `RL_SEED_BASE`, `RUN_TAG`, `Python version / random module behavior`, `Reward per step (hardcoded 1.0)`, `Number of actions (hardcoded 2)`, `Epsilon decay timing (after each episode)`, `Evaluation policy (greedy, no epsilon)`

## Provenance
- GapFinder commit: `cd8c8af2b9d079dd9a57443ed501c0dd8a467d34` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `f01046dd2f29515a730f43fce26caac555dcb0d94d0216bdeffa04fc793fd571`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
