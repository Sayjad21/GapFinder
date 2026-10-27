# Gap Report: dev-rl-nocause

Artifact `rlbench` · generated 2026-10-15 00:43 · 120 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Unexplained | +45.6% | +45.6% | ±8.7% | — |

## C1: mean_reward (paper 118.924)
**Unexplained** · gap +45.6% → +45.6% · 53 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (53 hypotheses tested).

### What did the paper report?
> We show that a small tabular Q-learner is stable across seeds on CartPole: its worst seed still balances for 69.1 steps on average.

- p. 1; value used: `mean_reward` = 118.924 steps (headline claim)

### What did we measure?
- Naive median 173.2 over 5 runs; repeats: 168, 173.2, 167.3, 175.4, 181.1
- Spread: range 167.3 to 181.1, noise band ±10.32 (2 x MAD), CV 3.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +45.6% (noise band ±8.7% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `theta_bins=30` (4.1 noise units, gap -10.0%); `lr_schedule=inv` (3.95 noise units, gap +11.3%); `theta_bins=1` (1.69 noise units, gap -31.0%)
- Near alternatives (closest across all claims):
  - `theta_bins=8`, `lr_schedule=inv`: this claim +2.0%, mean |gap| 15.4% (3 runs)
  - `eps_end=0.905`, `theta_bins=60`: this claim +12.1%, mean |gap| 20.6% (3 runs)
  - `lr_schedule=inv`, `eps_end=0.025`: this claim +2.6%, mean |gap| 23.6% (3 runs)

### History matching (every measured configuration, all claims together)
- 5 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 5 configurations
  - `lr_schedule, theta_bins`: lr_schedule=inv, theta_bins=8 (max I 0.66)
  - `eps_end, lr_schedule`: eps_end=0.025, lr_schedule=inv (max I 1.58)
  - `eps_end, theta_bins`: eps_end=0.905, theta_bins=60 (max I 2.1); eps_end=0.1, theta_bins=30 (max I 2.69)
  - `lr_schedule`: lr_schedule=inv (max I 2.56)
- 3 separate islands (no single-knob move joins them): lr_schedule=inv, theta_bins=8; eps_end=0.025, lr_schedule=inv; lr_schedule=inv | eps_end=0.905, theta_bins=60 | eps_end=0.1, theta_bins=30

Notes:
- {'theta_bins': '30'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'theta_bins': '30'} (gap +0.1%); it did not pass verification
- history matching: 5 of 53 tested configurations fit every claim within 3 sigma

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `theta_bins=8`, `lr_schedule=inv` | 3 | +2.0% | -28.7% | 15.4% |
| `eps_end=0.905`, `theta_bins=60` | 3 | +12.1% | +29.0% | 20.6% |
| `lr_schedule=inv`, `eps_end=0.025` | 3 | +2.6% | -44.5% | 23.6% |
| `theta_bins=3` | 4 | +40.8% | -7.5% | 24.1% |
| naive (reproduction as run) | 5 | +45.6% | -4.6% | 25.1% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
