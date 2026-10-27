# Gap Report: test-v11-04

Artifact `rlbench` · generated 2026-10-16 01:23 · 175 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +92.2% | -0.2% | ±1.9% | `eps_start=0.5`, `lr_schedule=inv` |

## C1: mean_reward (paper 94.93)
**Fits but unsupported** · gap +92.2% → -0.2% · 55 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0099`, `B0126`, `B0163` (3 run(s) of the same config)
- Config: `eps_start` naive `1.0`, changed to `0.5`
- Config: `lr_schedule` naive `const`, changed to `inv`
- Command:

  Replay: fork checkpoint `7abbe9eb-31fb-4acd-8d97-30d4f490cf55` and run
  ```
  RUN_TAG=cc8464d8758a "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_start 0.5 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 94.72, 74.36, 117.3; gap after -0.2%; result checkpoint `5fdb7d4d-1c9c-487a-af94-cbb9f7919622`
- Effect: candidate 94.72 minus naive 182.4 = -87.72, 95% bootstrap interval [-115.7, -61.55] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 94.9 on CartPole; the worst of its seeds reaches 63.9.

- p. 1; value used: `mean_reward` = 94.93 reward (headline claim)

### What did we measure?
- Naive median 182.4 over 5 runs; repeats: 182, 182.4, 176.5, 199.1, 182.5
- Spread: range 176.5 to 199.1, noise band ±1.824 (2 x MAD), CV 4.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +92.2% (noise band ±1.9% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `eps_start` the gap is +30.5% (it comes back)
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is +50.6% (it comes back)
- PASS · Held-out claim: C2: +112.3% to -82.9% (not worse beyond noise)
- FAIL · Evidence: `eps_start=0.5`: no evidence mentions '0.5'; it fits, but nothing says the authors used it
- FAIL · Evidence: `lr_schedule=inv`: no evidence mentions 'inv'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -87.72 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `theta_clip_min`, `theta_clip_max`, `omega_clip_min`, `omega_clip_max`, `RL_SEED_BASE`, `RUN_TAG`, `x_threshold`, `theta_threshold`, `reward_per_step`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=100` (46.54 noise units, gap +2.7%); `eps_start=0.2` (32.95 noise units, gap +28.9%); `max_steps=10000` (30.89 noise units, gap +32.8%); `max_steps=40` (15.46 noise units, gap -62.5%); `eps_start=0.01` (12.8 noise units, gap -67.6%) (and 7 more in the JSON)
- Near alternatives (closest across all claims):
  - `max_steps=100`: this claim +1.6%, mean |gap| 3.9% (4 runs)
  - `lr_schedule=linear`, `max_steps=100`: this claim +2.7%, mean |gap| 23.3% (3 runs)
  - `lr_schedule=inv`, `max_steps=100`: this claim -18.2%, mean |gap| 30.3% (3 runs)

### Equally good configurations
The target claim can't tell these 8 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `eps_start=0.5, lr_schedule=inv` (reported)
- `max_steps=100`
- `eps_start=0.2`
- `lr_schedule=linear, max_steps=100`
- `lr_schedule=inv, max_steps=100`
- `eps_start=0.5, lr_schedule=linear`
- `lr_schedule=inv, max_steps=10000`
- `eps_start=0.5, max_steps=100`

### History matching (every measured configuration, all claims together)
- 8 of 55 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 8 configurations
  - `max_steps`: max_steps=100 (max I 0.25)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.6); lr_schedule=inv, max_steps=100 (max I 2.22)
  - `eps_start, lr_schedule`: eps_start=0.5, lr_schedule=inv (max I 1.11); eps_start=0.5, lr_schedule=linear (max I 1.74)
  - `eps_start, max_steps`: eps_start=0.2, max_steps=10000 (max I 1.14); eps_start=0.5, max_steps=100 (max I 1.44)
  - `eps_start`: eps_start=0.2 (max I 1.22)
- 3 separate islands (no single-knob move joins them): max_steps=100; lr_schedule=linear, max_steps=100; eps_start=0.5, max_steps=100 | eps_start=0.5, lr_schedule=inv; eps_start=0.5, lr_schedule=linear | eps_start=0.2, max_steps=10000; eps_start=0.2

Notes:
- configurations the target claim can't tell apart from the answer: eps_start=0.5, lr_schedule=inv; max_steps=100; eps_start=0.2; lr_schedule=linear, max_steps=100; lr_schedule=inv, max_steps=100; eps_start=0.5, lr_schedule=linear; lr_schedule=inv, max_steps=10000; eps_start=0.5, max_steps=100

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 4 | +1.6% | +6.1% | 3.9% |
| `lr_schedule=linear`, `max_steps=100` | 3 | +2.7% | +44.0% | 23.3% |
| `lr_schedule=inv`, `max_steps=100` | 3 | -18.2% | -42.3% | 30.3% |
| `eps_start=0.5`, `max_steps=10000` | 3 | +7.6% | -68.9% | 38.2% |
| `lr_schedule=inv` | 4 | +30.5% | -52.3% | 41.4% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `theta_clip_min`, `theta_clip_max`, `omega_clip_min`, `omega_clip_max`, `RL_SEED_BASE`, `RUN_TAG`, `x_threshold`, `theta_threshold`, `reward_per_step`, `--out`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
