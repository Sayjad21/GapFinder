# Gap Report: test-v11-10

Artifact `rlbench` · generated 2026-10-15 00:38 · 134 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Unexplained | +91.1% | +91.1% | ±11.5% | — |

## C1: mean_reward (paper 94.93)
**Unexplained** · gap +91.1% → +91.1% · 32 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (32 hypotheses tested).

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 94.9 steps, and that its worst seed still balances for 63.9.

- p. 1; value used: `mean_reward` = 94.93 steps (headline claim)

### What did we measure?
- Naive median 181.4 over 5 runs; repeats: 176, 171.1, 181.4, 185.1, 197.9
- Spread: range 171.1 to 197.9, noise band ±10.92 (2 x MAD), CV 5.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +91.1% (noise band ±11.5% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `max_steps_evaluation`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=100` (7.49 noise units, gap +4.9%); `max_steps=2000` (5.07 noise units, gap +32.8%); `lr_schedule=inv` (3.18 noise units, gap +54.5%); `max_steps=40` (2.89 noise units, gap -57.9%); `lr_schedule=linear` (1.58 noise units, gap +73.0%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `lr_schedule=linear`: this claim +2.3%, mean |gap| 23.9% (5 runs)
  - `lr_schedule=inv`, `max_steps=100`: this claim -6.1%, mean |gap| 26.7% (5 runs)
  - `max_steps=100`: this claim +4.8%, mean |gap| 26.7% (6 runs)

### History matching (every measured configuration, all claims together)
- 3 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.51); lr_schedule=inv, max_steps=100 (max I 1.14)
  - `max_steps`: max_steps=100 (max I 0.91)

Notes:
- {'max_steps': '100'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'max_steps': '100'} (gap +4.8%); it did not pass verification
- history matching: 3 of 32 tested configurations fit every claim within 3 sigma

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100`, `lr_schedule=linear` | 5 | +2.3% | +45.5% | 23.9% |
| `lr_schedule=inv`, `max_steps=100` | 5 | -6.1% | -47.3% | 26.7% |
| `max_steps=100` | 6 | +4.8% | +48.7% | 26.7% |
| `lr_schedule=inv`, `max_steps=400` | 5 | +43.4% | -10.2% | 26.8% |
| `lr_schedule=inv` | 6 | +50.9% | -4.7% | 27.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `max_steps_evaluation`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
