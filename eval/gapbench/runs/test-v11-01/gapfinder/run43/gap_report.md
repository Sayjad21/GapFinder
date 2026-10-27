# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-14 21:27 · 171 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -53.4% | -6.3% | ±6.1% | `max_steps=500`, `init_q=0` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -53.4% → -6.3% · 50 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0102`, `B0148`, `B0149`, `B0150`, `B0151` (5 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `500`
- Config: `init_q` naive `0.0`, changed to `0`
- Command:

  Replay: fork checkpoint `e8885bfb-f09e-46cc-9709-eea5bce4a501` and run
  ```
  RUN_TAG=6c378ebd0abd "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 500 --init_q 0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 227.1, 281, 403.3, 331.1, 359.5; gap after -6.3%; result checkpoint `1a45d45e-db96-4401-9592-8c72b6ec851e`
- Effect: candidate 331.1 minus naive 164.9 = +166.2, 95% bootstrap interval [+77.67, +223.9] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 164.9 over 5 runs; repeats: 152.9, 164.9, 177.7, 154.1, 175.3
- Spread: range 152.9 to 177.7, noise band ±21.6 (2 x MAD), CV 7.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -53.4% (noise band ±6.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -52.0% (it comes back)
- PASS · Counterfactual (reversal test): without `init_q` the gap is -25.7% (it comes back)
- PASS · Held-out claim: C2: +6.5% to +29.3% (not worse beyond noise)
- FAIL · Evidence: `max_steps=500`: no evidence mentions '500'; it fits, but nothing says the authors used it
- FAIL · Evidence: `init_q=0`: no evidence mentions '0'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +166.2 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `g`, `mc`, `mp`, `l`, `f`, `dt`, `seed_generation`, `reward_per_step`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=400` (7.57 noise units, gap +7.1%); `max_steps=2000` (4.03 noise units, gap -28.7%); `max_steps=1000` (3.11 noise units, gap -34.3%); `init_q=1.0` (1.54 noise units, gap -43.9%); `gamma=0.999` (1.38 noise units, gap -44.9%)
- Near alternatives (closest across all claims):
  - `max_steps=10000`: this claim -10.1%, mean |gap| 11.2% (6 runs)
  - `max_steps=1000`: this claim +9.5%, mean |gap| 14.9% (6 runs)
  - `gamma=0.998`, `max_steps=500`: this claim -15.0%, mean |gap| 17.5% (5 runs)

### History matching (every measured configuration, all claims together)
- 2 of 49 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 2 configurations
  - `max_steps`: max_steps=1000 (max I 0.2); max_steps=10000 (max I 1.35)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=10000` | 6 | -10.1% | -12.4% | 11.2% |
| `max_steps=1000` | 6 | +9.5% | -20.4% | 14.9% |
| `gamma=0.998`, `max_steps=500` | 5 | -15.0% | +20.1% | 17.5% |
| `init_q=0`, `max_steps=500` | 5 | -6.3% | +29.3% | 17.8% |
| `max_steps=400`, `init_q=0` | 5 | -21.9% | +15.5% | 18.7% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `init_q=zero`: invalid_value, The argument --init_q expects a floating‑point number, but the supplied value 'zero' cannot be parsed as a float, causing the program to reject it; retried as `init_q=0`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `g`, `mc`, `mp`, `l`, `f`, `dt`, `seed_generation`, `reward_per_step`

## Provenance
- GapFinder commit: `634d827f07d6659ff82f6ea0924c8ba487e9d02a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
