# Gap Report: test-gen-03

Artifact `rlbench` · generated 2026-10-15 00:17 · 87 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -42.1% | -0.1% | ±4.9% | `max_steps=500` |

## C1: mean_reward (paper 302.05)
**Fits but unsupported** · gap -42.1% → -0.1% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0006`, `B0018`, `B0019`, `B0041`, `B0042`, `B0043` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `500`
- Command:

  Replay: fork checkpoint `952b5a56-6de0-4748-b8fe-06a4df9dc3d3` and run
  ```
  RUN_TAG=e929578d1a92 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 500 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 342.9, 266.7, 233.7, 314.1, 289.4, 339.7; gap after -0.1%; result checkpoint `ce983d57-7611-4052-a9db-44fa4611356d`
- Effect: candidate 301.7 minus naive 174.9 = +126.8, 95% bootstrap interval [+63.7, +156.5] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 302.1 steps, and that its worst seed still balances for 48.2.

- p. 1; value used: `mean_reward` = 302.05 steps (headline claim)

### What did we measure?
- Naive median 174.9 over 5 runs; repeats: 182.2, 174.9, 169.6, 167.4, 196.4
- Spread: range 167.4 to 196.4, noise band ±14.69 (2 x MAD), CV 6.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -42.1% (noise band ±4.9% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -42.1% (it comes back)
- PASS · Held-out claim: C2: +29.5% to +4.9% (not worse beyond noise)
- FAIL · Evidence: `max_steps=500`: no evidence mentions '500'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +126.8 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=1000` (8.47 noise units, gap +0.9%); `max_steps=400` (8.29 noise units, gap +1.8%); `max_steps=2000` (5.51 noise units, gap -15.3%); `max_steps=10000` (3.13 noise units, gap +26.9%)
- Near alternatives (closest across all claims):
  - `max_steps=1000`: this claim -3.0%, mean |gap| 1.5% (6 runs)
  - `max_steps=2000`: this claim -14.7%, mean |gap| 39.2% (6 runs)
  - `max_steps=10000`: this claim +58.3%, mean |gap| 42.1% (6 runs)

### History matching (every measured configuration, all claims together)
- 4 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 4 configurations
  - `max_steps`: max_steps=500 (max I 0.42); max_steps=2000 (max I 0.64); max_steps=1000 (max I 1.07); max_steps=400 (max I 1.33)
- Equally good values: `max_steps` in {500, 1000}

Notes:
- equally good values within one noise band (measured): max_steps in {500, 1000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=1000` | 6 | -3.0% | +0.1% | 1.5% |
| `max_steps=500` | 6 | -0.1% | +4.9% | 2.5% |
| naive (reproduction as run) | 5 | -42.1% | +29.5% | 35.8% |
| `max_steps=2000` | 6 | -14.7% | -63.7% | 39.2% |
| `max_steps=10000` | 6 | +58.3% | -25.8% | 42.1% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
