# Gap Report: test-v11-10

Artifact `rlbench` · generated 2026-10-14 12:54 · 85 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Paper-artifact inconsistency | +91.6% | +2.3% | ±13.8% | `max_steps=100` |

## C1: mean_reward (paper 94.93)
**Paper-artifact inconsistency** · gap +91.6% → +2.3% · 20 hypotheses tested
> Confirmed cause: reverting it brings the gap back, held-out claims hold, and the value has evidence

### Which experiment changed it?
- Branch: `B0006`, `B0014`, `B0015`, `B0016`, `B0017`, `B0018` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `8723db55-7305-4fc7-9709-334171fe8409` and run
  ```
  RUN_TAG=7cc1a454bf5d "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 86.47, 99.19, 98.65, 95.09, 99.92, 95.66; gap after +2.3%; result checkpoint `dc52c261-e98a-437d-8048-e887460b3967`
- Effect: candidate 97.15 minus naive 181.9 = -84.71, 95% bootstrap interval [-92.42, -70.18] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 94.9 steps

- p. 1; value used: `mean_reward` = 94.93 steps (headline claim)

### What did we measure?
- Naive median 181.9 over 5 runs; repeats: 163.5, 181.9, 180.6, 189.7, 188.4
- Spread: range 163.5 to 189.7, noise band ±13.12 (2 x MAD), CV 5.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +91.6% (noise band ±13.8% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is -84.71 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `eval.policy`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (3.2 noise units, gap +47.3%); `lr_schedule=linear` (1.32 noise units, gap +73.4%)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `lr_schedule=linear`: this claim +2.4%, mean |gap| 23.3% (5 runs)
  - `max_steps=100`, `lr_schedule=inv`: this claim -14.3%, mean |gap| 32.2% (5 runs)
  - `lr_schedule=inv`: this claim +32.3%, mean |gap| 35.4% (6 runs)

### History matching (every measured configuration, all claims together)
- 3 of 20 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `max_steps`: max_steps=100 (max I 0.34)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.57); lr_schedule=inv, max_steps=100 (max I 1.21)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 6 | +2.3% | +22.4% | 12.4% |
| `max_steps=100`, `lr_schedule=linear` | 5 | +2.4% | +44.2% | 23.3% |
| `max_steps=100`, `lr_schedule=inv` | 5 | -14.3% | -50.1% | 32.2% |
| `lr_schedule=inv` | 6 | +32.3% | -38.5% | 35.4% |
| `lr_schedule=linear` | 6 | +70.4% | -12.3% | 41.4% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `eval.policy`

## Provenance
- GapFinder commit: `b05f7288e1a4df8af69bb0b5e7633827b4cb46c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
