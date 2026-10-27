# Gap Report: dev-rl-nocause

Artifact `rlbench` · generated 2026-10-15 20:52 · 147 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Unexplained | +42.9% | +42.9% | ±5.4% | — |

## C1: mean_reward (paper 118.924)
**Unexplained** · gap +42.9% → +42.9% · 53 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (53 hypotheses tested).

### What did the paper report?
> We show that a small tabular Q-learner is stable across seeds on CartPole: its worst seed still balances for 69.1 steps on average.

- p. 1; value used: `mean_reward` = 118.924 steps (headline claim)

### What did we measure?
- Naive median 169.9 over 5 runs; repeats: 168.4, 178.7, 166.7, 191.3, 169.9
- Spread: range 166.7 to 191.3, noise band ±6.45 (2 x MAD), CV 5.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +42.9% (noise band ±5.4% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (5.56 noise units, gap +12.7%); `theta_bins=4` (4.79 noise units, gap +16.9%)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`: this claim +8.4%, mean |gap| 23.4% (6 runs)
  - `lr_schedule=linear`, `eps_end=0.001`: this claim +33.6%, mean |gap| 25.8% (2 runs)
  - `theta_bins=3`: this claim +49.8%, mean |gap| 27.2% (6 runs)

### History matching (every measured configuration, all claims together)
- 8 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 8 configurations
  - `eps_end, theta_bins`: eps_end=0.001, theta_bins=1 (max I 1.63); eps_end=0.001, theta_bins=30 (max I 1.68); eps_end=0.81, theta_bins=1 (max I 1.97); eps_end=0.905, theta_bins=1 (max I 2.9)
  - `lr_schedule`: lr_schedule=inv (max I 1.81)
  - `theta_bins`: theta_bins=30 (max I 2.12)
  - `lr_schedule, theta_bins`: lr_schedule=inv, theta_bins=4 (max I 2.25)
  - `eps_end, lr_schedule`: eps_end=0.001, lr_schedule=inv (max I 2.55)
- 2 separate islands (no single-knob move joins them): eps_end=0.001, theta_bins=1; eps_end=0.001, theta_bins=30; eps_end=0.81, theta_bins=1 | lr_schedule=inv; lr_schedule=inv, theta_bins=4; eps_end=0.001, lr_schedule=inv

Notes:
- {'lr_schedule': 'inv'} closes this claim but makes held-out claims worse; rejected
- closest configuration tried: {'lr_schedule': 'inv'} (gap +8.4%); it did not pass verification
- history matching: 8 of 53 tested configurations fit every claim within 3 sigma

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv` | 6 | +8.4% | -38.4% | 23.4% |
| `lr_schedule=linear`, `eps_end=0.001` | 2 | +33.6% | +17.9% | 25.8% |
| `theta_bins=3` | 6 | +49.8% | -4.6% | 27.2% |
| `theta_bins=4`, `lr_schedule=inv` | 5 | +11.8% | -47.9% | 29.8% |
| `theta_bins=4` | 6 | +55.3% | +9.1% | 32.2% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `cd8c8af2b9d079dd9a57443ed501c0dd8a467d34` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
