# Gap Report: test-v13-09

Artifact `rlbench` · generated 2026-10-16 01:39 · 160 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Paper-artifact inconsistency | +89.0% | -0.6% | ±10.3% | `max_steps=100` |

## C1: mean_reward (paper 99.495)
**Paper-artifact inconsistency** · gap +89.0% → -0.6% · 54 hypotheses tested
> Confirmed cause: reverting it brings the gap back, held-out claims hold, and the value has evidence

### Which experiment changed it?
- Branch: `B0006`, `B0020`, `B0021`, `B0044`, `B0045`, `B0046` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `38fa8c00-111d-49bf-b119-4b6f324c320b` and run
  ```
  RUN_TAG=8b920376108f "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 100, 98.67, 99.2, 99.5, 93.36, 90.88; gap after -0.6%; result checkpoint `d1f46d42-8700-4953-a7ec-f202745ad26e`
- Effect: candidate 98.94 minus naive 188.1 = -89.15, 95% bootstrap interval [-97.24, -54.5] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 99.5 steps, and that its worst seed still balances for 96.8.

- p. 1; value used: `mean_reward` = 99.495 steps (headline claim)

### What did we measure?
- Naive median 188.1 over 5 runs; repeats: 180.2, 193.2, 189.1, 141.5, 188.1
- Spread: range 141.5 to 193.2, noise band ±10.21 (2 x MAD), CV 11.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +89.0% (noise band ±10.3% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +89.0% (it comes back)
- PASS · Held-out claim: C2: -1.7% to -1.0% (not worse beyond noise)
- PASS · Evidence: `max_steps=100`: paper states '100'
- PASS · Effect vs noise: candidate minus naive is -89.15 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (3.37 noise units, gap +54.5%); `lr_schedule=linear` (3.25 noise units, gap +55.7%); `max_steps=40` (2.66 noise units, gap -61.7%)
- Near alternatives (closest across all claims):
  - `init_q=1.0`, `max_steps=100`: this claim -0.4%, mean |gap| 0.9% (5 runs)
  - `lr_schedule=linear`, `max_steps=100`: this claim -1.9%, mean |gap| 3.2% (5 runs)
  - `init_q=-1.0`, `max_steps=100`: this claim -3.5%, mean |gap| 17.7% (5 runs)

### Equally good configurations
The target claim can't tell these 4 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `init_q=1.0, max_steps=100`
- `lr_schedule=linear, max_steps=100`
- `init_q=-1.0, max_steps=100`

### History matching (every measured configuration, all claims together)
- 12 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.4); lr_schedule=inv, max_steps=100 (max I 2.08); lr_schedule=inv, max_steps=1000 (max I 2.31); lr_schedule=inv, max_steps=500 (max I 2.45); +1 more
  - `init_q, max_steps`: init_q=1.0, max_steps=100 (max I 0.42); init_q=-1.0, max_steps=100 (max I 1.06)
  - `max_steps`: max_steps=100 (max I 0.58)
  - `init_q, lr_schedule`: init_q=-1.0, lr_schedule=inv (max I 2.23)
  - `lr_schedule`: lr_schedule=inv (max I 2.6)

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=100; init_q=1.0, max_steps=100; lr_schedule=linear, max_steps=100; init_q=-1.0, max_steps=100

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 6 | -0.6% | -1.0% | 0.8% |
| `init_q=1.0`, `max_steps=100` | 5 | -0.4% | -1.5% | 0.9% |
| `lr_schedule=linear`, `max_steps=100` | 5 | -1.9% | -4.4% | 3.2% |
| `init_q=-1.0`, `max_steps=100` | 5 | -3.5% | -32.0% | 17.7% |
| `lr_schedule=linear`, `init_q=1.0` | 2 | +67.8% | +8.3% | 38.1% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
