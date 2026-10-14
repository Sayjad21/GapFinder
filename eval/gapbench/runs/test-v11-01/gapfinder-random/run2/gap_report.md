# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-14 11:33 · 92 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -47.6% | -2.3% | ±6.4% | `max_steps=500`, `gamma=1.0` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -47.6% → -2.3% · 46 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0035`, `B0077`, `B0078`, `B0079`, `B0080` (5 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `500`
- Config: `gamma` naive `0.99`, changed to `1.0`
- Command:

  Replay: fork checkpoint `4bf74cec-8c65-4674-a075-7f59a537d202` and run
  ```
  RUN_TAG=989752c9eb8b "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 1.0 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 500 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 329.2, 393.3, 345.1, 454.4, 330; gap after -2.3%; result checkpoint `7f457609-9882-4215-8120-ccb4f09d95b5`
- Effect: candidate 345.1 minus naive 185.1 = +160.1, 95% bootstrap interval [+145.6, +233.4] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 185.1 over 5 runs; repeats: 185.1, 196.5, 182.6, 198.5, 158
- Spread: range 158 to 198.5, noise band ±22.79 (2 x MAD), CV 8.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -47.6% (noise band ±6.4% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -45.9% (it comes back)
- PASS · Counterfactual (reversal test): without `gamma` the gap is -57.8% (it comes back)
- PASS · Held-out claim: C2: +211.0% to +59.4% (not worse beyond noise)
- FAIL · Evidence: `max_steps=500`: no evidence mentions '500'; it fits, but nothing says the authors used it
- FAIL · Evidence: `gamma=1.0`: no evidence mentions '1.0'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +160.1 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=1000` (5.23 noise units, gap +13.9%)
- Near alternatives (closest across all claims):
  - `max_steps=1000`: this claim -6.6%, mean |gap| 4.6% (6 runs)
  - `max_steps=1000`, `gamma=0.999`: this claim +7.2%, mean |gap| 8.9% (5 runs)
  - `max_steps=2000`, `gamma=1.0`: this claim +26.0%, mean |gap| 35.5% (5 runs)

### History matching (every measured configuration, all claims together)
- 6 of 46 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 6 configurations
  - `gamma, max_steps`: gamma=1.0, max_steps=500 (max I 0.83); gamma=0.999, max_steps=500 (max I 0.99); gamma=0.999, max_steps=1000 (max I 1.84); gamma=1.0, max_steps=2000 (max I 2)
  - `max_steps`: max_steps=1000 (max I 1.08)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=1000 (max I 2.87)
- Equally good values: `gamma` in {0.999, 1.0}

Notes:
- equally good values within one noise band (measured): gamma in {0.999, 1.0}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=1000` | 6 | -6.6% | -2.5% | 4.6% |
| `max_steps=1000`, `gamma=0.999` | 5 | +7.2% | +10.6% | 8.9% |
| `max_steps=500`, `gamma=1.0` | 5 | -2.3% | +59.4% | 30.9% |
| `max_steps=2000`, `gamma=1.0` | 5 | +26.0% | +45.1% | 35.5% |
| `gamma=0.95`, `max_steps=500` | 5 | -31.7% | -42.9% | 37.3% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `b05f7288e1a4df8af69bb0b5e7633827b4cb46c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
