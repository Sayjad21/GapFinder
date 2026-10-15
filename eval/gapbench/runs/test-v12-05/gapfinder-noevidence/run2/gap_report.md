# Gap Report: test-v12-05

Artifact `rlbench` · generated 2026-10-15 08:11 · 17 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +77.2% | +36.7% | ±13.0% | `lr_schedule=inv` |

## C1: mean_reward (paper 98.685)
**Fits but unsupported** · gap +77.2% → +36.7% · 2 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0007`, `B0013`, `B0014`, `B0015`, `B0016`, `B0017` (6 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `inv`
- Command:

  Replay: fork checkpoint `b103b5fe-616b-47fc-9a0f-66435647ab44` and run
  ```
  RUN_TAG=429713fc5856 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 135.6, 134.2, 122.9, 143.8, 135.6, 132; gap after +36.7%; result checkpoint `02b5e632-3df4-4c41-a869-40b6a62d0989`
- Effect: candidate 134.9 minus naive 174.8 = -39.96, 95% bootstrap interval [-59.15, -33.87] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 98.7 on CartPole; the worst of its seeds reaches 95.4.

- p. 1; value used: `mean_reward` = 98.685 (headline claim)

### What did we measure?
- Naive median 174.8 over 5 runs; repeats: 167.8, 200, 181.3, 171.1, 174.8
- Spread: range 167.8 to 200, noise band ±12.84 (2 x MAD), CV 7.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +77.2% (noise band ±13.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is +77.2% (it comes back)
- PASS · Held-out claim: C2: -46.1% to -75.9% (not worse beyond noise)
- FAIL · Evidence: `lr_schedule=inv`: evidence gate off: no evidence was looked for
- PASS · Effect vs noise: candidate minus naive is -39.96 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `max_steps`, `reward_per_step`, `RL_SEED_BASE`, `theta_clamp_min`, `theta_clamp_max`, `omega_clamp_min`, `omega_clamp_max`, `x_threshold`, `theta_threshold`, `init_state_range`, `discretise_theta_formula`, `discretise_omega_formula`, `RUN_TAG`, `python_version`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=linear` (1.17 noise units, gap +61.9%)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`: this claim +67.1%, mean |gap| 51.5% (6 runs)

### History matching (every measured configuration, all claims together)
- out-of-space likely: no tested configuration comes within 3 sigma of C1, among 2 tested

Notes:
- evidence gate off: no evidence was checked, so this cannot be labelled Explained

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=linear` | 6 | +67.1% | +36.0% | 51.5% |
| `lr_schedule=inv` | 6 | +36.7% | -75.9% | 56.3% |
| naive (reproduction as run) | 5 | +77.2% | -46.1% | 61.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `max_steps`, `reward_per_step`, `RL_SEED_BASE`, `theta_clamp_min`, `theta_clamp_max`, `omega_clamp_min`, `omega_clamp_max`, `x_threshold`, `theta_threshold`, `init_state_range`, `discretise_theta_formula`, `discretise_omega_formula`, `RUN_TAG`, `python_version`

## Provenance
- GapFinder commit: `f01fe3d9a0095f98d6304ad0543b917ca8e529eb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `f01046dd2f29515a730f43fce26caac555dcb0d94d0216bdeffa04fc793fd571`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
