# Gap Report: dev-rl-nocause

Artifact `rlbench` · generated 2026-10-14 22:24 · 164 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +40.7% | -4.0% | ±4.6% | `theta_bins=30`, `eps_end=0.1` |

## C1: mean_reward (paper 118.924)
**Fits but unsupported** · gap +40.7% → -4.0% · 53 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0078`, `B0109`, `B0110`, `B0111`, `B0112` (5 run(s) of the same config)
- Config: `theta_bins` naive `6`, changed to `30`
- Config: `eps_end` naive `0.05`, changed to `0.1`
- Command:

  Replay: fork checkpoint `949b2cce-1cf2-4924-80fb-d18521b2d512` and run
  ```
  RUN_TAG=503fbc05039b "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.1 --eps_decay 0.99 --theta_bins 30 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 140.5, 149.1, 66.16, 114.1, 97.83; gap after -4.0%; result checkpoint `7957257a-53a0-4fa3-955e-7e290c4e8cfa`
- Effect: candidate 114.1 minus naive 167.4 = -53.24, 95% bootstrap interval [-90.7, -15.21] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner is stable across seeds on CartPole: its worst seed still balances for 69.1 steps on average.

- p. 1; value used: `mean_reward` = 118.924 steps (headline claim)

### What did we measure?
- Naive median 167.4 over 5 runs; repeats: 167.4, 142.7, 164.6, 169.1, 183.1
- Spread: range 142.7 to 183.1, noise band ±5.46 (2 x MAD), CV 8.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +40.7% (noise band ±4.6% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `theta_bins` the gap is +52.4% (it comes back)
- PASS · Counterfactual (reversal test): without `eps_end` the gap is -17.8% (it comes back)
- PASS · Held-out claim: C2: -71.5% to -80.5% (not worse beyond noise)
- FAIL · Evidence: `theta_bins=30`: no evidence mentions '30'; it fits, but nothing says the authors used it
- FAIL · Evidence: `eps_end=0.1`: no evidence mentions '0.1'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -53.24 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (3.49 noise units, gap +24.7%)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`, `eps_end=0.005`: this claim +16.5%, mean |gap| 27.2% (5 runs)
  - `theta_bins=3`: this claim +52.0%, mean |gap| 28.6% (6 runs)
  - `theta_bins=8`: this claim +49.9%, mean |gap| 28.9% (6 runs)

### Equally good configurations
The target claim can't tell these 5 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `eps_end=0.1, theta_bins=30` (reported)
- `eps_end=0.1, theta_bins=3`
- `eps_end=0.001, lr_schedule=inv`
- `eps_end=0.1, lr_schedule=inv`
- `eps_end=0.005, lr_schedule=inv`

### History matching (every measured configuration, all claims together)
- 13 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `eps_end, lr_schedule`: eps_end=0.001, lr_schedule=inv (max I 1.06); eps_end=0.1, lr_schedule=inv (max I 1.4); eps_end=0.005, lr_schedule=inv (max I 1.44)
  - `eps_end, theta_bins`: eps_end=0.1, theta_bins=30 (max I 1.56); eps_end=0.1, theta_bins=3 (max I 1.59); eps_end=0.1, theta_bins=12 (max I 2.56)
  - `lr_schedule`: lr_schedule=inv (max I 1.89)
  - `theta_bins`: theta_bins=30 (max I 1.9)
  - `lr_schedule, theta_bins`: lr_schedule=inv, theta_bins=12 (max I 2.46); lr_schedule=linear, theta_bins=12 (max I 2.53)
- 2 separate islands (no single-knob move joins them): eps_end=0.001, lr_schedule=inv; eps_end=0.1, lr_schedule=inv; eps_end=0.005, lr_schedule=inv | eps_end=0.1, theta_bins=30; eps_end=0.1, theta_bins=3; theta_bins=30

Notes:
- configurations the target claim can't tell apart from the answer: eps_end=0.1, theta_bins=30; eps_end=0.1, theta_bins=3; eps_end=0.001, lr_schedule=inv; eps_end=0.1, lr_schedule=inv; eps_end=0.005, lr_schedule=inv

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv`, `eps_end=0.005` | 5 | +16.5% | -37.8% | 27.2% |
| `theta_bins=3` | 6 | +52.0% | +5.3% | 28.6% |
| `theta_bins=8` | 6 | +49.9% | +7.9% | 28.9% |
| `lr_schedule=inv` | 6 | +18.4% | -41.4% | 29.9% |
| `lr_schedule=inv`, `theta_bins=4` | 5 | +21.7% | -38.9% | 30.3% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `e0f13d101585ad1609a15fbf67b70128f4cfffc8` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
