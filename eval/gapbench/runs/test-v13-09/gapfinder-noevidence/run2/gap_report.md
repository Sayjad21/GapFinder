# Gap Report: test-v13-09

Artifact `rlbench` · generated 2026-10-16 00:23 · 139 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +75.9% | -5.4% | ±27.0% | `max_steps=100` |

## C1: mean_reward (paper 99.495)
**Fits but unsupported** · gap +75.9% → -5.4% · 55 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0006`, `B0020`, `B0021`, `B0042`, `B0043`, `B0044` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `b09044b9-1641-47a5-af7d-b17eb975e755` and run
  ```
  RUN_TAG=9a7388e0fc3d "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 92.74, 99.42, 92.41, 95.56, 88.43, 96.78; gap after -5.4%; result checkpoint `c9396959-2c3c-48d8-80ff-30ffd94c3892`
- Effect: candidate 94.15 minus naive 175 = -80.88, 95% bootstrap interval [-100.5, -65.91] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 99.5 steps, and that its worst seed still balances for 96.8.

- p. 1; value used: `mean_reward` = 99.495 steps (headline claim)

### What did we measure?
- Naive median 175 over 5 runs; repeats: 160.4, 196.5, 175, 161.6, 187.2
- Spread: range 160.4 to 196.5, noise band ±26.87 (2 x MAD), CV 9.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +75.9% (noise band ±27.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +75.9% (it comes back)
- PASS · Held-out claim: C2: -45.6% to -49.7% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: evidence gate off: no evidence was looked for
- PASS · Effect vs noise: candidate minus naive is -80.88 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (1.05 noise units, gap +47.4%)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `max_steps=100`: this claim -1.3%, mean |gap| 1.7% (5 runs)
  - `init_q=1.0`, `max_steps=100`: this claim -3.1%, mean |gap| 17.1% (5 runs)
  - `init_q=-1.0`, `max_steps=100`: this claim -5.4%, mean |gap| 28.1% (5 runs)

### Equally good configurations
The target claim can't tell these 5 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `lr_schedule=linear, max_steps=100`
- `init_q=-1.0, max_steps=100`
- `init_q=1.0, max_steps=100`
- `lr_schedule=inv, max_steps=1000`

### History matching (every measured configuration, all claims together)
- 10 of 55 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.11); lr_schedule=inv, max_steps=100 (max I 1.52); lr_schedule=inv, max_steps=1000 (max I 1.89); lr_schedule=inv, max_steps=10000 (max I 2.06); +1 more
  - `init_q, max_steps`: init_q=1.0, max_steps=100 (max I 0.63); init_q=-1.0, max_steps=100 (max I 0.77)
  - `max_steps`: max_steps=100 (max I 1.15)
  - `init_q, lr_schedule`: init_q=1.0, lr_schedule=inv (max I 2.24); init_q=-1.0, lr_schedule=inv (max I 2.85)
- 2 separate islands (no single-knob move joins them): lr_schedule=linear, max_steps=100; init_q=1.0, max_steps=100; init_q=-1.0, max_steps=100 | init_q=1.0, lr_schedule=inv; init_q=-1.0, lr_schedule=inv

Notes:
- evidence gate off: no evidence was checked, so this cannot be labelled Explained
- lr_schedule dropped: with repeats, {'max_steps': '100', 'lr_schedule': 'linear'} fits {'max_steps': '100'}'s gap by less than one noise band, so it is not needed
- configurations the target claim can't tell apart from the answer: max_steps=100; lr_schedule=linear, max_steps=100; init_q=-1.0, max_steps=100; init_q=1.0, max_steps=100; lr_schedule=inv, max_steps=1000

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=linear`, `max_steps=100` | 5 | -1.3% | -2.1% | 1.7% |
| `init_q=1.0`, `max_steps=100` | 5 | -3.1% | -31.1% | 17.1% |
| `max_steps=100` | 6 | -5.4% | -49.7% | 27.6% |
| `init_q=-1.0`, `max_steps=100` | 5 | -5.4% | -50.7% | 28.1% |
| `max_steps=1000`, `lr_schedule=inv` | 2 | +27.2% | -49.9% | 38.5% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`

## Provenance
- GapFinder commit: `e9c31fd1405f5c8aae4bd880eadcdc8d491fad02` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
