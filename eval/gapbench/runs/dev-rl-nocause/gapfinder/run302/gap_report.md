# Gap Report: dev-rl-nocause

Artifact `rlbench` · generated 2026-10-14 21:40 · 174 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +62.3% | -6.7% | ±3.7% | `theta_bins=30`, `eps_end=0.1` |

## C1: mean_reward (paper 118.924)
**Fits but unsupported** · gap +62.3% → -6.7% · 53 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0096`, `B0141`, `B0142` (3 run(s) of the same config)
- Config: `theta_bins` naive `6`, changed to `30`
- Config: `eps_end` naive `0.05`, changed to `0.1`
- Command:

  Replay: fork checkpoint `ca7a0dd0-fb38-4c6c-b9cb-0edf091fd25c` and run
  ```
  RUN_TAG=2a76691cd8e9 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.1 --eps_decay 0.99 --theta_bins 30 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 85.69, 126.1, 110.9; gap after -6.7%; result checkpoint `8d87019b-a923-4b20-bda9-bfd7a718f019`
- Effect: candidate 110.9 minus naive 193.1 = -82.14, 95% bootstrap interval [-108.6, -54.83] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner is stable across seeds on CartPole: its worst seed still balances for 69.1 steps on average.

- p. 1; value used: `mean_reward` = 118.924 steps (headline claim)

### What did we measure?
- Naive median 193.1 over 5 runs; repeats: 178, 195.3, 177.9, 194, 193.1
- Spread: range 177.9 to 195.3, noise band ±4.43 (2 x MAD), CV 4.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +62.3% (noise band ±3.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `theta_bins` the gap is +47.7% (it comes back)
- PASS · Counterfactual (reversal test): without `eps_end` the gap is -18.2% (it comes back)
- PASS · Held-out claim: C2: +139.0% to -76.5% (not worse beyond noise)
- FAIL · Evidence: `theta_bins=30`: no evidence mentions '30'; it fits, but nothing says the authors used it
- FAIL · Evidence: `eps_end=0.1`: no evidence mentions '0.1'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -82.14 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `theta_bins=1` (15.94 noise units, gap -3.0%); `lr_schedule=inv` (11.83 noise units, gap +18.3%); `lr_schedule=linear` (5.24 noise units, gap +42.8%); `eps_end=0.905` (4.86 noise units, gap +44.2%); `theta_bins=12` (4.33 noise units, gap +46.2%) (and 7 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`: this claim +12.7%, mean |gap| 20.2% (4 runs)
  - `lr_schedule=inv`, `eps_end=0.005`: this claim +12.3%, mean |gap| 24.3% (3 runs)
  - `theta_bins=12`, `lr_schedule=linear`: this claim +15.6%, mean |gap| 28.5% (3 runs)

### History matching (every measured configuration, all claims together)
- 10 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `eps_end, theta_bins`: eps_end=0.1, theta_bins=30 (max I 1.31); eps_end=0.1, theta_bins=3 (max I 1.37); eps_end=0.005, theta_bins=1 (max I 1.56)
  - `eps_end, lr_schedule`: eps_end=0.1, lr_schedule=inv (max I 1.39); eps_end=0.005, lr_schedule=inv (max I 1.45)
  - `lr_schedule`: lr_schedule=inv (max I 1.66)
  - `lr_schedule, theta_bins`: lr_schedule=inv, theta_bins=12 (max I 1.77); lr_schedule=linear, theta_bins=12 (max I 1.88)
  - `theta_bins`: theta_bins=30 (max I 1.95); theta_bins=1 (max I 2.25)
- 2 separate islands (no single-knob move joins them): eps_end=0.1, theta_bins=30; eps_end=0.1, theta_bins=3; eps_end=0.005, theta_bins=1 | eps_end=0.1, lr_schedule=inv; eps_end=0.005, lr_schedule=inv; lr_schedule=inv

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv` | 4 | +12.7% | -27.7% | 20.2% |
| `lr_schedule=inv`, `eps_end=0.005` | 3 | +12.3% | -36.4% | 24.3% |
| `theta_bins=12`, `lr_schedule=linear` | 3 | +15.6% | -41.4% | 28.5% |
| `theta_bins=12` | 4 | +46.7% | -21.3% | 34.0% |
| `eps_end=0.1`, `theta_bins=30` | 3 | -6.7% | -76.5% | 41.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `634d827f07d6659ff82f6ea0924c8ba487e9d02a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
