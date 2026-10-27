# Gap Report: test-v11-10

Artifact `rlbench` · generated 2026-10-16 01:26 · 124 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Paper-artifact inconsistency | +96.9% | +0.3% | ±14.8% | `max_steps=100` |

## C1: mean_reward (paper 94.93)
**Paper-artifact inconsistency** · gap +96.9% → +0.3% · 32 hypotheses tested
> Confirmed cause: reverting it brings the gap back, held-out claims hold, and the value has evidence

### Which experiment changed it?
- Branch: `B0006`, `B0018`, `B0019`, `B0042`, `B0043`, `B0044` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `6c60eacc-e91d-43ec-bd6c-274aa5679209` and run
  ```
  RUN_TAG=3a771b8a89c6 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 96.56, 95.84, 91.81, 97.14, 92.46, 94.56; gap after +0.3%; result checkpoint `a5c7cd84-fa4d-4c74-9edf-aa0affd896aa`
- Effect: candidate 95.2 minus naive 186.9 = -91.72, 95% bootstrap interval [-99.68, -70.86] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 94.9 steps

- p. 1; value used: `mean_reward` = 94.93 steps (headline claim)

### What did we measure?
- Naive median 186.9 over 5 runs; repeats: 192.1, 193.9, 163.5, 169.5, 186.9
- Spread: range 163.5 to 193.9, noise band ±14.02 (2 x MAD), CV 7.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +96.9% (noise band ±14.8% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +96.9% (it comes back)
- PASS · Held-out claim: C2: +109.5% to -12.1% (not worse beyond noise)
- PASS · Evidence: `max_steps=100`: paper states '100'
- PASS · Effect vs noise: candidate minus naive is -91.72 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `eval.policy`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (3.3 noise units, gap +48.2%); `max_steps=40` (2.64 noise units, gap -57.9%); `lr_schedule=linear` (1.31 noise units, gap +77.5%); `max_steps=20` (1.22 noise units, gap -78.9%)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `lr_schedule=linear`: this claim -4.0%, mean |gap| 20.8% (5 runs)
  - `max_steps=400`, `lr_schedule=inv`: this claim +40.8%, mean |gap| 23.6% (5 runs)
  - `lr_schedule=inv`, `max_steps=100`: this claim -8.7%, mean |gap| 24.6% (5 runs)

### Equally good configurations
The target claim can't tell these 2 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `lr_schedule=linear, max_steps=100`

### History matching (every measured configuration, all claims together)
- 3 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.22); lr_schedule=inv, max_steps=100 (max I 0.73)
  - `max_steps`: max_steps=100 (max I 0.3)

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=100; lr_schedule=linear, max_steps=100

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 6 | +0.3% | -12.1% | 6.2% |
| `max_steps=100`, `lr_schedule=linear` | 5 | -4.0% | -37.5% | 20.8% |
| `max_steps=400`, `lr_schedule=inv` | 5 | +40.8% | -6.4% | 23.6% |
| `lr_schedule=inv`, `max_steps=100` | 5 | -8.7% | -40.5% | 24.6% |
| `lr_schedule=inv`, `max_steps=500` | 5 | +60.0% | -11.6% | 35.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `eval.policy`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
