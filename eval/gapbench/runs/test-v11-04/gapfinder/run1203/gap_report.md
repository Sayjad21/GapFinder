# Gap Report: test-v11-04

Artifact `rlbench` · generated 2026-10-15 00:55 · 197 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +81.4% | +4.6% | ±14.4% | `max_steps=100` |

## C1: mean_reward (paper 94.93)
**Fits but unsupported** · gap +81.4% → +4.6% · 55 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0021`, `B0058`, `B0059`, `B0070`, `B0071`, `B0072` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `e6a22ba5-1724-4b72-92e0-2b5b5aa1fc29` and run
  ```
  RUN_TAG=214c62474935 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 94.73, 99.96, 99.7, 99.12, 94.27, 99.41; gap after +4.6%; result checkpoint `51f7c801-ad42-4b92-bc3b-e93bd2c9b422`
- Effect: candidate 99.27 minus naive 172.2 = -72.94, 95% bootstrap interval [-91.28, -65.77] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 94.9 on CartPole; the worst of its seeds reaches 63.9.

- p. 1; value used: `mean_reward` = 94.93 reward (headline claim)

### What did we measure?
- Naive median 172.2 over 5 runs; repeats: 172.2, 189.6, 165.4, 165.4, 186.7
- Spread: range 165.4 to 189.6, noise band ±13.69 (2 x MAD), CV 6.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +81.4% (noise band ±14.4% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +81.4% (it comes back)
- PASS · Held-out claim: C2: -67.0% to +49.1% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -72.94 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `theta_clip_min`, `theta_clip_max`, `omega_clip_min`, `omega_clip_max`, `RL_SEED_BASE`, `RUN_TAG`, `x_threshold`, `theta_threshold`, `reward_per_step`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (2.56 noise units, gap +44.4%); `eps_start=0.5` (2.05 noise units, gap +51.8%); `max_steps=10000` (2.05 noise units, gap +51.8%); `max_steps=40` (1.63 noise units, gap -57.9%); `eps_start=0.2` (1.04 noise units, gap -66.3%)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`, `max_steps=100`: this claim -1.8%, mean |gap| 5.3% (5 runs)
  - `lr_schedule=linear`, `max_steps=100`: this claim +3.2%, mean |gap| 25.9% (5 runs)
  - `eps_start=10`, `max_steps=100`: this claim +5.3%, mean |gap| 30.9% (5 runs)

### History matching (every measured configuration, all claims together)
- 7 of 55 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 7 configurations
  - `lr_schedule, max_steps`: lr_schedule=inv, max_steps=100 (max I 0.52); lr_schedule=linear, max_steps=100 (max I 1.12)
  - `max_steps`: max_steps=100 (max I 0.83)
  - `eps_start, lr_schedule`: eps_start=0.5, lr_schedule=linear (max I 1.11)
  - `eps_start, max_steps`: eps_start=10, max_steps=100 (max I 1.31); eps_start=0.5, max_steps=100 (max I 2.16); eps_start=0.2, max_steps=10000 (max I 2.77)
- 3 separate islands (no single-knob move joins them): lr_schedule=inv, max_steps=100; max_steps=100; lr_schedule=linear, max_steps=100 | eps_start=0.5, lr_schedule=linear | eps_start=0.2, max_steps=10000

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'max_steps': '40', 'eps_start': '0.5'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv`, `max_steps=100` | 5 | -1.8% | -8.8% | 5.3% |
| `lr_schedule=linear`, `max_steps=100` | 5 | +3.2% | +48.6% | 25.9% |
| `max_steps=100` | 6 | +4.6% | +49.1% | 26.8% |
| `eps_start=10`, `max_steps=100` | 5 | +5.3% | +56.5% | 30.9% |
| `lr_schedule=inv`, `max_steps=10000` | 5 | +45.0% | -38.5% | 41.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `theta_clip_min`, `theta_clip_max`, `omega_clip_min`, `omega_clip_max`, `RL_SEED_BASE`, `RUN_TAG`, `x_threshold`, `theta_threshold`, `reward_per_step`, `--out`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
