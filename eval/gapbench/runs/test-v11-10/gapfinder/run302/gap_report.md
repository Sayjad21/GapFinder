# Gap Report: test-v11-10

Artifact `rlbench` · generated 2026-10-14 21:48 · 145 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Paper-artifact inconsistency | +90.5% | -0.3% | ±4.9% | `max_steps=100` |

## C1: mean_reward (paper 94.93)
**Paper-artifact inconsistency** · gap +90.5% → -0.3% · 32 hypotheses tested
> Confirmed cause: reverting it brings the gap back, held-out claims hold, and the value has evidence

### Which experiment changed it?
- Branch: `B0006`, `B0018`, `B0019`, `B0020`, `B0021`, `B0022` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `1e2d761a-6f63-45dd-9285-f4342256a73c` and run
  ```
  RUN_TAG=229034c4f08c "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 92.75, 92.89, 93.22, 96, 97.79, 100; gap after -0.3%; result checkpoint `c6b2a3ff-144c-40fd-90be-15db8c539bb7`
- Effect: candidate 94.61 minus naive 180.8 = -86.2, 95% bootstrap interval [-91, -64.43] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 94.9 steps, and that its worst seed still balances for 63.9.

- p. 1; value used: `mean_reward` = 94.93 steps (headline claim)

### What did we measure?
- Naive median 180.8 over 5 runs; repeats: 187.4, 180.8, 154.3, 183.1, 178.5
- Spread: range 154.3 to 187.4, noise band ±4.63 (2 x MAD), CV 7.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +90.5% (noise band ±4.9% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +90.5% (it comes back)
- PASS · Held-out claim: C2: +45.9% to -17.1% (not worse beyond noise)
- PASS · Evidence: `max_steps=100`: paper states '100'
- PASS · Effect vs noise: candidate minus naive is -86.2 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `max_steps_evaluation`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=2000` (13.1 noise units, gap +26.6%); `max_steps=10000` (12.46 noise units, gap +29.7%); `lr_schedule=inv` (10.16 noise units, gap +40.9%); `max_steps=40` (6.68 noise units, gap -57.9%); `lr_schedule=linear` (4.17 noise units, gap +70.1%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `lr_schedule=linear`: this claim +2.7%, mean |gap| 23.4% (5 runs)
  - `lr_schedule=inv`, `max_steps=100`: this claim -6.4%, mean |gap| 24.8% (5 runs)
  - `lr_schedule=inv`, `max_steps=10000`: this claim +61.6%, mean |gap| 33.2% (5 runs)

### History matching (every measured configuration, all claims together)
- 3 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `max_steps`: max_steps=100 (max I 0.21)
  - `lr_schedule, max_steps`: lr_schedule=inv, max_steps=100 (max I 1.11); lr_schedule=linear, max_steps=100 (max I 1.25)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 6 | -0.3% | -17.1% | 8.7% |
| `max_steps=100`, `lr_schedule=linear` | 5 | +2.7% | +44.1% | 23.4% |
| `lr_schedule=inv`, `max_steps=100` | 5 | -6.4% | -43.2% | 24.8% |
| `lr_schedule=inv`, `max_steps=10000` | 5 | +61.6% | +4.9% | 33.2% |
| `max_steps=2000`, `lr_schedule=inv` | 5 | +48.7% | -36.7% | 42.7% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `max_steps_evaluation`

## Provenance
- GapFinder commit: `e0f13d101585ad1609a15fbf67b70128f4cfffc8` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
