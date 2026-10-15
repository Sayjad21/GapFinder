# Gap Report: test-v13-07

Artifact `rlbench` · generated 2026-10-15 23:49 · 90 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Explained | +89.7% | -15.4% | ±21.6% | `eps_decay=0.495` |

## C1: mean_reward (paper 89.7375)
**Explained** · gap +89.7% → -15.4% · 32 hypotheses tested
> Confirmed cause: reverting it brings the gap back, held-out claims hold, and the value has evidence

### Which experiment changed it?
- Branch: `B0013`, `B0024`, `B0025`, `B0033`, `B0034`, `B0035` (6 run(s) of the same config)
- Config: `eps_decay` naive `0.99`, changed to `0.495`
- Command:

  Replay: fork checkpoint `964b6915-9ac9-479e-97e6-5df3077422bd` and run
  ```
  RUN_TAG=404901dc096a "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.495 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 86.89, 87.78, 64.92, 106.1, 30.88, 50.87; gap after -15.4%; result checkpoint `0ce58974-2b6a-47d0-a4bc-c50a126dc765`
- Effect: candidate 75.9 minus naive 170.3 = -94.36, 95% bootstrap interval [-135.3, -71] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 89.7 on CartPole; the worst of its seeds reaches 69.9.

- p. 1; value used: `mean_reward` = 89.7375 reward (headline claim)

### What did we measure?
- Naive median 170.3 over 5 runs; repeats: 160.6, 183.9, 183, 170.3, 162.5
- Spread: range 160.6 to 183.9, noise band ±19.35 (2 x MAD), CV 6.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +89.7% (noise band ±21.6% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is -94.36 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `termination_angle`, `termination_position`, `reward_per_step`, `learning_rate_schedule_constant`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_decay=0.198` (4 noise units, gap +3.4%); `eps_decay=0.0` (3.29 noise units, gap +18.7%); `eps_decay=0.099` (3.28 noise units, gap -18.9%); `lr_schedule=inv` (3.23 noise units, gap +20.2%); `eps_decay=0.0198` (2.94 noise units, gap -26.3%)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`: this claim +28.3%, mean |gap| 35.0% (3 runs)
  - `eps_decay=0.198`: this claim -6.1%, mean |gap| 45.6% (6 runs)
  - `lr_schedule=inv`, `eps_decay=0.98`: this claim +15.3%, mean |gap| 48.7% (5 runs)

### History matching (every measured configuration, all claims together)
- out-of-space suspected: 6 tested configuration(s) fit C1, and every other claim (C2) fits some tested configuration, but none of the 32 tested configurations fits them all. The claims are mutually inconsistent under every tested condition, which points to a cause outside the exposed settings (code, data or evaluation)
- Fit C1 alone (6; worst claim's implausibility in brackets, lowest is the least inconsistent): eps_decay=0.099 (4.63); eps_decay=0.98, lr_schedule=inv (4.88); eps_decay=0.0198 (5.27); eps_decay=0.198 (5.42); eps_decay=0.0 (5.44); eps_decay=0.495 (5.49)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv` | 3 | +28.3% | -41.7% | 35.0% |
| `eps_decay=0.198` | 6 | -6.1% | -85.0% | 45.6% |
| `lr_schedule=inv`, `eps_decay=0.98` | 5 | +15.3% | -82.0% | 48.7% |
| `eps_decay=0.0` | 6 | -15.7% | -85.4% | 50.6% |
| `eps_decay=0.495` | 6 | -15.4% | -86.5% | 51.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `termination_angle`, `termination_position`, `reward_per_step`, `learning_rate_schedule_constant`

## Provenance
- GapFinder commit: `e9c31fd1405f5c8aae4bd880eadcdc8d491fad02` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
