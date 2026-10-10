# Gap Report: test-gen-05

Artifact `rlbench` · generated 2026-10-10 23:20 · 26 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Unexplained | +929.7% | +929.7% | ±121.7% | — |

## C1: mean_reward (paper 17.31)
**Unexplained** · gap +929.7% → +929.7% · 5 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (5 hypotheses tested).

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 17.3 steps, and that its worst seed still balances for 9.1.

- p. 1; value used: `mean_reward` = 17.31 steps (headline claim)

### What did we measure?
- Naive median 178.2 over 5 runs; repeats: 171.3, 197.7, 167.7, 178.2, 193.1
- Spread: range 167.7 to 197.7, noise band ±21.07 (2 x MAD), CV 7.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +929.7% (noise band ±121.7% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `discretise.theta_min`, `discretise.theta_max`, `discretise.omega_min`, `discretise.omega_max`, `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `init_state_range`, `x_threshold`, `theta_threshold`, `python_version`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (2.7 noise units, gap +600.9%); `eps_start=0.5` (2.14 noise units, gap +669.4%); `lr_schedule=linear` (1.55 noise units, gap +740.9%)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`, `eps_start=0.5`: this claim +484.1%, mean |gap| 247.6% (5 runs)
  - `lr_schedule=inv`: this claim +632.1%, mean |gap| 473.8% (5 runs)
  - `eps_start=0.5`: this claim +745.2%, mean |gap| 478.4% (5 runs)

Notes:
- closest configuration tried: {'lr_schedule': 'inv', 'eps_start': '0.5'} (gap +484.1%); it did not pass verification

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv`, `eps_start=0.5` | 5 | +484.1% | +11.0% | 247.6% |
| `lr_schedule=inv` | 5 | +632.1% | +315.4% | 473.8% |
| `eps_start=0.5` | 5 | +745.2% | +211.5% | 478.4% |
| naive (reproduction as run) | 5 | +929.7% | +1051.1% | 990.4% |
| `lr_schedule=linear` | 5 | +862.8% | +1430.2% | 1146.5% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `discretise.theta_min`, `discretise.theta_max`, `discretise.omega_min`, `discretise.omega_max`, `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `init_state_range`, `x_threshold`, `theta_threshold`, `python_version`

## Provenance
- GapFinder commit: `fb04d3a1ab0b0fec0acc5b342103e9444806727c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `3ed579043c7744915af32f075a3f319861ab223a18631caf42c5504685066d93`
- Cost: Nemotron billed $0.0554, sandbox reported $0.0000 (total $0.0554; this search; ledger extraction is included only if it shared the search's router)
