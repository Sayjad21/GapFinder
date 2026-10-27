# Gap Report: test-v13-09

Artifact `rlbench` · generated 2026-10-16 02:08 · 85 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Paper-artifact inconsistency | +78.7% | -0.5% | ±6.2% | `max_steps=100` |

## C1: mean_reward (paper 99.495)
**Paper-artifact inconsistency** · gap +78.7% → -0.5% · 32 hypotheses tested
> Confirmed cause: reverting it brings the gap back, held-out claims hold, and the value has evidence

### Which experiment changed it?
- Branch: `B0006`, `B0018`, `B0019`, `B0040` (4 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `95815449-a033-49cc-9bc0-a861fe2bb820` and run
  ```
  RUN_TAG=5e2ae4101630 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 99.18, 96.17, 98.89, 99.83; gap after -0.5%; result checkpoint `e96b0f75-659e-4e6d-90c9-36b49799f41e`
- Effect: candidate 99.03 minus naive 177.8 = -78.74, 95% bootstrap interval [-89.04, -76.04] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 99.5 steps, and that its worst seed still balances for 96.8.

- p. 1; value used: `mean_reward` = 99.495 steps (headline claim)

### What did we measure?
- Naive median 177.8 over 5 runs; repeats: 174.7, 176, 177.8, 189.6, 181.2
- Spread: range 174.7 to 189.6, noise band ±6.21 (2 x MAD), CV 3.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +78.7% (noise band ±6.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +78.7% (it comes back)
- PASS · Held-out claim: C2: +6.8% to -3.1% (not worse beyond noise)
- PASS · Evidence: `max_steps=100`: paper states '100'
- PASS · Effect vs noise: candidate minus naive is -78.74 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `theta_clip_low`, `theta_clip_high`, `omega_clip_low`, `omega_clip_high`, `g`, `mc`, `mp`, `l`, `f`, `dt`, `init_state_low`, `init_state_high`, `theta_range`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (9.79 noise units, gap +17.6%); `max_steps=150` (4.66 noise units, gap +49.6%); `max_steps=40` (3.02 noise units, gap -59.8%)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `lr_schedule=linear`: this claim -2.4%, mean |gap| 4.4% (3 runs)
  - `lr_schedule=inv`, `max_steps=100`: this claim -7.0%, mean |gap| 18.0% (3 runs)
  - `max_steps=150`: this claim +32.6%, mean |gap| 30.7% (4 runs)

### Equally good configurations
The target claim can't tell these 2 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `lr_schedule=linear, max_steps=100`

### History matching (every measured configuration, all claims together)
- 4 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 4 configurations
  - `max_steps`: max_steps=100 (max I 0.26)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.61); lr_schedule=inv, max_steps=100 (max I 1.53); lr_schedule=inv, max_steps=150 (max I 1.78)

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=100; lr_schedule=linear, max_steps=100

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 4 | -0.5% | -3.1% | 1.8% |
| `max_steps=100`, `lr_schedule=linear` | 3 | -2.4% | -6.5% | 4.4% |
| `lr_schedule=inv`, `max_steps=100` | 3 | -7.0% | -29.0% | 18.0% |
| `max_steps=150` | 4 | +32.6% | -28.8% | 30.7% |
| `max_steps=150`, `lr_schedule=linear` | 3 | +41.8% | +34.2% | 38.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `theta_clip_low`, `theta_clip_high`, `omega_clip_low`, `omega_clip_high`, `g`, `mc`, `mp`, `l`, `f`, `dt`, `init_state_low`, `init_state_high`, `theta_range`, `--out`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
