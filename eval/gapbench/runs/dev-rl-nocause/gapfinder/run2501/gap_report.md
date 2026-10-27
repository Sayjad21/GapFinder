# Gap Report: dev-rl-nocause

Artifact `rlbench` · generated 2026-10-16 01:41 · 127 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Unexplained | +51.1% | +51.1% | ±5.1% | — |

## C1: mean_reward (paper 118.924)
**Unexplained** · gap +51.1% → +51.1% · 53 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (53 hypotheses tested).

### What did the paper report?
> We show that a small tabular Q-learner is stable across seeds on CartPole: its worst seed still balances for 69.1 steps on average.

- p. 1; value used: `mean_reward` = 118.924 steps (headline claim)

### What did we measure?
- Naive median 179.6 over 5 runs; repeats: 176.6, 190.6, 168.4, 179.9, 179.6
- Spread: range 168.4 to 190.6, noise band ±6.05 (2 x MAD), CV 4.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +51.1% (noise band ±5.1% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `theta_bins=1` (9.82 noise units, gap -1.1%); `theta_bins=30` (8.93 noise units, gap -5.6%); `lr_schedule=inv` (6.31 noise units, gap +19.0%); `lr_schedule=linear` (3.87 noise units, gap +31.4%); `theta_bins=4` (2.57 noise units, gap +38.0%) (and 3 more in the JSON)
- Near alternatives (closest across all claims):
  - `eps_end=0.025`, `lr_schedule=inv`: this claim +11.0%, mean |gap| 13.9% (3 runs)
  - `lr_schedule=inv`, `eps_end=0.01`: this claim +8.1%, mean |gap| 21.1% (3 runs)
  - `lr_schedule=inv`, `theta_bins=4`: this claim +22.0%, mean |gap| 34.3% (3 runs)

### History matching (every measured configuration, all claims together)
- 10 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `eps_end, lr_schedule`: eps_end=0.01, lr_schedule=inv (max I 1.24); eps_end=0.025, lr_schedule=inv (max I 1.37)
  - `eps_end, theta_bins`: eps_end=0.81, theta_bins=1 (max I 1.81); eps_end=0.025, theta_bins=1 (max I 1.83); eps_end=0.01, theta_bins=1 (max I 2.3); eps_end=0.025, theta_bins=30 (max I 2.63); +1 more
  - `lr_schedule`: lr_schedule=inv (max I 1.95)
  - `theta_bins`: theta_bins=30 (max I 2.08)
  - `lr_schedule, theta_bins`: lr_schedule=inv, theta_bins=4 (max I 2.92)
- 2 separate islands (no single-knob move joins them): eps_end=0.81, theta_bins=1; eps_end=0.025, theta_bins=1; theta_bins=30 | eps_end=0.01, lr_schedule=inv; eps_end=0.025, lr_schedule=inv; lr_schedule=inv

Notes:
- {'theta_bins': '30'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'theta_bins': '30'} (gap -3.5%); it did not pass verification
- history matching: 10 of 53 tested configurations fit every claim within 3 sigma

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `eps_end=0.025`, `lr_schedule=inv` | 3 | +11.0% | -16.8% | 13.9% |
| `lr_schedule=inv`, `eps_end=0.01` | 3 | +8.1% | -34.1% | 21.1% |
| naive (reproduction as run) | 5 | +51.1% | -7.0% | 29.0% |
| `lr_schedule=inv`, `theta_bins=4` | 3 | +22.0% | -46.7% | 34.3% |
| `theta_bins=12` | 4 | +50.9% | -19.0% | 34.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
