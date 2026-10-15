# Gap Report: test-v12-08

Artifact `rlbench` · generated 2026-10-15 09:08 · 197 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +74.8% | -1.0% | ±9.0% | `max_steps=100` |

## C1: mean_reward (paper 98.685)
**Fits but unsupported** · gap +74.8% → -1.0% · 55 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0021`, `B0058`, `B0059`, `B0070`, `B0071`, `B0072` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `0dbdb34d-e0db-435f-9444-30304a0da1bb` and run
  ```
  RUN_TAG=6929744cad56 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 90.95, 99.92, 99.5, 85.98, 95.94, 99.88; gap after -1.0%; result checkpoint `ed4e0e27-1279-4a3d-8267-a97ce796e0d1`
- Effect: candidate 97.72 minus naive 172.5 = -74.78, 95% bootstrap interval [-84.68, -51.19] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 98.7 on CartPole; the worst of its seeds reaches 95.4.

- p. 1; value used: `mean_reward` = 98.685 (headline claim)

### What did we measure?
- Naive median 172.5 over 5 runs; repeats: 142.4, 175.9, 172.5, 177, 167.6
- Spread: range 142.4 to 177, noise band ±8.91 (2 x MAD), CV 8.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +74.8% (noise band ±9.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +74.8% (it comes back)
- PASS · Held-out claim: C2: -55.2% to -17.1% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: evidence gate off: no evidence was looked for
- PASS · Effect vs noise: candidate minus naive is -74.78 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `theta_clamp_min`, `theta_clamp_max`, `omega_clamp_min`, `omega_clamp_max`, `discretise_formula`, `RL_SEED_BASE`, `RUN_TAG`, `python_version`, `random_module_behavior`, `os_hardware_fp`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr=0.02` (7.27 noise units, gap -9.1%); `lr=0.5` (6.87 noise units, gap +12.8%); `lr=0.002` (6.83 noise units, gap -13.1%); `lr=1` (5.96 noise units, gap +21.0%); `lr=0.01` (5.83 noise units, gap -22.2%) (and 5 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`, `max_steps=100`, `lr=1`: this claim +1.3%, mean |gap| 3.1% (5 runs)
  - `lr=0.5`, `max_steps=100`: this claim +0.3%, mean |gap| 3.2% (5 runs)
  - `lr_schedule=inv`, `max_steps=100`: this claim -12.7%, mean |gap| 34.5% (5 runs)

### History matching (every measured configuration, all claims together)
- 4 of 55 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 4 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.07)
  - `lr, lr_schedule, max_steps`: lr=1, lr_schedule=inv, max_steps=100 (max I 0.3)
  - `lr, max_steps`: lr=0.5, max_steps=100 (max I 0.89)
  - `max_steps`: max_steps=100 (max I 1.62)
- 2 separate islands (no single-knob move joins them): lr_schedule=linear, max_steps=100; lr=0.5, max_steps=100; max_steps=100 | lr=1, lr_schedule=inv, max_steps=100

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'max_steps': '40', 'lr': '0.5'} for 'confirm-combo')
- evidence gate off: no evidence was checked, so this cannot be labelled Explained
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv`, `max_steps=100`, `lr=1` | 5 | +1.3% | +4.8% | 3.1% |
| `lr=0.5`, `max_steps=100` | 5 | +0.3% | -6.2% | 3.2% |
| `max_steps=100` | 6 | -1.0% | -17.1% | 9.0% |
| `lr_schedule=inv`, `max_steps=100` | 5 | -12.7% | -56.4% | 34.5% |
| `lr=1` | 6 | -6.3% | -84.0% | 45.1% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `theta_clamp_min`, `theta_clamp_max`, `omega_clamp_min`, `omega_clamp_max`, `discretise_formula`, `RL_SEED_BASE`, `RUN_TAG`, `python_version`, `random_module_behavior`, `os_hardware_fp`

## Provenance
- GapFinder commit: `f01fe3d9a0095f98d6304ad0543b917ca8e529eb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
