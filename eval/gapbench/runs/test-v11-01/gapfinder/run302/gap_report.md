# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-14 21:45 · 194 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -43.9% | +0.0% | ±0.9% | `max_steps=400`, `gamma=1.0` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -43.9% → +0.0% · 54 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0120`, `B0187`, `B0188`, `B0189`, `B0190` (5 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `400`
- Config: `gamma` naive `0.99`, changed to `1.0`
- Command:

  Replay: fork checkpoint `4faf181e-247d-4362-bd70-fa1e7f50a3d0` and run
  ```
  RUN_TAG=95cf80a92db2 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 1.0 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 400 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 371.4, 355, 353.4, 319.6, 320.1; gap after +0.0%; result checkpoint `3f23e57b-f5c8-4c2b-b316-809b5cb9b44c`
- Effect: candidate 353.4 minus naive 198.4 = +155.1, 95% bootstrap interval [+124.8, +180.3] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 198.4 over 5 runs; repeats: 200, 179.6, 198.4, 180.7, 198.4
- Spread: range 179.6 to 200, noise band ±3.22 (2 x MAD), CV 5.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -43.9% (noise band ±0.9% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -45.7% (it comes back)
- PASS · Counterfactual (reversal test): without `gamma` the gap is -20.1% (it comes back)
- PASS · Held-out claim: C2: +324.2% to +244.1% (not worse beyond noise)
- FAIL · Evidence: `max_steps=400`: no evidence mentions '400'; it fits, but nothing says the authors used it
- FAIL · Evidence: `gamma=1.0`: no evidence mentions '1.0'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +155.1 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=500` (41.45 noise units, gap -6.1%); `max_steps=2000` (27.95 noise units, gap -18.4%); `max_steps=10000` (26.79 noise units, gap +19.5%); `max_steps=1000` (16.85 noise units, gap -28.5%)
- Near alternatives (closest across all claims):
  - `gamma=0.995`, `max_steps=10000`: this claim +3.7%, mean |gap| 2.8% (5 runs)
  - `gamma=0.999`, `max_steps=500`: this claim +9.9%, mean |gap| 6.0% (5 runs)
  - `max_steps=2000`, `gamma=0.998`: this claim +0.1%, mean |gap| 6.5% (5 runs)

### History matching (every measured configuration, all claims together)
- 14 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `gamma, max_steps`: gamma=0.998, max_steps=2000 (max I 0.36); gamma=0.998, max_steps=500 (max I 1.05); gamma=0.995, max_steps=10000 (max I 1.31); gamma=0.999, max_steps=500 (max I 1.49); +5 more
  - `max_steps`: max_steps=2000 (max I 1.75)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `gamma=0.995`, `max_steps=10000` | 5 | +3.7% | -1.8% | 2.8% |
| `gamma=0.999`, `max_steps=500` | 5 | +9.9% | -2.2% | 6.0% |
| `max_steps=2000`, `gamma=0.998` | 5 | +0.1% | +12.8% | 6.5% |
| `gamma=0.999`, `max_steps=10000` | 5 | +8.2% | -9.6% | 8.9% |
| `max_steps=400` | 6 | -20.1% | +4.0% | 12.1% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `e0f13d101585ad1609a15fbf67b70128f4cfffc8` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
