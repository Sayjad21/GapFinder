# Gap Report: test-gen-03

Artifact `rlbench` · generated 2026-10-14 00:50 · 49 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -41.8% | +4.7% | ±1.1% | `max_steps=500` |

## C1: mean_reward (paper 302.05)
**Fits but unsupported** · gap -41.8% → +4.7% · 20 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0006`, `B0014`, `B0015`, `B0016` (4 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `500`
- Command:

  Replay: fork checkpoint `d91ae147-2182-4233-b1e3-da9ce636ac24` and run
  ```
  RUN_TAG=4baf8ecdd707 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 500 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 402.2, 334.6, 264.1, 298; gap after +4.7%; result checkpoint `e76ce612-3181-45dd-927a-31f1d18f2359`
- Effect: candidate 316.3 minus naive 175.8 = +140.5, 95% bootstrap interval [+85.42, +160] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 302.1 steps

- p. 1; value used: `mean_reward` = 302.05 steps (headline claim)

### What did we measure?
- Naive median 175.8 over 5 runs; repeats: 177.5, 171.3, 183.1, 175.8, 175
- Spread: range 171.3 to 183.1, noise band ±3.32 (2 x MAD), CV 2.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -41.8% (noise band ±1.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -41.8% (it comes back)
- PASS · Held-out claim: C2: +124.4% to +90.2% (not worse beyond noise)
- FAIL · Evidence: `max_steps=500`: no evidence mentions '500'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +140.5 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=1000` (1.64 noise units, gap +40.0%)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `max_steps=1000`: this claim -17.8%, mean |gap| 37.2% (3 runs)
  - `max_steps=2000`: this claim +85.6%, mean |gap| 44.9% (4 runs)
  - `max_steps=100`: this claim -68.4%, mean |gap| 45.9% (4 runs)

### History matching (every measured configuration, all claims together)
- 1 of 20 tested configurations fit every claim within 3 sigma

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=linear`, `max_steps=1000` | 3 | -17.8% | +56.6% | 37.2% |
| `max_steps=2000` | 4 | +85.6% | +4.1% | 44.9% |
| `max_steps=100` | 4 | -68.4% | +23.4% | 45.9% |
| `max_steps=500` | 4 | +4.7% | +90.2% | 47.4% |
| `max_steps=1000` | 4 | +53.0% | -63.6% | 58.3% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`

## Provenance
- GapFinder commit: `ee5bfaf3f91999664f6df4e7df12a48c78c40f73` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `fedcbdf1b57461a1273eeb81ccb09c30931e58de34a306249ffd0422bbf51ae6`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
