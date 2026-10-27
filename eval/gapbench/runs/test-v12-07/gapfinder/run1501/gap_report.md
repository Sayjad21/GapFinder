# Gap Report: test-v12-07

Artifact `rlbench` · generated 2026-10-15 19:28 · 24 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +78.9% | +26.1% | ±12.5% | `lr_schedule=inv`, `reward_norm=on` |

## C1: mean_reward (paper 98.685)
**Fits but unsupported** · gap +78.9% → +26.1% · 5 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0019`, `B0021`, `B0022`, `B0023`, `B0024` (5 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `inv`
- Config: `reward_norm` naive `off`, changed to `on`
- Command:

  Replay: fork checkpoint `3599c6fe-9eb9-4787-a952-4c64bc4cb528` and run
  ```
  RUN_TAG=b8f30c7dd325 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm on --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 151.2, 124.5, 123.2, 118.5, 139.7; gap after +26.1%; result checkpoint `0066a52d-8bc4-4010-a7eb-b5ad916b538c`
- Effect: candidate 124.5 minus naive 176.6 = -52.09, 95% bootstrap interval [-62.1, -32.04] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 98.7 steps, and that its worst seed still balances for 95.4.

- p. 1; value used: `mean_reward` = 98.685 steps (headline claim)

### What did we measure?
- Naive median 176.6 over 5 runs; repeats: 176.6, 166.2, 194, 176.4, 182.7
- Spread: range 166.2 to 194, noise band ±12.32 (2 x MAD), CV 5.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +78.9% (noise band ±12.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is +84.4% (it comes back)
- PASS · Counterfactual (reversal test): without `reward_norm` the gap is +39.0% (it comes back)
- PASS · Held-out claim: C2: -37.1% to -58.0% (not worse beyond noise)
- FAIL · Evidence: `lr_schedule=inv`: no evidence mentions 'inv'; it fits, but nothing says the authors used it
- FAIL · Evidence: `reward_norm=on`: no evidence mentions 'on'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -52.09 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `max_steps`, `CartPole_physics_constants`, `RUN_TAG`, `RL_SEED_BASE`, `reward_per_step`, `evaluation_policy`, `seed_generation_logic`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=linear` (1.81 noise units, gap +56.3%)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`: this claim +39.0%, mean |gap| 42.5% (6 runs)
  - `lr_schedule=linear`: this claim +74.0%, mean |gap| 57.9% (6 runs)

### History matching (every measured configuration, all claims together)
- out-of-space likely: no tested configuration comes within 3 sigma of C1, among 5 tested

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `reward_norm=on`, `lr_schedule=inv` | 5 | +26.1% | -58.0% | 42.1% |
| `lr_schedule=inv` | 6 | +39.0% | -46.1% | 42.5% |
| `lr_schedule=linear` | 6 | +74.0% | +41.8% | 57.9% |
| naive (reproduction as run) | 5 | +78.9% | -37.1% | 58.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `max_steps`, `CartPole_physics_constants`, `RUN_TAG`, `RL_SEED_BASE`, `reward_per_step`, `evaluation_policy`, `seed_generation_logic`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `f01046dd2f29515a730f43fce26caac555dcb0d94d0216bdeffa04fc793fd571`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
