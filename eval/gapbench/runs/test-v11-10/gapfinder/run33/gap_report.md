# Gap Report: test-v11-10

Artifact `rlbench` · generated 2026-10-14 21:18 · 116 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +80.1% | -17.9% | ±22.9% | `max_steps=100`, `lr_schedule=inv` |

## C1: mean_reward (paper 94.93)
**Fits but unsupported** · gap +80.1% → -17.9% · 32 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0073`, `B0093`, `B0094`, `B0095`, `B0096` (5 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Config: `lr_schedule` naive `const`, changed to `inv`
- Command:

  Replay: fork checkpoint `ff019339-6aea-4d1c-94ee-f5b45c6d6d57` and run
  ```
  RUN_TAG=405fb6f59310 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 72.27, 80.48, 77.93, 91.78, 77.07; gap after -17.9%; result checkpoint `b25f4c4f-2451-4ec2-aab0-0a79f0916d44`
- Effect: candidate 77.93 minus naive 171 = -93.07, 95% bootstrap interval [-114.4, -73.15] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 94.9 steps

- p. 1; value used: `mean_reward` = 94.93 steps (headline claim)

### What did we measure?
- Naive median 171 over 5 runs; repeats: 167.6, 171, 181.8, 196.1, 152.4
- Spread: range 152.4 to 196.1, noise band ±21.7 (2 x MAD), CV 9.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +80.1% (noise band ±22.9% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +47.6% (it comes back)
- FAIL · Counterfactual (reversal test): without `lr_schedule` the gap is +3.7% (it did NOT come back)
- PASS · Held-out claim: C2: -49.9% to -56.6% (not worse beyond noise)
- PASS · Evidence: `max_steps=100`: paper states '100'
- FAIL · Evidence: `lr_schedule=inv`: no evidence mentions 'inv'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -93.07 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `eval.policy`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives (closest across all claims):
  - `max_steps=100`: this claim +3.7%, mean |gap| 24.3% (6 runs)
  - `lr_schedule=linear`, `max_steps=100`: this claim +2.3%, mean |gap| 24.6% (5 runs)
  - `lr_schedule=inv`, `max_steps=1000`: this claim +44.5%, mean |gap| 37.2% (5 runs)

### History matching (every measured configuration, all claims together)
- 4 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 4 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.35); lr_schedule=inv, max_steps=100 (max I 1.29); lr_schedule=linear, max_steps=40 (max I 2.94)
  - `max_steps`: max_steps=100 (max I 0.4)
- Equally good values: `lr_schedule` in {inv, linear}

Notes:
- equally good values within one noise band (measured): lr_schedule in {inv, linear}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 6 | +3.7% | +44.8% | 24.3% |
| `lr_schedule=linear`, `max_steps=100` | 5 | +2.3% | +46.9% | 24.6% |
| `lr_schedule=inv`, `max_steps=1000` | 5 | +44.5% | -30.0% | 37.2% |
| `lr_schedule=inv`, `max_steps=100` | 5 | -17.9% | -56.6% | 37.2% |
| `lr_schedule=inv` | 6 | +47.6% | -44.8% | 46.2% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `eval.policy`

## Provenance
- GapFinder commit: `634d827f07d6659ff82f6ea0924c8ba487e9d02a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
