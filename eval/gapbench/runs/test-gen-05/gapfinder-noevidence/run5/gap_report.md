# Gap Report: test-gen-05

Artifact `rlbench` · generated 2026-10-13 00:09 · 30 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +989.1% | +63.0% | ±35.2% | `eps_start=0.1` |

## C1: mean_reward (paper 17.31)
**Fits but unsupported** · gap +989.1% → +63.0% · 5 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0009`, `B0022`, `B0023`, `B0024`, `B0025` (5 run(s) of the same config)
- Config: `eps_start` naive `1.0`, changed to `0.1`
- Command:

  Replay: fork checkpoint `898fbc1d-5178-4cba-8c4f-f295a17880cd` and run
  ```
  RUN_TAG=372fde0a4346 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 0.1 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 29.22, 22.38, 28.21, 36, 19.82; gap after +63.0%; result checkpoint `87ee12a5-f68b-45be-bfa2-17ecc14d2a4c`
- Effect: candidate 28.21 minus naive 188.5 = -160.3, 95% bootstrap interval [-164.3, -144.7] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 17.3 steps, and that its worst seed still balances for 9.1.

- p. 1; value used: `mean_reward` = 17.31 steps (headline claim)

### What did we measure?
- Naive median 188.5 over 5 runs; repeats: 191.6, 188.5, 190.4, 171.8, 168.5
- Spread: range 168.5 to 191.6, noise band ±6.09 (2 x MAD), CV 6.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +989.1% (noise band ±35.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `eps_start` the gap is +989.1% (it comes back)
- PASS · Held-out claim: C2: +1401.6% to +1.6% (not worse beyond noise)
- FAIL · Evidence: `eps_start=0.1`: evidence gate off: no evidence was looked for
- PASS · Effect vs noise: candidate minus naive is -160.3 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `done_x_threshold`, `done_theta_threshold`, `RL_SEED_BASE`, `reward_per_step`, `hardware`, `RUN_TAG`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.5` (11.46 noise units, gap +585.8%); `lr_schedule=inv` (8.65 noise units, gap +684.9%); `lr_schedule=linear` (2.92 noise units, gap +886.4%)
- Near alternatives (closest across all claims):
  - `eps_start=0.1`, `lr_schedule=inv`: this claim +34.9%, mean |gap| 17.7% (5 runs)
  - `eps_start=0.5`: this claim +642.7%, mean |gap| 362.0% (5 runs)
  - `lr_schedule=inv`: this claim +683.1%, mean |gap| 514.6% (5 runs)

Notes:
- evidence gate off: no evidence was checked, so this cannot be labelled Explained

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `eps_start=0.1`, `lr_schedule=inv` | 5 | +34.9% | -0.5% | 17.7% |
| `eps_start=0.1` | 5 | +63.0% | +1.6% | 32.3% |
| `eps_start=0.5` | 5 | +642.7% | +81.3% | 362.0% |
| `lr_schedule=inv` | 5 | +683.1% | +346.2% | 514.6% |
| `lr_schedule=linear` | 5 | +812.4% | +727.5% | 769.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `done_x_threshold`, `done_theta_threshold`, `RL_SEED_BASE`, `reward_per_step`, `hardware`, `RUN_TAG`

## Provenance
- GapFinder commit: `2e9291c6be5f4b9ffe219d44dfe2904a7d2d6a9f` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `3ed579043c7744915af32f075a3f319861ab223a18631caf42c5504685066d93`
- Cost: Nemotron billed $0.0558, sandbox reported $0.0000 (total $0.0558; this search; ledger extraction is included only if it shared the search's router)
