# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-14 21:27 · 199 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -46.4% | -4.6% | ±2.8% | `max_steps=400`, `gamma=0.999` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -46.4% → -4.6% · 54 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0134`, `B0168`, `B0169`, `B0170`, `B0171` (5 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `400`
- Config: `gamma` naive `0.99`, changed to `0.999`
- Command:

  Replay: fork checkpoint `8ec7566d-19b8-4542-8a59-dba922022e6f` and run
  ```
  RUN_TAG=52c384598bde "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.999 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 400 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 337.1, 400, 354, 310.6, 328.6; gap after -4.6%; result checkpoint `1d15a1b5-b843-4b21-8d60-a15d5cf42c0a`
- Effect: candidate 337.1 minus naive 189.3 = +147.8, 95% bootstrap interval [+127.3, +213.2] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 189.3 over 5 runs; repeats: 194.1, 189.4, 166.6, 189.3, 159.2
- Spread: range 159.2 to 194.1, noise band ±9.75 (2 x MAD), CV 8.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -46.4% (noise band ±2.8% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -50.1% (it comes back)
- PASS · Counterfactual (reversal test): without `gamma` the gap is -21.1% (it comes back)
- PASS · Held-out claim: C2: +159.9% to +254.0% (not worse beyond noise)
- FAIL · Evidence: `max_steps=400`: no evidence mentions '400'; it fits, but nothing says the authors used it
- FAIL · Evidence: `gamma=0.999`: no evidence mentions '0.999'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +147.8 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=2000` (15.94 noise units, gap -2.5%); `max_steps=10000` (7.87 noise units, gap -24.7%); `max_steps=500` (3.02 noise units, gap -38.1%)
- Near alternatives (closest across all claims):
  - `max_steps=2000`, `gamma=0.995`: this claim +6.9%, mean |gap| 10.3% (5 runs)
  - `max_steps=2000`: this claim +2.3%, mean |gap| 12.9% (6 runs)
  - `max_steps=1000`: this claim -13.6%, mean |gap| 18.5% (6 runs)

### History matching (every measured configuration, all claims together)
- 9 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 9 configurations
  - `max_steps`: max_steps=2000 (max I 0.37); max_steps=1000 (max I 2.53)
  - `gamma, max_steps`: gamma=0.995, max_steps=500 (max I 0.87); gamma=0.995, max_steps=10000 (max I 1.28); gamma=0.999, max_steps=500 (max I 1.66); gamma=0.995, max_steps=2000 (max I 1.78); +3 more
- Equally good values: `max_steps` in {400, 500}; `gamma` in {0.995, 0.999}

Notes:
- equally good values within one noise band (measured): max_steps in {400, 500}; gamma in {0.995, 0.999}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=2000`, `gamma=0.995` | 5 | +6.9% | +13.7% | 10.3% |
| `max_steps=2000` | 6 | +2.3% | -23.6% | 12.9% |
| `max_steps=1000` | 6 | -13.6% | +23.4% | 18.5% |
| `max_steps=500` | 6 | -19.7% | +18.5% | 19.1% |
| `max_steps=500`, `gamma=0.995` | 5 | -5.9% | -32.4% | 19.1% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `634d827f07d6659ff82f6ea0924c8ba487e9d02a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
