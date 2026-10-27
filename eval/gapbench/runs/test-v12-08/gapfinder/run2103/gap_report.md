# Gap Report: test-v12-08

Artifact `rlbench` · generated 2026-10-15 21:11 · 152 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +84.1% | +0.4% | ±10.3% | `max_steps=100` |

## C1: mean_reward (paper 98.685)
**Fits but unsupported** · gap +84.1% → +0.4% · 55 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0023`, `B0062`, `B0063`, `B0072` (4 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `0d90150b-0cc8-4c32-a52f-a29bf72e5d84` and run
  ```
  RUN_TAG=5fbd16bad516 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 94.89, 99.12, 99.11, 99.72; gap after +0.4%; result checkpoint `a5410409-3d84-487c-a67f-bb3d5b60482c`
- Effect: candidate 99.12 minus naive 181.7 = -82.59, 95% bootstrap interval [-88.7, -69.75] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 98.7 on CartPole; the worst of its seeds reaches 95.4.

- p. 1; value used: `mean_reward` = 98.685 (headline claim)

### What did we measure?
- Naive median 181.7 over 5 runs; repeats: 181.7, 167.2, 190.3, 184, 176.6
- Spread: range 167.2 to 190.3, noise band ±10.13 (2 x MAD), CV 4.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +84.1% (noise band ±10.3% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +84.1% (it comes back)
- PASS · Held-out claim: C2: -47.0% to +0.2% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -82.59 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `theta_clamp_min`, `theta_clamp_max`, `omega_clamp_min`, `omega_clamp_max`, `discretise_formula`, `RL_SEED_BASE`, `RUN_TAG`, `python_version`, `random_module_behavior`, `os_hardware_fp`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr=0.002` (8.02 noise units, gap -1.8%); `lr=0.02` (7.83 noise units, gap +3.8%); `lr=1` (7 noise units, gap -12.3%); `lr=0.05` (6.69 noise units, gap +15.4%); `lr_schedule=inv` (5.71 noise units, gap +25.5%) (and 5 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `max_steps=100`: this claim -1.2%, mean |gap| 2.0% (3 runs)
  - `lr=1`, `lr_schedule=inv`, `max_steps=100`: this claim +1.3%, mean |gap| 3.1% (3 runs)
  - `lr_schedule=inv`, `max_steps=100`: this claim -11.5%, mean |gap| 35.8% (3 runs)

### Equally good configurations
The target claim can't tell these 5 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `lr=1`
- `lr_schedule=linear, max_steps=100`
- `lr=0.02, lr_schedule=inv`
- `lr=1, lr_schedule=inv, max_steps=100`

### History matching (every measured configuration, all claims together)
- 9 of 55 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 9 configurations
  - `lr, lr_schedule, max_steps`: lr=1, lr_schedule=inv, max_steps=100 (max I 0.16)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.24); lr_schedule=inv, max_steps=100 (max I 2.28)
  - `max_steps`: max_steps=100 (max I 0.29)
  - `lr, lr_schedule`: lr=0.02, lr_schedule=inv (max I 1.79); lr=0.05, lr_schedule=linear (max I 2.28)
  - `lr`: lr=1 (max I 2.2); lr=0.02 (max I 2.56); lr=0.01 (max I 2.9)
- 3 separate islands (no single-knob move joins them): lr=1, lr_schedule=inv, max_steps=100; lr_schedule=linear, max_steps=100; max_steps=100 | lr=0.02, lr_schedule=inv; lr=1; lr=0.02 | lr=0.05, lr_schedule=linear

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=100; lr=1; lr_schedule=linear, max_steps=100; lr=0.02, lr_schedule=inv; lr=1, lr_schedule=inv, max_steps=100

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 4 | +0.4% | +0.2% | 0.3% |
| `lr_schedule=linear`, `max_steps=100` | 3 | -1.2% | -2.8% | 2.0% |
| `lr=1`, `lr_schedule=inv`, `max_steps=100` | 3 | +1.3% | +4.8% | 3.1% |
| `lr_schedule=inv`, `max_steps=100` | 3 | -11.5% | -60.1% | 35.8% |
| `lr_schedule=inv`, `lr=0.02` | 3 | +0.6% | -81.5% | 41.1% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `theta_clamp_min`, `theta_clamp_max`, `omega_clamp_min`, `omega_clamp_max`, `discretise_formula`, `RL_SEED_BASE`, `RUN_TAG`, `python_version`, `random_module_behavior`, `os_hardware_fp`

## Provenance
- GapFinder commit: `cd8c8af2b9d079dd9a57443ed501c0dd8a467d34` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
