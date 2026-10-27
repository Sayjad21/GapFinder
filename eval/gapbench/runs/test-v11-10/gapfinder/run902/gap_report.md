# Gap Report: test-v11-10

Artifact `rlbench` · generated 2026-10-14 23:51 · 106 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Partially explained | +106.6% | +4.9% | ±5.3% | `max_steps=100` |

## C1: mean_reward (paper 94.93)
**Partially explained** · gap +106.6% → +4.9% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it closes only part of the gap, or the paper's own value was not tested

### Which experiment changed it?
- Branch: `B0006`, `B0018`, `B0019`, `B0044` (4 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `17055132-08ba-433b-91e2-5cf69b20069b` and run
  ```
  RUN_TAG=5cc8ea413761 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 99.83, 99.55, 99.68, 93.61; gap after +4.9%; result checkpoint `d6e8248e-0e88-4618-bda2-064c2567d5f8`
- Effect: candidate 99.62 minus naive 196.2 = -96.55, 95% bootstrap interval [-103.9, -82.88] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 94.9 steps, and that its worst seed still balances for 63.9.

- p. 1; value used: `mean_reward` = 94.93 steps (headline claim)

### What did we measure?
- Naive median 196.2 over 5 runs; repeats: 177.8, 198.7, 189.5, 196.9, 196.2
- Spread: range 177.8 to 198.7, noise band ±5.01 (2 x MAD), CV 4.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +106.6% (noise band ±5.3% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +106.6% (it comes back)
- PASS · Held-out claim: C2: +153.0% to +51.9% (not worse beyond noise)
- PASS · Evidence: `max_steps=100`: paper states '100'
- PASS · Effect vs noise: candidate minus naive is -96.55 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `max_steps_evaluation`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (15.19 noise units, gap +26.5%); `max_steps=40` (9.24 noise units, gap -57.9%); `lr_schedule=linear` (5.58 noise units, gap +77.2%); `max_steps=20` (5.25 noise units, gap -78.9%); `max_steps=4` (2.06 noise units, gap -95.8%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `lr_schedule=linear`: this claim +2.8%, mean |gap| 24.4% (3 runs)
  - `lr_schedule=inv`, `max_steps=500`: this claim +51.1%, mean |gap| 38.4% (3 runs)
  - `lr_schedule=inv`: this claim +47.8%, mean |gap| 43.2% (4 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `lr_schedule=inv, max_steps=100`
- `lr_schedule=linear, max_steps=100`

### History matching (every measured configuration, all claims together)
- 3 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `max_steps`: max_steps=100 (max I 0.5)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.72); lr_schedule=inv, max_steps=100 (max I 0.82)

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=100; lr_schedule=inv, max_steps=100; lr_schedule=linear, max_steps=100

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100`, `lr_schedule=linear` | 3 | +2.8% | +46.0% | 24.4% |
| `max_steps=100` | 4 | +4.9% | +51.9% | 28.4% |
| `lr_schedule=inv`, `max_steps=500` | 3 | +51.1% | -25.6% | 38.4% |
| `lr_schedule=inv` | 4 | +47.8% | -38.7% | 43.2% |
| `max_steps=100`, `lr_schedule=inv` | 3 | -8.8% | -79.7% | 44.3% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `max_steps_evaluation`

## Provenance
- GapFinder commit: `efb2f63a257a40b9982099a274f2e882f272b80c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
