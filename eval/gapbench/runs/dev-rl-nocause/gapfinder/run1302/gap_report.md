# Gap Report: dev-rl-nocause

Artifact `rlbench` · generated 2026-10-15 01:02 · 136 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Unexplained | +50.3% | +50.3% | ±23.7% | — |

## C1: mean_reward (paper 118.924)
**Unexplained** · gap +50.3% → +50.3% · 53 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (53 hypotheses tested).

### What did the paper report?
> We show that a small tabular Q-learner is stable across seeds on CartPole: its worst seed still balances for 69.1 steps on average.

- p. 1; value used: `mean_reward` = 118.924 steps (headline claim)

### What did we measure?
- Naive median 178.8 over 5 runs; repeats: 200, 190.9, 164.7, 162.1, 178.8
- Spread: range 162.1 to 200, noise band ±28.16 (2 x MAD), CV 9.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +50.3% (noise band ±23.7% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (2.04 noise units, gap -2.1%); `theta_bins=30` (1.52 noise units, gap -14.2%)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`, `theta_bins=8`: this claim +9.7%, mean |gap| 11.8% (5 runs)
  - `lr_schedule=inv`, `eps_end=0.525`: this claim +22.7%, mean |gap| 19.0% (5 runs)
  - `lr_schedule=inv`: this claim +16.9%, mean |gap| 29.3% (6 runs)

### History matching (every measured configuration, all claims together)
- 26 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr_schedule, theta_bins`: lr_schedule=inv, theta_bins=8 (max I 0.66)
  - `eps_end, theta_bins`: eps_end=0.81, theta_bins=1 (max I 1.19); eps_end=0.1, theta_bins=30 (max I 1.6); eps_end=0.525, theta_bins=3 (max I 1.78); eps_end=0.525, theta_bins=1 (max I 1.79); +1 more
  - `eps_end, lr_schedule`: eps_end=0.1, lr_schedule=inv (max I 1.48)
  - `lr_schedule`: lr_schedule=inv (max I 1.51)
  - `theta_bins`: theta_bins=30 (max I 1.71)
  - `eps_end`: eps_end=0.1 (max I 1.77)

Notes:
- {'lr_schedule': 'inv'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'lr_schedule': 'inv'} (gap +16.9%); it did not pass verification
- history matching: 26 of 53 tested configurations fit every claim within 3 sigma

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv`, `theta_bins=8` | 5 | +9.7% | -13.8% | 11.8% |
| `lr_schedule=inv`, `eps_end=0.525` | 5 | +22.7% | +15.2% | 19.0% |
| `lr_schedule=inv` | 6 | +16.9% | -41.8% | 29.3% |
| `theta_bins=8`, `lr_schedule=linear` | 5 | +28.9% | -34.7% | 31.8% |
| `lr_schedule=inv`, `eps_end=0.1` | 5 | +14.2% | -53.9% | 34.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
