# Gap Report: test-v11-04

Artifact `rlbench` · generated 2026-10-15 18:57 · 199 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +90.0% | +1.2% | ±27.6% | `max_steps=100` |

## C1: mean_reward (paper 94.93)
**Fits but unsupported** · gap +90.0% → +1.2% · 55 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0021`, `B0058`, `B0059`, `B0070`, `B0071`, `B0072` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `8a7a1ad4-2208-45c9-a36e-e23d8156d0e2` and run
  ```
  RUN_TAG=4b31c4d49963 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 92.75, 94.06, 99.42, 89.67, 98.16, 99.42; gap after +1.2%; result checkpoint `f5382afc-2439-4d2c-b856-7bd4175e2340`
- Effect: candidate 96.11 minus naive 180.4 = -84.3, 95% bootstrap interval [-101.2, -72.72] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 94.9 on CartPole; the worst of its seeds reaches 63.9.

- p. 1; value used: `mean_reward` = 94.93 reward (headline claim)

### What did we measure?
- Naive median 180.4 over 5 runs; repeats: 180.4, 175.2, 196.6, 167.3, 193.7
- Spread: range 167.3 to 196.6, noise band ±26.18 (2 x MAD), CV 6.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +90.0% (noise band ±27.6% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +90.0% (it comes back)
- PASS · Held-out claim: C2: -25.0% to +11.8% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -84.3 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `theta_clip_min`, `theta_clip_max`, `omega_clip_min`, `omega_clip_max`, `RL_SEED_BASE`, `RUN_TAG`, `x_threshold`, `theta_threshold`, `reward_per_step`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.5` (2.65 noise units, gap +17.1%); `eps_start=0.2` (2.15 noise units, gap -30.8%); `lr_schedule=inv` (1.96 noise units, gap +35.9%); `max_steps=40` (1.17 noise units, gap -57.9%)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `max_steps=100`: this claim -1.9%, mean |gap| 5.3% (5 runs)
  - `lr_schedule=inv`, `max_steps=100`: this claim -10.3%, mean |gap| 24.9% (5 runs)
  - `max_steps=100`, `eps_start=50`: this claim +5.3%, mean |gap| 30.7% (5 runs)

### Equally good configurations
The target claim can't tell these 4 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `lr_schedule=linear, max_steps=100`
- `lr_schedule=inv, max_steps=100`
- `eps_start=0.5, lr_schedule=linear`

### History matching (every measured configuration, all claims together)
- 9 of 55 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 9 configurations
  - `max_steps`: max_steps=100 (max I 0.09)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.1); lr_schedule=inv, max_steps=100 (max I 0.96)
  - `eps_start, max_steps`: eps_start=50, max_steps=100 (max I 0.52); eps_start=0.5, max_steps=100 (max I 2.93)
  - `eps_start, lr_schedule`: eps_start=0.5, lr_schedule=linear (max I 0.95); eps_start=0.5, lr_schedule=inv (max I 2.88)
  - `eps_start`: eps_start=0.2 (max I 2.5); eps_start=0.5 (max I 2.77)

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=100; lr_schedule=linear, max_steps=100; lr_schedule=inv, max_steps=100; eps_start=0.5, lr_schedule=linear

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=linear`, `max_steps=100` | 5 | -1.9% | -8.6% | 5.3% |
| `max_steps=100` | 6 | +1.2% | +11.8% | 6.5% |
| `lr_schedule=inv`, `max_steps=100` | 5 | -10.3% | -39.4% | 24.9% |
| `max_steps=100`, `eps_start=50` | 5 | +5.3% | +56.1% | 30.7% |
| `lr_schedule=inv` | 6 | +37.5% | -38.0% | 37.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `theta_clip_min`, `theta_clip_max`, `omega_clip_min`, `omega_clip_max`, `RL_SEED_BASE`, `RUN_TAG`, `x_threshold`, `theta_threshold`, `reward_per_step`, `--out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
