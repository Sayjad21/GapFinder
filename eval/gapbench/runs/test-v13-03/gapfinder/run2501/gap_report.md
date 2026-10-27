# Gap Report: test-v13-03

Artifact `rlbench` · generated 2026-10-16 02:04 · 60 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +79.6% | -3.4% | ±21.2% | `max_steps=100` |

## C1: mean_reward (paper 99.495)
**Fits but unsupported** · gap +79.6% → -3.4% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0013`, `B0018`, `B0019`, `B0020`, `B0021`, `B0022` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `f408f58f-8917-427c-af6f-3d3eeaeccd25` and run
  ```
  RUN_TAG=f251d1ea5c34 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 99, 95.77, 95.73, 91.8, 99.83, 96.41; gap after -3.4%; result checkpoint `ee28367c-4b29-4490-a434-1b93cd661e85`
- Effect: candidate 96.09 minus naive 178.6 = -82.56, 95% bootstrap interval [-92.54, -74.36] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 99.5 steps, and that its worst seed still balances for 96.8.

- p. 1; value used: `mean_reward` = 99.495 steps (headline claim)

### What did we measure?
- Naive median 178.6 over 5 runs; repeats: 189.2, 170.1, 178.6, 165.4, 191.4
- Spread: range 165.4 to 191.4, noise band ±21.09 (2 x MAD), CV 6.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +79.6% (noise band ±21.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +79.6% (it comes back)
- PASS · Held-out claim: C2: -48.7% to -33.9% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -82.56 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `max_steps=100`: this claim -1.9%, mean |gap| 3.2% (5 runs)
  - `lr_schedule=inv`, `max_steps=100`: this claim -11.4%, mean |gap| 36.1% (5 runs)
  - `max_steps=500`, `lr_schedule=inv`: this claim +44.5%, mean |gap| 50.8% (2 runs)

### Equally good configurations
The target claim can't tell these 2 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `lr_schedule=linear, max_steps=100`

### History matching (every measured configuration, all claims together)
- 3 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.57); lr_schedule=inv, max_steps=100 (max I 1.57)
  - `max_steps`: max_steps=100 (max I 0.9)

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=100; lr_schedule=linear, max_steps=100

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=linear`, `max_steps=100` | 5 | -1.9% | -4.6% | 3.2% |
| `max_steps=100` | 6 | -3.4% | -33.9% | 18.7% |
| `lr_schedule=inv`, `max_steps=100` | 5 | -11.4% | -60.9% | 36.1% |
| `max_steps=500`, `lr_schedule=inv` | 2 | +44.5% | -57.1% | 50.8% |
| `max_steps=400`, `lr_schedule=inv` | 5 | +30.5% | -71.7% | 51.1% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
