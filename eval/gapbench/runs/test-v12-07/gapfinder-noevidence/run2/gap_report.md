# Gap Report: test-v12-07

Artifact `rlbench` · generated 2026-10-15 08:18 · 13 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Unexplained | +89.2% | +89.2% | ±9.5% | — |

## C1: mean_reward (paper 98.685)
**Unexplained** · gap +89.2% → +89.2% · 2 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (2 hypotheses tested).

### What did the paper report?
> Figure 1 (final evaluation): mean reward 98.7; worst seed 95.4.

- p. 1, Figure 1; value used: `mean_reward` = 98.685 steps (headline claim)

### What did we measure?
- Naive median 186.7 over 5 runs; repeats: 189.8, 179.7, 195.8, 186.7, 182
- Spread: range 179.7 to 195.8, noise band ±9.4 (2 x MAD), CV 3.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +89.2% (noise band ±9.5% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole physics constants (g, mc, mp, l, f, dt)`, `Discretization bounds (theta: -0.21 to 0.21, omega: -2.0 to 2.0)`, `Episode termination thresholds (x>2.4, th>12*pi/180)`, `Initial state distribution (uniform -0.05 to 0.05 for all 4 vars)`, `max_steps`, `Force magnitude (f)`, `Seed base (RL_SEED_BASE / RUN_TAG)`, `CartPole mass cart (mc)`, `CartPole mass pole (mp)`, `CartPole length (l)`, `CartPole timestep (dt)`, `CartPole gravity (g)`, `RUN_TAG`, `RL_SEED_BASE`, `Q-table default for unseen states during evaluation`, `Output rounding precision`, `Python random module implementation`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (7.42 noise units, gap +18.5%); `lr_schedule=linear` (1.45 noise units, gap +75.4%)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`: this claim +69.9%, mean |gap| 42.3% (4 runs)
  - `lr_schedule=inv`: this claim +22.8%, mean |gap| 53.2% (4 runs)

### History matching (every measured configuration, all claims together)
- 1 of 2 tested configurations fit every claim within 3 sigma

Notes:
- evidence gate off: no evidence was checked, so this cannot be labelled Explained
- {'lr_schedule': 'inv'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'lr_schedule': 'inv'} (gap +22.8%); it did not pass verification
- history matching: 1 of 2 tested configurations fit every claim within 3 sigma

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=linear` | 4 | +69.9% | +14.8% | 42.3% |
| `lr_schedule=inv` | 4 | +22.8% | -83.6% | 53.2% |
| naive (reproduction as run) | 5 | +89.2% | +40.5% | 64.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole physics constants (g, mc, mp, l, f, dt)`, `Discretization bounds (theta: -0.21 to 0.21, omega: -2.0 to 2.0)`, `Episode termination thresholds (x>2.4, th>12*pi/180)`, `Initial state distribution (uniform -0.05 to 0.05 for all 4 vars)`, `max_steps`, `Force magnitude (f)`, `Seed base (RL_SEED_BASE / RUN_TAG)`, `CartPole mass cart (mc)`, `CartPole mass pole (mp)`, `CartPole length (l)`, `CartPole timestep (dt)`, `CartPole gravity (g)`, `RUN_TAG`, `RL_SEED_BASE`, `Q-table default for unseen states during evaluation`, `Output rounding precision`, `Python random module implementation`

## Provenance
- GapFinder commit: `f01fe3d9a0095f98d6304ad0543b917ca8e529eb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `f01046dd2f29515a730f43fce26caac555dcb0d94d0216bdeffa04fc793fd571`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
