# Gap Report: test-v11-04

Artifact `rlbench` · generated 2026-10-15 00:23 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Unexplained | +105.9% | +105.9% | ±2.8% | — |

## C1: mean_reward (paper 94.93)
**Unexplained** · gap +105.9% → +105.9% · 32 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (32 hypotheses tested).

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 94.9 on CartPole; the worst of its seeds reaches 63.9.

- p. 1; value used: `mean_reward` = 94.93 reward (headline claim)

### What did we measure?
- Naive median 195.5 over 5 runs; repeats: 196.8, 172.9, 195.5, 179.8, 196.2
- Spread: range 172.9 to 196.8, noise band ±2.65 (2 x MAD), CV 5.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +105.9% (noise band ±2.8% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=100` (36.29 noise units, gap +4.6%); `lr=0.002` (34.79 noise units, gap -8.8%); `lr=0.02` (33.77 noise units, gap +11.7%); `lr=1` (31.55 noise units, gap +17.9%); `lr=0.01` (28.52 noise units, gap -26.3%) (and 20 more in the JSON)
- Near alternatives (closest across all claims):
  - `max_steps=100`: this claim +4.8%, mean |gap| 27.5% (6 runs)
  - `lr_schedule=inv`: this claim +32.4%, mean |gap| 39.4% (6 runs)
  - `lr=1`: this claim +1.7%, mean |gap| 40.2% (6 runs)

### History matching (every measured configuration, all claims together)
- 34 of 84 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.47); lr_schedule=inv, max_steps=100 (max I 0.66)
  - `eps_start, lr, lr_schedule, max_steps`: eps_start=0.2, lr=1, lr_schedule=inv, max_steps=100 (max I 0.52)
  - `eps_start, lr`: eps_start=0.1, lr=1 (max I 0.74); eps_start=0.02, lr=1 (max I 0.77)
  - `lr, max_steps`: lr=1, max_steps=400 (max I 0.75); lr=1, max_steps=1000 (max I 0.75); lr=1, max_steps=10000 (max I 0.78)
  - `lr, lr_schedule`: lr=0.02, lr_schedule=linear (max I 0.79)
  - `eps_start, lr_schedule`: eps_start=0.5, lr_schedule=linear (max I 0.81)
- 3 separate islands (no single-knob move joins them): lr_schedule=linear, max_steps=100; lr_schedule=inv, max_steps=100; eps_start=0.1, lr=1 | eps_start=0.5, lr_schedule=linear; eps_start=0.5, lr_schedule=inv | eps_start=0.2, lr=1, lr_schedule=inv, max_steps=100

Notes:
- stopped early: run budget of 200 reached (wanted 1 more run(s) of {'eps_start': '0.2', 'max_steps': '400'} for 'combine')
- closest configuration not verified: {'lr': '1', 'eps_start': '0.02'} (gap -0.6%, 1 of 5 confirmation runs); the budget ran out first, so no attribution is made
- history matching: 34 of 84 tested configurations fit every claim within 3 sigma

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 6 | +4.8% | +50.2% | 27.5% |
| `lr_schedule=inv` | 6 | +32.4% | -46.5% | 39.4% |
| `lr=1` | 6 | +1.7% | -78.7% | 40.2% |
| `lr=0.5` | 6 | +13.7% | -68.7% | 41.2% |
| `lr=0.05` | 6 | +28.6% | -59.4% | 44.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
