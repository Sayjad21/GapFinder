# Gap Report: test-v12-08

Artifact `rlbench` · generated 2026-10-15 07:34 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Explained | +99.3% | -0.6% | ±2.0% | `lr=1` |

## C1: mean_reward (paper 98.685)
**Explained** · gap +99.3% → -0.6% · 54 hypotheses tested
> Confirmed cause: reverting it brings the gap back, held-out claims hold, and the value has evidence

### Which experiment changed it?
- Branch: `B0009`, `B0034`, `B0035`, `B0063`, `B0064`, `B0065` (6 run(s) of the same config)
- Config: `lr` naive `0.1`, changed to `1`
- Command:

  Replay: fork checkpoint `8bb316bd-e633-443f-b9ff-7b7acc62540a` and run
  ```
  RUN_TAG=5b5afcc615fe "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 79.01, 118.3, 90.69, 45.35, 112.4, 105.4; gap after -0.6%; result checkpoint `7cd10473-fc3e-4a6e-83af-8604cffa5b6a`
- Effect: candidate 98.05 minus naive 196.7 = -98.63, 95% bootstrap interval [-134.8, -59.8] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 98.7 on CartPole; the worst of its seeds reaches 95.4.

- p. 1, Figure 1; value used: `mean_reward` = 98.685 (headline claim)

### What did we measure?
- Naive median 196.7 over 5 runs; repeats: 197.5, 196.9, 158.9, 196.7, 185.2
- Spread: range 158.9 to 197.5, noise band ±1.967 (2 x MAD), CV 8.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +99.3% (noise band ±2.0% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is -98.63 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=100` (48.26 noise units, gap -3.1%); `lr=0.05` (44.39 noise units, gap +10.8%); `lr=0.5` (34.08 noise units, gap +31.4%); `lr_schedule=inv` (29.81 noise units, gap +39.9%); `lr=0.02` (28.78 noise units, gap -41.9%) (and 10 more in the JSON)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `lr_schedule=linear`: this claim -0.9%, mean |gap| 1.4% (5 runs)
  - `max_steps=100`, `lr=0.5`: this claim +1.3%, mean |gap| 3.1% (5 runs)
  - `max_steps=100`: this claim -2.0%, mean |gap| 14.0% (6 runs)

### History matching (every measured configuration, all claims together)
- 17 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr, max_steps`: lr=0.5, max_steps=100 (max I 0.09); lr=1, max_steps=100 (max I 1.58); lr=0.05, max_steps=100 (max I 1.77)
  - `max_steps`: max_steps=100 (max I 0.56)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.58); lr_schedule=inv, max_steps=100 (max I 1.29)
  - `lr`: lr=0.02 (max I 1.66); lr=0.05 (max I 1.83)
  - `lr, lr_schedule`: lr=0.05, lr_schedule=inv (max I 1.67); lr=0.02, lr_schedule=linear (max I 1.69)

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'max_steps': '20', 'lr': '0.5'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100`, `lr_schedule=linear` | 5 | -0.9% | -1.9% | 1.4% |
| `max_steps=100`, `lr=0.5` | 5 | +1.3% | +4.8% | 3.1% |
| `max_steps=100` | 6 | -2.0% | -25.9% | 14.0% |
| `max_steps=100`, `lr_schedule=inv` | 5 | -13.2% | -64.0% | 38.6% |
| `lr_schedule=inv` | 3 | +50.0% | -37.7% | 43.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `f01fe3d9a0095f98d6304ad0543b917ca8e529eb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
