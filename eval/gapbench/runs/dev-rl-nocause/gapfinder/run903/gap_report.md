# Gap Report: dev-rl-nocause

Artifact `rlbench` · generated 2026-10-14 23:40 · 197 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Unexplained | +61.5% | +61.5% | ±6.2% | — |

## C1: mean_reward (paper 118.924)
**Unexplained** · gap +61.5% → +61.5% · 53 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (53 hypotheses tested).

### What did the paper report?
> We show that a small tabular Q-learner is stable across seeds on CartPole: its worst seed still balances for 69.1 steps on average.

- p. 1; value used: `mean_reward` = 118.924 steps (headline claim)

### What did we measure?
- Naive median 192 over 5 runs; repeats: 192.6, 188.3, 192, 196.4, 165.4
- Spread: range 165.4 to 196.4, noise band ±7.39 (2 x MAD), CV 6.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +61.5% (noise band ±6.2% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (8.35 noise units, gap +9.6%); `theta_bins=30` (6.1 noise units, gap -23.6%); `theta_bins=12` (5.26 noise units, gap +28.8%); `theta_bins=1` (2.73 noise units, gap -44.5%); `eps_end=0.81` (2.61 noise units, gap +45.2%) (and 7 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`: this claim +11.7%, mean |gap| 17.3% (6 runs)
  - `lr_schedule=inv`, `eps_end=0.005`: this claim +18.6%, mean |gap| 26.9% (5 runs)
  - `theta_bins=12`, `lr_schedule=linear`: this claim +19.2%, mean |gap| 33.9% (5 runs)

### History matching (every measured configuration, all claims together)
- 11 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `eps_end, theta_bins`: eps_end=0.981, theta_bins=60 (max I 0.51); eps_end=0.81, theta_bins=60 (max I 0.89); eps_end=0.981, theta_bins=1 (max I 0.93); eps_end=0.005, theta_bins=1 (max I 1.3); +2 more
  - `lr_schedule`: lr_schedule=inv (max I 1.12)
  - `eps_end, lr_schedule`: eps_end=0.005, lr_schedule=inv (max I 1.33)
  - `lr_schedule, theta_bins`: lr_schedule=linear, theta_bins=12 (max I 1.91)
  - `theta_bins`: theta_bins=30 (max I 2.03)
- 2 separate islands (no single-knob move joins them): eps_end=0.981, theta_bins=60; eps_end=0.81, theta_bins=60; eps_end=0.981, theta_bins=1 | lr_schedule=inv; eps_end=0.005, lr_schedule=inv; lr_schedule=linear, theta_bins=12

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'lr_schedule': 'linear', 'eps_end': '0.81'} for 'confirm-combo')
- closest configuration not verified: {'eps_end': '0.981', 'theta_bins': '60'} (gap +6.4%, 1 of 5 confirmation runs); the budget ran out first, so no attribution is made
- history matching: 11 of 53 tested configurations fit every claim within 3 sigma

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv` | 6 | +11.7% | -22.8% | 17.3% |
| `lr_schedule=inv`, `eps_end=0.005` | 5 | +18.6% | -35.3% | 26.9% |
| `theta_bins=12`, `lr_schedule=linear` | 5 | +19.2% | -48.6% | 33.9% |
| `eps_end=0.001` | 6 | +53.6% | +14.4% | 34.0% |
| `theta_bins=3` | 6 | +58.0% | +14.9% | 36.5% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `efb2f63a257a40b9982099a274f2e882f272b80c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
