# Gap Report: test-gen-05

Artifact `rlbench` · generated 2026-10-10 23:43 · 30 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +929.3% | +288.7% | ±82.4% | `lr_schedule=inv`, `eps_start=0.5` |

## C1: mean_reward (paper 17.31)
**Fits but unsupported** · gap +929.3% → +288.7% · 5 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0026`, `B0027`, `B0028`, `B0029`, `B0030` (5 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `inv`
- Config: `eps_start` naive `1.0`, changed to `0.5`
- Command:

  Replay: fork checkpoint `e687fd53-317e-4a7d-b515-0c2a2d504394` and run
  ```
  RUN_TAG=75da52782a8c "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_start 0.5 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 67.29, 88.92, 45.73, 63.22, 81.11; gap after +288.7%; result checkpoint `5b7c1e70-944e-4f05-8a33-bb50306a88b9`
- Effect: candidate 67.29 minus naive 178.2 = -110.9, 95% bootstrap interval [-125.8, -91.48] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 17.3 steps, and that its worst seed still balances for 9.1.

- p. 1; value used: `mean_reward` = 17.31 steps (headline claim)

### What did we measure?
- Naive median 178.2 over 5 runs; repeats: 194.2, 178.2, 175.1, 185.3, 158.1
- Spread: range 158.1 to 194.2, noise band ±14.26 (2 x MAD), CV 7.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +929.3% (noise band ±82.4% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is +743.2% (it comes back)
- PASS · Counterfactual (reversal test): without `eps_start` the gap is +712.8% (it comes back)
- PASS · Held-out claim: C2: +516.5% to +11.0% (not worse beyond noise)
- FAIL · Evidence: `lr_schedule=inv`: evidence gate off: no evidence was looked for
- FAIL · Evidence: `eps_start=0.5`: evidence gate off: no evidence was looked for
- PASS · Effect vs noise: candidate minus naive is -110.9 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `RL_SEED_BASE`, `RUN_TAG`, `termination_threshold_x`, `termination_threshold_theta`, `theta_clamp_min`, `theta_clamp_max`, `omega_clamp_min`, `omega_clamp_max`, `random_module`, `python_version`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives (closest across all claims):
  - `eps_start=0.5`: this claim +743.2%, mean |gap| 469.9% (5 runs)
  - `lr_schedule=inv`: this claim +712.8%, mean |gap| 647.1% (5 runs)
  - `eps_start=0.8`: this claim +889.0%, mean |gap| 672.0% (5 runs)

Notes:
- evidence gate off: no evidence was checked, so this cannot be labelled Explained

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `eps_start=0.5`, `lr_schedule=inv` | 5 | +288.7% | +11.0% | 149.9% |
| `eps_start=0.5` | 5 | +743.2% | +196.7% | 469.9% |
| `lr_schedule=inv` | 5 | +712.8% | +581.3% | 647.1% |
| `eps_start=0.8` | 5 | +889.0% | +454.9% | 672.0% |
| naive (reproduction as run) | 5 | +929.3% | +516.5% | 722.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `RL_SEED_BASE`, `RUN_TAG`, `termination_threshold_x`, `termination_threshold_theta`, `theta_clamp_min`, `theta_clamp_max`, `omega_clamp_min`, `omega_clamp_max`, `random_module`, `python_version`

## Provenance
- GapFinder commit: `fb04d3a1ab0b0fec0acc5b342103e9444806727c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `3ed579043c7744915af32f075a3f319861ab223a18631caf42c5504685066d93`
- Cost: Nemotron billed $0.0450, sandbox reported $0.0000 (total $0.0450; this search; ledger extraction is included only if it shared the search's router)
