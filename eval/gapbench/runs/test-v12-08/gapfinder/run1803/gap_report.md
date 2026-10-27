# Gap Report: test-v12-08

Artifact `rlbench` · generated 2026-10-15 19:54 · 199 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +91.7% | +0.5% | ±13.8% | `max_steps=100` |

## C1: mean_reward (paper 98.685)
**Fits but unsupported** · gap +91.7% → +0.5% · 55 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0021`, `B0058`, `B0059`, `B0072`, `B0073`, `B0074` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `a81439d5-0a83-415a-b8b5-76b48b1d077f` and run
  ```
  RUN_TAG=2dc413007356 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 100, 99.72, 100, 89.44, 98.66, 89.67; gap after +0.5%; result checkpoint `bf57627b-f339-45bf-be8b-d9bef509c11f`
- Effect: candidate 99.19 minus naive 189.2 = -89.98, 95% bootstrap interval [-104.3, -77.06] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 98.7 on CartPole; the worst of its seeds reaches 95.4.

- p. 1; value used: `mean_reward` = 98.685 (headline claim)

### What did we measure?
- Naive median 189.2 over 5 runs; repeats: 198.9, 168.7, 196, 189.2, 187.1
- Spread: range 168.7 to 198.9, noise band ±13.65 (2 x MAD), CV 6.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +91.7% (noise band ±13.8% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +91.7% (it comes back)
- PASS · Held-out claim: C2: +41.6% to -0.6% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -89.98 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `theta_clamp_min`, `theta_clamp_max`, `omega_clamp_min`, `omega_clamp_max`, `discretise_formula`, `RL_SEED_BASE`, `RUN_TAG`, `python_version`, `random_module_behavior`, `os_hardware_fp`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr=0.01` (5.34 noise units, gap -17.8%); `lr_schedule=inv` (5.11 noise units, gap +21.0%); `lr=1` (5.09 noise units, gap -21.3%); `lr=0.5` (4.83 noise units, gap +24.9%); `lr=0.002` (4.53 noise units, gap -29.0%) (and 6 more in the JSON)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `lr=0.5`: this claim +1.3%, mean |gap| 3.1% (5 runs)
  - `max_steps=100`, `lr_schedule=linear`: this claim -4.6%, mean |gap| 17.6% (5 runs)
  - `max_steps=100`, `lr_schedule=inv`: this claim -7.5%, mean |gap| 18.0% (5 runs)

### History matching (every measured configuration, all claims together)
- 10 of 55 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr, max_steps`: lr=0.5, max_steps=100 (max I 0.09); lr=1, max_steps=100 (max I 2.66)
  - `max_steps`: max_steps=100 (max I 0.39)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.73); lr_schedule=inv, max_steps=100 (max I 0.89)
  - `lr`: lr=0.02 (max I 2.11); lr=1 (max I 2.13); lr=0.01 (max I 2.16); lr=0.05 (max I 2.21); +1 more

Notes:
- stopped early: run budget of 200 reached (wanted 3 more run(s) of {'lr': '0.01', 'lr_schedule': 'inv'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 6 | +0.5% | -0.6% | 0.6% |
| `max_steps=100`, `lr=0.5` | 5 | +1.3% | +4.8% | 3.1% |
| `max_steps=100`, `lr_schedule=linear` | 5 | -4.6% | -30.5% | 17.6% |
| `max_steps=100`, `lr_schedule=inv` | 5 | -7.5% | -28.5% | 18.0% |
| `lr=0.2` | 6 | +75.8% | +16.6% | 46.2% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `theta_clamp_min`, `theta_clamp_max`, `omega_clamp_min`, `omega_clamp_max`, `discretise_formula`, `RL_SEED_BASE`, `RUN_TAG`, `python_version`, `random_module_behavior`, `os_hardware_fp`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
