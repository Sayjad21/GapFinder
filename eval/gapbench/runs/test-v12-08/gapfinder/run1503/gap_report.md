# Gap Report: test-v12-08

Artifact `rlbench` · generated 2026-10-15 19:30 · 161 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +91.3% | -0.6% | ±8.2% | `max_steps=100` |

## C1: mean_reward (paper 98.685)
**Fits but unsupported** · gap +91.3% → -0.6% · 55 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0021`, `B0058`, `B0059`, `B0072` (4 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `766cb3bb-9663-468e-b194-bb64d3a8b634` and run
  ```
  RUN_TAG=eef9c7977afc "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 92.5, 97.22, 98.95, 99.92; gap after -0.6%; result checkpoint `3b8d00da-2b26-433e-845e-0a4687561725`
- Effect: candidate 98.09 minus naive 188.8 = -90.71, 95% bootstrap interval [-96.72, -82.72] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 98.7 on CartPole; the worst of its seeds reaches 95.4.

- p. 1; value used: `mean_reward` = 98.685 (headline claim)

### What did we measure?
- Naive median 188.8 over 5 runs; repeats: 196.1, 188.8, 192.6, 181.3, 184.7
- Spread: range 181.3 to 196.1, noise band ±8.13 (2 x MAD), CV 3.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +91.3% (noise band ±8.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +91.3% (it comes back)
- PASS · Held-out claim: C2: +50.7% to -11.5% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -90.71 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `theta_clamp_min`, `theta_clamp_max`, `omega_clamp_min`, `omega_clamp_max`, `discretise_formula`, `RL_SEED_BASE`, `RUN_TAG`, `python_version`, `random_module_behavior`, `os_hardware_fp`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr=1` (10.45 noise units, gap -5.3%); `lr=0.01` (10.37 noise units, gap +5.9%); `lr=0.05` (7.28 noise units, gap +31.3%); `lr=0.002` (6.1 noise units, gap -41.1%); `lr=0.5` (5.64 noise units, gap +44.9%) (and 7 more in the JSON)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `lr_schedule=linear`: this claim -1.2%, mean |gap| 2.2% (3 runs)
  - `lr_schedule=inv`, `max_steps=100`, `lr=1`: this claim +1.3%, mean |gap| 3.1% (3 runs)
  - `lr_schedule=inv`, `max_steps=100`: this claim -10.7%, mean |gap| 34.1% (3 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `lr_schedule=linear, max_steps=100`
- `lr=1, lr_schedule=inv, max_steps=100`

### History matching (every measured configuration, all claims together)
- 9 of 55 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 9 configurations
  - `lr, lr_schedule, max_steps`: lr=1, lr_schedule=inv, max_steps=100 (max I 0.2)
  - `max_steps`: max_steps=100 (max I 0.56)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.76); lr_schedule=inv, max_steps=100 (max I 2.05)
  - `lr`: lr=1 (max I 2.02); lr=0.01 (max I 2.45)
  - `lr, lr_schedule`: lr=0.002, lr_schedule=inv (max I 2.54); lr=0.05, lr_schedule=linear (max I 2.81); lr=0.05, lr_schedule=inv (max I 2.82)
- 3 separate islands (no single-knob move joins them): lr=1, lr_schedule=inv, max_steps=100; max_steps=100; lr_schedule=linear, max_steps=100 | lr=0.002, lr_schedule=inv; lr=0.05, lr_schedule=linear; lr=0.05, lr_schedule=inv | lr=1; lr=0.01

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=100; lr_schedule=linear, max_steps=100; lr=1, lr_schedule=inv, max_steps=100

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100`, `lr_schedule=linear` | 3 | -1.2% | -3.3% | 2.2% |
| `lr_schedule=inv`, `max_steps=100`, `lr=1` | 3 | +1.3% | +4.8% | 3.1% |
| `max_steps=100` | 4 | -0.6% | -11.5% | 6.0% |
| `lr_schedule=inv`, `max_steps=100` | 3 | -10.7% | -57.4% | 34.1% |
| `lr=1` | 4 | -3.4% | -77.6% | 40.5% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `theta_clamp_min`, `theta_clamp_max`, `omega_clamp_min`, `omega_clamp_max`, `discretise_formula`, `RL_SEED_BASE`, `RUN_TAG`, `python_version`, `random_module_behavior`, `os_hardware_fp`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
