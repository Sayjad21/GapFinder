# Gap Report: test-v13-09

Artifact `rlbench` · generated 2026-10-16 02:08 · 136 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Paper-artifact inconsistency | +96.6% | -0.7% | ±5.3% | `max_steps=100` |

## C1: mean_reward (paper 99.495)
**Paper-artifact inconsistency** · gap +96.6% → -0.7% · 55 hypotheses tested
> Confirmed cause: reverting it brings the gap back, held-out claims hold, and the value has evidence

### Which experiment changed it?
- Branch: `B0006`, `B0020`, `B0021`, `B0046` (4 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `ee62204b-b858-4223-8ac9-9ffa9492f4b8` and run
  ```
  RUN_TAG=da9cbe9342a4 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 98.8, 99.31, 98.7, 95.66; gap after -0.7%; result checkpoint `f41a3118-d6df-430a-998e-a265bff88788`
- Effect: candidate 98.75 minus naive 195.6 = -96.88, 95% bootstrap interval [-101.4, -90.07] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 99.5 steps, and that its worst seed still balances for 96.8.

- p. 1; value used: `mean_reward` = 99.495 steps (headline claim)

### What did we measure?
- Naive median 195.6 over 5 runs; repeats: 198.3, 187.3, 191.7, 197.4, 195.6
- Spread: range 187.3 to 198.3, noise band ±5.31 (2 x MAD), CV 2.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +96.6% (noise band ±5.3% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +96.6% (it comes back)
- PASS · Held-out claim: C2: +82.5% to -5.4% (not worse beyond noise)
- PASS · Evidence: `max_steps=100`: paper states '100'
- PASS · Effect vs noise: candidate minus naive is -96.88 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=1000` (17.58 noise units, gap +2.8%); `lr_schedule=inv` (9.98 noise units, gap +43.4%); `max_steps=40` (6.9 noise units, gap -59.8%); `init_q=1.0` (6.14 noise units, gap +63.9%); `lr_schedule=linear` (5.41 noise units, gap +67.7%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `max_steps=100`: this claim -2.1%, mean |gap| 4.4% (3 runs)
  - `max_steps=100`, `init_q=-1.0`: this claim -3.2%, mean |gap| 11.0% (3 runs)
  - `init_q=1.0`, `max_steps=100`: this claim -3.4%, mean |gap| 17.4% (3 runs)

### Equally good configurations
The target claim can't tell these 4 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `init_q=1.0, max_steps=100`
- `lr_schedule=linear, max_steps=100`
- `init_q=-1.0, max_steps=100`

### History matching (every measured configuration, all claims together)
- 5 of 55 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 5 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.46); lr_schedule=inv, max_steps=100 (max I 2.68)
  - `max_steps`: max_steps=100 (max I 0.76)
  - `init_q, max_steps`: init_q=1.0, max_steps=100 (max I 1.57); init_q=-1.0, max_steps=100 (max I 2.05)

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=100; init_q=1.0, max_steps=100; lr_schedule=linear, max_steps=100; init_q=-1.0, max_steps=100

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 4 | -0.7% | -5.4% | 3.1% |
| `lr_schedule=linear`, `max_steps=100` | 3 | -2.1% | -6.6% | 4.4% |
| `max_steps=100`, `init_q=-1.0` | 3 | -3.2% | -18.8% | 11.0% |
| `init_q=1.0`, `max_steps=100` | 3 | -3.4% | -31.4% | 17.4% |
| `max_steps=100`, `lr_schedule=inv` | 3 | -5.4% | -38.2% | 21.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
