# Gap Report: test-v13-03

Artifact `rlbench` · generated 2026-10-16 02:05 · 175 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +75.6% | -1.5% | ±14.6% | `max_steps=100` |

## C1: mean_reward (paper 99.495)
**Fits but unsupported** · gap +75.6% → -1.5% · 37 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0027`, `B0067`, `B0068`, `B0077`, `B0078`, `B0079` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `cd351e96-4c6e-479f-9b11-ba371bd3310d` and run
  ```
  RUN_TAG=222f391f2582 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 100, 99.46, 96.46, 96.47, 96.55, 99.76; gap after -1.5%; result checkpoint `774c2a72-e841-4698-a6ac-8eed74c8f9d3`
- Effect: candidate 98 minus naive 174.8 = -76.76, 95% bootstrap interval [-91.67, -64.39] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 99.5 steps

- p. 1; value used: `mean_reward` = 99.495 steps (headline claim)

### What did we measure?
- Naive median 174.8 over 5 runs; repeats: 160, 174.8, 170.2, 182, 189.9
- Spread: range 160 to 189.9, noise band ±14.53 (2 x MAD), CV 6.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +75.6% (noise band ±14.6% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +75.6% (it comes back)
- PASS · Held-out claim: C2: -37.2% to -12.9% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -76.76 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `theta_clamp_min`, `theta_clamp_max`, `omega_clamp_min`, `omega_clamp_max`, `cartpole_g`, `cartpole_mc`, `cartpole_mp`, `cartpole_l`, `cartpole_f`, `cartpole_dt`, `done_x_threshold`, `done_th_threshold`, `RL_SEED_BASE`, `RUN_TAG`, `discretization_formula`, `q_init_unseen_eval`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_decay=0.099` (4.33 noise units, gap +12.4%); `eps_decay=0.495` (3.28 noise units, gap +27.7%); `eps_decay=0.198` (2.33 noise units, gap -41.7%); `eps_decay=0.98` (1.85 noise units, gap +48.6%); `lr_schedule=inv` (1.71 noise units, gap +50.7%) (and 3 more in the JSON)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `init_q=1.0`: this claim +0.4%, mean |gap| 1.5% (5 runs)
  - `max_steps=100`, `lr_schedule=linear`: this claim -2.0%, mean |gap| 2.6% (5 runs)
  - `init_q=-1.0`, `max_steps=100`: this claim -7.3%, mean |gap| 26.6% (5 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `init_q=1.0, max_steps=100`
- `lr_schedule=linear, max_steps=100`

### History matching (every measured configuration, all claims together)
- 7 of 36 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 7 configurations
  - `init_q, max_steps`: init_q=1.0, max_steps=100 (max I 0.28); init_q=-1.0, max_steps=100 (max I 1.29)
  - `max_steps`: max_steps=100 (max I 0.4)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.52); lr_schedule=inv, max_steps=100 (max I 2.61)
  - `eps_decay`: eps_decay=0.495 (max I 2.56)
  - `eps_decay, init_q`: eps_decay=0.099, init_q=-1.0 (max I 2.93)
- 3 separate islands (no single-knob move joins them): init_q=1.0, max_steps=100; max_steps=100; lr_schedule=linear, max_steps=100 | eps_decay=0.495 | eps_decay=0.099, init_q=-1.0

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=100; init_q=1.0, max_steps=100; lr_schedule=linear, max_steps=100

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100`, `init_q=1.0` | 5 | +0.4% | +2.5% | 1.5% |
| `max_steps=100`, `lr_schedule=linear` | 5 | -2.0% | -3.3% | 2.6% |
| `max_steps=100` | 6 | -1.5% | -12.9% | 7.2% |
| `init_q=-1.0`, `max_steps=100` | 5 | -7.3% | -45.9% | 26.6% |
| `lr_schedule=linear` | 6 | +61.7% | +10.5% | 36.1% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `init_q=zero`: invalid_value, The argument --init_q expects a floating‑point number, but the supplied value 'zero' cannot be parsed as a float, causing the program to reject it; retried as `init_q=0`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `theta_clamp_min`, `theta_clamp_max`, `omega_clamp_min`, `omega_clamp_max`, `cartpole_g`, `cartpole_mc`, `cartpole_mp`, `cartpole_l`, `cartpole_f`, `cartpole_dt`, `done_x_threshold`, `done_th_threshold`, `RL_SEED_BASE`, `RUN_TAG`, `discretization_formula`, `q_init_unseen_eval`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
