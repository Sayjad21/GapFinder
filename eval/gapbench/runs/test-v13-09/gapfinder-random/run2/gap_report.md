# Gap Report: test-v13-09

Artifact `rlbench` · generated 2026-10-16 00:23 · 112 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Paper-artifact inconsistency | +96.0% | -3.5% | ±3.3% | `max_steps=100` |

## C1: mean_reward (paper 99.495)
**Paper-artifact inconsistency** · gap +96.0% → -3.5% · 54 hypotheses tested
> Confirmed cause: reverting it brings the gap back, held-out claims hold, and the value has evidence

### Which experiment changed it?
- Branch: `B0010`, `B0026`, `B0027`, `B0034` (4 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `1f9e8073-5426-4843-af0b-4c1e77002716` and run
  ```
  RUN_TAG=ab863c2d3572 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 93.1, 90.05, 100, 98.95; gap after -3.5%; result checkpoint `aac18088-db70-438f-a28f-7916dd9dcefa`
- Effect: candidate 96.03 minus naive 195.1 = -99.03, 95% bootstrap interval [-103.9, -82.45] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 99.5 steps, and that its worst seed still balances for 96.8.

- p. 1; value used: `mean_reward` = 99.495 steps (headline claim)

### What did we measure?
- Naive median 195.1 over 5 runs; repeats: 196.7, 177.9, 195.1, 183.7, 196.3
- Spread: range 177.9 to 196.7, noise band ±3.33 (2 x MAD), CV 4.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +96.0% (noise band ±3.3% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +96.0% (it comes back)
- PASS · Held-out claim: C2: +68.9% to -29.2% (not worse beyond noise)
- PASS · Evidence: `max_steps=100`: paper states '100'
- PASS · Effect vs noise: candidate minus naive is -99.03 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (27.38 noise units, gap -4.4%); `max_steps=40` (10.79 noise units, gap -59.9%); `init_q=-1.0` (10.73 noise units, gap +60.1%); `lr_schedule=linear` (9.13 noise units, gap +65.5%); `init_q=1.0` (8.5 noise units, gap +67.6%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `init_q=-1.0`: this claim -0.3%, mean |gap| 0.7% (3 runs)
  - `max_steps=100`, `init_q=1.0`: this claim -0.2%, mean |gap| 1.0% (3 runs)
  - `lr_schedule=linear`, `max_steps=100`: this claim -2.2%, mean |gap| 3.3% (3 runs)

### Equally good configurations
The target claim can't tell these 4 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `init_q=-1.0, max_steps=100`
- `init_q=1.0, max_steps=100`
- `lr_schedule=linear, max_steps=100`

### History matching (every measured configuration, all claims together)
- 6 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 6 configurations
  - `init_q, max_steps`: init_q=-1.0, max_steps=100 (max I 0.32); init_q=1.0, max_steps=100 (max I 0.35)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.69); lr_schedule=inv, max_steps=100 (max I 1.97)
  - `max_steps`: max_steps=100 (max I 0.82)
  - `init_q, lr_schedule`: init_q=-1.0, lr_schedule=inv (max I 2.96)
- 2 separate islands (no single-knob move joins them): init_q=-1.0, max_steps=100; init_q=1.0, max_steps=100; lr_schedule=linear, max_steps=100 | init_q=-1.0, lr_schedule=inv

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=100; init_q=-1.0, max_steps=100; init_q=1.0, max_steps=100; lr_schedule=linear, max_steps=100

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100`, `init_q=-1.0` | 3 | -0.3% | -1.2% | 0.7% |
| `max_steps=100`, `init_q=1.0` | 3 | -0.2% | -1.9% | 1.0% |
| `lr_schedule=linear`, `max_steps=100` | 3 | -2.2% | -4.4% | 3.3% |
| `max_steps=100` | 4 | -3.5% | -29.2% | 16.3% |
| `init_q=1.0`, `lr_schedule=inv` | 3 | +49.8% | -22.3% | 36.1% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`

## Provenance
- GapFinder commit: `e9c31fd1405f5c8aae4bd880eadcdc8d491fad02` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
