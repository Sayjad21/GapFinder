# Gap Report: test-v12-08

Artifact `rlbench` · generated 2026-10-15 19:54 · 199 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +80.2% | +0.8% | ±17.4% | `max_steps=100` |

## C1: mean_reward (paper 98.685)
**Fits but unsupported** · gap +80.2% → +0.8% · 54 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0021`, `B0058`, `B0059`, `B0070`, `B0071`, `B0072` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `807450fe-1403-44a3-bcb8-2d90a85060e8` and run
  ```
  RUN_TAG=7b255ea2754c "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 96.4, 99.65, 95.62, 99.41, 99.5, 99.67; gap after +0.8%; result checkpoint `09722649-db47-40ce-962f-b3f96b7eddc6`
- Effect: candidate 99.45 minus naive 177.8 = -78.39, 95% bootstrap interval [-89.4, -60.73] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 98.7 on CartPole; the worst of its seeds reaches 95.4.

- p. 1; value used: `mean_reward` = 98.685 (headline claim)

### What did we measure?
- Naive median 177.8 over 5 runs; repeats: 180.9, 169.3, 155.8, 190.4, 177.8
- Spread: range 155.8 to 190.4, noise band ±17.14 (2 x MAD), CV 7.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +80.2% (noise band ±17.4% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +80.2% (it comes back)
- PASS · Held-out claim: C2: -49.2% to +1.8% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -78.39 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `theta_clamp_min`, `theta_clamp_max`, `omega_clamp_min`, `omega_clamp_max`, `discretise_formula`, `RL_SEED_BASE`, `RUN_TAG`, `python_version`, `random_module_behavior`, `os_hardware_fp`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr=1` (4.5 noise units, gap -2.0%); `lr=0.002` (4.23 noise units, gap +6.7%); `lr=0.01` (3.08 noise units, gap -26.7%); `lr=0.001` (2.78 noise units, gap -31.9%); `lr=0.5` (2.7 noise units, gap +33.2%) (and 5 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `max_steps=100`: this claim -0.7%, mean |gap| 1.2% (5 runs)
  - `lr_schedule=inv`, `max_steps=100`: this claim -16.1%, mean |gap| 42.8% (5 runs)
  - `lr=0.01`, `lr_schedule=linear`: this claim +8.0%, mean |gap| 44.7% (5 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `lr_schedule=linear, max_steps=100`
- `lr=0.01, lr_schedule=linear`

### History matching (every measured configuration, all claims together)
- 11 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.09); lr_schedule=inv, max_steps=100 (max I 1.81)
  - `max_steps`: max_steps=100 (max I 0.29)
  - `lr, lr_schedule`: lr=0.01, lr_schedule=linear (max I 2.25); lr=0.01, lr_schedule=inv (max I 2.49)
  - `lr, max_steps`: lr=1, max_steps=100 (max I 2.47)
  - `lr`: lr=0.02 (max I 2.48); lr=1 (max I 2.57); lr=0.002 (max I 2.6); lr=0.05 (max I 2.61)
- 2 separate islands (no single-knob move joins them): lr_schedule=linear, max_steps=100; max_steps=100; lr_schedule=inv, max_steps=100 | lr=0.01, lr_schedule=linear; lr=0.01, lr_schedule=inv

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=100; lr_schedule=linear, max_steps=100; lr=0.01, lr_schedule=linear

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=linear`, `max_steps=100` | 5 | -0.7% | -1.7% | 1.2% |
| `max_steps=100` | 6 | +0.8% | +1.8% | 1.3% |
| `lr_schedule=inv`, `max_steps=100` | 5 | -16.1% | -69.5% | 42.8% |
| `lr=0.01`, `lr_schedule=linear` | 5 | +8.0% | -81.3% | 44.7% |
| `lr=1` | 6 | -16.7% | -87.1% | 51.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `theta_clamp_min`, `theta_clamp_max`, `omega_clamp_min`, `omega_clamp_max`, `discretise_formula`, `RL_SEED_BASE`, `RUN_TAG`, `python_version`, `random_module_behavior`, `os_hardware_fp`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
