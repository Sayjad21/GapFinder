# Gap Report: dev-rl-nocause

Artifact `rlbench` · generated 2026-10-15 20:52 · 199 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Unexplained | +51.2% | +51.2% | ±6.2% | — |

## C1: mean_reward (paper 118.924)
**Unexplained** · gap +51.2% → +51.2% · 70 hypotheses tested

### Which experiment changed it?
- None: no tested change moved the gap (70 hypotheses tested).

### What did the paper report?
> We show that a small tabular Q-learner is stable across seeds on CartPole: its worst seed still balances for 69.1 steps on average.

- p. 1; value used: `mean_reward` = 118.924 steps (headline claim)

### What did we measure?
- Naive median 179.8 over 5 runs; repeats: 182.8, 179.8, 176.1, 156.7, 198.4
- Spread: range 156.7 to 198.4, noise band ±7.35 (2 x MAD), CV 8.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +51.2% (noise band ±6.2% of the paper value)

### Why do we believe it?
- nothing to verify: no explanation was proposed

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `theta_bins=1` (3.5 noise units, gap -29.6%); `lr_schedule=inv` (1.76 noise units, gap +40.3%); `lr_schedule=linear` (1.73 noise units, gap +40.5%); `eps_end=0.1` (1.1 noise units, gap +44.4%)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`, `eps_end=0.025`: this claim +23.4%, mean |gap| 13.6% (5 runs)
  - `eps_end=0.0`, `lr_schedule=inv`: this claim +26.2%, mean |gap| 16.9% (2 runs)
  - `eps_end=0.525`, `lr_schedule=inv`: this claim +28.0%, mean |gap| 20.3% (5 runs)

### History matching (every measured configuration, all claims together)
- 27 of 70 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `eps_end, lr_schedule`: eps_end=0.1, lr_schedule=inv (max I 0.89); eps_end=0.001, lr_schedule=inv (max I 0.9)
  - `eps_end, theta_bins`: eps_end=0.1, theta_bins=30 (max I 1.23); eps_end=0.81, theta_bins=1 (max I 1.54); eps_end=0.0, theta_bins=1 (max I 1.54); eps_end=0.025, theta_bins=1 (max I 1.55); +1 more
  - `lr_schedule, theta_bins`: lr_schedule=inv, theta_bins=8 (max I 1.29); lr_schedule=linear, theta_bins=8 (max I 1.51); lr_schedule=inv, theta_bins=12 (max I 1.57)
- 2 separate islands (no single-knob move joins them): eps_end=0.1, lr_schedule=inv; eps_end=0.001, lr_schedule=inv; lr_schedule=inv, theta_bins=8 | eps_end=0.1, theta_bins=30; eps_end=0.81, theta_bins=1; eps_end=0.0, theta_bins=1

Notes:
- stopped early: run budget of 200 reached (wanted 3 more run(s) of {'theta_bins': '8', 'lr_schedule': 'linear'} for 'confirm-combo')
- {'theta_bins': '30', 'eps_end': '0.1'} (gap -12.7%) was verified from existing runs and rejected: {'theta_bins': '30', 'eps_end': '0.1'} closes this claim but makes held-out claims worse; rejected
- {'theta_bins': '1', 'eps_end': '0.025'} (gap -2.0%) was verified from existing runs and rejected: {'theta_bins': '1', 'eps_end': '0.025'} closes this claim but makes held-out claims worse; rejected
- {'theta_bins': '8', 'lr_schedule': 'inv'} (gap -6.5%) was verified from existing runs and rejected: {'theta_bins': '8', 'lr_schedule': 'inv'} closes this claim but makes held-out claims worse; rejected
- closest configuration not verified: {'lr_schedule': 'linear', 'theta_bins': '8'} (gap +17.9%, 2 of 5 confirmation runs); the budget ran out first, so no attribution is made
- history matching: 27 of 70 tested configurations fit every claim within 3 sigma

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv`, `eps_end=0.025` | 5 | +23.4% | -3.7% | 13.6% |
| `eps_end=0.0`, `lr_schedule=inv` | 2 | +26.2% | +7.6% | 16.9% |
| `eps_end=0.525`, `lr_schedule=inv` | 5 | +28.0% | +12.7% | 20.3% |
| `eps_end=0.1`, `lr_schedule=inv` | 5 | +5.0% | -40.9% | 22.9% |
| `eps_end=0.01`, `lr_schedule=inv` | 5 | +18.8% | -27.1% | 23.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `cd8c8af2b9d079dd9a57443ed501c0dd8a467d34` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
