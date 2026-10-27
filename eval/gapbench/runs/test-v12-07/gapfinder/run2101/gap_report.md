# Gap Report: test-v12-07

Artifact `rlbench` · generated 2026-10-15 21:08 · 28 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +93.8% | +37.1% | ±10.2% | `lr_schedule=inv` |

## C1: mean_reward (paper 98.685)
**Fits but unsupported** · gap +93.8% → +37.1% · 5 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0007`, `B0014`, `B0015`, `B0016`, `B0017`, `B0018` (6 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `inv`
- Command:

  Replay: fork checkpoint `b0a59a74-915d-48d2-8506-83d10017a17f` and run
  ```
  RUN_TAG=f3ac178a328d "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 108.9, 159.8, 112.1, 132.6, 156.3, 138.1; gap after +37.1%; result checkpoint `5486db12-2117-4854-a006-f0c97b46573a`
- Effect: candidate 135.3 minus naive 191.2 = -55.89, 95% bootstrap interval [-66.02, -17.64] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 98.7 steps, and that its worst seed still balances for 95.4.

- p. 1; value used: `mean_reward` = 98.685 steps (headline claim)

### What did we measure?
- Naive median 191.2 over 5 runs; repeats: 196.2, 193.6, 191.2, 152.5, 175.6
- Spread: range 152.5 to 196.2, noise band ±10.03 (2 x MAD), CV 10.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +93.8% (noise band ±10.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is +93.8% (it comes back)
- PASS · Held-out claim: C2: +45.9% to -37.8% (not worse beyond noise)
- FAIL · Evidence: `lr_schedule=inv`: no evidence mentions 'inv'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -55.89 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `max_steps`, `CartPole_physics_constants`, `RUN_TAG`, `RL_SEED_BASE`, `reward_per_step`, `evaluation_policy`, `seed_generation_logic`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=linear` (2.2 noise units, gap +71.4%)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`, `reward_norm=on`: this claim +41.7%, mean |gap| 44.8% (5 runs)
  - `lr_schedule=linear`, `reward_norm=on`: this claim +71.6%, mean |gap| 54.1% (5 runs)
  - `lr_schedule=linear`: this claim +72.3%, mean |gap| 63.2% (6 runs)

### History matching (every measured configuration, all claims together)
- 1 of 5 tested configurations fit every claim within 3 sigma

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv` | 6 | +37.1% | -37.8% | 37.5% |
| `lr_schedule=inv`, `reward_norm=on` | 5 | +41.7% | -48.0% | 44.8% |
| `lr_schedule=linear`, `reward_norm=on` | 5 | +71.6% | +36.6% | 54.1% |
| `lr_schedule=linear` | 6 | +72.3% | +54.0% | 63.2% |
| naive (reproduction as run) | 5 | +93.8% | +45.9% | 69.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `max_steps`, `CartPole_physics_constants`, `RUN_TAG`, `RL_SEED_BASE`, `reward_per_step`, `evaluation_policy`, `seed_generation_logic`

## Provenance
- GapFinder commit: `cd8c8af2b9d079dd9a57443ed501c0dd8a467d34` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `f01046dd2f29515a730f43fce26caac555dcb0d94d0216bdeffa04fc793fd571`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
