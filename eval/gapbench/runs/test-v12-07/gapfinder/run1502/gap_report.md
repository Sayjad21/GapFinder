# Gap Report: test-v12-07

Artifact `rlbench` · generated 2026-10-15 19:28 · 17 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Unexplained | +90.1% | +90.1% | ±20.2% | — |

## C1: mean_reward (paper 98.685)
**Unexplained** · gap +90.1% → +90.1% · 2 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (2 hypotheses tested).

### What did the paper report?
> Figure 1 (final evaluation): mean reward 98.7; worst seed 95.4.

- p. 1, Figure 1; value used: `mean_reward` = 98.685 steps (headline claim)

### What did we measure?
- Naive median 187.6 over 5 runs; repeats: 200, 170.1, 177.6, 187.6, 194.5
- Spread: range 170.1 to 200, noise band ±19.98 (2 x MAD), CV 6.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +90.1% (noise band ±20.2% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole physics constants (g, mc, mp, l, f, dt)`, `Discretization bounds (theta: -0.21 to 0.21, omega: -2.0 to 2.0)`, `Episode termination thresholds (x>2.4, th>12*pi/180)`, `Initial state distribution (uniform -0.05 to 0.05 for all 4 vars)`, `max_steps`, `Force magnitude (f)`, `Seed base (RL_SEED_BASE / RUN_TAG)`, `CartPole mass cart (mc)`, `CartPole mass pole (mp)`, `CartPole length (l)`, `CartPole timestep (dt)`, `CartPole gravity (g)`, `RUN_TAG`, `RL_SEED_BASE`, `Q-table default for unseen states during evaluation`, `Output rounding precision`, `Python random module implementation`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (3.38 noise units, gap +21.5%); `lr_schedule=linear` (1.56 noise units, gap +58.4%)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`: this claim +41.4%, mean |gap| 46.6% (6 runs)
  - `lr_schedule=linear`: this claim +71.3%, mean |gap| 62.5% (6 runs)

### History matching (every measured configuration, all claims together)
- out-of-space likely: no tested configuration comes within 3 sigma of C1, among 2 tested

Notes:
- {'lr_schedule': 'inv'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'lr_schedule': 'inv'} (gap +41.4%); it did not pass verification
- history matching: out-of-space likely: no tested configuration comes within 3 sigma of C1, among 2 tested

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| naive (reproduction as run) | 5 | +90.1% | -2.9% | 46.5% |
| `lr_schedule=inv` | 6 | +41.4% | -51.8% | 46.6% |
| `lr_schedule=linear` | 6 | +71.3% | +53.6% | 62.5% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole physics constants (g, mc, mp, l, f, dt)`, `Discretization bounds (theta: -0.21 to 0.21, omega: -2.0 to 2.0)`, `Episode termination thresholds (x>2.4, th>12*pi/180)`, `Initial state distribution (uniform -0.05 to 0.05 for all 4 vars)`, `max_steps`, `Force magnitude (f)`, `Seed base (RL_SEED_BASE / RUN_TAG)`, `CartPole mass cart (mc)`, `CartPole mass pole (mp)`, `CartPole length (l)`, `CartPole timestep (dt)`, `CartPole gravity (g)`, `RUN_TAG`, `RL_SEED_BASE`, `Q-table default for unseen states during evaluation`, `Output rounding precision`, `Python random module implementation`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `f01046dd2f29515a730f43fce26caac555dcb0d94d0216bdeffa04fc793fd571`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
