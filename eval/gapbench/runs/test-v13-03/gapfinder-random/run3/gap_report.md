# Gap Report: test-v13-03

Artifact `rlbench` · generated 2026-10-16 00:39 · 166 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +92.9% | -3.8% | ±12.4% | `max_steps=100` |

## C1: mean_reward (paper 99.495)
**Fits but unsupported** · gap +92.9% → -3.8% · 51 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0029`, `B0057`, `B0058`, `B0061`, `B0062`, `B0063` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `b3124bc7-4d3c-47c9-8a7b-22019afed673` and run
  ```
  RUN_TAG=00e668116f20 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 87.99, 97.39, 94.63, 87.06, 100, 96.83; gap after -3.8%; result checkpoint `b7aee1ba-d2ae-45b6-8c86-338bc6d3b667`
- Effect: candidate 95.73 minus naive 191.9 = -96.19, 95% bootstrap interval [-105.6, -72.59] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 99.5 steps

- p. 1; value used: `mean_reward` = 99.495 steps (headline claim)

### What did we measure?
- Naive median 191.9 over 5 runs; repeats: 163.7, 179, 198.1, 197.7, 191.9
- Spread: range 163.7 to 198.1, noise band ±12.29 (2 x MAD), CV 7.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +92.9% (noise band ±12.4% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +92.9% (it comes back)
- PASS · Held-out claim: C2: +65.1% to -37.6% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -96.19 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `theta_clamp_min`, `theta_clamp_max`, `omega_clamp_min`, `omega_clamp_max`, `cartpole_g`, `cartpole_mc`, `cartpole_mp`, `cartpole_l`, `cartpole_f`, `cartpole_dt`, `done_x_threshold`, `done_th_threshold`, `RL_SEED_BASE`, `RUN_TAG`, `discretization_formula`, `q_init_unseen_eval`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_decay=0.198` (7.03 noise units, gap -6.0%); `eps_decay=0.0198` (5.52 noise units, gap -24.7%); `eps_decay=0.0` (4.13 noise units, gap -41.9%); `eps_decay=0.099` (4.01 noise units, gap -43.4%); `eps_decay=0.998` (3.83 noise units, gap +45.5%) (and 8 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `max_steps=100`: this claim -2.5%, mean |gap| 5.1% (5 runs)
  - `max_steps=100`, `init_q=1.0`: this claim -2.5%, mean |gap| 12.6% (5 runs)
  - `max_steps=100`, `init_q=-1.0`: this claim -6.8%, mean |gap| 30.3% (5 runs)

### Equally good configurations
The target claim can't tell these 5 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `eps_decay=0.495`
- `init_q=1.0, max_steps=100`
- `lr_schedule=linear, max_steps=100`
- `init_q=-1.0, max_steps=100`

### History matching (every measured configuration, all claims together)
- 8 of 50 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 8 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.2); lr_schedule=inv, max_steps=100 (max I 1.91)
  - `init_q, max_steps`: init_q=1.0, max_steps=100 (max I 0.49); init_q=-1.0, max_steps=100 (max I 0.92)
  - `max_steps`: max_steps=100 (max I 0.83)
  - `eps_decay`: eps_decay=0.0198 (max I 1.73); eps_decay=0.099 (max I 2.14)
  - `init_q, lr_schedule`: init_q=-1.0, lr_schedule=inv (max I 2.5)
- 3 separate islands (no single-knob move joins them): lr_schedule=linear, max_steps=100; init_q=1.0, max_steps=100; max_steps=100 | eps_decay=0.0198; eps_decay=0.099 | init_q=-1.0, lr_schedule=inv

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=100; eps_decay=0.495; init_q=1.0, max_steps=100; lr_schedule=linear, max_steps=100; init_q=-1.0, max_steps=100

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=linear`, `max_steps=100` | 5 | -2.5% | -7.6% | 5.1% |
| `max_steps=100`, `init_q=1.0` | 5 | -2.5% | -22.6% | 12.6% |
| `max_steps=100` | 6 | -3.8% | -37.6% | 20.7% |
| `max_steps=100`, `init_q=-1.0` | 5 | -6.8% | -53.9% | 30.3% |
| `init_q=-1.0`, `lr_schedule=inv` | 5 | +27.1% | -55.5% | 41.3% |

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
