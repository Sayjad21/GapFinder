# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-15 01:12 · 199 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -48.0% | +0.2% | ±4.9% | `max_steps=400`, `gamma=0.998` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -48.0% → +0.2% · 54 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0136`, `B0192`, `B0193`, `B0194`, `B0195` (5 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `400`
- Config: `gamma` naive `0.99`, changed to `0.998`
- Command:

  Replay: fork checkpoint `7f1a7fa5-c8ec-4236-b012-fc826f6909ad` and run
  ```
  RUN_TAG=caa286d72483 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.998 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 400 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 354.3, 400, 328.8, 372.8, 312.9; gap after +0.2%; result checkpoint `c63423b2-f5de-479a-beb8-28ec1179c045`
- Effect: candidate 354.3 minus naive 183.8 = +170.5, 95% bootstrap interval [+133.9, +215.6] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 183.8 over 5 runs; repeats: 197.6, 185.4, 175.2, 169.1, 183.8
- Spread: range 169.1 to 197.6, noise band ±17.27 (2 x MAD), CV 6.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -48.0% (noise band ±4.9% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -45.1% (it comes back)
- PASS · Counterfactual (reversal test): without `gamma` the gap is -27.2% (it comes back)
- PASS · Held-out claim: C2: +212.2% to +206.6% (not worse beyond noise)
- FAIL · Evidence: `max_steps=400`: no evidence mentions '400'; it fits, but nothing says the authors used it
- FAIL · Evidence: `gamma=0.998`: no evidence mentions '0.998'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +170.5 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=500` (8.44 noise units, gap -6.7%); `max_steps=1000` (3.99 noise units, gap +28.5%); `max_steps=2000` (3.93 noise units, gap -28.8%)
- Near alternatives (closest across all claims):
  - `max_steps=500`, `gamma=0.999`: this claim +2.4%, mean |gap| 5.0% (5 runs)
  - `max_steps=2000`, `gamma=0.995`: this claim -2.0%, mean |gap| 6.3% (5 runs)
  - `max_steps=1000`: this claim +7.3%, mean |gap| 12.5% (6 runs)

### History matching (every measured configuration, all claims together)
- 14 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `max_steps`: max_steps=10000 (max I 0.19); max_steps=2000 (max I 0.6); max_steps=1000 (max I 2.03)
  - `gamma, max_steps`: gamma=0.995, max_steps=1000 (max I 0.57); gamma=0.998, max_steps=500 (max I 0.92); gamma=0.999, max_steps=500 (max I 0.92); gamma=1.0, max_steps=400 (max I 1.17); +3 more

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'max_steps': '1000', 'gamma': '1.0'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=500`, `gamma=0.999` | 5 | +2.4% | +7.5% | 5.0% |
| `max_steps=2000`, `gamma=0.995` | 5 | -2.0% | +10.6% | 6.3% |
| `max_steps=1000` | 6 | +7.3% | -17.7% | 12.5% |
| `max_steps=500`, `gamma=0.998` | 5 | +9.9% | +26.9% | 18.4% |
| `max_steps=10000` | 6 | -23.4% | -21.3% | 22.4% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
