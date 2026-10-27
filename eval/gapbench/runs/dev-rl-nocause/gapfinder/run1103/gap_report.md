# Gap Report: dev-rl-nocause

Artifact `rlbench` · generated 2026-10-15 00:29 · 197 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +46.1% | -19.9% | ±20.2% | `theta_bins=30` |

## C1: mean_reward (paper 118.924)
**Fits but unsupported** · gap +46.1% → -19.9% · 70 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0012`, `B0039`, `B0040`, `B0050`, `B0051`, `B0052` (6 run(s) of the same config)
- Config: `theta_bins` naive `6`, changed to `30`
- Command:

  Replay: fork checkpoint `83993f64-7531-4f81-956a-068a0df2ad40` and run
  ```
  RUN_TAG=9347fcff7f29 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 30 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 89.26, 148.7, 71.63, 101.3, 52.17, 102; gap after -19.9%; result checkpoint `2c414a22-87d2-4d8b-9e3b-2c496e4ecc3a`
- Effect: candidate 95.29 minus naive 173.7 = -78.42, 95% bootstrap interval [-120.6, -33.01] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner is stable across seeds on CartPole: its worst seed still balances for 69.1 steps on average.

- p. 1; value used: `mean_reward` = 118.924 steps (headline claim)

### What did we measure?
- Naive median 173.7 over 5 runs; repeats: 185.7, 173.7, 172.7, 158.2, 194
- Spread: range 158.2 to 194, noise band ±24.03 (2 x MAD), CV 7.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +46.1% (noise band ±20.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `theta_bins` the gap is +46.1% (it comes back)
- PASS · Held-out claim: C2: +2.5% to -73.4% (not worse beyond noise)
- FAIL · Evidence: `theta_bins=30`: no evidence mentions '30'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -78.42 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (1.75 noise units, gap -10.8%); `theta_bins=3` (1.15 noise units, gap +22.8%)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`, `eps_end=0.1`: this claim +0.9%, mean |gap| 22.3% (5 runs)
  - `eps_end=0.025`, `lr_schedule=inv`: this claim +1.7%, mean |gap| 23.0% (5 runs)
  - `eps_end=0.001`, `lr_schedule=inv`: this claim +11.4%, mean |gap| 23.9% (5 runs)

### History matching (every measured configuration, all claims together)
- 25 of 70 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `eps_end, lr_schedule`: eps_end=0.0, lr_schedule=inv (max I 0.39); eps_end=0.025, lr_schedule=inv (max I 0.83); eps_end=0.1, lr_schedule=inv (max I 0.91); eps_end=0.001, lr_schedule=inv (max I 0.98); +1 more
  - `lr_schedule, theta_bins`: lr_schedule=inv, theta_bins=8 (max I 0.83); lr_schedule=linear, theta_bins=12 (max I 0.95); lr_schedule=inv, theta_bins=4 (max I 1.13)
  - `eps_end, theta_bins`: eps_end=0.001, theta_bins=30 (max I 1.19); eps_end=0.025, theta_bins=30 (max I 1.23)
- 2 separate islands (no single-knob move joins them): eps_end=0.0, lr_schedule=inv; lr_schedule=inv, theta_bins=8; eps_end=0.025, lr_schedule=inv | eps_end=0.001, theta_bins=30; eps_end=0.025, theta_bins=30; eps_end=0.01, theta_bins=30

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'lr_schedule': 'inv', 'eps_end': '0.0'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv`, `eps_end=0.1` | 5 | +0.9% | -43.7% | 22.3% |
| `eps_end=0.025`, `lr_schedule=inv` | 5 | +1.7% | -44.3% | 23.0% |
| `eps_end=0.001`, `lr_schedule=inv` | 5 | +11.4% | -36.5% | 23.9% |
| naive (reproduction as run) | 5 | +46.1% | +2.5% | 24.3% |
| `lr_schedule=inv` | 6 | +17.3% | -32.4% | 24.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
