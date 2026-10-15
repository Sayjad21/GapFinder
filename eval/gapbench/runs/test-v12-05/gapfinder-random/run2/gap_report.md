# Gap Report: test-v12-05

Artifact `rlbench` · generated 2026-10-15 08:11 · 13 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +85.9% | +39.9% | ±7.0% | `lr_schedule=inv` |

## C1: mean_reward (paper 98.685)
**Fits but unsupported** · gap +85.9% → +39.9% · 2 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0006`, `B0008`, `B0009`, `B0010` (4 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `inv`
- Command:

  Replay: fork checkpoint `f21342ca-e79b-4b27-8ab9-208276cf0c76` and run
  ```
  RUN_TAG=3167e85284c3 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 123.6, 133.5, 146.4, 142.7; gap after +39.9%; result checkpoint `a23f0398-9c87-4471-a8cd-24f557f1168c`
- Effect: candidate 138.1 minus naive 183.5 = -45.37, 95% bootstrap interval [-48.54, -29.32] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 98.7 on CartPole; the worst of its seeds reaches 95.4.

- p. 1; value used: `mean_reward` = 98.685 (headline claim)

### What did we measure?
- Naive median 183.5 over 5 runs; repeats: 183.5, 186.9, 170.6, 173.6, 184.3
- Spread: range 170.6 to 186.9, noise band ±6.87 (2 x MAD), CV 4.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +85.9% (noise band ±7.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is +85.9% (it comes back)
- PASS · Held-out claim: C2: -26.8% to -64.6% (not worse beyond noise)
- FAIL · Evidence: `lr_schedule=inv`: no evidence mentions 'inv'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -45.37 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `max_steps`, `reward_per_step`, `RL_SEED_BASE`, `theta_clamp_min`, `theta_clamp_max`, `omega_clamp_min`, `omega_clamp_max`, `x_threshold`, `theta_threshold`, `init_state_range`, `discretise_theta_formula`, `discretise_omega_formula`, `RUN_TAG`, `python_version`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=linear` (2.18 noise units, gap +70.7%)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`: this claim +70.4%, mean |gap| 39.8% (4 runs)

### History matching (every measured configuration, all claims together)
- out-of-space likely: no tested configuration comes within 3 sigma of C1, among 2 tested

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=linear` | 4 | +70.4% | +9.2% | 39.8% |
| `lr_schedule=inv` | 4 | +39.9% | -64.6% | 52.3% |
| naive (reproduction as run) | 5 | +85.9% | -26.8% | 56.3% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `max_steps`, `reward_per_step`, `RL_SEED_BASE`, `theta_clamp_min`, `theta_clamp_max`, `omega_clamp_min`, `omega_clamp_max`, `x_threshold`, `theta_threshold`, `init_state_range`, `discretise_theta_formula`, `discretise_omega_formula`, `RUN_TAG`, `python_version`

## Provenance
- GapFinder commit: `f01fe3d9a0095f98d6304ad0543b917ca8e529eb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `f01046dd2f29515a730f43fce26caac555dcb0d94d0216bdeffa04fc793fd571`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
