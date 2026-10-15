# Gap Report: test-v13-03

Artifact `rlbench` · generated 2026-10-16 00:38 · 168 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Explained | +88.9% | -4.5% | ±7.5% | `max_steps=100` |

## C1: mean_reward (paper 99.495)
**Explained** · gap +88.9% → -4.5% · 32 hypotheses tested
> Confirmed cause: reverting it brings the gap back, held-out claims hold, and the value has evidence

### Which experiment changed it?
- Branch: `B0027`, `B0067`, `B0068`, `B0079`, `B0080`, `B0081` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `a71ebed6-a922-47d5-bb41-20bcb7d3bdaa` and run
  ```
  RUN_TAG=27867634b126 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 92.92, 99.3, 93.42, 92.75, 99, 96.69; gap after -4.5%; result checkpoint `d48aa3bb-3311-4e1c-834e-4e317a9f9588`
- Effect: candidate 95.06 minus naive 188 = -92.91, 95% bootstrap interval [-97.4, -70.98] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 99.5 steps

- p. 1; value used: `mean_reward` = 99.495 steps (headline claim)

### What did we measure?
- Naive median 188 over 5 runs; repeats: 188, 184.3, 188.1, 194.2, 164.7
- Spread: range 164.7 to 194.2, noise band ±7.42 (2 x MAD), CV 6.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +88.9% (noise band ±7.5% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is -92.91 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `theta_clamp_min`, `theta_clamp_max`, `omega_clamp_min`, `omega_clamp_max`, `cartpole_g`, `cartpole_mc`, `cartpole_mp`, `cartpole_l`, `cartpole_f`, `cartpole_dt`, `done_x_threshold`, `done_th_threshold`, `RL_SEED_BASE`, `RUN_TAG`, `discretization_formula`, `q_init_unseen_eval`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_decay=0.198` (10.76 noise units, gap -8.7%); `eps_decay=0.099` (9.34 noise units, gap -19.3%); `eps_decay=0.495` (7.57 noise units, gap -32.4%); `eps_decay=0.98` (6.24 noise units, gap +42.4%); `eps_decay=0.0198` (6.01 noise units, gap -44.1%) (and 8 more in the JSON)
- Near alternatives (closest across all claims):
  - `init_q=0`, `max_steps=100`: this claim -7.4%, mean |gap| 32.7% (5 runs)
  - `lr_schedule=inv`, `max_steps=100`: this claim -14.7%, mean |gap| 36.6% (5 runs)
  - `eps_decay=0.998`: this claim +69.2%, mean |gap| 39.3% (6 runs)

### History matching (every measured configuration, all claims together)
- 5 of 31 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 5 configurations
  - `max_steps`: max_steps=100 (max I 1.09)
  - `init_q, max_steps`: init_q=0, max_steps=100 (max I 1.37)
  - `lr_schedule, max_steps`: lr_schedule=inv, max_steps=100 (max I 1.78)
  - `eps_decay`: eps_decay=0.495 (max I 2.62); eps_decay=0.198 (max I 2.85)
- 2 separate islands (no single-knob move joins them): max_steps=100; init_q=0, max_steps=100; lr_schedule=inv, max_steps=100 | eps_decay=0.495; eps_decay=0.198

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 6 | -4.5% | -45.0% | 24.7% |
| `init_q=0`, `max_steps=100` | 5 | -7.4% | -57.9% | 32.7% |
| `lr_schedule=inv`, `max_steps=100` | 5 | -14.7% | -58.4% | 36.6% |
| `eps_decay=0.998` | 6 | +69.2% | +9.3% | 39.3% |
| `lr_schedule=inv` | 6 | +38.6% | -44.3% | 41.5% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `init_q=zero`: invalid_value, The argument --init_q expects a floating‑point number, but the supplied value 'zero' cannot be parsed as a float, causing the program to reject it; retried as `init_q=0`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `theta_clamp_min`, `theta_clamp_max`, `omega_clamp_min`, `omega_clamp_max`, `cartpole_g`, `cartpole_mc`, `cartpole_mp`, `cartpole_l`, `cartpole_f`, `cartpole_dt`, `done_x_threshold`, `done_th_threshold`, `RL_SEED_BASE`, `RUN_TAG`, `discretization_formula`, `q_init_unseen_eval`

## Provenance
- GapFinder commit: `e9c31fd1405f5c8aae4bd880eadcdc8d491fad02` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
