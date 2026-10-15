# Gap Report: test-v12-07

Artifact `rlbench` · generated 2026-10-15 07:30 · 23 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +95.0% | +34.8% | ±8.9% | `lr_schedule=inv` |

## C1: mean_reward (paper 98.685)
**Fits but unsupported** · gap +95.0% → +34.8% · 5 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0007`, `B0012`, `B0013`, `B0014` (4 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `inv`
- Command:

  Replay: fork checkpoint `b591c963-51ff-4b3e-9b8d-a9d7d8bc561c` and run
  ```
  RUN_TAG=ac97935fc379 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 116.6, 139.7, 152.4, 126.3; gap after +34.8%; result checkpoint `f0dc1ce9-3039-41a7-80c4-b846b98a819e`
- Effect: candidate 133 minus naive 192.4 = -59.42, 95% bootstrap interval [-67.89, -37.95] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 98.7 steps, and that its worst seed still balances for 95.4.

- p. 1; value used: `mean_reward` = 98.685 steps (headline claim)

### What did we measure?
- Naive median 192.4 over 5 runs; repeats: 197.8, 182.7, 191.6, 192.4, 196.8
- Spread: range 182.7 to 197.8, noise band ±8.81 (2 x MAD), CV 3.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +95.0% (noise band ±8.9% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is +95.0% (it comes back)
- PASS · Held-out claim: C2: +78.0% to -71.3% (not worse beyond noise)
- FAIL · Evidence: `lr_schedule=inv`: no evidence mentions 'inv'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -59.42 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `max_steps`, `CartPole_physics_constants`, `RUN_TAG`, `RL_SEED_BASE`, `reward_per_step`, `evaluation_policy`, `seed_generation_logic`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=linear` (2.93 noise units, gap +68.8%); `reward_norm=on` (1.17 noise units, gap +84.6%)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`: this claim +67.2%, mean |gap| 47.6% (4 runs)
  - `reward_norm=on`: this claim +90.3%, mean |gap| 53.1% (4 runs)
  - `lr_schedule=linear`, `reward_norm=on`: this claim +70.2%, mean |gap| 54.1% (3 runs)

### History matching (every measured configuration, all claims together)
- out-of-space likely: no tested configuration comes within 3 sigma of C1, among 5 tested

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=linear` | 4 | +67.2% | +27.9% | 47.6% |
| `reward_norm=on` | 4 | +90.3% | +15.8% | 53.1% |
| `lr_schedule=inv` | 4 | +34.8% | -71.3% | 53.1% |
| `lr_schedule=linear`, `reward_norm=on` | 3 | +70.2% | +37.9% | 54.1% |
| `lr_schedule=inv`, `reward_norm=on` | 3 | +44.7% | -67.7% | 56.2% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `max_steps`, `CartPole_physics_constants`, `RUN_TAG`, `RL_SEED_BASE`, `reward_per_step`, `evaluation_policy`, `seed_generation_logic`

## Provenance
- GapFinder commit: `f01fe3d9a0095f98d6304ad0543b917ca8e529eb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `f01046dd2f29515a730f43fce26caac555dcb0d94d0216bdeffa04fc793fd571`
- Cost: Nemotron billed $0.0411, sandbox reported $0.0000 (total $0.0411; this search; ledger extraction is included only if it shared the search's router)
