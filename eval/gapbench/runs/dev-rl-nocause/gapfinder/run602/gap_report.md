# Gap Report: dev-rl-nocause

Artifact `rlbench` · generated 2026-10-14 22:24 · 133 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +51.5% | -13.6% | ±8.6% | `theta_bins=30`, `eps_end=0.025` |

## C1: mean_reward (paper 118.924)
**Fits but unsupported** · gap +51.5% → -13.6% · 53 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0072`, `B0108`, `B0109` (3 run(s) of the same config)
- Config: `theta_bins` naive `6`, changed to `30`
- Config: `eps_end` naive `0.05`, changed to `0.025`
- Command:

  Replay: fork checkpoint `ae61f7bf-ae8d-4cbd-b551-5da9eb892d84` and run
  ```
  RUN_TAG=24140484a271 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.025 --eps_decay 0.99 --theta_bins 30 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 113.7, 89.75, 102.8; gap after -13.6%; result checkpoint `e1b060f5-42c9-4034-a127-c3c414990544`
- Effect: candidate 102.8 minus naive 180.2 = -77.38, 95% bootstrap interval [-96.05, -59.51] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner is stable across seeds on CartPole: its worst seed still balances for 69.1 steps on average.

- p. 1; value used: `mean_reward` = 118.924 steps (headline claim)

### What did we measure?
- Naive median 180.2 over 5 runs; repeats: 189.2, 180.2, 185.3, 166.2, 176.8
- Spread: range 166.2 to 189.2, noise band ±10.22 (2 x MAD), CV 4.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +51.5% (noise band ±8.6% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `theta_bins` the gap is +49.6% (it comes back)
- PASS · Counterfactual (reversal test): without `eps_end` the gap is -23.9% (it comes back)
- PASS · Held-out claim: C2: +27.4% to -78.1% (not worse beyond noise)
- FAIL · Evidence: `theta_bins=30`: no evidence mentions '30'; it fits, but nothing says the authors used it
- FAIL · Evidence: `eps_end=0.025`: no evidence mentions '0.025'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -77.38 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (4.29 noise units, gap +14.6%); `theta_bins=1` (3.18 noise units, gap +24.2%); `eps_end=0.981` (1.98 noise units, gap +34.5%); `lr_schedule=linear` (1.55 noise units, gap +38.2%)
- Near alternatives (closest across all claims):
  - `eps_end=0.981`, `theta_bins=60`: this claim +6.2%, mean |gap| 4.7% (3 runs)
  - `eps_end=0.81`, `theta_bins=60`: this claim +8.7%, mean |gap| 11.9% (3 runs)
  - `theta_bins=12`: this claim +44.1%, mean |gap| 22.8% (4 runs)

### Equally good configurations
The target claim can't tell these 9 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `eps_end=0.025, theta_bins=30` (reported)
- `lr_schedule=inv`
- `theta_bins=1`
- `eps_end=0.81, theta_bins=1`
- `eps_end=0.01, theta_bins=30`
- `lr_schedule=inv, theta_bins=4`
- `eps_end=0.981, theta_bins=60`
- `eps_end=0.01, theta_bins=1`
- `eps_end=0.025, lr_schedule=inv`

### History matching (every measured configuration, all claims together)
- 10 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr_schedule, theta_bins`: lr_schedule=inv, theta_bins=4 (max I 0.8)
  - `eps_end, theta_bins`: eps_end=0.01, theta_bins=30 (max I 1.21); eps_end=0.81, theta_bins=60 (max I 1.31); eps_end=0.81, theta_bins=1 (max I 1.35); eps_end=0.981, theta_bins=60 (max I 1.51); +2 more
  - `lr_schedule`: lr_schedule=inv (max I 1.43)
  - `eps_end, lr_schedule`: eps_end=0.025, lr_schedule=inv (max I 1.89)
  - `theta_bins`: theta_bins=1 (max I 2.4)
- 2 separate islands (no single-knob move joins them): eps_end=0.01, theta_bins=30; eps_end=0.81, theta_bins=60; eps_end=0.81, theta_bins=1 | lr_schedule=inv, theta_bins=4; lr_schedule=inv; eps_end=0.025, lr_schedule=inv
- Equally good values: `eps_end` in {0.01, 0.025}

Notes:
- configurations the target claim can't tell apart from the answer: eps_end=0.025, theta_bins=30; lr_schedule=inv; theta_bins=1; eps_end=0.81, theta_bins=1; eps_end=0.01, theta_bins=30; lr_schedule=inv, theta_bins=4; eps_end=0.981, theta_bins=60; eps_end=0.01, theta_bins=1; eps_end=0.025, lr_schedule=inv
- equally good values within one noise band (measured): eps_end in {0.01, 0.025}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `eps_end=0.981`, `theta_bins=60` | 3 | +6.2% | -3.2% | 4.7% |
| `eps_end=0.81`, `theta_bins=60` | 3 | +8.7% | +15.1% | 11.9% |
| `theta_bins=12` | 4 | +44.1% | -1.6% | 22.8% |
| `lr_schedule=inv`, `theta_bins=4` | 3 | +11.4% | -37.1% | 24.3% |
| `lr_schedule=inv`, `eps_end=0.01` | 3 | +31.2% | +19.1% | 25.1% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `e0f13d101585ad1609a15fbf67b70128f4cfffc8` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
