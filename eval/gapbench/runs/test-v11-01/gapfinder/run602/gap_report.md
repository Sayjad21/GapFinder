# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-14 22:31 · 198 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -47.0% | +4.9% | ±3.1% | `gamma=0.999`, `max_steps=500` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -47.0% → +4.9% · 54 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0117`, `B0183`, `B0184`, `B0185`, `B0186` (5 run(s) of the same config)
- Config: `gamma` naive `0.99`, changed to `0.999`
- Config: `max_steps` naive `200`, changed to `500`
- Command:

  Replay: fork checkpoint `e49ccb70-6404-4335-aaa4-e1705b4da203` and run
  ```
  RUN_TAG=48ba24925f70 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.999 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 500 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 370.7, 401.3, 326.9, 326.2, 468.9; gap after +4.9%; result checkpoint `b44e5c9d-a063-464c-aa09-71ef697e513f`
- Effect: candidate 370.7 minus naive 187.2 = +183.5, 95% bootstrap interval [+133.3, +265.8] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 187.2 over 5 runs; repeats: 200, 184, 187.2, 171.9, 192.6
- Spread: range 171.9 to 200, noise band ±10.79 (2 x MAD), CV 5.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -47.0% (noise band ±3.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `gamma` the gap is -17.6% (it comes back)
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -45.5% (it comes back)
- PASS · Held-out claim: C2: +211.0% to +211.0% (not worse beyond noise)
- FAIL · Evidence: `gamma=0.999`: no evidence mentions '0.999'; it fits, but nothing says the authors used it
- FAIL · Evidence: `max_steps=500`: no evidence mentions '500'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +183.5 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=1000` (11.02 noise units, gap -13.4%); `max_steps=10000` (9.59 noise units, gap -17.7%); `max_steps=400` (9.58 noise units, gap -17.8%); `max_steps=2000` (2.76 noise units, gap +38.6%)
- Near alternatives (closest across all claims):
  - `max_steps=1000`: this claim -13.1%, mean |gap| 8.6% (6 runs)
  - `gamma=0.995`, `max_steps=500`: this claim -9.8%, mean |gap| 11.4% (5 runs)
  - `max_steps=10000`: this claim -19.4%, mean |gap| 12.1% (6 runs)

### History matching (every measured configuration, all claims together)
- 10 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `max_steps`: max_steps=1000 (max I 0.36); max_steps=10000 (max I 0.64)
  - `gamma, max_steps`: gamma=0.995, max_steps=1000 (max I 1); gamma=0.995, max_steps=500 (max I 1.38); gamma=1.0, max_steps=500 (max I 1.93); gamma=0.995, max_steps=400 (max I 2.08); +3 more
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=10000 (max I 2.41)

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'max_steps': '500', 'lr_schedule': 'linear'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=1000` | 6 | -13.1% | -4.2% | 8.6% |
| `gamma=0.995`, `max_steps=500` | 5 | -9.8% | +12.9% | 11.4% |
| `max_steps=10000` | 6 | -19.4% | -4.8% | 12.1% |
| `gamma=0.995`, `max_steps=1000` | 5 | -8.6% | +15.9% | 12.3% |
| `gamma=1.0`, `max_steps=1000` | 5 | -15.2% | -21.2% | 18.2% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `e0f13d101585ad1609a15fbf67b70128f4cfffc8` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
