# Gap Report: test-v11-10

Artifact `rlbench` · generated 2026-10-15 21:05 · 92 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Paper-artifact inconsistency | +99.3% | -2.7% | ±6.6% | `max_steps=100` |

## C1: mean_reward (paper 94.93)
**Paper-artifact inconsistency** · gap +99.3% → -2.7% · 32 hypotheses tested
> Confirmed cause: reverting it brings the gap back, held-out claims hold, and the value has evidence

### Which experiment changed it?
- Branch: `B0006`, `B0018`, `B0019`, `B0042` (4 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `6fe7831c-88db-43d1-b5e8-c0aa809ed5ca` and run
  ```
  RUN_TAG=398c5ec0c982 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 99.72, 88.54, 89.94, 94.78; gap after -2.7%; result checkpoint `a87b92d2-5241-4bf4-8f43-c5c0d944b157`
- Effect: candidate 92.36 minus naive 189.2 = -96.87, 95% bootstrap interval [-106.9, -88.68] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 94.9 steps, and that its worst seed still balances for 63.9.

- p. 1; value used: `mean_reward` = 94.93 steps (headline claim)

### What did we measure?
- Naive median 189.2 over 5 runs; repeats: 189.2, 186.1, 179.6, 200, 189.8
- Spread: range 179.6 to 200, noise band ±6.27 (2 x MAD), CV 3.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +99.3% (noise band ±6.6% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +99.3% (it comes back)
- PASS · Held-out claim: C2: +109.8% to -14.8% (not worse beyond noise)
- PASS · Evidence: `max_steps=100`: paper states '100'
- PASS · Effect vs noise: candidate minus naive is -96.87 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `max_steps_evaluation`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (8.69 noise units, gap +41.9%); `max_steps=1000` (6.58 noise units, gap +55.9%); `max_steps=40` (6.27 noise units, gap -57.9%); `max_steps=20` (3.05 noise units, gap -79.2%); `lr_schedule=linear` (2.98 noise units, gap +79.7%)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `lr_schedule=inv`: this claim -12.0%, mean |gap| 22.9% (3 runs)
  - `max_steps=100`, `lr_schedule=linear`: this claim +2.9%, mean |gap| 24.3% (3 runs)
  - `max_steps=2000`, `lr_schedule=inv`: this claim +61.7%, mean |gap| 37.5% (2 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `lr_schedule=inv, max_steps=100`
- `lr_schedule=linear, max_steps=100`

### History matching (every measured configuration, all claims together)
- 3 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `max_steps`: max_steps=100 (max I 0.24)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.68); lr_schedule=inv, max_steps=100 (max I 1.11)

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=100; lr_schedule=inv, max_steps=100; lr_schedule=linear, max_steps=100

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 4 | -2.7% | -14.8% | 8.7% |
| `max_steps=100`, `lr_schedule=inv` | 3 | -12.0% | -33.9% | 22.9% |
| `max_steps=100`, `lr_schedule=linear` | 3 | +2.9% | +45.7% | 24.3% |
| `max_steps=2000`, `lr_schedule=inv` | 2 | +61.7% | +13.2% | 37.5% |
| `lr_schedule=inv`, `max_steps=500` | 2 | +65.8% | -9.9% | 37.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `max_steps_evaluation`

## Provenance
- GapFinder commit: `cd8c8af2b9d079dd9a57443ed501c0dd8a467d34` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
