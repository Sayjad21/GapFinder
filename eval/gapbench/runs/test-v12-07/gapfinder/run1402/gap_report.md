# Gap Report: test-v12-07

Artifact `rlbench` · generated 2026-10-15 19:03 · 12 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +92.1% | +40.3% | ±17.4% | `lr_schedule=inv` |

## C1: mean_reward (paper 98.685)
**Fits but unsupported** · gap +92.1% → +40.3% · 2 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0007`, `B0008`, `B0009`, `B0010`, `B0011`, `B0012` (6 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `inv`
- Command:

  Replay: fork checkpoint `383356b5-2b13-4d61-a063-cae7102161b5` and run
  ```
  RUN_TAG=40fdac58505c "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 151, 146.4, 130.3, 142.5, 133.4, 134.4; gap after +40.3%; result checkpoint `756344f0-0ac8-42d8-a7a9-f6bc813b533d`
- Effect: candidate 138.5 minus naive 189.6 = -51.06, 95% bootstrap interval [-59.4, -27.23] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> Figure 1 (final evaluation): mean reward 98.7; worst seed 95.4.

- p. 1, Figure 1; value used: `mean_reward` = 98.685 steps (headline claim)

### What did we measure?
- Naive median 189.6 over 5 runs; repeats: 152.7, 189.6, 198.1, 196.6, 170.1
- Spread: range 152.7 to 198.1, noise band ±17.15 (2 x MAD), CV 10.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +92.1% (noise band ±17.4% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is +92.1% (it comes back)
- PASS · Held-out claim: C2: +40.4% to -65.8% (not worse beyond noise)
- FAIL · Evidence: `lr_schedule=inv`: no evidence mentions 'inv'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -51.06 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole physics constants (g, mc, mp, l, f, dt)`, `Discretization bounds (theta: -0.21 to 0.21, omega: -2.0 to 2.0)`, `Episode termination thresholds (x>2.4, th>12*pi/180)`, `Initial state distribution (uniform -0.05 to 0.05 for all 4 vars)`, `max_steps`, `Force magnitude (f)`, `Seed base (RL_SEED_BASE / RUN_TAG)`, `CartPole mass cart (mc)`, `CartPole mass pole (mp)`, `CartPole length (l)`, `CartPole timestep (dt)`, `CartPole gravity (g)`, `RUN_TAG`, `RL_SEED_BASE`, `Q-table default for unseen states during evaluation`, `Output rounding precision`, `Python random module implementation`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives: none recorded

### History matching (every measured configuration, all claims together)
- out-of-space likely: no tested configuration comes within 3 sigma of C1, among 2 tested

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv` | 6 | +40.3% | -65.8% | 53.1% |
| naive (reproduction as run) | 5 | +92.1% | +40.4% | 66.2% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole physics constants (g, mc, mp, l, f, dt)`, `Discretization bounds (theta: -0.21 to 0.21, omega: -2.0 to 2.0)`, `Episode termination thresholds (x>2.4, th>12*pi/180)`, `Initial state distribution (uniform -0.05 to 0.05 for all 4 vars)`, `max_steps`, `Force magnitude (f)`, `Seed base (RL_SEED_BASE / RUN_TAG)`, `CartPole mass cart (mc)`, `CartPole mass pole (mp)`, `CartPole length (l)`, `CartPole timestep (dt)`, `CartPole gravity (g)`, `RUN_TAG`, `RL_SEED_BASE`, `Q-table default for unseen states during evaluation`, `Output rounding precision`, `Python random module implementation`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `f01046dd2f29515a730f43fce26caac555dcb0d94d0216bdeffa04fc793fd571`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
