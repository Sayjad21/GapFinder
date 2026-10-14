# Gap Report: test-v11-04

Artifact `rlbench` · generated 2026-10-14 12:35 · 181 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +93.3% | +2.1% | ±12.6% | `max_steps=100` |

## C1: mean_reward (paper 94.93)
**Fits but unsupported** · gap +93.3% → +2.1% · 47 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0017`, `B0075`, `B0076`, `B0077`, `B0078`, `B0079` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `07a76d7a-e767-4d8f-b070-6acdf5b84a5d` and run
  ```
  RUN_TAG=d3ba26ec8735 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 99.44, 92.41, 99.84, 93, 94.48, 99.31; gap after +2.1%; result checkpoint `7db4bab3-8aaa-4e90-b9bc-831b3fda614d`
- Effect: candidate 96.9 minus naive 183.5 = -86.58, 95% bootstrap interval [-99.12, -66.46] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 94.9 on CartPole; the worst of its seeds reaches 63.9.

- p. 1; value used: `mean_reward` = 94.93 reward (headline claim)

### What did we measure?
- Naive median 183.5 over 5 runs; repeats: 189.5, 157.5, 183.5, 195.8, 180
- Spread: range 157.5 to 195.8, noise band ±11.96 (2 x MAD), CV 8.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +93.3% (noise band ±12.6% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +93.3% (it comes back)
- PASS · Held-out claim: C2: -7.0% to +23.9% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -86.58 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `theta_clip_min`, `theta_clip_max`, `omega_clip_min`, `omega_clip_max`, `RL_SEED_BASE`, `RUN_TAG`, `x_threshold`, `theta_threshold`, `reward_per_step`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.5` (6.4 noise units, gap +12.7%); `lr_schedule=inv` (5.86 noise units, gap +19.5%); `eps_start=0.1` (4.1 noise units, gap -41.6%); `eps_start=0.02` (2.33 noise units, gap -63.9%); `eps_start=0.0` (1.57 noise units, gap -73.4%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `lr_schedule=linear`: this claim +2.3%, mean |gap| 18.0% (5 runs)
  - `eps_start=0.5`: this claim +41.9%, mean |gap| 32.8% (6 runs)
  - `max_steps=100`, `lr_schedule=inv`: this claim -12.7%, mean |gap| 36.1% (5 runs)

### History matching (every measured configuration, all claims together)
- 8 of 47 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 8 configurations
  - `max_steps`: max_steps=100 (max I 0.18)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.35); lr_schedule=inv, max_steps=100 (max I 1.22)
  - `eps_start, max_steps`: eps_start=0.5, max_steps=100 (max I 1.04); eps_start=0.0, max_steps=1000 (max I 2.46)
  - `eps_start, lr_schedule`: eps_start=0.5, lr_schedule=inv (max I 1.23); eps_start=0.5, lr_schedule=linear (max I 1.51)
  - `lr_schedule`: lr_schedule=inv (max I 2.93)
- 2 separate islands (no single-knob move joins them): max_steps=100; lr_schedule=linear, max_steps=100; eps_start=0.5, max_steps=100 | eps_start=0.0, max_steps=1000

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 6 | +2.1% | +23.9% | 13.0% |
| `max_steps=100`, `lr_schedule=linear` | 5 | +2.3% | +33.6% | 18.0% |
| `eps_start=0.5` | 6 | +41.9% | -23.8% | 32.8% |
| `max_steps=100`, `lr_schedule=inv` | 5 | -12.7% | -59.5% | 36.1% |
| `max_steps=100`, `eps_start=0.5` | 5 | -9.0% | -67.1% | 38.1% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `theta_clip_min`, `theta_clip_max`, `omega_clip_min`, `omega_clip_max`, `RL_SEED_BASE`, `RUN_TAG`, `x_threshold`, `theta_threshold`, `reward_per_step`, `--out`

## Provenance
- GapFinder commit: `b05f7288e1a4df8af69bb0b5e7633827b4cb46c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0631, sandbox reported $0.0000 (total $0.0631; this search; ledger extraction is included only if it shared the search's router)
