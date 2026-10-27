# Gap Report: dev-rl-nocause

Artifact `rlbench` · generated 2026-10-15 00:15 · 198 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Unexplained | +49.5% | +49.5% | ±6.6% | — |

## C1: mean_reward (paper 118.924)
**Unexplained** · gap +49.5% → +49.5% · 65 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (65 hypotheses tested).

### What did the paper report?
> We show that a small tabular Q-learner is stable across seeds on CartPole: its worst seed still balances for 69.1 steps on average.

- p. 1; value used: `mean_reward` = 118.924 steps (headline claim)

### What did we measure?
- Naive median 177.8 over 5 runs; repeats: 181.7, 177.8, 183.9, 175.6, 148.6
- Spread: range 148.6 to 183.9, noise band ±7.88 (2 x MAD), CV 8.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +49.5% (noise band ±6.6% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (6.56 noise units, gap +6.1%); `theta_bins=1` (5.09 noise units, gap -15.8%); `theta_bins=30` (3.54 noise units, gap -26.0%); `eps_end=0.81` (2.24 noise units, gap +34.7%); `eps_end=0.1` (2.15 noise units, gap +35.2%)
- Near alternatives (closest across all claims):
  - `eps_end=0.1`, `lr_schedule=inv`: this claim +23.1%, mean |gap| 15.7% (5 runs)
  - `eps_end=0.1`: this claim +49.5%, mean |gap| 24.8% (6 runs)
  - `eps_end=0.525`, `lr_schedule=inv`: this claim +28.9%, mean |gap| 28.0% (5 runs)

### History matching (every measured configuration, all claims together)
- 17 of 65 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `eps_end, lr_schedule`: eps_end=0.1, lr_schedule=inv (max I 2.1)
  - `lr_schedule`: lr_schedule=inv (max I 2.33)
  - `eps_end, theta_bins`: eps_end=0.525, theta_bins=3 (max I 2.51); eps_end=0.025, theta_bins=30 (max I 2.74); eps_end=0.905, theta_bins=30 (max I 2.75); eps_end=0.01, theta_bins=30 (max I 2.75); +4 more
- 3 separate islands (no single-knob move joins them): eps_end=0.025, theta_bins=30; eps_end=0.905, theta_bins=30; eps_end=0.01, theta_bins=30 | eps_end=0.1, lr_schedule=inv; lr_schedule=inv; eps_end=0.525, lr_schedule=inv | eps_end=0.525, theta_bins=3; eps_end=0.981, theta_bins=3

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'theta_bins': '3', 'eps_end': '0.525'} for 'confirm-combo')
- closest configuration not verified: {'theta_bins': '1', 'eps_end': '0.005'} (gap -2.2%, 1 of 5 confirmation runs); the budget ran out first, so no attribution is made
- history matching: 17 of 65 tested configurations fit every claim within 3 sigma

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `eps_end=0.1`, `lr_schedule=inv` | 5 | +23.1% | +8.4% | 15.7% |
| `eps_end=0.1` | 6 | +49.5% | +0.1% | 24.8% |
| naive (reproduction as run) | 5 | +49.5% | -1.9% | 25.7% |
| `eps_end=0.525`, `lr_schedule=inv` | 5 | +28.9% | -27.0% | 28.0% |
| `lr_schedule=inv` | 6 | +18.0% | -47.1% | 32.5% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
