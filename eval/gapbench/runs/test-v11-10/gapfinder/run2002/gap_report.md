# Gap Report: test-v11-10

Artifact `rlbench` · generated 2026-10-15 21:06 · 116 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Partially explained | +91.0% | +4.1% | ±23.5% | `max_steps=100` |

## C1: mean_reward (paper 94.93)
**Partially explained** · gap +91.0% → +4.1% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it closes only part of the gap, or the paper's own value was not tested

### Which experiment changed it?
- Branch: `B0006`, `B0018`, `B0019`, `B0040`, `B0041`, `B0042` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `04e3d8fd-13b2-41a0-8a20-46829b068f53` and run
  ```
  RUN_TAG=0d25446f5e67 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 98.72, 96.39, 86.78, 98.85, 99.27, 99.42; gap after +4.1%; result checkpoint `5667ba04-d3f4-45dd-bc6e-0998d1dd2cc4`
- Effect: candidate 98.78 minus naive 181.3 = -82.52, 95% bootstrap interval [-99.51, -67.09] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 94.9 steps, and that its worst seed still balances for 63.9.

- p. 1; value used: `mean_reward` = 94.93 steps (headline claim)

### What did we measure?
- Naive median 181.3 over 5 runs; repeats: 181.3, 180.7, 192.5, 159.4, 193.6
- Spread: range 159.4 to 193.6, noise band ±22.35 (2 x MAD), CV 7.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +91.0% (noise band ±23.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +91.0% (it comes back)
- PASS · Held-out claim: C2: +112.1% to +47.1% (not worse beyond noise)
- PASS · Evidence: `max_steps=100`: paper states '100'
- PASS · Effect vs noise: candidate minus naive is -82.52 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `max_steps_evaluation`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=10000` (2.14 noise units, gap +40.5%); `max_steps=40` (1.41 noise units, gap -57.9%); `lr_schedule=inv` (1.35 noise units, gap +59.2%)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `lr_schedule=linear`: this claim +2.8%, mean |gap| 23.6% (5 runs)
  - `lr_schedule=inv`, `max_steps=100`: this claim -13.1%, mean |gap| 25.5% (5 runs)
  - `lr_schedule=inv`, `max_steps=1000`: this claim +47.2%, mean |gap| 29.4% (2 runs)

### Equally good configurations
The target claim can't tell these 2 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `lr_schedule=linear, max_steps=100`

### History matching (every measured configuration, all claims together)
- 3 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `max_steps`: max_steps=100 (max I 0.42)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.74); lr_schedule=inv, max_steps=100 (max I 1.13)

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=100; lr_schedule=linear, max_steps=100

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100`, `lr_schedule=linear` | 5 | +2.8% | +44.5% | 23.6% |
| `lr_schedule=inv`, `max_steps=100` | 5 | -13.1% | -37.9% | 25.5% |
| `max_steps=100` | 6 | +4.1% | +47.1% | 25.6% |
| `lr_schedule=inv`, `max_steps=1000` | 2 | +47.2% | -11.5% | 29.4% |
| `lr_schedule=inv`, `max_steps=400` | 5 | +43.6% | -22.9% | 33.3% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `max_steps_evaluation`

## Provenance
- GapFinder commit: `cd8c8af2b9d079dd9a57443ed501c0dd8a467d34` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
