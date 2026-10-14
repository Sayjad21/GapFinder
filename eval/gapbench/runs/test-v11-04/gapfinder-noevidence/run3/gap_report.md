# Gap Report: test-v11-04

Artifact `rlbench` · generated 2026-10-14 12:35 · 198 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +90.5% | +1.9% | ±3.7% | `lr_schedule=linear`, `max_steps=100` |

## C1: mean_reward (paper 94.93)
**Fits but unsupported** · gap +90.5% → +1.9% · 47 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0095`, `B0143`, `B0144`, `B0145`, `B0146` (5 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `linear`
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `3b04cc68-4ae0-4dc2-9623-b6335a59d6cc` and run
  ```
  RUN_TAG=3541eaf2aa1d "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule linear --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 92.68, 96.75, 98.52, 96.14, 98.81; gap after +1.9%; result checkpoint `2719c396-cb9b-4115-9db6-5956c738d342`
- Effect: candidate 96.75 minus naive 180.9 = -84.14, 95% bootstrap interval [-99.8, -74.31] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 94.9 on CartPole; the worst of its seeds reaches 63.9.

- p. 1; value used: `mean_reward` = 94.93 reward (headline claim)

### What did we measure?
- Naive median 180.9 over 5 runs; repeats: 182.7, 200, 179.8, 180.9, 169.4
- Spread: range 169.4 to 200, noise band ±3.55 (2 x MAD), CV 6.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +90.5% (noise band ±3.7% of the paper value)

### Why do we believe it?
- FAIL · Counterfactual (reversal test): without `lr_schedule` the gap is +3.4% (it did NOT come back)
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +78.7% (it comes back)
- PASS · Held-out claim: C2: +61.0% to +44.4% (not worse beyond noise)
- FAIL · Evidence: `lr_schedule=linear`: evidence gate off: no evidence was looked for
- FAIL · Evidence: `max_steps=100`: evidence gate off: no evidence was looked for
- PASS · Effect vs noise: candidate minus naive is -84.14 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `theta_clip_min`, `theta_clip_max`, `omega_clip_min`, `omega_clip_max`, `RL_SEED_BASE`, `RUN_TAG`, `x_threshold`, `theta_threshold`, `reward_per_step`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.5` (18.67 noise units, gap +20.7%); `lr_schedule=inv` (10.13 noise units, gap +52.7%); `eps_start=0.02` (7.93 noise units, gap -60.9%); `eps_start=10` (3.52 noise units, gap +77.4%); `max_steps=20` (3.11 noise units, gap -78.9%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `max_steps=100`: this claim +3.4%, mean |gap| 19.2% (6 runs)
  - `lr_schedule=inv`, `max_steps=100`: this claim -11.8%, mean |gap| 30.0% (5 runs)
  - `eps_start=0.5`, `max_steps=100`: this claim -10.4%, mean |gap| 30.0% (5 runs)

### History matching (every measured configuration, all claims together)
- 7 of 47 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 7 configurations
  - `max_steps`: max_steps=100 (max I 0.32)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.48); lr_schedule=inv, max_steps=100 (max I 1.15)
  - `eps_start, max_steps`: eps_start=10, max_steps=100 (max I 0.8); eps_start=0.5, max_steps=100 (max I 1.31); eps_start=0.1, max_steps=500 (max I 1.42)
  - `eps_start, lr_schedule`: eps_start=0.5, lr_schedule=linear (max I 1.18)
- 3 separate islands (no single-knob move joins them): max_steps=100; lr_schedule=linear, max_steps=100; eps_start=10, max_steps=100 | eps_start=0.5, lr_schedule=linear | eps_start=0.1, max_steps=500

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'max_steps': '500', 'eps_start': '0.02'} for 'confirm-combo')
- evidence gate off: no evidence was checked, so this cannot be labelled Explained
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 6 | +3.4% | +34.9% | 19.2% |
| `lr_schedule=linear`, `max_steps=100` | 5 | +1.9% | +44.4% | 23.2% |
| `lr_schedule=inv`, `max_steps=100` | 5 | -11.8% | -48.2% | 30.0% |
| `eps_start=0.5`, `max_steps=100` | 5 | -10.4% | -49.6% | 30.0% |
| `eps_start=10`, `max_steps=100` | 5 | +5.3% | +56.5% | 30.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `theta_clip_min`, `theta_clip_max`, `omega_clip_min`, `omega_clip_max`, `RL_SEED_BASE`, `RUN_TAG`, `x_threshold`, `theta_threshold`, `reward_per_step`, `--out`

## Provenance
- GapFinder commit: `b05f7288e1a4df8af69bb0b5e7633827b4cb46c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
