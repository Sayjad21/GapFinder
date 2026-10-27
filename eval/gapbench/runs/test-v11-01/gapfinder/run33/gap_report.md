# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-14 21:19 · 141 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -47.2% | -6.3% | ±3.3% | `max_steps=500` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -47.2% → -6.3% · 50 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0006`, `B0032`, `B0033`, `B0034`, `B0035`, `B0036` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `500`
- Command:

  Replay: fork checkpoint `68258b4a-ced6-4b00-a127-f9e32bddcc8a` and run
  ```
  RUN_TAG=ad4345acd451 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 500 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 334, 241.5, 342.5, 235.1, 350.4, 328.6; gap after -6.3%; result checkpoint `07b81a35-3152-4219-9cba-5b678dd19169`
- Effect: candidate 331.3 minus naive 186.6 = +144.7, 95% bootstrap interval [+53.51, +171] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 186.6 over 5 runs; repeats: 192.5, 187.2, 174.2, 186.6, 164.2
- Spread: range 164.2 to 192.5, noise band ±11.72 (2 x MAD), CV 6.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -47.2% (noise band ±3.3% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -47.2% (it comes back)
- PASS · Held-out claim: C2: +52.2% to +17.4% (not worse beyond noise)
- FAIL · Evidence: `max_steps=500`: no evidence mentions '500'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +144.7 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `g`, `mc`, `mp`, `l`, `f`, `dt`, `seed_generation`, `reward_per_step`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=400` (10.54 noise units, gap -12.2%); `max_steps=1000` (3.3 noise units, gap -36.3%)
- Near alternatives (closest across all claims):
  - `max_steps=400`, `gamma=0.998`: this claim -17.7%, mean |gap| 11.8% (5 runs)
  - `gamma=0.998`, `max_steps=500`: this claim +4.3%, mean |gap| 14.3% (5 runs)
  - `max_steps=2000`: this claim +5.3%, mean |gap| 17.5% (6 runs)

### History matching (every measured configuration, all claims together)
- 6 of 49 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 6 configurations
  - `gamma, max_steps`: gamma=0.998, max_steps=500 (max I 0.7); gamma=1.0, max_steps=400 (max I 1.98); gamma=0.998, max_steps=400 (max I 2.9)
  - `max_steps`: max_steps=400 (max I 2.48); max_steps=500 (max I 2.52)
  - `init_q, max_steps`: init_q=1.0, max_steps=400 (max I 2.73)
- Equally good values: `max_steps` in {500, 2000}

Notes:
- equally good values within one noise band (measured): max_steps in {500, 2000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=400`, `gamma=0.998` | 5 | -17.7% | +5.9% | 11.8% |
| `max_steps=500` | 6 | -6.3% | +17.4% | 11.8% |
| `gamma=0.998`, `max_steps=500` | 5 | +4.3% | +24.3% | 14.3% |
| `max_steps=2000` | 6 | +5.3% | +29.8% | 17.5% |
| `max_steps=10000` | 6 | -23.6% | +15.1% | 19.3% |

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
