# Gap Report: dev-rl-nocause

Artifact `rlbench` · generated 2026-10-14 22:13 · 132 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +35.9% | +1.2% | ±21.3% | `theta_bins=60`, `eps_end=0.905` |

## C1: mean_reward (paper 118.924)
**Fits but unsupported** · gap +35.9% → +1.2% · 53 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0092`, `B0109`, `B0110`, `B0111`, `B0112` (5 run(s) of the same config)
- Config: `theta_bins` naive `6`, changed to `60`
- Config: `eps_end` naive `0.05`, changed to `0.905`
- Command:

  Replay: fork checkpoint `37c2a83c-0069-41fc-8205-efe5626bbc28` and run
  ```
  RUN_TAG=b136e0aafc08 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.905 --eps_decay 0.99 --theta_bins 60 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 111.2, 134.3, 111.2, 120.4, 123.4; gap after +1.2%; result checkpoint `762e0def-88cc-45e6-8e7e-c0a91a1c31bd`
- Effect: candidate 120.4 minus naive 161.6 = -41.16, 95% bootstrap interval [-67.54, -10.39] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner is stable across seeds on CartPole: its worst seed still balances for 69.1 steps on average.

- p. 1; value used: `mean_reward` = 118.924 steps (headline claim)

### What did we measure?
- Naive median 161.6 over 5 runs; repeats: 174.2, 124.8, 190.1, 161.6, 155.2
- Spread: range 124.8 to 190.1, noise band ±25.3 (2 x MAD), CV 15.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +35.9% (noise band ±21.3% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `theta_bins` the gap is +53.1% (it comes back)
- PASS · Counterfactual (reversal test): without `eps_end` the gap is -68.3% (it comes back)
- PASS · Held-out claim: C2: -73.0% to -16.4% (not worse beyond noise)
- FAIL · Evidence: `theta_bins=60`: no evidence mentions '60'; it fits, but nothing says the authors used it
- FAIL · Evidence: `eps_end=0.905`: no evidence mentions '0.905'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -41.16 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (1.64 noise units, gap -1.0%)
- Near alternatives (closest across all claims):
  - `eps_end=0.981`, `theta_bins=60`: this claim -3.5%, mean |gap| 6.0% (5 runs)
  - `lr_schedule=inv`, `eps_end=0.001`: this claim +28.7%, mean |gap| 22.6% (5 runs)
  - `theta_bins=12`: this claim +38.9%, mean |gap| 25.2% (6 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `eps_end=0.905, theta_bins=60` (reported)
- `theta_bins=30`
- `eps_end=0.981, theta_bins=60`

### History matching (every measured configuration, all claims together)
- the naive configuration is within noise of every claim
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `eps_end, theta_bins`: eps_end=0.905, theta_bins=60 (max I 0.17); eps_end=0.981, theta_bins=60 (max I 0.36); eps_end=0.905, theta_bins=1 (max I 1.08); eps_end=0.001, theta_bins=1 (max I 1.34); +1 more
  - `eps_end, lr_schedule`: eps_end=0.0, lr_schedule=inv (max I 0.67); eps_end=0.0, lr_schedule=linear (max I 1.44)
  - `lr_schedule`: lr_schedule=inv (max I 0.85)
  - `eps_end`: eps_end=0.525 (max I 1.21)
  - `theta_bins`: theta_bins=30 (max I 1.42)
- Equally good values: `eps_end` in {0.905, 0.981}

Notes:
- configurations the target claim can't tell apart from the answer: eps_end=0.905, theta_bins=60; theta_bins=30; eps_end=0.981, theta_bins=60
- equally good values within one noise band (measured): eps_end in {0.905, 0.981}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `eps_end=0.981`, `theta_bins=60` | 5 | -3.5% | -8.4% | 6.0% |
| `theta_bins=60`, `eps_end=0.905` | 5 | +1.2% | -16.4% | 8.8% |
| `lr_schedule=inv`, `eps_end=0.001` | 5 | +28.7% | -16.4% | 22.6% |
| `theta_bins=12` | 6 | +38.9% | -11.4% | 25.2% |
| `lr_schedule=inv` | 6 | +7.5% | -44.5% | 26.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `e0f13d101585ad1609a15fbf67b70128f4cfffc8` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
