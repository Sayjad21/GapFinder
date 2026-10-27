# Gap Report: test-v11-10

Artifact `rlbench` · generated 2026-10-14 21:27 · 145 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +91.7% | +2.9% | ±2.5% | `max_steps=100`, `lr_schedule=linear` |

## C1: mean_reward (paper 94.93)
**Fits but unsupported** · gap +91.7% → +2.9% · 32 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0079`, `B0102`, `B0103`, `B0104`, `B0105` (5 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Config: `lr_schedule` naive `const`, changed to `linear`
- Command:

  Replay: fork checkpoint `689fbb50-71bd-448c-bdcf-1df19066b38b` and run
  ```
  RUN_TAG=ffb279d58746 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule linear --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 98.22, 97.25, 96.45, 97.67, 97.64; gap after +2.9%; result checkpoint `e11fa151-39e4-4464-ae27-5b522f2c07a7`
- Effect: candidate 97.64 minus naive 182 = -84.33, 95% bootstrap interval [-95.86, -62.44] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 94.9 steps

- p. 1; value used: `mean_reward` = 94.93 steps (headline claim)

### What did we measure?
- Naive median 182 over 5 runs; repeats: 182, 154.2, 180.8, 183, 195.7
- Spread: range 154.2 to 195.7, noise band ±2.35 (2 x MAD), CV 8.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +91.7% (noise band ±2.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +71.5% (it comes back)
- FAIL · Counterfactual (reversal test): without `lr_schedule` the gap is +5.2% (it did NOT come back)
- PASS · Held-out claim: C2: +72.5% to +47.7% (not worse beyond noise)
- PASS · Evidence: `max_steps=100`: paper states '100'
- FAIL · Evidence: `lr_schedule=linear`: no evidence mentions 'linear'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -84.33 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `eval.policy`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (21.89 noise units, gap +37.5%); `max_steps=40` (12.27 noise units, gap -61.3%); `max_steps=20` (5.16 noise units, gap -78.9%)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`: this claim +44.7%, mean |gap| 25.3% (6 runs)
  - `max_steps=100`, `lr_schedule=inv`: this claim -9.8%, mean |gap| 28.5% (5 runs)
  - `max_steps=100`: this claim +5.2%, mean |gap| 30.0% (6 runs)

### History matching (every measured configuration, all claims together)
- 3 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `max_steps`: max_steps=100 (max I 0.61)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.68); lr_schedule=inv, max_steps=100 (max I 0.9)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100`, `lr_schedule=linear` | 5 | +2.9% | +47.7% | 25.3% |
| `lr_schedule=inv` | 6 | +44.7% | -6.0% | 25.3% |
| `max_steps=100`, `lr_schedule=inv` | 5 | -9.8% | -47.2% | 28.5% |
| `max_steps=100` | 6 | +5.2% | +54.7% | 30.0% |
| `max_steps=400`, `lr_schedule=inv` | 5 | +57.3% | -30.7% | 44.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `eval.policy`

## Provenance
- GapFinder commit: `634d827f07d6659ff82f6ea0924c8ba487e9d02a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
