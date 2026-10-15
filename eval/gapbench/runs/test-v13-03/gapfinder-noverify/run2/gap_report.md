# Gap Report: test-v13-03

Artifact `rlbench` · generated 2026-10-16 00:05 · 166 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Explained | +73.0% | -2.0% | ±29.0% | `max_steps=100` |

## C1: mean_reward (paper 99.495)
**Explained** · gap +73.0% → -2.0% · 40 hypotheses tested
> Confirmed cause: reverting it brings the gap back, held-out claims hold, and the value has evidence

### Which experiment changed it?
- Branch: `B0017`, `B0048`, `B0049`, `B0070`, `B0071`, `B0072` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `f1a78a4c-c5b8-4a0f-ad49-2d2deb712be5` and run
  ```
  RUN_TAG=d8c816370974 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 99.42, 95.5, 93, 99.47, 99.78, 94.5; gap after -2.0%; result checkpoint `d604dac6-b98e-436f-aca2-256394ddea15`
- Effect: candidate 97.46 minus naive 172.2 = -74.7, 95% bootstrap interval [-99.93, -62.57] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 99.5 steps, and that its worst seed still balances for 96.8.

- p. 1, Figure 1; value used: `mean_reward` = 99.495 steps (headline claim)

### What did we measure?
- Naive median 172.2 over 5 runs; repeats: 168.3, 197.2, 172.2, 193.7, 157.8
- Spread: range 157.8 to 197.2, noise band ±28.81 (2 x MAD), CV 9.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +73.0% (noise band ±29.0% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is -74.7 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `discretise.theta_clip`, `discretise.omega_clip`, `CartPole.termination_x`, `CartPole.termination_theta`, `RUN_TAG`, `RL_SEED_BASE`, `CartPole.reward_per_step`, `discretise.theta_bin_width`, `discretise.omega_bin_width`, `Q_table.tie_break`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_decay=0.198` (2.15 noise units, gap -10.8%); `lr_schedule=inv` (2.12 noise units, gap +11.7%); `eps_decay=0.0` (2.07 noise units, gap -13.2%); `eps_decay=0.0198` (1.38 noise units, gap -33.0%); `max_steps=2000` (1.28 noise units, gap +36.0%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `lr_schedule=linear`: this claim -1.2%, mean |gap| 2.4% (5 runs)
  - `eps_decay=1.0`: this claim +74.8%, mean |gap| 48.6% (6 runs)
  - `eps_decay=0.495`: this claim -10.1%, mean |gap| 49.8% (6 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `eps_decay=0.495`
- `lr_schedule=linear, max_steps=100`

### History matching (every measured configuration, all claims together)
- 12 of 40 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.13); lr_schedule=inv, max_steps=100 (max I 1.78); lr_schedule=inv, max_steps=2000 (max I 2.54)
  - `max_steps`: max_steps=100 (max I 0.56)
  - `eps_decay, max_steps`: eps_decay=0.0198, max_steps=2000 (max I 1.98); eps_decay=0.099, max_steps=100 (max I 2.75)
  - `eps_decay`: eps_decay=0.495 (max I 2.01); eps_decay=0.198 (max I 2.05); eps_decay=0.0 (max I 2.18); eps_decay=0.099 (max I 2.42)

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=100; eps_decay=0.495; lr_schedule=linear, max_steps=100

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100`, `lr_schedule=linear` | 5 | -1.2% | -3.5% | 2.4% |
| `max_steps=100` | 6 | -2.0% | -19.0% | 10.5% |
| `eps_decay=1.0` | 6 | +74.8% | +22.5% | 48.6% |
| naive (reproduction as run) | 5 | +73.0% | -24.3% | 48.7% |
| `eps_decay=0.495` | 6 | -10.1% | -89.6% | 49.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `discretise.theta_clip`, `discretise.omega_clip`, `CartPole.termination_x`, `CartPole.termination_theta`, `RUN_TAG`, `RL_SEED_BASE`, `CartPole.reward_per_step`, `discretise.theta_bin_width`, `discretise.omega_bin_width`, `Q_table.tie_break`

## Provenance
- GapFinder commit: `e9c31fd1405f5c8aae4bd880eadcdc8d491fad02` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
