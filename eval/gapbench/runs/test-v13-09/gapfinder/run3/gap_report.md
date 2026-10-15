# Gap Report: test-v13-09

Artifact `rlbench` · generated 2026-10-16 01:01 · 124 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Paper-artifact inconsistency | +83.4% | -3.2% | ±2.5% | `max_steps=100` |

## C1: mean_reward (paper 99.495)
**Paper-artifact inconsistency** · gap +83.4% → -3.2% · 32 hypotheses tested
> Confirmed cause: reverting it brings the gap back, held-out claims hold, and the value has evidence

### Which experiment changed it?
- Branch: `B0006`, `B0018`, `B0019`, `B0042`, `B0043`, `B0044` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `ba2eeb63-e514-4164-8b93-36f3e4e7fb0f` and run
  ```
  RUN_TAG=2a3c5b51c89b "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 91.04, 93.66, 100, 98.94, 99.35, 93.03; gap after -3.2%; result checkpoint `05a9569b-58dc-4d79-8f9e-daed33cc4fe1`
- Effect: candidate 96.3 minus naive 182.5 = -86.21, 95% bootstrap interval [-97.62, -70.09] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 99.5 steps, and that its worst seed still balances for 96.8.

- p. 1; value used: `mean_reward` = 99.495 steps (headline claim)

### What did we measure?
- Naive median 182.5 over 5 runs; repeats: 182.2, 183.7, 182.5, 195.9, 164.7
- Spread: range 164.7 to 195.9, noise band ±2.46 (2 x MAD), CV 6.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +83.4% (noise band ±2.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +83.4% (it comes back)
- PASS · Held-out claim: C2: +48.1% to -32.4% (not worse beyond noise)
- PASS · Evidence: `max_steps=100`: paper states '100'
- PASS · Effect vs noise: candidate minus naive is -86.21 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `theta_clip_low`, `theta_clip_high`, `omega_clip_low`, `omega_clip_high`, `g`, `mc`, `mp`, `l`, `f`, `dt`, `init_state_low`, `init_state_high`, `theta_range`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=10000` (15.75 noise units, gap +44.5%); `max_steps=150` (14.75 noise units, gap +47.0%); `lr_schedule=linear` (12.01 noise units, gap +53.7%); `lr_schedule=inv` (9.76 noise units, gap +59.3%); `max_steps=40` (8.84 noise units, gap -61.6%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `max_steps=100`: this claim -2.0%, mean |gap| 3.9% (5 runs)
  - `max_steps=150`: this claim +45.3%, mean |gap| 24.0% (6 runs)
  - `lr_schedule=inv`, `max_steps=400`: this claim +57.5%, mean |gap| 32.4% (2 runs)

### Equally good configurations
The target claim can't tell these 2 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `lr_schedule=linear, max_steps=100`

### History matching (every measured configuration, all claims together)
- 3 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.55); lr_schedule=inv, max_steps=100 (max I 1.76)
  - `max_steps`: max_steps=100 (max I 0.86)

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=100; lr_schedule=linear, max_steps=100

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=linear`, `max_steps=100` | 5 | -2.0% | -5.7% | 3.9% |
| `max_steps=100` | 6 | -3.2% | -32.4% | 17.8% |
| `max_steps=150` | 6 | +45.3% | +2.6% | 24.0% |
| `lr_schedule=inv`, `max_steps=400` | 2 | +57.5% | -7.4% | 32.4% |
| `lr_schedule=linear`, `max_steps=150` | 5 | +41.5% | +28.9% | 35.2% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `theta_clip_low`, `theta_clip_high`, `omega_clip_low`, `omega_clip_high`, `g`, `mc`, `mp`, `l`, `f`, `dt`, `init_state_low`, `init_state_high`, `theta_range`, `--out`

## Provenance
- GapFinder commit: `e9c31fd1405f5c8aae4bd880eadcdc8d491fad02` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0501, sandbox reported $0.0000 (total $0.0501; this search; ledger extraction is included only if it shared the search's router)
