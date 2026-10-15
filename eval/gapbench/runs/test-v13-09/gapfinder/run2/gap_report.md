# Gap Report: test-v13-09

Artifact `rlbench` · generated 2026-10-16 00:22 · 168 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Partially explained | +87.8% | -5.1% | ±7.6% | `max_steps=100` |

## C1: mean_reward (paper 99.495)
**Partially explained** · gap +87.8% → -5.1% · 54 hypotheses tested
> Plausible explanation (fits but unsupported): it closes only part of the gap, or the paper's own value was not tested

### Which experiment changed it?
- Branch: `B0006`, `B0020`, `B0021`, `B0044`, `B0045`, `B0046` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `bd3860fb-b55c-45ad-8463-b1fd3b7a5f95` and run
  ```
  RUN_TAG=236e156c8158 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 94.04, 99.78, 99.66, 92.28, 93.66, 94.81; gap after -5.1%; result checkpoint `336d8379-6257-44db-bffe-d95e034172c9`
- Effect: candidate 94.43 minus naive 186.8 = -92.41, 95% bootstrap interval [-96.27, -73.73] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 99.5 steps, and that its worst seed still balances for 96.8.

- p. 1; value used: `mean_reward` = 99.495 steps (headline claim)

### What did we measure?
- Naive median 186.8 over 5 runs; repeats: 190.6, 186.8, 172.9, 167.7, 189.5
- Spread: range 167.7 to 190.6, noise band ±7.58 (2 x MAD), CV 5.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +87.8% (noise band ±7.6% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +87.8% (it comes back)
- PASS · Held-out claim: C2: +7.8% to -42.4% (not worse beyond noise)
- PASS · Evidence: `max_steps=100`: paper states '100'
- PASS · Effect vs noise: candidate minus naive is -92.41 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (7.12 noise units, gap +33.6%); `max_steps=40` (3.23 noise units, gap -63.2%); `lr_schedule=linear` (2.76 noise units, gap +66.8%)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `lr_schedule=linear`: this claim -1.2%, mean |gap| 1.8% (5 runs)
  - `max_steps=100`, `init_q=-1.0`: this claim -0.9%, mean |gap| 3.1% (5 runs)
  - `max_steps=100`, `init_q=1.0`: this claim -5.6%, mean |gap| 21.1% (5 runs)

### Equally good configurations
The target claim can't tell these 4 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `lr_schedule=linear, max_steps=100`
- `init_q=-1.0, max_steps=100`
- `init_q=1.0, max_steps=100`

### History matching (every measured configuration, all claims together)
- 5 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 5 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.49); lr_schedule=inv, max_steps=100 (max I 2.39)
  - `init_q, max_steps`: init_q=-1.0, max_steps=100 (max I 0.98); init_q=1.0, max_steps=100 (max I 1.49)
  - `max_steps`: max_steps=100 (max I 1.54)

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=100; lr_schedule=linear, max_steps=100; init_q=-1.0, max_steps=100; init_q=1.0, max_steps=100

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100`, `lr_schedule=linear` | 5 | -1.2% | -2.3% | 1.8% |
| `max_steps=100`, `init_q=-1.0` | 5 | -0.9% | -5.3% | 3.1% |
| `max_steps=100`, `init_q=1.0` | 5 | -5.6% | -36.6% | 21.1% |
| `max_steps=100` | 6 | -5.1% | -42.4% | 23.7% |
| `max_steps=100`, `lr_schedule=inv` | 5 | -8.9% | -62.2% | 35.5% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`

## Provenance
- GapFinder commit: `e9c31fd1405f5c8aae4bd880eadcdc8d491fad02` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0331, sandbox reported $0.0000 (total $0.0331; this search; ledger extraction is included only if it shared the search's router)
