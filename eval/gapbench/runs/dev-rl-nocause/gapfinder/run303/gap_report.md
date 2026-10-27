# Gap Report: dev-rl-nocause

Artifact `rlbench` · generated 2026-10-14 21:41 · 198 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +54.8% | -19.8% | ±4.5% | `theta_bins=30` |

## C1: mean_reward (paper 118.924)
**Fits but unsupported** · gap +54.8% → -19.8% · 53 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0012`, `B0057`, `B0058`, `B0059`, `B0060`, `B0061` (6 run(s) of the same config)
- Config: `theta_bins` naive `6`, changed to `30`
- Command:

  Replay: fork checkpoint `95dbac3e-58ae-47e9-b3aa-5d8b5dd08e46` and run
  ```
  RUN_TAG=6b181e000536 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 30 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 116.6, 61.03, 87.85, 102.9, 107.9, 63.4; gap after -19.8%; result checkpoint `3bd04f00-a3fd-40d6-a625-cf2c76a63c90`
- Effect: candidate 95.38 minus naive 184.1 = -88.69, 95% bootstrap interval [-124.7, -75.62] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner is stable across seeds on CartPole: its worst seed still balances for 69.1 steps on average.

- p. 1; value used: `mean_reward` = 118.924 steps (headline claim)

### What did we measure?
- Naive median 184.1 over 5 runs; repeats: 196.3, 170.4, 186.7, 184.1, 183.7
- Spread: range 170.4 to 196.3, noise band ±5.31 (2 x MAD), CV 5.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +54.8% (noise band ±4.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `theta_bins` the gap is +54.8% (it comes back)
- PASS · Held-out claim: C2: +93.8% to -73.0% (not worse beyond noise)
- FAIL · Evidence: `theta_bins=30`: no evidence mentions '30'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -88.69 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (9.93 noise units, gap +10.4%); `theta_bins=3` (8.55 noise units, gap +16.6%); `eps_end=0.1` (4.13 noise units, gap +36.3%); `eps_end=0.01` (3.5 noise units, gap +39.2%); `lr_schedule=linear` (3.3 noise units, gap +40.0%) (and 5 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`, `eps_end=0.01`: this claim +23.4%, mean |gap| 19.4% (5 runs)
  - `lr_schedule=inv`, `eps_end=0.1`: this claim +13.5%, mean |gap| 30.1% (5 runs)
  - `lr_schedule=inv`: this claim +16.0%, mean |gap| 30.5% (6 runs)

### History matching (every measured configuration, all claims together)
- 9 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 9 configurations
  - `lr_schedule, theta_bins`: lr_schedule=linear, theta_bins=12 (max I 0.35)
  - `eps_end, theta_bins`: eps_end=0.025, theta_bins=30 (max I 1.12); eps_end=0.905, theta_bins=60 (max I 1.47); eps_end=0.1, theta_bins=30 (max I 2.37); eps_end=0.1, theta_bins=3 (max I 2.4)
  - `eps_end, lr_schedule`: eps_end=0.025, lr_schedule=inv (max I 1.23); eps_end=0.1, lr_schedule=inv (max I 1.61); eps_end=0.01, lr_schedule=inv (max I 2.99)
  - `lr_schedule`: lr_schedule=inv (max I 2.37)
- 4 separate islands (no single-knob move joins them): eps_end=0.025, lr_schedule=inv; eps_end=0.1, lr_schedule=inv; lr_schedule=inv | eps_end=0.025, theta_bins=30; eps_end=0.1, theta_bins=30; eps_end=0.1, theta_bins=3 | lr_schedule=linear, theta_bins=12 | eps_end=0.905, theta_bins=60

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'lr_schedule': 'linear', 'eps_end': '0.01'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv`, `eps_end=0.01` | 5 | +23.4% | -15.5% | 19.4% |
| `lr_schedule=inv`, `eps_end=0.1` | 5 | +13.5% | -46.8% | 30.1% |
| `lr_schedule=inv` | 6 | +16.0% | -44.9% | 30.5% |
| `eps_end=0.1` | 6 | +41.3% | -20.8% | 31.0% |
| `theta_bins=30`, `eps_end=0.025` | 5 | -3.7% | -64.7% | 34.2% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `634d827f07d6659ff82f6ea0924c8ba487e9d02a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
