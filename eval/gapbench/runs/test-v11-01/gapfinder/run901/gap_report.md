# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-14 23:46 · 199 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -50.0% | -5.8% | ±5.3% | `max_steps=400`, `gamma=1.0` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -50.0% → -5.8% · 54 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0138`, `B0196`, `B0197`, `B0198`, `B0199` (5 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `400`
- Config: `gamma` naive `0.99`, changed to `1.0`
- Command:

  Replay: fork checkpoint `5caa83cf-6e45-46d1-ba1e-f99c249b2757` and run
  ```
  RUN_TAG=0097a2160fa4 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 1.0 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 400 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 339, 400, 332.9, 301.3, 320.7; gap after -5.8%; result checkpoint `3237faa0-59b5-4ae6-b8b5-47b34a61ee59`
- Effect: candidate 332.9 minus naive 176.6 = +156.3, 95% bootstrap interval [+124.7, +212.8] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 176.6 over 5 runs; repeats: 176.6, 197.8, 186, 176.4, 153
- Spread: range 153 to 197.8, noise band ±18.85 (2 x MAD), CV 9.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -50.0% (noise band ±5.3% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -47.8% (it comes back)
- PASS · Counterfactual (reversal test): without `gamma` the gap is -22.1% (it comes back)
- PASS · Held-out claim: C2: +29.1% to +106.5% (not worse beyond noise)
- FAIL · Evidence: `max_steps=400`: no evidence mentions '400'; it fits, but nothing says the authors used it
- FAIL · Evidence: `gamma=1.0`: no evidence mentions '1.0'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +156.3 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=1000` (6.55 noise units, gap -15.1%); `max_steps=500` (5.85 noise units, gap +18.8%); `max_steps=2000` (3.9 noise units, gap -29.2%); `max_steps=10000` (2.11 noise units, gap -38.8%); `gamma=0.998` (1.12 noise units, gap -44.0%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `gamma=0.999`, `max_steps=1000`: this claim -5.9%, mean |gap| 13.7% (5 runs)
  - `max_steps=1000`: this claim -29.1%, mean |gap| 16.0% (6 runs)
  - `max_steps=2000`: this claim -27.1%, mean |gap| 16.9% (6 runs)

### History matching (every measured configuration, all claims together)
- 14 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `max_steps`: max_steps=10000 (max I 0.91); max_steps=500 (max I 1.05)
  - `gamma, max_steps`: gamma=0.999, max_steps=1000 (max I 0.95); gamma=0.999, max_steps=500 (max I 1.39); gamma=0.999, max_steps=400 (max I 1.6); gamma=0.998, max_steps=500 (max I 1.8); +3 more
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=2000 (max I 1.63)
- 2 separate islands (no single-knob move joins them): max_steps=10000; gamma=0.999, max_steps=1000; max_steps=500 | lr_schedule=linear, max_steps=2000

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'max_steps': '500', 'gamma': '0.999'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `gamma=0.999`, `max_steps=1000` | 5 | -5.9% | +21.5% | 13.7% |
| `max_steps=1000` | 6 | -29.1% | +2.9% | 16.0% |
| `max_steps=2000` | 6 | -27.1% | -6.7% | 16.9% |
| `gamma=0.998`, `max_steps=1000` | 5 | -9.8% | +28.0% | 18.9% |
| `max_steps=400`, `gamma=0.998` | 5 | -24.6% | +17.2% | 20.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `efb2f63a257a40b9982099a274f2e882f272b80c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
