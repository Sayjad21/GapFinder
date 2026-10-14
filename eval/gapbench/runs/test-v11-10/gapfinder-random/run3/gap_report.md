# Gap Report: test-v11-10

Artifact `rlbench` · generated 2026-10-14 12:55 · 73 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Paper-artifact inconsistency | +90.5% | -0.3% | ±4.6% | `max_steps=100` |

## C1: mean_reward (paper 94.93)
**Paper-artifact inconsistency** · gap +90.5% → -0.3% · 20 hypotheses tested
> Confirmed cause: reverting it brings the gap back, held-out claims hold, and the value has evidence

### Which experiment changed it?
- Branch: `B0013`, `B0029`, `B0030`, `B0031`, `B0032`, `B0033` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `a4ef355a-109d-4e62-a3de-804b43a442aa` and run
  ```
  RUN_TAG=f15eb8e25af3 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 87.04, 85.87, 99.69, 92.74, 96.47, 99.23; gap after -0.3%; result checkpoint `6262ea28-3469-457d-bfdb-f90798c695e7`
- Effect: candidate 94.6 minus naive 180.9 = -86.26, 95% bootstrap interval [-93.7, -65.42] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 94.9 steps

- p. 1; value used: `mean_reward` = 94.93 steps (headline claim)

### What did we measure?
- Naive median 180.9 over 5 runs; repeats: 181.4, 152, 178.7, 180.9, 188.3
- Spread: range 152 to 188.3, noise band ±4.38 (2 x MAD), CV 8.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +90.5% (noise band ±4.6% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +90.5% (it comes back)
- PASS · Held-out claim: C2: -18.9% to -14.1% (not worse beyond noise)
- PASS · Evidence: `max_steps=100`: paper states '100'
- PASS · Effect vs noise: candidate minus naive is -86.26 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `eval.policy`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (5.46 noise units, gap +65.3%); `lr_schedule=linear` (3.5 noise units, gap +74.3%); `max_steps=20` (2.51 noise units, gap -78.9%)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `lr_schedule=linear`: this claim +2.0%, mean |gap| 23.4% (5 runs)
  - `max_steps=100`, `lr_schedule=inv`: this claim -19.8%, mean |gap| 35.3% (5 runs)
  - `lr_schedule=inv`, `max_steps=500`: this claim +39.0%, mean |gap| 36.8% (5 runs)

### History matching (every measured configuration, all claims together)
- 3 of 20 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `max_steps`: max_steps=100 (max I 0.14)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.54); lr_schedule=inv, max_steps=100 (max I 1.6)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 6 | -0.3% | -14.1% | 7.2% |
| `max_steps=100`, `lr_schedule=linear` | 5 | +2.0% | +44.8% | 23.4% |
| `max_steps=100`, `lr_schedule=inv` | 5 | -19.8% | -50.9% | 35.3% |
| `lr_schedule=inv`, `max_steps=500` | 5 | +39.0% | -34.7% | 36.8% |
| `lr_schedule=inv`, `max_steps=2000` | 5 | +54.9% | -35.8% | 45.3% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `eval.policy`

## Provenance
- GapFinder commit: `b05f7288e1a4df8af69bb0b5e7633827b4cb46c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
