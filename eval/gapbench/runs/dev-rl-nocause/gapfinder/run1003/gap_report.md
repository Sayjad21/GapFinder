# Gap Report: dev-rl-nocause

Artifact `rlbench` · generated 2026-10-15 00:16 · 198 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +47.4% | -0.2% | ±17.8% | `theta_bins=1`, `eps_end=0.001` |

## C1: mean_reward (paper 118.924)
**Fits but unsupported** · gap +47.4% → -0.2% · 70 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0087`, `B0135`, `B0136`, `B0137`, `B0138` (5 run(s) of the same config)
- Config: `theta_bins` naive `6`, changed to `1`
- Config: `eps_end` naive `0.05`, changed to `0.001`
- Command:

  Replay: fork checkpoint `7c243950-6b49-4fe6-b0a9-603039100648` and run
  ```
  RUN_TAG=512b23dc46ad "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.001 --eps_decay 0.99 --theta_bins 1 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 118.9, 66.52, 163.9, 65.91, 118.7; gap after -0.2%; result checkpoint `04ff7cbb-10fe-404e-a6d8-01f0770099ec`
- Effect: candidate 118.7 minus naive 175.2 = -56.57, 95% bootstrap interval [-114, -20.39] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner is stable across seeds on CartPole: its worst seed still balances for 69.1 steps on average.

- p. 1; value used: `mean_reward` = 118.924 steps (headline claim)

### What did we measure?
- Naive median 175.2 over 5 runs; repeats: 185.8, 147.4, 197.4, 175.2, 174.7
- Spread: range 147.4 to 197.4, noise band ±21.22 (2 x MAD), CV 10.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +47.4% (noise band ±17.8% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `theta_bins` the gap is +43.9% (it comes back)
- PASS · Counterfactual (reversal test): without `eps_end` the gap is -30.0% (it comes back)
- PASS · Held-out claim: C2: +59.2% to -76.4% (not worse beyond noise)
- FAIL · Evidence: `theta_bins=1`: no evidence mentions '1'; it fits, but nothing says the authors used it
- FAIL · Evidence: `eps_end=0.001`: no evidence mentions '0.001'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -56.57 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=linear` (1.24 noise units, gap +25.3%); `lr_schedule=inv` (1.24 noise units, gap +25.3%)
- Near alternatives (closest across all claims):
  - `theta_bins=12`, `lr_schedule=linear`: this claim +9.9%, mean |gap| 15.6% (5 runs)
  - `lr_schedule=inv`, `theta_bins=8`: this claim +3.2%, mean |gap| 23.2% (5 runs)
  - `lr_schedule=inv`, `eps_end=0.525`: this claim +22.7%, mean |gap| 24.5% (5 runs)

### History matching (every measured configuration, all claims together)
- 47 of 70 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `eps_end, lr_schedule`: eps_end=0.005, lr_schedule=inv (max I 0.5); eps_end=0.0, lr_schedule=inv (max I 0.99); eps_end=0.001, lr_schedule=inv (max I 1.04); eps_end=0.01, lr_schedule=inv (max I 1.22)
  - `eps_end, theta_bins`: eps_end=0.01, theta_bins=1 (max I 0.55); eps_end=0.0, theta_bins=30 (max I 0.87); eps_end=0.1, theta_bins=30 (max I 1.25)
  - `lr_schedule, theta_bins`: lr_schedule=inv, theta_bins=8 (max I 0.57); lr_schedule=inv, theta_bins=4 (max I 0.81); lr_schedule=linear, theta_bins=12 (max I 1.19)

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'theta_bins': '30', 'eps_end': '0.0'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `theta_bins=12`, `lr_schedule=linear` | 5 | +9.9% | -21.3% | 15.6% |
| `lr_schedule=inv`, `theta_bins=8` | 5 | +3.2% | -43.1% | 23.2% |
| `lr_schedule=inv`, `eps_end=0.525` | 5 | +22.7% | -26.2% | 24.5% |
| `lr_schedule=inv` | 6 | +20.3% | -29.4% | 24.9% |
| `theta_bins=8` | 6 | +52.5% | +1.7% | 27.1% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
