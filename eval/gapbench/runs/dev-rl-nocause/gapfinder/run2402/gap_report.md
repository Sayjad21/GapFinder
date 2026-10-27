# Gap Report: dev-rl-nocause

Artifact `rlbench` · generated 2026-10-16 01:13 · 124 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +53.7% | +13.7% | ±5.2% | `lr_schedule=inv` |

## C1: mean_reward (paper 118.924)
**Fits but unsupported** · gap +53.7% → +13.7% · 53 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0015`, `B0039`, `B0040`, `B0053` (4 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `inv`
- Command:

  Replay: fork checkpoint `322cdc63-c82c-4ad1-b509-200d0b35a483` and run
  ```
  RUN_TAG=b440348eb37b "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 126.4, 147.7, 144.1, 120; gap after +13.7%; result checkpoint `e1c0e264-5a22-446c-830d-af676231b426`
- Effect: candidate 135.2 minus naive 182.8 = -47.62, 95% bootstrap interval [-68.61, -33.2] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner is stable across seeds on CartPole: its worst seed still balances for 69.1 steps on average.

- p. 1; value used: `mean_reward` = 118.924 steps (headline claim)

### What did we measure?
- Naive median 182.8 over 5 runs; repeats: 182.8, 185.9, 178.9, 182, 193
- Spread: range 178.9 to 193, noise band ±6.16 (2 x MAD), CV 2.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +53.7% (noise band ±5.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is +53.7% (it comes back)
- PASS · Held-out claim: C2: +23.2% to -39.9% (not worse beyond noise)
- FAIL · Evidence: `lr_schedule=inv`: no evidence mentions 'inv'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -47.62 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `theta_bins=30` (7.84 noise units, gap -13.2%); `eps_end=0.01` (3.09 noise units, gap +37.7%); `theta_bins=12` (1.66 noise units, gap +45.1%); `lr_schedule=linear` (1.42 noise units, gap +46.4%); `eps_end=0.0` (1.24 noise units, gap +47.3%)
- Near alternatives (closest across all claims):
  - `eps_end=0.525`, `lr_schedule=inv`: this claim +30.6%, mean |gap| 16.7% (2 runs)
  - `eps_end=0.0`, `lr_schedule=linear`: this claim +31.9%, mean |gap| 19.9% (2 runs)
  - `eps_end=0.0`, `theta_bins=8`: this claim +45.0%, mean |gap| 23.2% (2 runs)

### Equally good configurations
The target claim can't tell these 8 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `lr_schedule=inv` (reported)
- `lr_schedule=linear, theta_bins=12`
- `lr_schedule=inv, theta_bins=8`
- `eps_end=0.01, theta_bins=30`
- `lr_schedule=inv, theta_bins=4`
- `eps_end=0.005, lr_schedule=inv`
- `eps_end=0.0, lr_schedule=inv`
- `eps_end=0.005, theta_bins=30`

### History matching (every measured configuration, all claims together)
- 7 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 7 configurations
  - `lr_schedule, theta_bins`: lr_schedule=linear, theta_bins=12 (max I 1.08); lr_schedule=inv, theta_bins=8 (max I 1.13); lr_schedule=inv, theta_bins=4 (max I 2.73)
  - `eps_end, lr_schedule`: eps_end=0.01, lr_schedule=inv (max I 1.58); eps_end=0.0, lr_schedule=inv (max I 2.9)
  - `lr_schedule`: lr_schedule=inv (max I 2.23)
  - `eps_end, theta_bins`: eps_end=0.01, theta_bins=30 (max I 2.32)
- 3 separate islands (no single-knob move joins them): lr_schedule=inv, theta_bins=8; eps_end=0.01, lr_schedule=inv; lr_schedule=inv | lr_schedule=linear, theta_bins=12 | eps_end=0.01, theta_bins=30

Notes:
- configurations the target claim can't tell apart from the answer: lr_schedule=inv; lr_schedule=linear, theta_bins=12; lr_schedule=inv, theta_bins=8; eps_end=0.01, theta_bins=30; lr_schedule=inv, theta_bins=4; eps_end=0.005, lr_schedule=inv; eps_end=0.0, lr_schedule=inv; eps_end=0.005, theta_bins=30

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `eps_end=0.525`, `lr_schedule=inv` | 2 | +30.6% | +2.8% | 16.7% |
| `eps_end=0.0`, `lr_schedule=linear` | 2 | +31.9% | -7.9% | 19.9% |
| `eps_end=0.0`, `theta_bins=8` | 2 | +45.0% | +1.4% | 23.2% |
| `eps_end=0.005`, `lr_schedule=linear` | 2 | +34.3% | +13.1% | 23.7% |
| `lr_schedule=inv`, `eps_end=0.01` | 3 | +9.5% | -38.5% | 24.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
