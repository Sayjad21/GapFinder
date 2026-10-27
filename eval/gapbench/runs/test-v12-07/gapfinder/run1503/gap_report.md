# Gap Report: test-v12-07

Artifact `rlbench` · generated 2026-10-15 19:29 · 125 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Explains target, conflicts with held-out | +73.1% | +21.1% | ±10.7% | `init_q=-1.0`, `lr_schedule=inv` |

## C1: mean_reward (paper 98.685)
**Explains target, conflicts with held-out** · gap +73.1% → +21.1% · 54 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0075`, `B0088`, `B0121` (3 run(s) of the same config)
- Config: `init_q` naive `0.0`, changed to `-1.0`
- Config: `lr_schedule` naive `const`, changed to `inv`
- Command: not recorded
- Output: `mean_reward` 103.3, 119.6, 133.7; gap after +21.1%
- Effect: candidate 119.6 minus naive 170.8 = -51.23, 95% bootstrap interval [-71.88, -31.56] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 98.7 steps, and that its worst seed still balances for 95.4.

- p. 1; value used: `mean_reward` = 98.685 steps (headline claim)

### What did we measure?
- Naive median 170.8 over 5 runs; repeats: 157.1, 170.5, 170.8, 176.1, 176.7
- Spread: range 157.1 to 176.7, noise band ±10.54 (2 x MAD), CV 4.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +73.1% (noise band ±10.7% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is -51.23 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole physics constants (g, mc, mp, l, f, dt)`, `Discretization bounds (theta: -0.21 to 0.21, omega: -2.0 to 2.0)`, `CartPole masscart (mc) and masspole (mp) values`, `Reset state range (uniform -0.05 to 0.05 for 4 state vars)`, `Done thresholds (abs(x) > 2.4, abs(th) > 12*pi/180)`, `max_steps`, `RL_SEED_BASE`, `RUN_TAG`, `Python version / random module behavior`, `Reward per step (hardcoded 1.0)`, `Number of actions (hardcoded 2)`, `Epsilon decay timing (after each episode)`, `Evaluation policy (greedy, no epsilon)`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr=0.05` (6.82 noise units, gap +0.2%); `lr=0.01` (6.09 noise units, gap -8.1%); `lr=0.002` (5.98 noise units, gap -9.2%); `lr=1` (5.65 noise units, gap -12.7%); `lr=0.02` (5.34 noise units, gap -16.0%) (and 4 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr=1`, `init_q=-1.0`: this claim -2.3%, mean |gap| 44.1% (3 runs)
  - `lr_schedule=inv`, `lr=0.05`: this claim -6.2%, mean |gap| 45.6% (3 runs)
  - `lr=0.05`, `init_q=1.0`: this claim +5.3%, mean |gap| 45.7% (3 runs)

### History matching (every measured configuration, all claims together)
- out-of-space suspected: 18 tested configuration(s) fit C1, and every other claim (C2) fits some tested configuration, but none of the 54 tested configurations fits them all. The claims are mutually inconsistent under every tested condition, which points to a cause outside the exposed settings (code, data or evaluation)
- Fit C1 alone (10; worst claim's implausibility in brackets, lowest is the least inconsistent): lr=0.05, lr_schedule=inv (5.88); init_q=-1.0, lr=1 (6.01); lr=1 (6.12); init_q=1.0, lr=1 (6.13); init_q=1.0, lr=0.05 (6.16); lr=0.05, lr_schedule=linear (6.22)

Notes:
- skipped init_q='random small': knob value 'random small' has shell metacharacters
- {'lr': '0.05'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'lr': '0.05'} (gap +17.3%); it did not pass verification
- history matching: out-of-space suspected: 18 tested configuration(s) fit C1, and every other claim (C2) fits some tested configuration, but none of the 54 tested configurations fits them all. The claims are mutually inconsistent under every tested condition, which points to a cause outside the exposed settings (code, data or evaluation)
- {'init_q': '-1.0', 'lr_schedule': 'inv'} matches C1 (I=2.63) but breaks C2 (I=4.34); no tested condition matches all claims, so the rest of the gap probably lies in code, data or evaluation, which GapFinder doesn't change

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv`, `init_q=-1.0` | 3 | +21.1% | -60.0% | 40.6% |
| `lr=1`, `init_q=-1.0` | 3 | -2.3% | -85.9% | 44.1% |
| `lr_schedule=inv`, `lr=0.05` | 3 | -6.2% | -85.0% | 45.6% |
| `lr=0.05`, `init_q=1.0` | 3 | +5.3% | -86.1% | 45.7% |
| `lr_schedule=inv`, `init_q=1.0` | 2 | +48.9% | -43.8% | 46.4% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole physics constants (g, mc, mp, l, f, dt)`, `Discretization bounds (theta: -0.21 to 0.21, omega: -2.0 to 2.0)`, `CartPole masscart (mc) and masspole (mp) values`, `Reset state range (uniform -0.05 to 0.05 for 4 state vars)`, `Done thresholds (abs(x) > 2.4, abs(th) > 12*pi/180)`, `max_steps`, `RL_SEED_BASE`, `RUN_TAG`, `Python version / random module behavior`, `Reward per step (hardcoded 1.0)`, `Number of actions (hardcoded 2)`, `Epsilon decay timing (after each episode)`, `Evaluation policy (greedy, no epsilon)`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `f01046dd2f29515a730f43fce26caac555dcb0d94d0216bdeffa04fc793fd571`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
