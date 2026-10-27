# Gap Report: test-v11-04

Artifact `rlbench` · generated 2026-10-14 21:46 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +93.1% | -2.0% | ±6.7% | `lr_schedule=linear`, `eps_start=0.5` |

## C1: mean_reward (paper 94.93)
**Fits but unsupported** · gap +93.1% → -2.0% · 55 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0097`, `B0157`, `B0158`, `B0159`, `B0160` (5 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `linear`
- Config: `eps_start` naive `1.0`, changed to `0.5`
- Command:

  Replay: fork checkpoint `afabd2e4-eb5f-499a-9091-cef9e396255c` and run
  ```
  RUN_TAG=84b52c76f974 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule linear --eps_start 0.5 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 88.59, 126.3, 76.19, 93.02, 106.3; gap after -2.0%; result checkpoint `ac676e53-2a3b-41e9-99ea-718a074fb64b`
- Effect: candidate 93.02 minus naive 183.3 = -90.27, 95% bootstrap interval [-102.3, -56.59] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 94.9 on CartPole; the worst of its seeds reaches 63.9.

- p. 1; value used: `mean_reward` = 94.93 (headline claim)

### What did we measure?
- Naive median 183.3 over 5 runs; repeats: 186.5, 179.3, 183.3, 162.4, 186.4
- Spread: range 162.4 to 186.5, noise band ±6.35 (2 x MAD), CV 5.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +93.1% (noise band ±6.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is +30.1% (it comes back)
- PASS · Counterfactual (reversal test): without `eps_start` the gap is +74.9% (it comes back)
- PASS · Held-out claim: C2: +41.5% to -83.1% (not worse beyond noise)
- FAIL · Evidence: `lr_schedule=linear`: no evidence mentions 'linear'; it fits, but nothing says the authors used it
- FAIL · Evidence: `eps_start=0.5`: no evidence mentions '0.5'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -90.27 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=100` (12.43 noise units, gap -10.0%); `max_steps=40` (5.26 noise units, gap -57.9%); `eps_start=0.2` (4.99 noise units, gap -59.7%); `lr_schedule=inv` (4.42 noise units, gap +63.5%); `eps_start=0.0` (3.62 noise units, gap -68.9%) (and 5 more in the JSON)
- Near alternatives (closest across all claims):
  - `max_steps=100`: this claim +4.6%, mean |gap| 25.6% (6 runs)
  - `lr_schedule=linear`, `max_steps=100`: this claim +3.4%, mean |gap| 25.8% (5 runs)
  - `max_steps=100`, `lr_schedule=inv`: this claim -12.9%, mean |gap| 33.2% (5 runs)

### History matching (every measured configuration, all claims together)
- 5 of 55 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 5 configurations
  - `max_steps`: max_steps=100 (max I 0.68)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 1.1); lr_schedule=inv, max_steps=100 (max I 1.3)
  - `eps_start, max_steps`: eps_start=0.5, max_steps=100 (max I 1.82)
  - `eps_start, lr_schedule`: eps_start=0.5, lr_schedule=linear (max I 1.83)
- 2 separate islands (no single-knob move joins them): max_steps=100; lr_schedule=linear, max_steps=100; lr_schedule=inv, max_steps=100 | eps_start=0.5, lr_schedule=linear

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'eps_start': '0.0', 'lr_schedule': 'linear'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 6 | +4.6% | +46.6% | 25.6% |
| `lr_schedule=linear`, `max_steps=100` | 5 | +3.4% | +48.1% | 25.8% |
| `max_steps=100`, `lr_schedule=inv` | 5 | -12.9% | -53.6% | 33.2% |
| `lr_schedule=inv` | 6 | +45.2% | -34.6% | 39.9% |
| `lr_schedule=linear`, `eps_start=0.5` | 5 | -2.0% | -83.1% | 42.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `e0f13d101585ad1609a15fbf67b70128f4cfffc8` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
