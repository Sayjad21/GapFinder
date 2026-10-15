# Gap Report: test-v12-08

Artifact `rlbench` · generated 2026-10-15 09:07 · 199 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +84.0% | -3.5% | ±11.9% | `lr=1` |

## C1: mean_reward (paper 98.685)
**Fits but unsupported** · gap +84.0% → -3.5% · 55 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0009`, `B0034`, `B0035`, `B0075`, `B0076`, `B0077` (6 run(s) of the same config)
- Config: `lr` naive `0.1`, changed to `1`
- Command:

  Replay: fork checkpoint `2b531e79-1206-4283-887c-1818fc9e81b7` and run
  ```
  RUN_TAG=790aafd51385 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 98.66, 98.45, 69.72, 92.01, 78.2, 101.7; gap after -3.5%; result checkpoint `9f2925bb-1896-4164-8175-50e8a09ccca0`
- Effect: candidate 95.23 minus naive 181.5 = -86.31, 95% bootstrap interval [-117.9, -79.06] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 98.7 on CartPole; the worst of its seeds reaches 95.4.

- p. 1; value used: `mean_reward` = 98.685 (headline claim)

### What did we measure?
- Naive median 181.5 over 5 runs; repeats: 198.1, 175.7, 181.5, 194.4, 176.4
- Spread: range 175.7 to 198.1, noise band ±11.7 (2 x MAD), CV 5.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +84.0% (noise band ±11.9% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr` the gap is +84.0% (it comes back)
- PASS · Held-out claim: C2: -52.4% to -86.9% (not worse beyond noise)
- FAIL · Evidence: `lr=1`: no evidence mentions '1'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -86.31 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `theta_clamp_min`, `theta_clamp_max`, `omega_clamp_min`, `omega_clamp_max`, `discretise_formula`, `RL_SEED_BASE`, `RUN_TAG`, `python_version`, `random_module_behavior`, `os_hardware_fp`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=100` (7.04 noise units, gap +0.5%); `lr=0.01` (7 noise units, gap +0.9%); `lr=0.002` (6.03 noise units, gap -12.4%); `lr=0.05` (5.13 noise units, gap +23.2%); `lr=0.02` (4.77 noise units, gap -27.4%) (and 6 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr=1`, `max_steps=100`, `lr_schedule=inv`: this claim +1.3%, mean |gap| 3.1% (5 runs)
  - `max_steps=100`: this claim -4.4%, mean |gap| 27.1% (6 runs)
  - `max_steps=100`, `lr_schedule=inv`: this claim -19.8%, mean |gap| 45.5% (5 runs)

### History matching (every measured configuration, all claims together)
- 15 of 55 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.01); lr_schedule=inv, max_steps=100 (max I 2.11)
  - `lr, lr_schedule, max_steps`: lr=1, lr_schedule=inv, max_steps=100 (max I 0.16)
  - `max_steps`: max_steps=100 (max I 0.71)
  - `lr, lr_schedule`: lr=0.05, lr_schedule=inv (max I 1.51); lr=0.002, lr_schedule=linear (max I 2.18); lr=0.01, lr_schedule=linear (max I 2.22)
  - `lr`: lr=0.02 (max I 1.65); lr=1 (max I 1.67); lr=0.01 (max I 2.03)

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'lr': '1', 'max_steps': '40'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr=1`, `max_steps=100`, `lr_schedule=inv` | 5 | +1.3% | +4.8% | 3.1% |
| `max_steps=100` | 6 | -4.4% | -49.9% | 27.1% |
| `lr=1` | 6 | -3.5% | -86.9% | 45.2% |
| `max_steps=100`, `lr_schedule=inv` | 5 | -19.8% | -71.2% | 45.5% |
| `lr=0.05` | 6 | +19.4% | -73.8% | 46.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `theta_clamp_min`, `theta_clamp_max`, `omega_clamp_min`, `omega_clamp_max`, `discretise_formula`, `RL_SEED_BASE`, `RUN_TAG`, `python_version`, `random_module_behavior`, `os_hardware_fp`

## Provenance
- GapFinder commit: `f01fe3d9a0095f98d6304ad0543b917ca8e529eb` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0441, sandbox reported $0.0000 (total $0.0441; this search; ledger extraction is included only if it shared the search's router)
