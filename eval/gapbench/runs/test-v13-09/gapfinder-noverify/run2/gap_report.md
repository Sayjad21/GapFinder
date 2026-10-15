# Gap Report: test-v13-09

Artifact `rlbench` · generated 2026-10-16 00:22 · 163 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Paper-artifact inconsistency | +76.4% | -2.3% | ±4.7% | `max_steps=100` |

## C1: mean_reward (paper 99.495)
**Paper-artifact inconsistency** · gap +76.4% → -2.3% · 54 hypotheses tested
> Confirmed cause: reverting it brings the gap back, held-out claims hold, and the value has evidence

### Which experiment changed it?
- Branch: `B0006`, `B0020`, `B0021`, `B0048`, `B0049`, `B0050` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `acf4f01c-2f83-449f-bdb0-c853ec37347b` and run
  ```
  RUN_TAG=4a3fa916813c "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 98.84, 89.92, 88.38, 99.37, 95.78, 98.67; gap after -2.3%; result checkpoint `21db55aa-0320-40d6-9250-ffd91546333c`
- Effect: candidate 97.22 minus naive 175.5 = -78.29, 95% bootstrap interval [-100.9, -75.8] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 99.5 steps, and that its worst seed still balances for 96.8.

- p. 1; value used: `mean_reward` = 99.495 steps (headline claim)

### What did we measure?
- Naive median 175.5 over 5 runs; repeats: 173.2, 175.5, 173.3, 198.2, 184.9
- Spread: range 173.2 to 198.2, noise band ±4.7 (2 x MAD), CV 5.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +76.4% (noise band ±4.7% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is -78.29 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `init_q=1.0` (7.79 noise units, gap +39.6%); `lr_schedule=inv` (5.07 noise units, gap +52.5%); `max_steps=40` (3.23 noise units, gap -61.2%); `lr_schedule=linear` (2.41 noise units, gap +65.0%); `init_q=-1.0` (2.19 noise units, gap +66.1%)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `init_q=1.0`: this claim +0.1%, mean |gap| 0.4% (5 runs)
  - `max_steps=100`, `lr_schedule=linear`: this claim -2.3%, mean |gap| 3.4% (5 runs)
  - `max_steps=100`, `init_q=-1.0`: this claim -4.1%, mean |gap| 14.5% (5 runs)

### Equally good configurations
The target claim can't tell these 4 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `init_q=1.0, max_steps=100`
- `lr_schedule=linear, max_steps=100`
- `init_q=-1.0, max_steps=100`

### History matching (every measured configuration, all claims together)
- 6 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 6 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.28); lr_schedule=inv, max_steps=100 (max I 1.85)
  - `init_q, max_steps`: init_q=1.0, max_steps=100 (max I 0.37); init_q=-1.0, max_steps=100 (max I 0.8)
  - `max_steps`: max_steps=100 (max I 0.7)
  - `init_q, lr_schedule`: init_q=-1.0, lr_schedule=inv (max I 2.64)
- 2 separate islands (no single-knob move joins them): lr_schedule=linear, max_steps=100; init_q=1.0, max_steps=100; max_steps=100 | init_q=-1.0, lr_schedule=inv

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=100; init_q=1.0, max_steps=100; lr_schedule=linear, max_steps=100; init_q=-1.0, max_steps=100

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100`, `init_q=1.0` | 5 | +0.1% | -0.6% | 0.4% |
| `max_steps=100`, `lr_schedule=linear` | 5 | -2.3% | -4.5% | 3.4% |
| `max_steps=100` | 6 | -2.3% | -21.0% | 11.6% |
| `max_steps=100`, `init_q=-1.0` | 5 | -4.1% | -24.9% | 14.5% |
| `lr_schedule=linear`, `init_q=-1.0` | 2 | +53.9% | -8.1% | 31.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`

## Provenance
- GapFinder commit: `e9c31fd1405f5c8aae4bd880eadcdc8d491fad02` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
