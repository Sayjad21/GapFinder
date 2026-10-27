# Gap Report: test-v11-04

Artifact `rlbench` · generated 2026-10-15 01:14 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Unexplained | +94.7% | +94.7% | ±24.3% | — |

## C1: mean_reward (paper 94.93)
**Unexplained** · gap +94.7% → +94.7% · 57 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (57 hypotheses tested).

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 94.9 on CartPole; the worst of its seeds reaches 63.9.

- p. 1; value used: `mean_reward` = 94.93 reward (headline claim)

### What did we measure?
- Naive median 184.8 over 5 runs; repeats: 181.8, 196.4, 147.1, 184.8, 197.8
- Spread: range 147.1 to 197.8, noise band ±23.09 (2 x MAD), CV 11.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +94.7% (noise band ±24.3% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr=1` (3.85 noise units, gap +1.2%); `max_steps=100` (3.68 noise units, gap +5.3%); `lr=0.02` (3.61 noise units, gap -6.9%); `lr=0.5` (3.13 noise units, gap +18.5%); `lr=0.002` (2.75 noise units, gap -27.8%) (and 10 more in the JSON)
- Near alternatives (closest across all claims):
  - `max_steps=100`: this claim +4.3%, mean |gap| 26.6% (6 runs)
  - `lr_schedule=inv`, `max_steps=100`: this claim -14.0%, mean |gap| 33.3% (5 runs)
  - `eps_start=0.2`, `lr=1`: this claim +7.3%, mean |gap| 42.8% (5 runs)

### History matching (every measured configuration, all claims together)
- 27 of 57 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.08); lr_schedule=inv, max_steps=100 (max I 0.93)
  - `max_steps`: max_steps=100 (max I 0.44)
  - `lr, lr_schedule`: lr=0.02, lr_schedule=linear (max I 0.61); lr=0.02, lr_schedule=inv (max I 0.93)
  - `eps_start, lr_schedule`: eps_start=0.2, lr_schedule=linear (max I 0.66)
  - `lr`: lr=0.5 (max I 0.96)
  - `eps_start, lr`: eps_start=0.1, lr=1 (max I 0.98); eps_start=0.2, lr=1 (max I 0.98)
  - `lr, max_steps`: lr=0.02, max_steps=10000 (max I 1.04)

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'max_steps': '100', 'lr_schedule': 'linear'} for 'confirm-combo')
- closest configuration not verified: {'lr': '0.02', 'lr_schedule': 'linear'} (gap -1.0%, 1 of 5 confirmation runs); the budget ran out first, so no attribution is made
- history matching: 27 of 57 tested configurations fit every claim within 3 sigma

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 6 | +4.3% | +48.9% | 26.6% |
| `lr_schedule=inv`, `max_steps=100` | 5 | -14.0% | -52.5% | 33.3% |
| `eps_start=0.2`, `lr=1` | 5 | +7.3% | -78.2% | 42.8% |
| `eps_start=0.1`, `lr=1` | 5 | +5.4% | -82.2% | 43.8% |
| `lr=1` | 6 | -9.0% | -79.3% | 44.1% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
