# Gap Report: test-gen-05

Artifact `rlbench` · generated 2026-10-10 22:59 · 20 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Partially explained | +977.8% | +222.8% | ±44.8% | `eps_start=0.5`, `lr_schedule=inv` |

## C1: mean_reward (paper 17.31)
**Partially explained** · gap +977.8% → +222.8% · 5 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0018`, `B0019`, `B0020` (3 run(s) of the same config)
- Config: `eps_start` naive `1.0`, changed to `0.5`
- Config: `lr_schedule` naive `const`, changed to `inv`
- Command:

  Replay: fork checkpoint `63728e08-d167-4385-916c-254b461962a7` and run
  ```
  RUN_TAG=e6308c446de7 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_start 0.5 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 87.64, 55.88, 48.65; gap after +222.8%; result checkpoint `cb4a0a18-e674-4957-ad1c-afceb7036ddd`
- Effect: candidate 55.88 minus naive 186.6 = -130.7, 95% bootstrap interval [-137.2, -98.25] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 17.3 steps, and that its worst seed still balances for 9.1.

- p. 1; value used: `mean_reward` = 17.31 steps (headline claim)

### What did we measure?
- Naive median 186.6 over 5 runs; repeats: 186.6, 177.7, 188.8, 182.7, 190.6
- Spread: range 177.7 to 190.6, noise band ±7.76 (2 x MAD), CV 2.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +977.8% (noise band ±44.8% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is -130.7 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `discretise.theta_clamp_min`, `discretise.theta_clamp_max`, `discretise.omega_clamp_min`, `discretise.omega_clamp_max`, `CartPole.x_threshold`, `CartPole.theta_threshold`, `eval_tiebreak_prefer_action0`, `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `CartPole.reset_initial_range`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=linear` (3.22 noise units, gap +833.6%)
- Near alternatives (closest across all claims):
  - `eps_start=0.5`: this claim +617.9%, mean |gap| 352.4% (3 runs)
  - `lr_schedule=inv`: this claim +634.3%, mean |gap| 503.4% (3 runs)
  - `eps_start=0.8`: this claim +926.3%, mean |gap| 692.3% (3 runs)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `eps_start=0.5`, `lr_schedule=inv` | 3 | +222.8% | +19.2% | 121.0% |
| `eps_start=0.5` | 3 | +617.9% | +86.8% | 352.4% |
| `lr_schedule=inv` | 3 | +634.3% | +372.5% | 503.4% |
| `eps_start=0.8` | 3 | +926.3% | +458.2% | 692.3% |
| naive (reproduction as run) | 5 | +977.8% | +1068.1% | 1023.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `discretise.theta_clamp_min`, `discretise.theta_clamp_max`, `discretise.omega_clamp_min`, `discretise.omega_clamp_max`, `CartPole.x_threshold`, `CartPole.theta_threshold`, `eval_tiebreak_prefer_action0`, `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `CartPole.reset_initial_range`

## Provenance
- GapFinder commit: `fb04d3a1ab0b0fec0acc5b342103e9444806727c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `3ed579043c7744915af32f075a3f319861ab223a18631caf42c5504685066d93`
- Cost: Nemotron billed $0.0502, sandbox reported $0.0000 (total $0.0502; this search; ledger extraction is included only if it shared the search's router)
