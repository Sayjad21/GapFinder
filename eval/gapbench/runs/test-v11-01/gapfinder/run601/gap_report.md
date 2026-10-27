# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-14 22:31 · 199 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -47.3% | -1.4% | ±3.0% | `max_steps=1000` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -47.3% → -1.4% · 54 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0017`, `B0083`, `B0084`, `B0085`, `B0086`, `B0087` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `1000`
- Command:

  Replay: fork checkpoint `dcde2aa5-fbe3-45b3-8f30-c7e1bd94d803` and run
  ```
  RUN_TAG=04f7f8a7c755 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 1000 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 395.9, 315.1, 382.1, 386.3, 248.5, 275; gap after -1.4%; result checkpoint `050f2d2c-52e9-4c3d-8689-ab6cf5b7a5cd`
- Effect: candidate 348.6 minus naive 186.2 = +162.5, 95% bootstrap interval [+69.07, +209.6] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 186.2 over 5 runs; repeats: 187.8, 161.4, 191.4, 174.5, 186.2
- Spread: range 161.4 to 191.4, noise band ±10.53 (2 x MAD), CV 6.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -47.3% (noise band ±3.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -47.3% (it comes back)
- PASS · Held-out claim: C2: +209.6% to +17.7% (not worse beyond noise)
- FAIL · Evidence: `max_steps=1000`: no evidence mentions '1000'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +162.5 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=500` (13.19 noise units, gap -8.0%); `max_steps=400` (6.45 noise units, gap -28.1%); `gamma=1.0` (1.31 noise units, gap -43.4%); `gamma=0.999` (1.31 noise units, gap -43.4%); `gamma=0.998` (1.31 noise units, gap -43.4%)
- Near alternatives (closest across all claims):
  - `max_steps=1000`, `gamma=0.998`: this claim +7.0%, mean |gap| 7.2% (5 runs)
  - `max_steps=2000`: this claim +12.2%, mean |gap| 13.4% (6 runs)
  - `gamma=0.999`, `max_steps=500`: this claim -7.1%, mean |gap| 15.5% (5 runs)

### History matching (every measured configuration, all claims together)
- 15 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `gamma, max_steps`: gamma=0.95, max_steps=1000 (max I 0.52); gamma=0.999, max_steps=500 (max I 0.67); gamma=1.0, max_steps=500 (max I 1); gamma=0.999, max_steps=2000 (max I 1.25); +3 more
  - `max_steps`: max_steps=1000 (max I 1.02); max_steps=500 (max I 1.13)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=2000 (max I 1.6)
- 2 separate islands (no single-knob move joins them): gamma=0.95, max_steps=1000; gamma=0.999, max_steps=500; gamma=1.0, max_steps=500 | lr_schedule=linear, max_steps=2000

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'max_steps': '400', 'gamma': '0.998'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=1000`, `gamma=0.998` | 5 | +7.0% | +7.4% | 7.2% |
| `max_steps=1000` | 6 | -1.4% | +17.7% | 9.5% |
| `max_steps=2000` | 6 | +12.2% | -14.7% | 13.4% |
| `gamma=0.999`, `max_steps=500` | 5 | -7.1% | +24.0% | 15.5% |
| `max_steps=1000`, `gamma=0.999` | 5 | -7.6% | +37.1% | 22.3% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `e0f13d101585ad1609a15fbf67b70128f4cfffc8` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
