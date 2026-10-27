# Gap Report: test-v11-04

Artifact `rlbench` · generated 2026-10-14 23:33 · 197 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +76.8% | +2.4% | ±2.5% | `max_steps=100` |

## C1: mean_reward (paper 94.93)
**Fits but unsupported** · gap +76.8% → +2.4% · 55 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0021`, `B0058`, `B0059`, `B0070`, `B0071`, `B0072` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `24cd0058-e3a5-44c0-8755-47592eb717a2` and run
  ```
  RUN_TAG=57a8b06dab40 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 99.01, 92.28, 98.98, 93.58, 95.45, 99.92; gap after +2.4%; result checkpoint `250d506f-61a4-4ad9-b7de-7bde94aab7f9`
- Effect: candidate 97.22 minus naive 167.8 = -70.58, 95% bootstrap interval [-99.97, -68.66] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 94.9 on CartPole; the worst of its seeds reaches 63.9.

- p. 1; value used: `mean_reward` = 94.93 reward (headline claim)

### What did we measure?
- Naive median 167.8 over 5 runs; repeats: 167.8, 167.8, 166.6, 176.4, 198.5
- Spread: range 166.6 to 198.5, noise band ±2.38 (2 x MAD), CV 7.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +76.8% (noise band ±2.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +76.8% (it comes back)
- PASS · Held-out claim: C2: -28.1% to +20.6% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -70.58 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `theta_clip_min`, `theta_clip_max`, `omega_clip_min`, `omega_clip_max`, `RL_SEED_BASE`, `RUN_TAG`, `x_threshold`, `theta_threshold`, `reward_per_step`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.2` (27.07 noise units, gap -8.9%); `eps_start=0.1` (11.91 noise units, gap -46.9%); `max_steps=40` (7.54 noise units, gap -57.9%); `lr_schedule=inv` (6.42 noise units, gap +60.7%)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `max_steps=100`: this claim +2.3%, mean |gap| 24.0% (5 runs)
  - `lr_schedule=inv`, `max_steps=100`: this claim -15.2%, mean |gap| 30.0% (5 runs)
  - `lr_schedule=inv`: this claim +36.1%, mean |gap| 36.9% (6 runs)

### History matching (every measured configuration, all claims together)
- 7 of 55 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 7 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.2); lr_schedule=inv, max_steps=100 (max I 1.02)
  - `max_steps`: max_steps=100 (max I 0.21)
  - `eps_start, lr_schedule`: eps_start=0.5, lr_schedule=inv (max I 0.68); eps_start=0.5, lr_schedule=linear (max I 0.72)
  - `eps_start`: eps_start=0.2 (max I 1.41)
  - `eps_start, max_steps`: eps_start=0.5, max_steps=100 (max I 2.26)
- 3 separate islands (no single-knob move joins them): lr_schedule=linear, max_steps=100; max_steps=100; lr_schedule=inv, max_steps=100 | eps_start=0.5, lr_schedule=inv; eps_start=0.5, lr_schedule=linear | eps_start=0.2

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'max_steps': '40', 'eps_start': '0.5'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 6 | +2.4% | +20.6% | 11.5% |
| `lr_schedule=linear`, `max_steps=100` | 5 | +2.3% | +45.7% | 24.0% |
| `lr_schedule=inv`, `max_steps=100` | 5 | -15.2% | -44.8% | 30.0% |
| `lr_schedule=inv` | 6 | +36.1% | -37.8% | 36.9% |
| `max_steps=40` | 6 | -57.9% | -37.7% | 47.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `theta_clip_min`, `theta_clip_max`, `omega_clip_min`, `omega_clip_max`, `RL_SEED_BASE`, `RUN_TAG`, `x_threshold`, `theta_threshold`, `reward_per_step`, `--out`

## Provenance
- GapFinder commit: `efb2f63a257a40b9982099a274f2e882f272b80c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
