# Gap Report: dev-rl-nocause

Artifact `rlbench` · generated 2026-10-15 00:43 · 111 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Unexplained | +40.6% | +40.6% | ±29.7% | — |

## C1: mean_reward (paper 118.924)
**Unexplained** · gap +40.6% → +40.6% · 53 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (53 hypotheses tested).

### What did the paper report?
> We show that a small tabular Q-learner is stable across seeds on CartPole: its worst seed still balances for 69.1 steps on average.

- p. 1; value used: `mean_reward` = 118.924 steps (headline claim)

### What did we measure?
- Naive median 167.2 over 5 runs; repeats: 192.7, 196.4, 167.2, 154.6, 149.6
- Spread: range 149.6 to 196.4, noise band ±35.33 (2 x MAD), CV 12.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +40.6% (noise band ±29.7% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives (closest across all claims):
  - `eps_end=0.001`, `lr_schedule=inv`: this claim +13.5%, mean |gap| 32.7% (5 runs)
  - `eps_end=0.005`, `theta_bins=30`: this claim -0.8%, mean |gap| 39.4% (5 runs)
  - `theta_bins=8`: this claim +44.5%, mean |gap| 39.8% (6 runs)

### History matching (every measured configuration, all claims together)
- 41 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr_schedule, theta_bins`: lr_schedule=linear, theta_bins=12 (max I 0.58); lr_schedule=inv, theta_bins=12 (max I 1.07)
  - `eps_end, theta_bins`: eps_end=0.981, theta_bins=1 (max I 0.59); eps_end=0.001, theta_bins=1 (max I 0.81); eps_end=0.005, theta_bins=30 (max I 0.95); eps_end=0.005, theta_bins=1 (max I 1.13); +2 more
  - `eps_end, lr_schedule`: eps_end=0.1, lr_schedule=inv (max I 0.99); eps_end=0.005, lr_schedule=linear (max I 1.2)

Notes:
- closest configuration tried: {'theta_bins': '30'} (gap -18.9%); it did not pass verification
- history matching: 41 of 53 tested configurations fit every claim within 3 sigma

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `eps_end=0.001`, `lr_schedule=inv` | 5 | +13.5% | -52.0% | 32.7% |
| naive (reproduction as run) | 5 | +40.6% | -26.1% | 33.3% |
| `eps_end=0.005`, `theta_bins=30` | 5 | -0.8% | -78.0% | 39.4% |
| `theta_bins=8` | 6 | +44.5% | +35.0% | 39.8% |
| `theta_bins=12` | 6 | +53.0% | +36.6% | 44.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
