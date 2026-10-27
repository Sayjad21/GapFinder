# Gap Report: test-v11-04

Artifact `rlbench` · generated 2026-10-14 21:13 · 197 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +84.7% | +1.5% | ±12.8% | `max_steps=100` |

## C1: mean_reward (paper 94.93)
**Fits but unsupported** · gap +84.7% → +1.5% · 55 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0021`, `B0103`, `B0104`, `B0105`, `B0106`, `B0107` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `7fe4d057-01eb-4d26-b1dc-1cb38326e2ab` and run
  ```
  RUN_TAG=4775f1d768c8 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 92.34, 92.42, 96.91, 99.98, 99.64, 95.86; gap after +1.5%; result checkpoint `902fa98e-4f25-488d-becc-f3e2aaa05da0`
- Effect: candidate 96.38 minus naive 175.4 = -79, 95% bootstrap interval [-93.45, -70.92] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 94.9 on CartPole; the worst of its seeds reaches 63.9.

- p. 1; value used: `mean_reward` = 94.93 reward (headline claim)

### What did we measure?
- Naive median 175.4 over 5 runs; repeats: 182.7, 169.3, 191.6, 175.4, 169.4
- Spread: range 169.3 to 191.6, noise band ±12.17 (2 x MAD), CV 5.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +84.7% (noise band ±12.8% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +84.7% (it comes back)
- PASS · Held-out claim: C2: -18.2% to +18.7% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -79 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `theta_clip_min`, `theta_clip_max`, `omega_clip_min`, `omega_clip_max`, `RL_SEED_BASE`, `RUN_TAG`, `x_threshold`, `theta_threshold`, `reward_per_step`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.5` (6.39 noise units, gap +2.8%); `eps_start=0.2` (5.78 noise units, gap -10.6%); `lr_schedule=inv` (3.06 noise units, gap +45.5%); `eps_start=0.02` (2.76 noise units, gap -49.4%); `max_steps=40` (2.09 noise units, gap -57.9%) (and 2 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `max_steps=100`: this claim +3.6%, mean |gap| 25.5% (5 runs)
  - `lr_schedule=inv`, `max_steps=100`: this claim -7.0%, mean |gap| 26.5% (5 runs)
  - `lr_schedule=inv`: this claim +56.6%, mean |gap| 35.3% (6 runs)

### History matching (every measured configuration, all claims together)
- 5 of 55 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 5 configurations
  - `max_steps`: max_steps=100 (max I 0.42)
  - `lr_schedule, max_steps`: lr_schedule=inv, max_steps=100 (max I 1.14); lr_schedule=linear, max_steps=100 (max I 1.32)
  - `eps_start, max_steps`: eps_start=0.5, max_steps=100 (max I 1.63)
  - `eps_start, lr_schedule`: eps_start=0.5, lr_schedule=linear (max I 2.6)
- 2 separate islands (no single-knob move joins them): max_steps=100; lr_schedule=inv, max_steps=100; lr_schedule=linear, max_steps=100 | eps_start=0.5, lr_schedule=linear

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'eps_start': '0.5', 'lr_schedule': 'linear'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 6 | +1.5% | +18.7% | 10.1% |
| `lr_schedule=linear`, `max_steps=100` | 5 | +3.6% | +47.4% | 25.5% |
| `lr_schedule=inv`, `max_steps=100` | 5 | -7.0% | -46.1% | 26.5% |
| `lr_schedule=inv` | 6 | +56.6% | -14.0% | 35.3% |
| `eps_start=0.5`, `max_steps=100` | 5 | -10.8% | -74.1% | 42.5% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `theta_clip_min`, `theta_clip_max`, `omega_clip_min`, `omega_clip_max`, `RL_SEED_BASE`, `RUN_TAG`, `x_threshold`, `theta_threshold`, `reward_per_step`, `--out`

## Provenance
- GapFinder commit: `958fafed572bbbf30aedd8af86ba04a1fefc05c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
