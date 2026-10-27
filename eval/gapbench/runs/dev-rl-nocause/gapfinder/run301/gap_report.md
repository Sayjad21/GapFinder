# Gap Report: dev-rl-nocause

Artifact `rlbench` · generated 2026-10-14 21:40 · 125 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +54.1% | -9.3% | ±13.8% | `theta_bins=1` |

## C1: mean_reward (paper 118.924)
**Fits but unsupported** · gap +54.1% → -9.3% · 54 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0008`, `B0033`, `B0034`, `B0035` (4 run(s) of the same config)
- Config: `theta_bins` naive `6`, changed to `1`
- Command:

  Replay: fork checkpoint `db39090c-d148-46a8-832f-bca8babc4e4a` and run
  ```
  RUN_TAG=95822c5fd512 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 1 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 66.98, 116.6, 99.2, 116.9; gap after -9.3%; result checkpoint `d92cda3c-b680-43ef-97f7-8b2733eff6fe`
- Effect: candidate 107.9 minus naive 183.2 = -75.31, 95% bootstrap interval [-91.4, -61.41] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner is stable across seeds on CartPole: its worst seed still balances for 69.1 steps on average.

- p. 1; value used: `mean_reward` = 118.924 steps (headline claim)

### What did we measure?
- Naive median 183.2 over 5 runs; repeats: 175, 183, 183.2, 194.8, 196
- Spread: range 175 to 196, noise band ±16.36 (2 x MAD), CV 4.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +54.1% (noise band ±13.8% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `theta_bins` the gap is +54.1% (it comes back)
- PASS · Held-out claim: C2: +53.6% to -77.1% (not worse beyond noise)
- FAIL · Evidence: `theta_bins=1`: no evidence mentions '1'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -75.31 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `theta_bins=30` (3.37 noise units, gap -7.7%); `lr_schedule=inv` (2.77 noise units, gap +15.9%); `theta_bins=12` (1.89 noise units, gap +28.1%); `theta_bins=3` (1.38 noise units, gap +35.1%); `theta_bins=8` (1.26 noise units, gap +36.7%) (and 2 more in the JSON)
- Near alternatives (closest across all claims):
  - `eps_end=0.005`, `lr_schedule=inv`: this claim +20.8%, mean |gap| 20.7% (3 runs)
  - `theta_bins=12`, `lr_schedule=linear`: this claim +2.7%, mean |gap| 20.8% (3 runs)
  - `theta_bins=12`: this claim +37.7%, mean |gap| 21.4% (4 runs)

### History matching (every measured configuration, all claims together)
- 8 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 8 configurations
  - `lr_schedule, theta_bins`: lr_schedule=linear, theta_bins=12 (max I 0.75); lr_schedule=inv, theta_bins=8 (max I 1.08); lr_schedule=inv, theta_bins=12 (max I 2.18)
  - `theta_bins`: theta_bins=30 (max I 1.88); theta_bins=1 (max I 2.23)
  - `lr_schedule`: lr_schedule=inv (max I 2.39)
  - `eps_end, lr_schedule`: eps_end=0.005, lr_schedule=inv (max I 2.82)
  - `eps_end, theta_bins`: eps_end=0.005, theta_bins=30 (max I 2.83)
- 2 separate islands (no single-knob move joins them): lr_schedule=linear, theta_bins=12; lr_schedule=inv, theta_bins=8; lr_schedule=inv, theta_bins=12 | theta_bins=30; theta_bins=1; eps_end=0.005, theta_bins=30
- Equally good values: `theta_bins` in {1, 30}

Notes:
- equally good values within one noise band (measured): theta_bins in {1, 30}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `eps_end=0.005`, `lr_schedule=inv` | 3 | +20.8% | -20.6% | 20.7% |
| `theta_bins=12`, `lr_schedule=linear` | 3 | +2.7% | -38.8% | 20.8% |
| `theta_bins=12` | 4 | +37.7% | -5.0% | 21.4% |
| `theta_bins=3` | 4 | +47.8% | -9.9% | 28.8% |
| `theta_bins=8`, `lr_schedule=inv` | 3 | -2.5% | -59.2% | 30.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `634d827f07d6659ff82f6ea0924c8ba487e9d02a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
