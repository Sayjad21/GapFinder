# Gap Report: test-v13-03

Artifact `rlbench` · generated 2026-10-16 00:39 · 160 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +84.0% | -0.7% | ±9.5% | `max_steps=100` |

## C1: mean_reward (paper 99.495)
**Fits but unsupported** · gap +84.0% → -0.7% · 51 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0027`, `B0067`, `B0068`, `B0079` (4 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `04eef23f-a87f-4554-a44e-1be682b0e506` and run
  ```
  RUN_TAG=696d4075fb5f "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 99, 99.45, 91.67, 98.58; gap after -0.7%; result checkpoint `735255bb-e5be-4497-be78-07d1b49d532b`
- Effect: candidate 98.79 minus naive 183 = -84.23, 95% bootstrap interval [-95.29, -77.74] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 99.5 steps

- p. 1; value used: `mean_reward` = 99.495 steps (headline claim)

### What did we measure?
- Naive median 183 over 5 runs; repeats: 183, 181.1, 188.5, 174.7, 187.8
- Spread: range 174.7 to 188.5, noise band ±9.49 (2 x MAD), CV 3.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +84.0% (noise band ±9.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +84.0% (it comes back)
- PASS · Held-out claim: C2: -24.2% to -4.0% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: evidence gate off: no evidence was looked for
- PASS · Effect vs noise: candidate minus naive is -84.23 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `theta_clamp_min`, `theta_clamp_max`, `omega_clamp_min`, `omega_clamp_max`, `cartpole_g`, `cartpole_mc`, `cartpole_mp`, `cartpole_l`, `cartpole_f`, `cartpole_dt`, `done_x_threshold`, `done_th_threshold`, `RL_SEED_BASE`, `RUN_TAG`, `discretization_formula`, `q_init_unseen_eval`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_decay=0.495` (7.99 noise units, gap -7.8%); `lr_schedule=inv` (7.64 noise units, gap +11.1%); `eps_decay=0.0198` (7.08 noise units, gap +16.4%); `eps_decay=0.0` (6.09 noise units, gap -25.9%); `eps_decay=0.099` (5.97 noise units, gap -27.1%) (and 7 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `max_steps=100`: this claim -3.8%, mean |gap| 10.6% (3 runs)
  - `max_steps=100`, `init_q=0`: this claim -6.8%, mean |gap| 28.7% (3 runs)
  - `max_steps=100`, `lr_schedule=inv`: this claim -10.5%, mean |gap| 33.7% (3 runs)

### Equally good configurations
The target claim can't tell these 4 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `init_q=0, max_steps=100`
- `lr_schedule=linear, max_steps=100`
- `init_q=-1.0, max_steps=100`

### History matching (every measured configuration, all claims together)
- 8 of 50 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 8 configurations
  - `max_steps`: max_steps=100 (max I 0.63)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.86); lr_schedule=inv, max_steps=100 (max I 1.74)
  - `init_q, max_steps`: init_q=0, max_steps=100 (max I 0.95); init_q=-1.0, max_steps=100 (max I 1.22)
  - `eps_decay, init_q`: eps_decay=0.495, init_q=-1.0 (max I 2.48)
  - `eps_decay`: eps_decay=0.0198 (max I 2.69); eps_decay=0.495 (max I 2.91)
- 2 separate islands (no single-knob move joins them): max_steps=100; lr_schedule=linear, max_steps=100; init_q=0, max_steps=100 | eps_decay=0.495, init_q=-1.0; eps_decay=0.0198; eps_decay=0.495

Notes:
- evidence gate off: no evidence was checked, so this cannot be labelled Explained
- configurations the target claim can't tell apart from the answer: max_steps=100; init_q=0, max_steps=100; lr_schedule=linear, max_steps=100; init_q=-1.0, max_steps=100

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 4 | -0.7% | -4.0% | 2.4% |
| `lr_schedule=linear`, `max_steps=100` | 3 | -3.8% | -17.4% | 10.6% |
| `max_steps=100`, `init_q=0` | 3 | -6.8% | -50.5% | 28.7% |
| `max_steps=100`, `lr_schedule=inv` | 3 | -10.5% | -57.0% | 33.7% |
| `init_q=-1.0`, `lr_schedule=linear` | 2 | +49.8% | -19.3% | 34.6% |

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
