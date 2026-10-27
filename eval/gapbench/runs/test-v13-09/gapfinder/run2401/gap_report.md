# Gap Report: test-v13-09

Artifact `rlbench` · generated 2026-10-16 01:38 · 111 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Partially explained | +78.5% | -6.7% | ±20.3% | `max_steps=100` |

## C1: mean_reward (paper 99.495)
**Partially explained** · gap +78.5% → -6.7% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it closes only part of the gap, or the paper's own value was not tested

### Which experiment changed it?
- Branch: `B0006`, `B0018`, `B0019`, `B0046`, `B0047`, `B0048` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `b630a092-5ea8-4ed0-93ce-5d2566ba08af` and run
  ```
  RUN_TAG=8dcbc54f725a "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 91.69, 93.98, 95.06, 90, 95.94, 88.62; gap after -6.7%; result checkpoint `6c89d730-122a-4ceb-b1f3-510ef3f0d738`
- Effect: candidate 92.83 minus naive 177.6 = -84.73, 95% bootstrap interval [-94.69, -55.24] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 99.5 steps, and that its worst seed still balances for 96.8.

- p. 1; value used: `mean_reward` = 99.495 steps (headline claim)

### What did we measure?
- Naive median 177.6 over 5 runs; repeats: 177.6, 184.6, 139.1, 166.1, 187.6
- Spread: range 139.1 to 187.6, noise band ±20.15 (2 x MAD), CV 11.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +78.5% (noise band ±20.3% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +78.5% (it comes back)
- PASS · Held-out claim: C2: -45.6% to -45.8% (not worse beyond noise)
- PASS · Evidence: `max_steps=100`: paper states '100'
- PASS · Effect vs noise: candidate minus naive is -84.73 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (3.41 noise units, gap +9.4%)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `max_steps=100`: this claim -1.8%, mean |gap| 5.6% (5 runs)
  - `max_steps=400`, `lr_schedule=linear`: this claim +67.5%, mean |gap| 33.8% (2 runs)
  - `lr_schedule=inv`, `max_steps=1000`: this claim +63.2%, mean |gap| 35.5% (2 runs)

### Equally good configurations
The target claim can't tell these 2 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `lr_schedule=linear, max_steps=100`

### History matching (every measured configuration, all claims together)
- 8 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 8 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.74); lr_schedule=inv, max_steps=100 (max I 2.44); lr_schedule=linear, max_steps=40 (max I 2.67); lr_schedule=inv, max_steps=40 (max I 2.69); +2 more
  - `max_steps`: max_steps=100 (max I 1.94)
  - `lr_schedule`: lr_schedule=inv (max I 2.47)

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=100; lr_schedule=linear, max_steps=100

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=linear`, `max_steps=100` | 5 | -1.8% | -9.4% | 5.6% |
| `max_steps=100` | 6 | -6.7% | -45.8% | 26.3% |
| `max_steps=400`, `lr_schedule=linear` | 2 | +67.5% | -0.2% | 33.8% |
| `lr_schedule=inv`, `max_steps=1000` | 2 | +63.2% | -7.9% | 35.5% |
| `lr_schedule=inv`, `max_steps=100` | 5 | -12.3% | -66.4% | 39.3% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
