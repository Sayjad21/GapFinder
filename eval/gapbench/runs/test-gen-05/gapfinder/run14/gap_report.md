# Gap Report: test-gen-05

Artifact `rlbench` · generated 2026-10-13 20:57 · 68 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +920.3% | +76.5% | ±63.3% | `eps_start=0.1` |

## C1: mean_reward (paper 17.31)
**Fits but unsupported** · gap +920.3% → +76.5% · 13 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0008`, `B0024`, `B0025`, `B0026`, `B0027`, `B0028` (6 run(s) of the same config)
- Config: `eps_start` naive `1.0`, changed to `0.1`
- Command:

  Replay: fork checkpoint `de74ba66-76f3-46e2-9d71-13f48008b4de` and run
  ```
  RUN_TAG=4f81611f6889 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 0.1 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 33.2, 69.12, 11.53, 41.42, 27.91, 25.54; gap after +76.5%; result checkpoint `905b7b7a-c4c2-4fcb-a7bc-12d6d116848c`
- Effect: candidate 30.55 minus naive 176.6 = -146.1, 95% bootstrap interval [-169.2, -119.6] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 17.3 steps, and that its worst seed still balances for 9.1.

- p. 1; value used: `mean_reward` = 17.31 steps (headline claim)

### What did we measure?
- Naive median 176.6 over 5 runs; repeats: 193.8, 171.1, 176.6, 192.8, 171.2
- Spread: range 171.1 to 193.8, noise band ±10.96 (2 x MAD), CV 6.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +920.3% (noise band ±63.3% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `eps_start` the gap is +920.3% (it comes back)
- PASS · Held-out claim: C2: +1122.0% to +1.4% (not worse beyond noise)
- FAIL · Evidence: `eps_start=0.1`: no evidence mentions '0.1'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -146.1 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.0` (14.22 noise units, gap +19.8%); `eps_start=0.02` (12.69 noise units, gap +117.0%); `eps_start=0.5` (5.19 noise units, gap +591.4%); `lr_schedule=inv` (4.37 noise units, gap +643.8%); `lr_schedule=linear` (1.3 noise units, gap +838.2%)
- Near alternatives (closest across all claims):
  - `eps_start=0.1`, `lr_schedule=linear`: this claim -2.5%, mean |gap| 2.1% (5 runs)
  - `eps_start=0.0`, `lr_schedule=inv`: this claim -28.6%, mean |gap| 14.9% (5 runs)
  - `eps_start=0.02`: this claim +37.2%, mean |gap| 18.7% (6 runs)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `eps_start=0.1`, `lr_schedule=linear` | 5 | -2.5% | +1.6% | 2.1% |
| `eps_start=0.0`, `lr_schedule=inv` | 5 | -28.6% | +1.1% | 14.9% |
| `eps_start=0.02` | 6 | +37.2% | +0.3% | 18.7% |
| `eps_start=0.02`, `lr_schedule=inv` | 5 | -40.3% | -0.5% | 20.4% |
| `eps_start=0.0`, `lr_schedule=linear` | 5 | -44.7% | +1.1% | 22.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `out`

## Provenance
- GapFinder commit: `c5b1a93e0b25688f10e132758f8a6371b4ebbf19` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `7e8e15007902d4b39f8940e3fb2a13a0e258c9d87b46215a72cd3b65ed9d57d9`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
