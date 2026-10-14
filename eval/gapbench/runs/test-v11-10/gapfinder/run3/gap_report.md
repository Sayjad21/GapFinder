# Gap Report: test-v11-10

Artifact `rlbench` · generated 2026-10-14 12:54 · 97 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Paper-artifact inconsistency | +93.2% | +2.6% | ±3.1% | `max_steps=100` |

## C1: mean_reward (paper 94.93)
**Paper-artifact inconsistency** · gap +93.2% → +2.6% · 20 hypotheses tested
> Confirmed cause: reverting it brings the gap back, held-out claims hold, and the value has evidence

### Which experiment changed it?
- Branch: `B0006`, `B0014`, `B0015`, `B0016`, `B0017`, `B0018` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `131a6a8f-d9b2-4780-9294-4cb59c3dd072` and run
  ```
  RUN_TAG=7b8186858019 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 99.53, 94.8, 93.52, 99.73, 95.21, 99.69; gap after +2.6%; result checkpoint `2956e007-8484-4cef-bb81-81316c6246ea`
- Effect: candidate 97.37 minus naive 183.4 = -86.03, 95% bootstrap interval [-97.8, -72.85] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 94.9 steps

- p. 1; value used: `mean_reward` = 94.93 steps (headline claim)

### What did we measure?
- Naive median 183.4 over 5 runs; repeats: 198.2, 183.4, 164.8, 184.9, 181.9
- Spread: range 164.8 to 198.2, noise band ±2.94 (2 x MAD), CV 6.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +93.2% (noise band ±3.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +93.2% (it comes back)
- PASS · Held-out claim: C2: +19.6% to +27.6% (not worse beyond noise)
- PASS · Evidence: `max_steps=100`: paper states '100'
- PASS · Effect vs noise: candidate minus naive is -86.03 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `eval.policy`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (9.35 noise units, gap +64.2%); `max_steps=20` (4.6 noise units, gap -78.9%); `lr_schedule=linear` (3.41 noise units, gap +82.6%)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `max_steps=100`: this claim +2.1%, mean |gap| 23.3% (5 runs)
  - `max_steps=100`, `lr_schedule=inv`: this claim -11.6%, mean |gap| 38.5% (5 runs)
  - `max_steps=500`, `lr_schedule=inv`: this claim +67.4%, mean |gap| 38.7% (5 runs)

### History matching (every measured configuration, all claims together)
- 3 of 20 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `max_steps`: max_steps=100 (max I 0.41)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.48); lr_schedule=inv, max_steps=100 (max I 1.6)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 6 | +2.6% | +27.6% | 15.1% |
| `lr_schedule=linear`, `max_steps=100` | 5 | +2.1% | +44.6% | 23.3% |
| `max_steps=100`, `lr_schedule=inv` | 5 | -11.6% | -65.4% | 38.5% |
| `max_steps=500`, `lr_schedule=inv` | 5 | +67.4% | +10.1% | 38.7% |
| `max_steps=2000`, `lr_schedule=inv` | 5 | +55.5% | -36.2% | 45.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `eval.policy`

## Provenance
- GapFinder commit: `b05f7288e1a4df8af69bb0b5e7633827b4cb46c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0323, sandbox reported $0.0000 (total $0.0323; this search; ledger extraction is included only if it shared the search's router)
