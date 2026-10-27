# Gap Report: dev-rl-nocause

Artifact `rlbench` · generated 2026-10-15 00:46 · 199 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +59.7% | -0.9% | ±7.6% | `theta_bins=1`, `eps_end=0.001` |

## C1: mean_reward (paper 118.924)
**Fits but unsupported** · gap +59.7% → -0.9% · 71 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0114`, `B0190`, `B0191` (3 run(s) of the same config)
- Config: `theta_bins` naive `6`, changed to `1`
- Config: `eps_end` naive `0.05`, changed to `0.001`
- Command:

  Replay: fork checkpoint `cf0a259a-2426-4c61-a477-eed5b645f4c5` and run
  ```
  RUN_TAG=23ac34be1c24 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.001 --eps_decay 0.99 --theta_bins 1 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 133.4, 100.7, 117.9; gap after -0.9%; result checkpoint `aeb63ff1-8ff6-4abc-b5f5-adb256055df7`
- Effect: candidate 117.9 minus naive 189.9 = -72.05, 95% bootstrap interval [-92, -51.98] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner is stable across seeds on CartPole: its worst seed still balances for 69.1 steps on average.

- p. 1; value used: `mean_reward` = 118.924 steps (headline claim)

### What did we measure?
- Naive median 189.9 over 5 runs; repeats: 183.8, 196.1, 189.9, 190.8, 185.4
- Spread: range 183.8 to 196.1, noise band ±9.07 (2 x MAD), CV 2.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +59.7% (noise band ±7.6% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `theta_bins` the gap is +68.2% (it comes back)
- PASS · Counterfactual (reversal test): without `eps_end` the gap is -23.8% (it comes back)
- PASS · Held-out claim: C2: +112.6% to -76.1% (not worse beyond noise)
- FAIL · Evidence: `theta_bins=1`: no evidence mentions '1'; it fits, but nothing says the authors used it
- FAIL · Evidence: `eps_end=0.001`: no evidence mentions '0.001'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -72.05 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `theta_bins=30` (6.21 noise units, gap -12.3%); `lr_schedule=inv` (4.17 noise units, gap +27.9%); `eps_end=0.1` (2.16 noise units, gap +43.2%); `eps_end=0.905` (2.08 noise units, gap +43.9%); `theta_bins=8` (2.06 noise units, gap +44.0%) (and 6 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`, `eps_end=0.0`: this claim +22.7%, mean |gap| 12.4% (3 runs)
  - `lr_schedule=inv`, `theta_bins=8`: this claim +3.4%, mean |gap| 12.8% (3 runs)
  - `theta_bins=8`: this claim +38.2%, mean |gap| 20.9% (4 runs)

### History matching (every measured configuration, all claims together)
- 5 of 71 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 5 configurations
  - `lr_schedule, theta_bins`: lr_schedule=inv, theta_bins=8 (max I 1.64)
  - `eps_end, lr_schedule`: eps_end=0.001, lr_schedule=inv (max I 1.99); eps_end=0.01, lr_schedule=inv (max I 2.51)
  - `eps_end, theta_bins`: eps_end=0.525, theta_bins=3 (max I 2.54)
  - `eps_end, lr_schedule, theta_bins`: eps_end=0.905, lr_schedule=inv, theta_bins=30 (max I 2.75)
- 4 separate islands (no single-knob move joins them): eps_end=0.001, lr_schedule=inv; eps_end=0.01, lr_schedule=inv | lr_schedule=inv, theta_bins=8 | eps_end=0.525, theta_bins=3 | eps_end=0.905, lr_schedule=inv, theta_bins=30

Notes:
- stopped early: run budget of 200 reached (wanted 2 more run(s) of {'lr_schedule': 'inv', 'eps_end': '0.025'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv`, `eps_end=0.0` | 3 | +22.7% | -2.0% | 12.4% |
| `lr_schedule=inv`, `theta_bins=8` | 3 | +3.4% | -22.2% | 12.8% |
| `theta_bins=8` | 4 | +38.2% | +3.5% | 20.9% |
| `lr_schedule=inv` | 4 | +28.7% | -13.0% | 20.9% |
| `theta_bins=30`, `lr_schedule=inv`, `eps_end=0.905` | 3 | -16.9% | -30.2% | 23.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
