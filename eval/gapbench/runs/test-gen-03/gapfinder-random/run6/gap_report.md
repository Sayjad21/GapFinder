# Gap Report: test-gen-03

Artifact `rlbench` · generated 2026-10-12 23:48 · 14 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -38.1% | -12.3% | ±2.1% | `max_steps=500` |

## C1: mean_reward (paper 302.05)
**Fits but unsupported** · gap -38.1% → -12.3% · 5 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0008`, `B0010`, `B0011` (3 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `500`
- Command:

  Replay: fork checkpoint `f8b7b07b-fd6e-4aa1-b0bd-2fba46734095` and run
  ```
  RUN_TAG=3a1f230547a4 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 500 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 242, 264.9, 338.5; gap after -12.3%; result checkpoint `70e01a2e-94f7-4072-8d35-9b6f2f75ee4e`
- Effect: candidate 264.9 minus naive 186.9 = +78.02, 95% bootstrap interval [+56.09, +151.3] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 302.1 steps, and that its worst seed still balances for 48.2.

- p. 1; value used: `mean_reward` = 302.05 steps (headline claim)

### What did we measure?
- Naive median 186.9 over 5 runs; repeats: 198.5, 188.5, 183.7, 173.7, 186.9
- Spread: range 173.7 to 198.5, noise band ±6.38 (2 x MAD), CV 4.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -38.1% (noise band ±2.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -38.1% (it comes back)
- PASS · Held-out claim: C2: +125.8% to -43.8% (not worse beyond noise)
- FAIL · Evidence: `max_steps=500`: no evidence mentions '500'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +78.02 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `g`, `mc`, `mp`, `l`, `f`, `dt`, `theta_clamp_min/max`, `omega_clamp_min/max`, `RUN_TAG`, `x_threshold`, `theta_threshold`, `initial_state_range`, `RL_SEED_BASE`, `discretise_formula`, `target_calculation`, `python_version`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `max_steps=500`: this claim -38.9%, mean |gap| 118.4% (3 runs)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=500` | 3 | -12.3% | -43.8% | 28.1% |
| naive (reproduction as run) | 5 | -38.1% | +125.8% | 82.0% |
| `lr_schedule=linear`, `max_steps=500` | 3 | -38.9% | +197.9% | 118.4% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `g`, `mc`, `mp`, `l`, `f`, `dt`, `theta_clamp_min/max`, `omega_clamp_min/max`, `RUN_TAG`, `x_threshold`, `theta_threshold`, `initial_state_range`, `RL_SEED_BASE`, `discretise_formula`, `target_calculation`, `python_version`

## Provenance
- GapFinder commit: `2e9291c6be5f4b9ffe219d44dfe2904a7d2d6a9f` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `3ed579043c7744915af32f075a3f319861ab223a18631caf42c5504685066d93`
- Cost: Nemotron billed $0.1557, sandbox reported $0.0000 (total $0.1557; this search; ledger extraction is included only if it shared the search's router)
