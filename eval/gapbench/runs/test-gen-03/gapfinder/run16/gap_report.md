# Gap Report: test-gen-03

Artifact `rlbench` · generated 2026-10-13 20:59 · 51 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -36.1% | -2.3% | ±2.4% | `max_steps=400` |

## C1: mean_reward (paper 302.05)
**Fits but unsupported** · gap -36.1% → -2.3% · 12 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0011`, `B0039`, `B0040`, `B0041`, `B0042`, `B0043` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `400`
- Command:

  Replay: fork checkpoint `d1caa356-ed23-4b4a-8d93-0ac05390e5e8` and run
  ```
  RUN_TAG=b878aa85a6d3 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 400 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 327, 225.5, 296.8, 314.4, 293.1, 202.8; gap after -2.3%; result checkpoint `d2b22868-95ed-479a-ab8d-19851ee427c8`
- Effect: candidate 295 minus naive 192.9 = +102.1, 95% bootstrap interval [+30.3, +136.4] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 302.1 steps, and that its worst seed still balances for 48.2.

- p. 1; value used: `mean_reward` = 302.05 steps (headline claim)

### What did we measure?
- Naive median 192.9 over 5 runs; repeats: 144.3, 196.5, 192.9, 170.1, 195.9
- Spread: range 144.3 to 196.5, noise band ±7.33 (2 x MAD), CV 12.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -36.1% (noise band ±2.4% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -36.1% (it comes back)
- PASS · Held-out claim: C2: +228.9% to +18.3% (not worse beyond noise)
- FAIL · Evidence: `max_steps=400`: no evidence mentions '400'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +102.1 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=500` (12.14 noise units, gap +6.7%); `max_steps=2000` (2.64 noise units, gap +29.7%)
- Near alternatives (closest across all claims):
  - `max_steps=2000`: this claim +9.7%, mean |gap| 23.2% (6 runs)
  - `lr_schedule=linear`, `max_steps=500`: this claim -32.0%, mean |gap| 24.7% (5 runs)
  - `max_steps=500`: this claim +17.4%, mean |gap| 37.6% (6 runs)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=400` | 6 | -2.3% | +18.3% | 10.3% |
| `max_steps=2000` | 6 | +9.7% | -36.6% | 23.2% |
| `lr_schedule=linear`, `max_steps=500` | 5 | -32.0% | +17.5% | 24.7% |
| `max_steps=500` | 6 | +17.4% | +57.7% | 37.6% |
| `max_steps=1000` | 6 | +8.6% | +69.4% | 39.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`

## Provenance
- GapFinder commit: `c5b1a93e0b25688f10e132758f8a6371b4ebbf19` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `7e8e15007902d4b39f8940e3fb2a13a0e258c9d87b46215a72cd3b65ed9d57d9`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
