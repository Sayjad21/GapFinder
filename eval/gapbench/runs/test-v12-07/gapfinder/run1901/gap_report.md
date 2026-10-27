# Gap Report: test-v12-07

Artifact `rlbench` · generated 2026-10-15 19:52 · 32 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +89.7% | +24.5% | ±6.5% | `lr_schedule=inv`, `reward_norm=on` |

## C1: mean_reward (paper 98.685)
**Fits but unsupported** · gap +89.7% → +24.5% · 5 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0019`, `B0021`, `B0022`, `B0023`, `B0024` (5 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `inv`
- Config: `reward_norm` naive `off`, changed to `on`
- Command:

  Replay: fork checkpoint `65b04049-f883-42d0-989b-4fb52a281212` and run
  ```
  RUN_TAG=7b2a3f8a86ec "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm on --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 122.8, 96.05, 118.9, 136.1, 149.8; gap after +24.5%; result checkpoint `30eac1ab-f6b1-4727-a9bc-f2d4b6cdf998`
- Effect: candidate 122.8 minus naive 187.2 = -64.35, 95% bootstrap interval [-76.98, -22.21] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 98.7 steps, and that its worst seed still balances for 95.4.

- p. 1; value used: `mean_reward` = 98.685 steps (headline claim)

### What did we measure?
- Naive median 187.2 over 5 runs; repeats: 133.7, 178, 187.2, 190.4, 190.4
- Spread: range 133.7 to 190.4, noise band ±6.39 (2 x MAD), CV 13.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +89.7% (noise band ±6.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is +81.8% (it comes back)
- PASS · Counterfactual (reversal test): without `reward_norm` the gap is +43.9% (it comes back)
- PASS · Held-out claim: C2: +40.8% to -61.2% (not worse beyond noise)
- FAIL · Evidence: `lr_schedule=inv`: no evidence mentions 'inv'; it fits, but nothing says the authors used it
- FAIL · Evidence: `reward_norm=on`: no evidence mentions 'on'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -64.35 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `max_steps`, `CartPole_physics_constants`, `RUN_TAG`, `RL_SEED_BASE`, `reward_per_step`, `evaluation_policy`, `seed_generation_logic`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=linear` (1.77 noise units, gap +78.2%)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`: this claim +43.9%, mean |gap| 50.3% (6 runs)
  - `reward_norm=on`, `lr_schedule=linear`: this claim +72.4%, mean |gap| 57.6% (5 runs)
  - `lr_schedule=linear`: this claim +70.2%, mean |gap| 58.4% (6 runs)

### History matching (every measured configuration, all claims together)
- 2 of 5 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 2 configurations
  - `lr_schedule, reward_norm`: lr_schedule=inv, reward_norm=on (max I 1.58)
  - `lr_schedule`: lr_schedule=inv (max I 2.71)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `reward_norm=on`, `lr_schedule=inv` | 5 | +24.5% | -61.2% | 42.8% |
| `lr_schedule=inv` | 6 | +43.9% | -56.7% | 50.3% |
| `reward_norm=on`, `lr_schedule=linear` | 5 | +72.4% | +42.8% | 57.6% |
| `lr_schedule=linear` | 6 | +70.2% | +46.6% | 58.4% |
| `reward_norm=on` | 5 | +81.8% | -44.4% | 63.1% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `max_steps`, `CartPole_physics_constants`, `RUN_TAG`, `RL_SEED_BASE`, `reward_per_step`, `evaluation_policy`, `seed_generation_logic`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `f01046dd2f29515a730f43fce26caac555dcb0d94d0216bdeffa04fc793fd571`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
