# Gap Report: test-gen-03

Artifact `rlbench` · generated 2026-10-13 00:05 · 18 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -39.1% | -8.9% | ±6.2% | `max_steps=500` |

## C1: mean_reward (paper 302.05)
**Fits but unsupported** · gap -39.1% → -8.9% · 5 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0006`, `B0010`, `B0011`, `B0012`, `B0013` (5 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `500`
- Command:

  Replay: fork checkpoint `520a9c67-bfa2-4ed4-8641-0cbbece23613` and run
  ```
  RUN_TAG=6a2af00f3309 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 500 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 275.3, 302.6, 190.8, 211.8, 301.8; gap after -8.9%; result checkpoint `2ba412fe-751a-468c-a988-32d291b25978`
- Effect: candidate 275.3 minus naive 184 = +91.25, 95% bootstrap interval [+37.2, +121.4] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 302.1 steps

- p. 1; value used: `mean_reward` = 302.05 steps (headline claim)

### What did we measure?
- Naive median 184 over 5 runs; repeats: 163.2, 184, 193.4, 190.5, 149
- Spread: range 149 to 193.4, noise band ±18.85 (2 x MAD), CV 10.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -39.1% (noise band ±6.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -39.1% (it comes back)
- PASS · Held-out claim: C2: +63.4% to +3.0% (not worse beyond noise)
- FAIL · Evidence: `max_steps=500`: evidence gate off: no evidence was looked for
- PASS · Effect vs noise: candidate minus naive is +91.25 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `gravity`, `masscart`, `masspole`, `length`, `force_mag`, `tau`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=1000` (1.95 noise units, gap -26.9%)
- Near alternatives (closest across all claims):
  - `max_steps=1000`: this claim -26.9%, mean |gap| 39.9% (5 runs)

Notes:
- evidence gate off: no evidence was checked, so this cannot be labelled Explained

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=500` | 5 | -8.9% | +3.0% | 5.9% |
| `max_steps=1000` | 5 | -26.9% | -52.8% | 39.9% |
| naive (reproduction as run) | 5 | -39.1% | +63.4% | 51.2% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `gravity`, `masscart`, `masspole`, `length`, `force_mag`, `tau`, `--out`

## Provenance
- GapFinder commit: `2e9291c6be5f4b9ffe219d44dfe2904a7d2d6a9f` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `3ed579043c7744915af32f075a3f319861ab223a18631caf42c5504685066d93`
- Cost: Nemotron billed $0.0627, sandbox reported $0.0000 (total $0.0627; this search; ledger extraction is included only if it shared the search's router)
