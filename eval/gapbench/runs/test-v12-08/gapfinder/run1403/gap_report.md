# Gap Report: test-v12-08

Artifact `rlbench` · generated 2026-10-15 19:07 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +90.7% | -1.3% | ±24.0% | `max_steps=100` |

## C1: mean_reward (paper 98.685)
**Fits but unsupported** · gap +90.7% → -1.3% · 55 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0021`, `B0058`, `B0059`, `B0072`, `B0073`, `B0074` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `09f256ed-f980-4897-b345-9c6cd224b427` and run
  ```
  RUN_TAG=8d2cc363d9a2 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 95.58, 99.71, 99.52, 89.97, 98.97, 95.78; gap after -1.3%; result checkpoint `64638dac-9502-45cc-aa13-46aff3f542c6`
- Effect: candidate 97.37 minus naive 188.2 = -90.78, 95% bootstrap interval [-102.5, -58.66] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 98.7 on CartPole; the worst of its seeds reaches 95.4.

- p. 1; value used: `mean_reward` = 98.685 (headline claim)

### What did we measure?
- Naive median 188.2 over 5 runs; repeats: 165.9, 188.7, 188.2, 150.9, 200
- Spread: range 150.9 to 200, noise band ±23.7 (2 x MAD), CV 11.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +90.7% (noise band ±24.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +90.7% (it comes back)
- PASS · Held-out claim: C2: -14.6% to -17.6% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -90.78 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `theta_clamp_min`, `theta_clamp_max`, `omega_clamp_min`, `omega_clamp_max`, `discretise_formula`, `RL_SEED_BASE`, `RUN_TAG`, `python_version`, `random_module_behavior`, `os_hardware_fp`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr=1` (3.42 noise units, gap -8.5%); `lr=0.5` (3.11 noise units, gap +15.9%); `lr=0.001` (3.11 noise units, gap -16.0%); `lr=0.05` (2.87 noise units, gap +21.7%); `lr_schedule=inv` (2.63 noise units, gap +27.4%) (and 5 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr=0.5`, `max_steps=100`: this claim +1.3%, mean |gap| 3.1% (5 runs)
  - `max_steps=100`, `lr_schedule=linear`: this claim -4.0%, mean |gap| 16.3% (5 runs)
  - `lr=0.05`, `max_steps=100`: this claim -13.1%, mean |gap| 43.7% (2 runs)

### History matching (every measured configuration, all claims together)
- 20 of 55 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr, max_steps`: lr=0.5, max_steps=100 (max I 0.09); lr=0.05, max_steps=100 (max I 1.21); lr=1, max_steps=100 (max I 1.63)
  - `max_steps`: max_steps=100 (max I 0.47)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.66); lr_schedule=inv, max_steps=100 (max I 1.29)
  - `lr, lr_schedule`: lr=0.05, lr_schedule=linear (max I 1.56); lr=0.001, lr_schedule=linear (max I 1.78)
  - `lr`: lr=0.5 (max I 1.76); lr=0.01 (max I 1.83)

Notes:
- stopped early: run budget of 200 reached (wanted 3 more run(s) of {'max_steps': '100', 'lr': '0.05'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr=0.5`, `max_steps=100` | 5 | +1.3% | +4.8% | 3.1% |
| `max_steps=100` | 6 | -1.3% | -17.6% | 9.4% |
| `max_steps=100`, `lr_schedule=linear` | 5 | -4.0% | -28.5% | 16.3% |
| `lr=0.05`, `max_steps=100` | 2 | -13.1% | -74.3% | 43.7% |
| `lr=0.05`, `lr_schedule=inv` | 5 | +0.8% | -86.7% | 43.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `theta_clamp_min`, `theta_clamp_max`, `omega_clamp_min`, `omega_clamp_max`, `discretise_formula`, `RL_SEED_BASE`, `RUN_TAG`, `python_version`, `random_module_behavior`, `os_hardware_fp`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
