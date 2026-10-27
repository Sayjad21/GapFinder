# Gap Report: dev-rl-nocause

Artifact `rlbench` · generated 2026-10-15 20:50 · 143 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +52.1% | +10.6% | ±20.9% | `lr_schedule=inv` |

## C1: mean_reward (paper 118.924)
**Fits but unsupported** · gap +52.1% → +10.6% · 53 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0015`, `B0035`, `B0036`, `B0053`, `B0054`, `B0055` (6 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `inv`
- Command:

  Replay: fork checkpoint `1c9ca82a-a136-42fd-aa66-16fe917226c0` and run
  ```
  RUN_TAG=d89bd329d01a "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 144.1, 132.6, 130.4, 153.8, 120.4, 104; gap after +10.6%; result checkpoint `df3500ad-e8bf-4241-b22c-db3b338cd219`
- Effect: candidate 131.5 minus naive 180.9 = -49.44, 95% bootstrap interval [-77.56, -30.39] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner is stable across seeds on CartPole: its worst seed still balances for 69.1 steps on average.

- p. 1; value used: `mean_reward` = 118.924 steps (headline claim)

### What did we measure?
- Naive median 180.9 over 5 runs; repeats: 164.7, 193.4, 195.6, 174.9, 180.9
- Spread: range 164.7 to 195.6, noise band ±24.86 (2 x MAD), CV 7.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +52.1% (noise band ±20.9% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is +52.1% (it comes back)
- PASS · Held-out claim: C2: +16.5% to -54.5% (not worse beyond noise)
- FAIL · Evidence: `lr_schedule=inv`: no evidence mentions 'inv'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -49.44 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `theta_bins=3` (2.06 noise units, gap +9.0%); `theta_bins=30` (1.89 noise units, gap -12.7%); `theta_bins=1` (1.67 noise units, gap -17.2%); `theta_bins=8` (1.19 noise units, gap +27.2%)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`, `theta_bins=3`: this claim +24.5%, mean |gap| 15.9% (2 runs)
  - `eps_end=0.525`, `lr_schedule=inv`: this claim +31.8%, mean |gap| 22.0% (2 runs)
  - `theta_bins=8`, `lr_schedule=inv`: this claim -4.4%, mean |gap| 22.3% (5 runs)

### Equally good configurations
The target claim can't tell these 8 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `lr_schedule=inv` (reported)
- `theta_bins=1`
- `theta_bins=30`
- `lr_schedule=inv, theta_bins=8`
- `eps_end=0.001, theta_bins=1`
- `eps_end=0.981, theta_bins=1`
- `eps_end=0.001, lr_schedule=inv`
- `eps_end=0.905, theta_bins=1`

### History matching (every measured configuration, all claims together)
- 18 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr_schedule, theta_bins`: lr_schedule=inv, theta_bins=8 (max I 0.78); lr_schedule=inv, theta_bins=3 (max I 2.34); lr_schedule=linear, theta_bins=8 (max I 2.39)
  - `lr_schedule`: lr_schedule=inv (max I 1.2)
  - `eps_end, theta_bins`: eps_end=0.001, theta_bins=1 (max I 1.37); eps_end=0.981, theta_bins=1 (max I 1.68); eps_end=0.905, theta_bins=1 (max I 1.94)
  - `eps_end, lr_schedule`: eps_end=0.001, lr_schedule=inv (max I 1.85)
  - `theta_bins`: theta_bins=30 (max I 1.91); theta_bins=1 (max I 1.97)

Notes:
- configurations the target claim can't tell apart from the answer: lr_schedule=inv; theta_bins=1; theta_bins=30; lr_schedule=inv, theta_bins=8; eps_end=0.001, theta_bins=1; eps_end=0.981, theta_bins=1; eps_end=0.001, lr_schedule=inv; eps_end=0.905, theta_bins=1

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv`, `theta_bins=3` | 2 | +24.5% | +7.2% | 15.9% |
| `eps_end=0.525`, `lr_schedule=inv` | 2 | +31.8% | +12.2% | 22.0% |
| `theta_bins=8`, `lr_schedule=inv` | 5 | -4.4% | -40.1% | 22.3% |
| `lr_schedule=inv`, `eps_end=0.001` | 5 | +13.4% | -45.6% | 29.5% |
| `theta_bins=8` | 6 | +38.6% | -23.5% | 31.1% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `cd8c8af2b9d079dd9a57443ed501c0dd8a467d34` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
