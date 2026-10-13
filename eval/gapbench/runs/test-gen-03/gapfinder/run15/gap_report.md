# Gap Report: test-gen-03

Artifact `rlbench` · generated 2026-10-14 00:51 · 55 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Unexplained | -42.7% | -42.7% | ±5.3% | — |

## C1: mean_reward (paper 302.05)
**Unexplained** · gap -42.7% → -42.7% · 20 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (20 hypotheses tested).

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 302.1 steps, and that its worst seed still balances for 48.2.

- p. 1; value used: `mean_reward` = 302.05 steps (headline claim)

### What did we measure?
- Naive median 173.1 over 5 runs; repeats: 170.8, 173.1, 187.1, 190.9, 165.1
- Spread: range 165.1 to 190.9, noise band ±16.05 (2 x MAD), CV 6.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -42.7% (noise band ±5.3% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `evaluation_policy`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=1000` (7.74 noise units, gap -1.5%); `max_steps=500` (7.19 noise units, gap +4.5%)
- Near alternatives (closest across all claims):
  - `max_steps=1000`: this claim -6.2%, mean |gap| 13.3% (6 runs)
  - `max_steps=2000`: this claim +33.9%, mean |gap| 33.5% (6 runs)
  - `max_steps=500`: this claim +7.3%, mean |gap| 66.7% (6 runs)

### History matching (every measured configuration, all claims together)
- 2 of 20 tested configurations fit every claim within 3 sigma

Notes:
- {'max_steps': '500'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'max_steps': '500'} (gap +7.3%); it did not pass verification
- history matching: 2 of 20 tested configurations fit every claim within 3 sigma

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=1000` | 6 | -6.2% | -20.5% | 13.3% |
| `max_steps=2000` | 6 | +33.9% | -33.0% | 33.5% |
| naive (reproduction as run) | 5 | -42.7% | +32.1% | 37.4% |
| `max_steps=500` | 6 | +7.3% | +126.2% | 66.7% |
| `max_steps=100` | 6 | -67.6% | +71.3% | 69.5% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `evaluation_policy`

## Provenance
- GapFinder commit: `e89cebde86417c8c65704c51b94620ddb20a97ce` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `fedcbdf1b57461a1273eeb81ccb09c30931e58de34a306249ffd0422bbf51ae6`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
