# Gap Report: test-v11-04

Artifact `rlbench` · generated 2026-10-15 19:46 · 190 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +89.1% | -3.2% | ±24.0% | `max_steps=100` |

## C1: mean_reward (paper 94.93)
**Fits but unsupported** · gap +89.1% → -3.2% · 55 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0021`, `B0058`, `B0059`, `B0070`, `B0071`, `B0072` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `bdc5a539-d16c-4bfc-90f5-44d424e73d3f` and run
  ```
  RUN_TAG=7f76ec06ced7 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 98.58, 93.36, 88.42, 96.03, 88.84, 90.36; gap after -3.2%; result checkpoint `2447e6d0-4e19-4c35-9ca9-e2df14f12dc8`
- Effect: candidate 91.86 minus naive 179.5 = -87.67, 95% bootstrap interval [-100.9, -75.13] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 94.9 on CartPole; the worst of its seeds reaches 63.9.

- p. 1; value used: `mean_reward` = 94.93 reward (headline claim)

### What did we measure?
- Naive median 179.5 over 5 runs; repeats: 168.1, 183.7, 167.3, 195, 179.5
- Spread: range 167.3 to 195, noise band ±22.8 (2 x MAD), CV 6.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +89.1% (noise band ±24.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +89.1% (it comes back)
- PASS · Held-out claim: C2: +42.2% to -7.0% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -87.67 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `theta_clip_min`, `theta_clip_max`, `omega_clip_min`, `omega_clip_max`, `RL_SEED_BASE`, `RUN_TAG`, `x_threshold`, `theta_threshold`, `reward_per_step`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.5` (2.93 noise units, gap +18.8%); `eps_start=0.2` (2.5 noise units, gap -29.0%); `eps_start=0.02` (2.1 noise units, gap -38.7%); `eps_start=0.01` (1.85 noise units, gap -44.7%); `eps_start=0.0` (1.42 noise units, gap -55.0%) (and 3 more in the JSON)
- Near alternatives (closest across all claims):
  - `eps_start=0.5`, `max_steps=100`: this claim -2.1%, mean |gap| 20.5% (5 runs)
  - `lr_schedule=linear`, `max_steps=100`: this claim +1.8%, mean |gap| 21.1% (5 runs)
  - `lr_schedule=inv`, `max_steps=100`: this claim -10.4%, mean |gap| 30.2% (5 runs)

### Equally good configurations
The target claim can't tell these 4 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `lr_schedule=linear, max_steps=100`
- `eps_start=0.5, max_steps=100`
- `eps_start=0.5, lr_schedule=linear`

### History matching (every measured configuration, all claims together)
- 6 of 55 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 6 configurations
  - `max_steps`: max_steps=100 (max I 0.27)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.41); lr_schedule=inv, max_steps=100 (max I 1.07)
  - `eps_start, max_steps`: eps_start=0.5, max_steps=100 (max I 0.83)
  - `eps_start, lr_schedule`: eps_start=0.5, lr_schedule=linear (max I 1.67)
  - `eps_start`: eps_start=0.2 (max I 2.31)
- 3 separate islands (no single-knob move joins them): max_steps=100; lr_schedule=linear, max_steps=100; eps_start=0.5, max_steps=100 | eps_start=0.5, lr_schedule=linear | eps_start=0.2

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=100; lr_schedule=linear, max_steps=100; eps_start=0.5, max_steps=100; eps_start=0.5, lr_schedule=linear

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 6 | -3.2% | -7.0% | 5.1% |
| `eps_start=0.5`, `max_steps=100` | 5 | -2.1% | -38.8% | 20.5% |
| `lr_schedule=linear`, `max_steps=100` | 5 | +1.8% | +40.5% | 21.1% |
| `lr_schedule=inv`, `max_steps=100` | 5 | -10.4% | -50.0% | 30.2% |
| `lr_schedule=inv` | 6 | +57.3% | +6.5% | 31.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `theta_clip_min`, `theta_clip_max`, `omega_clip_min`, `omega_clip_max`, `RL_SEED_BASE`, `RUN_TAG`, `x_threshold`, `theta_threshold`, `reward_per_step`, `--out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
