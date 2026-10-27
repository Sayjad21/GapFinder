# Gap Report: test-v11-04

Artifact `rlbench` · generated 2026-10-15 19:21 · 146 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +96.2% | +4.6% | ±16.8% | `max_steps=100` |

## C1: mean_reward (paper 94.93)
**Fits but unsupported** · gap +96.2% → +4.6% · 55 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0021`, `B0058`, `B0059`, `B0072` (4 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `5c8690ed-bff6-46cf-b677-035394357a02` and run
  ```
  RUN_TAG=23bba5b327d9 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 99.72, 99.1, 92.64, 99.41; gap after +4.6%; result checkpoint `5986b477-399a-4c21-90dc-5d5c5949743b`
- Effect: candidate 99.25 minus naive 186.3 = -87.02, 95% bootstrap interval [-103.4, -80.13] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 94.9 on CartPole; the worst of its seeds reaches 63.9.

- p. 1; value used: `mean_reward` = 94.93 reward (headline claim)

### What did we measure?
- Naive median 186.3 over 5 runs; repeats: 186.3, 198.3, 197.4, 178.3, 180.9
- Spread: range 178.3 to 198.3, noise band ±15.92 (2 x MAD), CV 4.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +96.2% (noise band ±16.8% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +96.2% (it comes back)
- PASS · Held-out claim: C2: +110.0% to +48.7% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -87.02 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `theta_clip_min`, `theta_clip_max`, `omega_clip_min`, `omega_clip_max`, `RL_SEED_BASE`, `RUN_TAG`, `x_threshold`, `theta_threshold`, `reward_per_step`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.5` (4.4 noise units, gap +22.5%); `eps_start=0.2` (3.81 noise units, gap -32.3%); `eps_start=0.0` (3.65 noise units, gap -35.0%); `eps_start=0.01` (3 noise units, gap -45.9%); `max_steps=40` (2.29 noise units, gap -57.9%) (and 6 more in the JSON)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `eps_start=0.5`: this claim -5.0%, mean |gap| 15.1% (3 runs)
  - `max_steps=100`, `lr_schedule=linear`: this claim -5.7%, mean |gap| 24.3% (3 runs)
  - `max_steps=100`, `lr_schedule=inv`: this claim -5.0%, mean |gap| 30.9% (3 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `eps_start=0.5, max_steps=100`
- `eps_start=0.5, lr_schedule=linear`

### History matching (every measured configuration, all claims together)
- 6 of 55 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 6 configurations
  - `max_steps`: max_steps=100 (max I 0.35)
  - `eps_start, max_steps`: eps_start=0.5, max_steps=100 (max I 0.44)
  - `lr_schedule, max_steps`: lr_schedule=inv, max_steps=100 (max I 0.73); lr_schedule=linear, max_steps=100 (max I 0.88)
  - `eps_start, lr_schedule`: eps_start=0.5, lr_schedule=linear (max I 1.38)
  - `eps_start`: eps_start=0.5 (max I 2.94)

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=100; eps_start=0.5, max_steps=100; eps_start=0.5, lr_schedule=linear

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100`, `eps_start=0.5` | 3 | -5.0% | -25.3% | 15.1% |
| `max_steps=100`, `lr_schedule=linear` | 3 | -5.7% | -43.0% | 24.3% |
| `max_steps=100` | 4 | +4.6% | +48.7% | 26.7% |
| `max_steps=100`, `lr_schedule=inv` | 3 | -5.0% | -56.9% | 30.9% |
| `lr_schedule=linear`, `eps_start=0.5` | 3 | +9.8% | -84.0% | 46.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `theta_clip_min`, `theta_clip_max`, `omega_clip_min`, `omega_clip_max`, `RL_SEED_BASE`, `RUN_TAG`, `x_threshold`, `theta_threshold`, `reward_per_step`, `--out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
