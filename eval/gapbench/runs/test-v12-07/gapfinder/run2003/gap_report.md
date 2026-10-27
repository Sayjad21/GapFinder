# Gap Report: test-v12-07

Artifact `rlbench` · generated 2026-10-15 21:10 · 132 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Unexplained | +80.3% | +80.3% | ±4.1% | — |

## C1: mean_reward (paper 98.685)
**Unexplained** · gap +80.3% → +80.3% · 54 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (54 hypotheses tested).

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 98.7 steps, and that its worst seed still balances for 95.4.

- p. 1; value used: `mean_reward` = 98.685 steps (headline claim)

### What did we measure?
- Naive median 177.9 over 5 runs; repeats: 179.9, 181.9, 177.2, 175.6, 177.9
- Spread: range 175.6 to 181.9, noise band ±4.08 (2 x MAD), CV 1.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +80.3% (noise band ±4.1% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole physics constants (g, mc, mp, l, f, dt)`, `Discretization bounds (theta: -0.21 to 0.21, omega: -2.0 to 2.0)`, `CartPole masscart (mc) and masspole (mp) values`, `Reset state range (uniform -0.05 to 0.05 for 4 state vars)`, `Done thresholds (abs(x) > 2.4, abs(th) > 12*pi/180)`, `max_steps`, `RL_SEED_BASE`, `RUN_TAG`, `Python version / random module behavior`, `Reward per step (hardcoded 1.0)`, `Number of actions (hardcoded 2)`, `Epsilon decay timing (after each episode)`, `Evaluation policy (greedy, no epsilon)`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr=0.002` (18.54 noise units, gap -3.6%); `lr=0.01` (16.26 noise units, gap -13.1%); `lr=0.02` (15.96 noise units, gap -14.3%); `lr=0.05` (14.06 noise units, gap +22.1%); `lr=0.2` (12.54 noise units, gap +28.4%) (and 5 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr=0.5`, `init_q=1.0`: this claim +57.9%, mean |gap| 37.9% (2 runs)
  - `lr_schedule=inv`, `init_q=1.0`: this claim +45.5%, mean |gap| 40.1% (2 runs)
  - `init_q=-1.0`, `lr=1`: this claim +3.1%, mean |gap| 45.1% (3 runs)

### History matching (every measured configuration, all claims together)
- 1 of 54 tested configurations fit every claim within 3 sigma

Notes:
- skipped init_q='random small': knob value 'random small' has shell metacharacters
- {'lr': '0.01'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'lr': '0.01'} (gap -21.9%); it did not pass verification
- history matching: 1 of 54 tested configurations fit every claim within 3 sigma

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr=0.5`, `init_q=1.0` | 2 | +57.9% | -18.0% | 37.9% |
| `lr_schedule=inv`, `init_q=1.0` | 2 | +45.5% | -34.8% | 40.1% |
| `init_q=-1.0`, `lr=1` | 3 | +3.1% | -87.1% | 45.1% |
| naive (reproduction as run) | 5 | +80.3% | -11.7% | 46.0% |
| `lr_schedule=inv`, `lr=5` | 3 | -2.2% | -90.1% | 46.1% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole physics constants (g, mc, mp, l, f, dt)`, `Discretization bounds (theta: -0.21 to 0.21, omega: -2.0 to 2.0)`, `CartPole masscart (mc) and masspole (mp) values`, `Reset state range (uniform -0.05 to 0.05 for 4 state vars)`, `Done thresholds (abs(x) > 2.4, abs(th) > 12*pi/180)`, `max_steps`, `RL_SEED_BASE`, `RUN_TAG`, `Python version / random module behavior`, `Reward per step (hardcoded 1.0)`, `Number of actions (hardcoded 2)`, `Epsilon decay timing (after each episode)`, `Evaluation policy (greedy, no epsilon)`

## Provenance
- GapFinder commit: `cd8c8af2b9d079dd9a57443ed501c0dd8a467d34` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `f01046dd2f29515a730f43fce26caac555dcb0d94d0216bdeffa04fc793fd571`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
