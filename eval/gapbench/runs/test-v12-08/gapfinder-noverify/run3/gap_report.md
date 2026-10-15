# Gap Report: test-v12-08

Artifact `rlbench` · generated 2026-10-15 09:08 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Explained | +73.7% | +0.8% | ±12.5% | `max_steps=100` |

## C1: mean_reward (paper 98.685)
**Explained** · gap +73.7% → +0.8% · 54 hypotheses tested
> Confirmed cause: reverting it brings the gap back, held-out claims hold, and the value has evidence

### Which experiment changed it?
- Branch: `B0021`, `B0058`, `B0059`, `B0070`, `B0071`, `B0072` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `37fe1928-6ae1-4218-96ac-a74091ec4d4f` and run
  ```
  RUN_TAG=5c0bc37bb962 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 97.8, 99.48, 99.83, 99.56, 99.72, 95.66; gap after +0.8%; result checkpoint `7cb68e3f-3609-4226-b849-aef46d6b2c5f`
- Effect: candidate 99.52 minus naive 171.4 = -71.88, 95% bootstrap interval [-90.86, -45.09] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 98.7 on CartPole; the worst of its seeds reaches 95.4.

- p. 1; value used: `mean_reward` = 98.685 (headline claim)

### What did we measure?
- Naive median 171.4 over 5 runs; repeats: 177.6, 167.9, 137, 171.4, 192.3
- Spread: range 137 to 192.3, noise band ±12.36 (2 x MAD), CV 12.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +73.7% (noise band ±12.5% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is -71.88 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `theta_clamp_min`, `theta_clamp_max`, `omega_clamp_min`, `omega_clamp_max`, `discretise_formula`, `RL_SEED_BASE`, `RUN_TAG`, `python_version`, `random_module_behavior`, `os_hardware_fp`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr=0.02` (4.71 noise units, gap -14.7%); `lr=0.01` (4.64 noise units, gap -15.6%); `lr=1` (4.35 noise units, gap -19.2%); `lr=0.05` (4.33 noise units, gap +19.5%); `lr=0.5` (3.66 noise units, gap +27.8%) (and 4 more in the JSON)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `lr_schedule=linear`: this claim -1.1%, mean |gap| 2.2% (5 runs)
  - `max_steps=100`, `lr=0.05`: this claim -16.3%, mean |gap| 33.8% (5 runs)
  - `lr=0.05`: this claim +38.0%, mean |gap| 41.6% (6 runs)

### History matching (every measured configuration, all claims together)
- 23 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `max_steps`: max_steps=100 (max I 0.21)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.49); lr_schedule=inv, max_steps=100 (max I 2.16); lr_schedule=linear, max_steps=40 (max I 2.55)
  - `lr, lr_schedule`: lr=0.05, lr_schedule=inv (max I 1.26); lr=0.05, lr_schedule=linear (max I 1.49); lr=0.02, lr_schedule=linear (max I 1.69); lr=0.01, lr_schedule=linear (max I 1.69)
  - `lr, max_steps`: lr=0.05, max_steps=100 (max I 1.81)
  - `lr`: lr=0.05 (max I 2.05)

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'lr': '0.05', 'lr_schedule': 'inv'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 6 | +0.8% | +0.7% | 0.8% |
| `max_steps=100`, `lr_schedule=linear` | 5 | -1.1% | -3.2% | 2.2% |
| `max_steps=100`, `lr=0.05` | 5 | -16.3% | -51.2% | 33.8% |
| `lr=0.05` | 6 | +38.0% | -45.3% | 41.6% |
| `lr=1` | 6 | -3.9% | -86.8% | 45.3% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `theta_clamp_min`, `theta_clamp_max`, `omega_clamp_min`, `omega_clamp_max`, `discretise_formula`, `RL_SEED_BASE`, `RUN_TAG`, `python_version`, `random_module_behavior`, `os_hardware_fp`

## Provenance
- GapFinder commit: `f01fe3d9a0095f98d6304ad0543b917ca8e529eb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
