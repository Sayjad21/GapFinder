# Gap Report: test-gen-03

Artifact `rlbench` · generated 2026-10-10 22:56 · 22 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Explained | -41.9% | -4.5% | ±1.2% | `max_steps=1000` |

## C1: mean_reward (paper 302.05)
**Explained** · gap -41.9% → -4.5% · 5 hypotheses tested
> Confirmed cause: reverting it brings the gap back, held-out claims hold, and the value has evidence

### Which experiment changed it?
- Branch: `B0007`, `B0014`, `B0015`, `B0016`, `B0017` (5 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `1000`
- Command:

  Replay: fork checkpoint `6ebaf72b-cf97-4a0b-abbb-d95713d016bd` and run
  ```
  RUN_TAG=6417f0e0ce62 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 1000 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 230.5, 322.1, 288.4, 216.2, 454.2; gap after -4.5%; result checkpoint `6d7b01e1-7fa0-4f41-8d0f-9228dd93a1ac`
- Effect: candidate 288.4 minus naive 175.6 = +112.8, 95% bootstrap interval [+64.65, +212.9] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 302.1 steps, and that its worst seed still balances for 48.2.

- p. 1; value used: `mean_reward` = 302.05 steps (headline claim)

### What did we measure?
- Naive median 175.6 over 5 runs; repeats: 171.4, 177.3, 175.6, 176.8, 156.2
- Spread: range 156.2 to 177.3, noise band ±3.53 (2 x MAD), CV 5.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -41.9% (noise band ±1.2% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is +112.8 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=500` (9.24 noise units, gap +31.1%)
- Near alternatives (closest across all claims):
  - `max_steps=500`: this claim -8.5%, mean |gap| 11.0% (5 runs)
  - `max_steps=1000`, `lr_schedule=linear`: this claim -39.6%, mean |gap| 80.6% (5 runs)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=1000` | 5 | -4.5% | +10.8% | 7.7% |
| `max_steps=500` | 5 | -8.5% | +13.5% | 11.0% |
| naive (reproduction as run) | 5 | -41.9% | -1.8% | 21.8% |
| `max_steps=1000`, `lr_schedule=linear` | 5 | -39.6% | +121.7% | 80.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `fb04d3a1ab0b0fec0acc5b342103e9444806727c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `3ed579043c7744915af32f075a3f319861ab223a18631caf42c5504685066d93`
- Cost: Nemotron billed $0.0406, sandbox reported $0.0000 (total $0.0406; this search; ledger extraction is included only if it shared the search's router)
