# Gap Report: test-v11-04

Artifact `rlbench` · generated 2026-10-15 19:46 · 198 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +89.7% | +4.6% | ±22.6% | `max_steps=100` |

## C1: mean_reward (paper 94.93)
**Fits but unsupported** · gap +89.7% → +4.6% · 55 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0021`, `B0058`, `B0059`, `B0078`, `B0079`, `B0080` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `47237508-510d-4df2-a217-f4cf4a84b748` and run
  ```
  RUN_TAG=eb8fdd860909 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 99.52, 99.23, 99.55, 90.17, 88.48, 99.44; gap after +4.6%; result checkpoint `6ef8ddd6-a49b-4aa7-847a-d1b2344e0500`
- Effect: candidate 99.33 minus naive 180.1 = -80.79, 95% bootstrap interval [-97.83, -67.37] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 94.9 on CartPole; the worst of its seeds reaches 63.9.

- p. 1; value used: `mean_reward` = 94.93 reward (headline claim)

### What did we measure?
- Naive median 180.1 over 5 runs; repeats: 164.7, 164.9, 180.1, 189.9, 190.8
- Spread: range 164.7 to 190.8, noise band ±21.44 (2 x MAD), CV 7.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +89.7% (noise band ±22.6% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +89.7% (it comes back)
- PASS · Held-out claim: C2: -7.0% to +47.2% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -80.79 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `theta_clip_min`, `theta_clip_max`, `omega_clip_min`, `omega_clip_max`, `RL_SEED_BASE`, `RUN_TAG`, `x_threshold`, `theta_threshold`, `reward_per_step`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.5` (2.58 noise units, gap +31.5%); `eps_start=0.2` (2.42 noise units, gap -35.2%); `lr_schedule=inv` (2.08 noise units, gap +42.8%); `eps_start=0.1` (1.88 noise units, gap -47.3%); `eps_start=50` (1.4 noise units, gap +58.0%) (and 4 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`, `max_steps=100`: this claim -7.5%, mean |gap| 24.2% (5 runs)
  - `max_steps=100`, `lr_schedule=linear`: this claim +4.1%, mean |gap| 27.2% (5 runs)
  - `eps_start=50`, `max_steps=100`: this claim +5.3%, mean |gap| 30.9% (5 runs)

### History matching (every measured configuration, all claims together)
- 10 of 55 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `max_steps`: max_steps=100 (max I 0.24)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.54); lr_schedule=inv, max_steps=100 (max I 0.72); lr_schedule=inv, max_steps=2000 (max I 2.94)
  - `eps_start, max_steps`: eps_start=50, max_steps=100 (max I 0.67); eps_start=0.5, max_steps=100 (max I 1.32)
  - `eps_start, lr_schedule`: eps_start=0.5, lr_schedule=inv (max I 1.58); eps_start=0.5, lr_schedule=linear (max I 1.92)
  - `eps_start`: eps_start=0.5 (max I 2.14); eps_start=0.2 (max I 2.69)

Notes:
- stopped early: run budget of 200 reached (wanted 3 more run(s) of {'max_steps': '100', 'eps_start': '0.5'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv`, `max_steps=100` | 5 | -7.5% | -41.0% | 24.2% |
| `max_steps=100` | 6 | +4.6% | +47.2% | 25.9% |
| `max_steps=100`, `lr_schedule=linear` | 5 | +4.1% | +50.2% | 27.2% |
| `eps_start=50`, `max_steps=100` | 5 | +5.3% | +56.5% | 30.9% |
| `max_steps=2000`, `lr_schedule=inv` | 2 | +36.8% | -36.0% | 36.4% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `theta_clip_min`, `theta_clip_max`, `omega_clip_min`, `omega_clip_max`, `RL_SEED_BASE`, `RUN_TAG`, `x_threshold`, `theta_threshold`, `reward_per_step`, `--out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
