# Gap Report: test-v11-10

Artifact `rlbench` · generated 2026-10-14 22:37 · 89 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Partially explained | +83.1% | +3.6% | ±12.3% | `max_steps=100` |

## C1: mean_reward (paper 94.93)
**Partially explained** · gap +83.1% → +3.6% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it closes only part of the gap, or the paper's own value was not tested

### Which experiment changed it?
- Branch: `B0006`, `B0018`, `B0019`, `B0020` (4 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `5c982374-7a6a-4519-b6da-ebdd062b87db` and run
  ```
  RUN_TAG=c137916e3b59 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 99.89, 96.12, 96.89, 99.73; gap after +3.6%; result checkpoint `c05877eb-167e-48c3-9413-383c4278ca21`
- Effect: candidate 98.31 minus naive 173.8 = -75.47, 95% bootstrap interval [-83.56, -69.67] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 94.9 steps, and that its worst seed still balances for 63.9.

- p. 1; value used: `mean_reward` = 94.93 steps (headline claim)

### What did we measure?
- Naive median 173.8 over 5 runs; repeats: 173.8, 172.5, 182.1, 165.9, 179.6
- Spread: range 165.9 to 182.1, noise band ±11.63 (2 x MAD), CV 3.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +83.1% (noise band ±12.3% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +83.1% (it comes back)
- PASS · Held-out claim: C2: -20.5% to +34.5% (not worse beyond noise)
- PASS · Evidence: `max_steps=100`: paper states '100'
- PASS · Effect vs noise: candidate minus naive is -75.47 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `max_steps_evaluation`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (3.48 noise units, gap +40.5%); `lr_schedule=linear` (2.48 noise units, gap +52.6%); `max_steps=40` (1.75 noise units, gap -61.7%)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `max_steps=100`: this claim +3.9%, mean |gap| 27.4% (3 runs)
  - `lr_schedule=inv`, `max_steps=100`: this claim -13.9%, mean |gap| 34.5% (3 runs)
  - `lr_schedule=inv`: this claim +41.4%, mean |gap| 39.2% (4 runs)

### Equally good configurations
The target claim can't tell these 2 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `lr_schedule=linear, max_steps=100`

### History matching (every measured configuration, all claims together)
- 3 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `max_steps`: max_steps=100 (max I 0.65)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.94); lr_schedule=inv, max_steps=100 (max I 1.86)

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=100; lr_schedule=linear, max_steps=100

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 4 | +3.6% | +34.5% | 19.0% |
| `lr_schedule=linear`, `max_steps=100` | 3 | +3.9% | +50.9% | 27.4% |
| `lr_schedule=inv`, `max_steps=100` | 3 | -13.9% | -55.2% | 34.5% |
| `lr_schedule=inv` | 4 | +41.4% | -37.1% | 39.2% |
| `max_steps=400`, `lr_schedule=inv` | 3 | +56.2% | -30.8% | 43.5% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `max_steps_evaluation`

## Provenance
- GapFinder commit: `e0f13d101585ad1609a15fbf67b70128f4cfffc8` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
