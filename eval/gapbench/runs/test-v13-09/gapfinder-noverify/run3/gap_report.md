# Gap Report: test-v13-09

Artifact `rlbench` · generated 2026-10-16 01:01 · 118 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Partially explained | +89.2% | -7.3% | ±17.3% | `max_steps=100` |

## C1: mean_reward (paper 99.495)
**Partially explained** · gap +89.2% → -7.3% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it closes only part of the gap, or the paper's own value was not tested

### Which experiment changed it?
- Branch: `B0006`, `B0018`, `B0019`, `B0042`, `B0043`, `B0044` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `b6530b04-47df-45c7-9cdd-5e9299e20028` and run
  ```
  RUN_TAG=e7f4d040742a "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 79.59, 94.8, 88.06, 99.51, 91.57, 92.91; gap after -7.3%; result checkpoint `a726115a-97c1-476e-a577-dea158dc4daa`
- Effect: candidate 92.24 minus naive 188.3 = -96.04, 95% bootstrap interval [-104, -64.64] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 99.5 steps, and that its worst seed still balances for 96.8.

- p. 1; value used: `mean_reward` = 99.495 steps (headline claim)

### What did we measure?
- Naive median 188.3 over 5 runs; repeats: 153, 188.3, 166.9, 195.3, 196.9
- Spread: range 153 to 196.9, noise band ±17.26 (2 x MAD), CV 10.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +89.2% (noise band ±17.3% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is -96.04 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `theta_clip_low`, `theta_clip_high`, `omega_clip_low`, `omega_clip_high`, `g`, `mc`, `mp`, `l`, `f`, `dt`, `init_state_low`, `init_state_high`, `theta_range`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (2.93 noise units, gap +38.4%); `max_steps=150` (2.76 noise units, gap +41.4%); `max_steps=40` (1.7 noise units, gap -59.8%); `lr_schedule=linear` (1 noise units, gap +71.9%)
- Near alternatives (closest across all claims):
  - `max_steps=150`: this claim +43.2%, mean |gap| 24.5% (6 runs)
  - `lr_schedule=linear`, `max_steps=100`: this claim -7.1%, mean |gap| 33.4% (5 runs)
  - `lr_schedule=linear`, `max_steps=150`: this claim +45.2%, mean |gap| 41.9% (2 runs)

### Equally good configurations
The target claim can't tell these 4 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `lr_schedule=inv, max_steps=150`
- `lr_schedule=linear, max_steps=100`
- `lr_schedule=inv, max_steps=1000`

### History matching (every measured configuration, all claims together)
- 8 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 8 configurations
  - `max_steps`: max_steps=100 (max I 0.99)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 1.03); lr_schedule=inv, max_steps=150 (max I 1.32); lr_schedule=inv, max_steps=100 (max I 1.52); lr_schedule=linear, max_steps=150 (max I 2.62); +2 more
  - `lr_schedule`: lr_schedule=inv (max I 2.52)

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=100; lr_schedule=inv, max_steps=150; lr_schedule=linear, max_steps=100; lr_schedule=inv, max_steps=1000

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=150` | 6 | +43.2% | +5.7% | 24.5% |
| `max_steps=100` | 6 | -7.3% | -51.2% | 29.3% |
| `lr_schedule=linear`, `max_steps=100` | 5 | -7.1% | -59.6% | 33.4% |
| `lr_schedule=linear`, `max_steps=150` | 2 | +45.2% | +38.5% | 41.9% |
| `lr_schedule=inv`, `max_steps=150` | 5 | +20.6% | -66.1% | 43.4% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `theta_clip_low`, `theta_clip_high`, `omega_clip_low`, `omega_clip_high`, `g`, `mc`, `mp`, `l`, `f`, `dt`, `init_state_low`, `init_state_high`, `theta_range`, `--out`

## Provenance
- GapFinder commit: `e9c31fd1405f5c8aae4bd880eadcdc8d491fad02` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
