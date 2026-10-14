# Gap Report: test-v11-10

Artifact `rlbench` · generated 2026-10-14 12:17 · 80 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +93.7% | +3.0% | ±25.4% | `max_steps=100`, `lr_schedule=linear` |

## C1: mean_reward (paper 94.93)
**Fits but unsupported** · gap +93.7% → +3.0% · 20 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0050`, `B0065`, `B0066`, `B0067`, `B0068` (5 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Config: `lr_schedule` naive `const`, changed to `linear`
- Command:

  Replay: fork checkpoint `5b10e8cd-3b8b-4766-a4a9-f4081b9a472f` and run
  ```
  RUN_TAG=dfd4c66c0681 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule linear --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 96.19, 97.79, 98.56, 99.02, 97.73; gap after +3.0%; result checkpoint `d70da036-04b2-4fa9-a6d5-f6823cb78827`
- Effect: candidate 97.79 minus naive 183.8 = -86.05, 95% bootstrap interval [-96.03, -69.09] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 94.9 steps, and that its worst seed still balances for 63.9.

- p. 1; value used: `mean_reward` = 94.93 steps (headline claim)

### What did we measure?
- Naive median 183.8 over 5 runs; repeats: 169.9, 165, 188.2, 183.8, 195.9
- Spread: range 165 to 195.9, noise band ±24.1 (2 x MAD), CV 7.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +93.7% (noise band ±25.4% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +70.1% (it comes back)
- FAIL · Counterfactual (reversal test): without `lr_schedule` the gap is +3.8% (it did NOT come back)
- PASS · Held-out claim: C2: +28.3% to +48.0% (not worse beyond noise)
- PASS · Evidence: `max_steps=100`: paper states '100'
- FAIL · Evidence: `lr_schedule=linear`: no evidence mentions 'linear'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -86.05 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `max_steps_evaluation`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (3.02 noise units, gap +16.9%)
- Near alternatives (closest across all claims):
  - `max_steps=100`: this claim +3.8%, mean |gap| 26.3% (6 runs)
  - `max_steps=400`, `lr_schedule=inv`: this claim +47.5%, mean |gap| 41.1% (5 runs)
  - `max_steps=100`, `lr_schedule=inv`: this claim -11.0%, mean |gap| 42.1% (5 runs)

### History matching (every measured configuration, all claims together)
- 3 of 20 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `max_steps`: max_steps=100 (max I 0.52)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.77); lr_schedule=inv, max_steps=100 (max I 1.18)
- Equally good values: `lr_schedule` in {inv, linear}

Notes:
- equally good values within one noise band (measured): lr_schedule in {inv, linear}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=linear`, `max_steps=100` | 5 | +3.0% | +48.0% | 25.5% |
| `max_steps=100` | 6 | +3.8% | +48.7% | 26.3% |
| `max_steps=400`, `lr_schedule=inv` | 5 | +47.5% | -34.7% | 41.1% |
| `max_steps=100`, `lr_schedule=inv` | 5 | -11.0% | -73.2% | 42.1% |
| `lr_schedule=inv` | 6 | +53.2% | -32.1% | 42.7% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `max_steps_evaluation`

## Provenance
- GapFinder commit: `b05f7288e1a4df8af69bb0b5e7633827b4cb46c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0519, sandbox reported $0.0000 (total $0.0519; this search; ledger extraction is included only if it shared the search's router)
