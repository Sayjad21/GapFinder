# Gap Report: test-gen-03

Artifact `rlbench` · generated 2026-10-12 22:17 · 16 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -37.7% | +14.5% | ±4.0% | `max_steps=500` |

## C1: mean_reward (paper 302.05)
**Fits but unsupported** · gap -37.7% → +14.5% · 5 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0006`, `B0010`, `B0011` (3 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `500`
- Command:

  Replay: fork checkpoint `95f3bf5c-816f-4e9a-9b7e-4afc14d42193` and run
  ```
  RUN_TAG=4f883e3f1281 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 500 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 348.7, 345.8, 340.6; gap after +14.5%; result checkpoint `151bff89-1e64-4d22-8d6a-c9c212cdf167`
- Effect: candidate 345.8 minus naive 188.1 = +157.8, 95% bootstrap interval [+150.7, +166.1] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 302.1 steps

- p. 1; value used: `mean_reward` = 302.05 steps (headline claim)

### What did we measure?
- Naive median 188.1 over 5 runs; repeats: 192.3, 175.1, 188.1, 182, 196.9
- Spread: range 175.1 to 196.9, noise band ±12.11 (2 x MAD), CV 4.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -37.7% (noise band ±4.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -37.7% (it comes back)
- PASS · Held-out claim: C2: +70.9% to +11.7% (not worse beyond noise)
- FAIL · Evidence: `max_steps=500`: no evidence mentions '500'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +157.8 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives (closest across all claims):
  - `max_steps=1000`: this claim +30.5%, mean |gap| 15.8% (3 runs)
  - `max_steps=500`, `lr_schedule=linear`: this claim -38.0%, mean |gap| 112.6% (3 runs)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=500` | 3 | +14.5% | +11.7% | 13.1% |
| `max_steps=1000` | 3 | +30.5% | +1.0% | 15.8% |
| naive (reproduction as run) | 5 | -37.7% | +70.9% | 54.3% |
| `max_steps=500`, `lr_schedule=linear` | 3 | -38.0% | +187.3% | 112.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`

## Provenance
- GapFinder commit: `56779a9cc2cef642dbf91ede59da97a848c305cd` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `3ed579043c7744915af32f075a3f319861ab223a18631caf42c5504685066d93`
- Cost: Nemotron billed $0.1398, sandbox reported $0.0000 (total $0.1398; this search; ledger extraction is included only if it shared the search's router)
