# Gap Report: test-gen-02

Artifact `rlbench` · generated 2026-10-10 22:52 · 15 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Unexplained | +215.8% | +215.8% | ±20.4% | — |

## C1: mean_reward (paper 59.35)
**Unexplained** · gap +215.8% → +215.8% · 2 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (2 hypotheses tested).

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 59.4 on CartPole; the worst of its seeds reaches 9.8.

- p. 1; value used: `mean_reward` = 59.35 reward (headline claim)

### What did we measure?
- Naive median 187.4 over 5 runs; repeats: 181.9, 193.5, 193.6, 169.5, 187.4
- Spread: range 169.5 to 193.6, noise band ±12.13 (2 x MAD), CV 5.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +215.8% (noise band ±20.4% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `discretise.theta_bounds`, `discretise.omega_bounds`, `done.x_threshold`, `done.theta_threshold`, `step.reward`, `RL_SEED_BASE`, `RUN_TAG`, `eps_start`, `python_random_module`, `os_scheduling`, `hardware_cpu`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (4.69 noise units, gap +119.8%); `lr_schedule=linear` (1.68 noise units, gap +181.4%)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`: this claim +119.8%, mean |gap| 185.6% (5 runs)
  - `lr_schedule=linear`: this claim +176.6%, mean |gap| 697.5% (5 runs)

Notes:
- closest configuration tried: {'lr_schedule': 'inv'} (gap +119.8%); it did not pass verification

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv` | 5 | +119.8% | +251.3% | 185.6% |
| `lr_schedule=linear` | 5 | +176.6% | +1218.3% | 697.5% |
| naive (reproduction as run) | 5 | +215.8% | +1265.5% | 740.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `discretise.theta_bounds`, `discretise.omega_bounds`, `done.x_threshold`, `done.theta_threshold`, `step.reward`, `RL_SEED_BASE`, `RUN_TAG`, `eps_start`, `python_random_module`, `os_scheduling`, `hardware_cpu`

## Provenance
- GapFinder commit: `fb04d3a1ab0b0fec0acc5b342103e9444806727c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `16ad3c4a71eefac5fc45f4c9a201b3fc6f51a0c3cef30e8c3ea67682f56fab21`
- Cost: Nemotron billed $0.0438, sandbox reported $0.0000 (total $0.0438; this search; ledger extraction is included only if it shared the search's router)
