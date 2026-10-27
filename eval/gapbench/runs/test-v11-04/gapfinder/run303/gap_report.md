# Gap Report: test-v11-04

Artifact `rlbench` · generated 2026-10-14 21:47 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +77.1% | +4.3% | ±9.5% | `max_steps=100` |

## C1: mean_reward (paper 94.93)
**Fits but unsupported** · gap +77.1% → +4.3% · 54 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0021`, `B0103`, `B0104`, `B0105`, `B0106`, `B0107` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `793b1ac5-93e9-4b5b-a9df-f156e62d2e04` and run
  ```
  RUN_TAG=949a041e4238 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 99.21, 96.76, 99.42, 98.8, 100, 86.61; gap after +4.3%; result checkpoint `637b7eb9-20cf-4e83-b239-c93b6b587dd9`
- Effect: candidate 99 minus naive 168.1 = -69.07, 95% bootstrap interval [-93.77, -55.18] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 94.9 on CartPole; the worst of its seeds reaches 63.9.

- p. 1; value used: `mean_reward` = 94.93 reward (headline claim)

### What did we measure?
- Naive median 168.1 over 5 runs; repeats: 194.2, 163.6, 172.4, 148, 168.1
- Spread: range 148 to 194.2, noise band ±8.98 (2 x MAD), CV 9.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +77.1% (noise band ±9.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +77.1% (it comes back)
- PASS · Held-out claim: C2: +1.2% to +47.5% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -69.07 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `theta_clip_min`, `theta_clip_max`, `omega_clip_min`, `omega_clip_max`, `RL_SEED_BASE`, `RUN_TAG`, `x_threshold`, `theta_threshold`, `reward_per_step`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.2` (6.24 noise units, gap -18.1%); `lr_schedule=inv` (2.64 noise units, gap +52.1%); `max_steps=40` (1.86 noise units, gap -59.4%); `eps_start=0.5` (1.55 noise units, gap +62.4%); `eps_start=0.02` (1.32 noise units, gap -64.6%)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `max_steps=100`: this claim +3.2%, mean |gap| 24.5% (5 runs)
  - `lr_schedule=inv`, `max_steps=100`: this claim -13.1%, mean |gap| 34.4% (5 runs)
  - `lr_schedule=inv`: this claim +53.1%, mean |gap| 40.0% (6 runs)

### History matching (every measured configuration, all claims together)
- 6 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 6 configurations
  - `max_steps`: max_steps=100 (max I 0.45)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.73); lr_schedule=inv, max_steps=100 (max I 1.28)
  - `eps_start, lr_schedule`: eps_start=0.5, lr_schedule=linear (max I 0.79)
  - `eps_start, max_steps`: eps_start=0.5, max_steps=100 (max I 1.89)
  - `eps_start`: eps_start=0.2 (max I 1.97)
- 3 separate islands (no single-knob move joins them): max_steps=100; lr_schedule=linear, max_steps=100; lr_schedule=inv, max_steps=100 | eps_start=0.5, lr_schedule=linear | eps_start=0.2

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'eps_start': '0.5', 'lr_schedule': 'linear'} for 'confirm-combo')
- lr_schedule dropped: with repeats, {'lr_schedule': 'linear', 'max_steps': '100'} fits {'max_steps': '100'}'s gap by less than one noise band, so it is not needed
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=linear`, `max_steps=100` | 5 | +3.2% | +45.8% | 24.5% |
| `max_steps=100` | 6 | +4.3% | +47.5% | 25.9% |
| `lr_schedule=inv`, `max_steps=100` | 5 | -13.1% | -55.7% | 34.4% |
| naive (reproduction as run) | 5 | +77.1% | +1.2% | 39.1% |
| `lr_schedule=inv` | 6 | +53.1% | +26.9% | 40.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `theta_clip_min`, `theta_clip_max`, `omega_clip_min`, `omega_clip_max`, `RL_SEED_BASE`, `RUN_TAG`, `x_threshold`, `theta_threshold`, `reward_per_step`, `--out`

## Provenance
- GapFinder commit: `e0f13d101585ad1609a15fbf67b70128f4cfffc8` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
