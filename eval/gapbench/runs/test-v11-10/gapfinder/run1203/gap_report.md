# Gap Report: test-v11-10

Artifact `rlbench` · generated 2026-10-15 00:59 · 116 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Paper-artifact inconsistency | +86.4% | +0.3% | ±25.2% | `max_steps=100` |

## C1: mean_reward (paper 94.93)
**Paper-artifact inconsistency** · gap +86.4% → +0.3% · 32 hypotheses tested
> Confirmed cause: reverting it brings the gap back, held-out claims hold, and the value has evidence

### Which experiment changed it?
- Branch: `B0006`, `B0018`, `B0019`, `B0040`, `B0041`, `B0042` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `0a992d80-3401-4394-8a9f-5db9f2c0ca7e` and run
  ```
  RUN_TAG=acfc77f4ec84 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 97.01, 94.36, 93.24, 95.48, 94.93, 99.84; gap after +0.3%; result checkpoint `49d40c9a-e576-410f-a90b-d5a84cce503b`
- Effect: candidate 95.21 minus naive 176.9 = -81.73, 95% bootstrap interval [-94.18, -56.33] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 94.9 steps

- p. 1; value used: `mean_reward` = 94.93 steps (headline claim)

### What did we measure?
- Naive median 176.9 over 5 runs; repeats: 194.7, 176.9, 145.3, 178.4, 165
- Spread: range 145.3 to 194.7, noise band ±23.95 (2 x MAD), CV 10.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +86.4% (noise band ±25.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +86.4% (it comes back)
- PASS · Held-out claim: C2: -12.7% to -3.8% (not worse beyond noise)
- PASS · Evidence: `max_steps=100`: paper states '100'
- PASS · Effect vs noise: candidate minus naive is -81.73 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `eval.policy`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (2.04 noise units, gap +34.9%); `max_steps=2000` (1.49 noise units, gap +48.8%); `max_steps=10000` (1.44 noise units, gap +50.0%); `max_steps=40` (1.13 noise units, gap -57.9%)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `lr_schedule=linear`: this claim +2.5%, mean |gap| 23.2% (5 runs)
  - `lr_schedule=inv`, `max_steps=100`: this claim -9.2%, mean |gap| 25.4% (5 runs)
  - `max_steps=500`, `lr_schedule=inv`: this claim +42.2%, mean |gap| 32.2% (5 runs)

### Equally good configurations
The target claim can't tell these 2 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `lr_schedule=linear, max_steps=100`

### History matching (every measured configuration, all claims together)
- 6 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 6 configurations
  - `max_steps`: max_steps=100 (max I 0.07)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.38); lr_schedule=inv, max_steps=100 (max I 0.71); lr_schedule=inv, max_steps=400 (max I 2.7); lr_schedule=inv, max_steps=40 (max I 2.79)
  - `lr_schedule`: lr_schedule=inv (max I 2.67)

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=100; lr_schedule=linear, max_steps=100

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 6 | +0.3% | -3.8% | 2.1% |
| `max_steps=100`, `lr_schedule=linear` | 5 | +2.5% | +44.0% | 23.2% |
| `lr_schedule=inv`, `max_steps=100` | 5 | -9.2% | -41.6% | 25.4% |
| `max_steps=500`, `lr_schedule=inv` | 5 | +42.2% | -22.1% | 32.2% |
| `lr_schedule=inv`, `max_steps=400` | 5 | +24.1% | -46.5% | 35.3% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `eval.policy`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
