# Gap Report: test-v11-10

Artifact `rlbench` · generated 2026-10-14 23:51 · 122 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Partially explained | +90.4% | +4.5% | ±24.6% | `max_steps=100` |

## C1: mean_reward (paper 94.93)
**Partially explained** · gap +90.4% → +4.5% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it closes only part of the gap, or the paper's own value was not tested

### Which experiment changed it?
- Branch: `B0006`, `B0018`, `B0019`, `B0042`, `B0043`, `B0044` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `5bc6d3a4-ffa5-40e7-9770-924411bfb859` and run
  ```
  RUN_TAG=bbceb2abe083 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 96.56, 98.84, 99.89, 99.54, 99.83, 94.12; gap after +4.5%; result checkpoint `cea4a45b-ac42-4915-9d08-98347d5e20e3`
- Effect: candidate 99.19 minus naive 180.7 = -81.52, 95% bootstrap interval [-95.44, -69.04] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 94.9 steps

- p. 1; value used: `mean_reward` = 94.93 steps (headline claim)

### What did we measure?
- Naive median 180.7 over 5 runs; repeats: 196.4, 169.1, 180.7, 166.8, 188
- Spread: range 166.8 to 196.4, noise band ±23.31 (2 x MAD), CV 7.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +90.4% (noise band ±24.6% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +90.4% (it comes back)
- PASS · Held-out claim: C2: -3.4% to +50.5% (not worse beyond noise)
- PASS · Evidence: `max_steps=100`: paper states '100'
- PASS · Effect vs noise: candidate minus naive is -81.52 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `eval.policy`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (2.2 noise units, gap +36.3%); `max_steps=40` (1.32 noise units, gap -57.9%); `lr_schedule=linear` (1.19 noise units, gap +61.2%)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `max_steps=100`: this claim +3.5%, mean |gap| 24.8% (5 runs)
  - `lr_schedule=inv`, `max_steps=400`: this claim +36.8%, mean |gap| 40.8% (5 runs)
  - `max_steps=10000`, `lr_schedule=inv`: this claim +61.2%, mean |gap| 44.9% (5 runs)

### Equally good configurations
The target claim can't tell these 2 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `lr_schedule=linear, max_steps=100`

### History matching (every measured configuration, all claims together)
- 3 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.33); lr_schedule=inv, max_steps=100 (max I 1.79)
  - `max_steps`: max_steps=100 (max I 0.57)

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=100; lr_schedule=linear, max_steps=100

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=linear`, `max_steps=100` | 5 | +3.5% | +46.1% | 24.8% |
| `max_steps=100` | 6 | +4.5% | +50.5% | 27.5% |
| `lr_schedule=inv`, `max_steps=400` | 5 | +36.8% | -44.9% | 40.8% |
| `max_steps=10000`, `lr_schedule=inv` | 5 | +61.2% | -28.6% | 44.9% |
| `lr_schedule=inv`, `max_steps=100` | 5 | -14.6% | -77.4% | 46.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `eval.policy`

## Provenance
- GapFinder commit: `efb2f63a257a40b9982099a274f2e882f272b80c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
