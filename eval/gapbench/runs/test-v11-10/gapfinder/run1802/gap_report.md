# Gap Report: test-v11-10

Artifact `rlbench` · generated 2026-10-15 19:49 · 107 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Unexplained | +67.2% | +67.2% | ±14.8% | — |

## C1: mean_reward (paper 94.93)
**Unexplained** · gap +67.2% → +67.2% · 32 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (32 hypotheses tested).

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 94.9 steps, and that its worst seed still balances for 63.9.

- p. 1; value used: `mean_reward` = 94.93 steps (headline claim)

### What did we measure?
- Naive median 158.7 over 5 runs; repeats: 194, 151.7, 172.5, 152.9, 158.7
- Spread: range 151.7 to 194, noise band ±14.04 (2 x MAD), CV 10.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +67.2% (noise band ±14.8% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `max_steps_evaluation`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=100` (4.29 noise units, gap +3.8%)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`, `max_steps=100`: this claim -4.5%, mean |gap| 15.1% (5 runs)
  - `lr_schedule=linear`, `max_steps=100`: this claim +2.1%, mean |gap| 22.8% (5 runs)
  - `max_steps=100`: this claim +5.2%, mean |gap| 29.6% (6 runs)

### History matching (every measured configuration, all claims together)
- 8 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 8 configurations
  - `lr_schedule, max_steps`: lr_schedule=inv, max_steps=100 (max I 0.54); lr_schedule=linear, max_steps=100 (max I 0.62); lr_schedule=linear, max_steps=40 (max I 2.72); lr_schedule=inv, max_steps=1000 (max I 2.77); +2 more
  - `max_steps`: max_steps=100 (max I 0.99)
  - `lr_schedule`: lr_schedule=linear (max I 2.96)

Notes:
- {'max_steps': '100'} closes this claim but makes held-out claims worse; rejected
- lr_schedule dropped: with repeats, {'max_steps': '100', 'lr_schedule': 'linear'} fits {'max_steps': '100'}'s gap by less than one noise band, so it is not needed
- closest configuration tried: {'max_steps': '100'} (gap +5.2%); it did not pass verification
- history matching: 8 of 32 tested configurations fit every claim within 3 sigma

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv`, `max_steps=100` | 5 | -4.5% | -25.7% | 15.1% |
| `lr_schedule=linear`, `max_steps=100` | 5 | +2.1% | +43.4% | 22.8% |
| `max_steps=100` | 6 | +5.2% | +54.1% | 29.6% |
| `lr_schedule=inv` | 5 | +55.5% | -11.0% | 33.2% |
| naive (reproduction as run) | 5 | +67.2% | -18.8% | 43.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `max_steps_evaluation`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
