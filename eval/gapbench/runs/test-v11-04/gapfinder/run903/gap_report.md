# Gap Report: test-v11-04

Artifact `rlbench` · generated 2026-10-14 23:49 · 195 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +75.6% | +3.7% | ±16.5% | `eps_start=0.5`, `lr_schedule=linear` |

## C1: mean_reward (paper 94.93)
**Fits but unsupported** · gap +75.6% → +3.7% · 54 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0144`, `B0184`, `B0185`, `B0186`, `B0187` (5 run(s) of the same config)
- Config: `eps_start` naive `1.0`, changed to `0.5`
- Config: `lr_schedule` naive `const`, changed to `linear`
- Command:

  Replay: fork checkpoint `b2230edf-2b04-46c2-abf3-4b8762820075` and run
  ```
  RUN_TAG=4086673b00a8 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule linear --eps_start 0.5 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 126.6, 107.3, 82.38, 92.95, 98.45; gap after +3.7%; result checkpoint `70f3c5c0-a3e5-4813-a0c3-1ae3a525e44d`
- Effect: candidate 98.45 minus naive 166.7 = -68.27, 95% bootstrap interval [-96.29, -42.34] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 94.9 on CartPole; the worst of its seeds reaches 63.9.

- p. 1; value used: `mean_reward` = 94.93 reward (headline claim)

### What did we measure?
- Naive median 166.7 over 5 runs; repeats: 166.7, 152, 198.6, 174.5, 163
- Spread: range 152 to 198.6, noise band ±15.64 (2 x MAD), CV 10.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +75.6% (noise band ±16.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `eps_start` the gap is +67.8% (it comes back)
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is +40.2% (it comes back)
- PASS · Held-out claim: C2: -15.0% to -83.3% (not worse beyond noise)
- FAIL · Evidence: `eps_start=0.5`: no evidence mentions '0.5'; it fits, but nothing says the authors used it
- FAIL · Evidence: `lr_schedule=linear`: no evidence mentions 'linear'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -68.27 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `theta_clip_min`, `theta_clip_max`, `omega_clip_min`, `omega_clip_max`, `RL_SEED_BASE`, `RUN_TAG`, `x_threshold`, `theta_threshold`, `reward_per_step`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=100` (4.27 noise units, gap +5.3%); `eps_start=0.2` (3.81 noise units, gap -12.9%); `eps_start=0.1` (1.92 noise units, gap -44.1%); `max_steps=40` (1.08 noise units, gap -57.9%)
- Near alternatives (closest across all claims):
  - `max_steps=100`: this claim +3.7%, mean |gap| 18.9% (6 runs)
  - `max_steps=100`, `lr_schedule=linear`: this claim +2.8%, mean |gap| 24.4% (5 runs)
  - `max_steps=100`, `lr_schedule=inv`: this claim -12.5%, mean |gap| 30.8% (5 runs)

### Equally good configurations
The target claim can't tell these 5 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `eps_start=0.5, lr_schedule=linear` (reported)
- `max_steps=100`
- `eps_start=0.2`
- `lr_schedule=linear, max_steps=100`
- `eps_start=0.5, lr_schedule=inv`

### History matching (every measured configuration, all claims together)
- 9 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 9 configurations
  - `max_steps`: max_steps=100 (max I 0.3)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.4); lr_schedule=inv, max_steps=100 (max I 1.01); lr_schedule=inv, max_steps=40 (max I 2.94)
  - `eps_start, lr_schedule`: eps_start=0.5, lr_schedule=linear (max I 1.14); eps_start=0.5, lr_schedule=inv (max I 1.47); eps_start=0.2, lr_schedule=linear (max I 2.86)
  - `eps_start, max_steps`: eps_start=0.5, max_steps=100 (max I 1.82)
  - `eps_start`: eps_start=0.2 (max I 2.32)
- 2 separate islands (no single-knob move joins them): max_steps=100; lr_schedule=linear, max_steps=100; lr_schedule=inv, max_steps=100 | eps_start=0.5, lr_schedule=linear; eps_start=0.5, lr_schedule=inv; eps_start=0.2
- Equally good values: `lr_schedule` in {inv, linear}

Notes:
- configurations the target claim can't tell apart from the answer: eps_start=0.5, lr_schedule=linear; max_steps=100; eps_start=0.2; lr_schedule=linear, max_steps=100; eps_start=0.5, lr_schedule=inv
- equally good values within one noise band (measured): lr_schedule in {inv, linear}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 6 | +3.7% | +34.2% | 18.9% |
| `max_steps=100`, `lr_schedule=linear` | 5 | +2.8% | +46.1% | 24.4% |
| `max_steps=100`, `lr_schedule=inv` | 5 | -12.5% | -49.1% | 30.8% |
| `lr_schedule=linear` | 5 | +67.8% | +11.7% | 39.8% |
| `lr_schedule=linear`, `eps_start=0.5` | 5 | +3.7% | -83.3% | 43.5% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `theta_clip_min`, `theta_clip_max`, `omega_clip_min`, `omega_clip_max`, `RL_SEED_BASE`, `RUN_TAG`, `x_threshold`, `theta_threshold`, `reward_per_step`, `--out`

## Provenance
- GapFinder commit: `efb2f63a257a40b9982099a274f2e882f272b80c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
