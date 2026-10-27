# Gap Report: test-v11-10

Artifact `rlbench` · generated 2026-10-14 21:48 · 92 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Partially explained | +91.7% | +3.2% | ±11.4% | `max_steps=100` |

## C1: mean_reward (paper 94.93)
**Partially explained** · gap +91.7% → +3.2% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it closes only part of the gap, or the paper's own value was not tested

### Which experiment changed it?
- Branch: `B0006`, `B0018`, `B0019`, `B0020` (4 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `8329751d-0acf-4928-933e-f6e1623002f0` and run
  ```
  RUN_TAG=70bde9a5918d "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 99.21, 96.72, 99.42, 96.09; gap after +3.2%; result checkpoint `33d84906-f635-4c21-b85e-5064733b15f4`
- Effect: candidate 97.97 minus naive 181.9 = -83.97, 95% bootstrap interval [-95.14, -78] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 94.9 steps

- p. 1; value used: `mean_reward` = 94.93 steps (headline claim)

### What did we measure?
- Naive median 181.9 over 5 runs; repeats: 181.9, 195.2, 176.5, 184.8, 175.4
- Spread: range 175.4 to 195.2, noise band ±10.83 (2 x MAD), CV 4.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +91.7% (noise band ±11.4% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +91.7% (it comes back)
- PASS · Held-out claim: C2: +23.9% to +29.9% (not worse beyond noise)
- PASS · Evidence: `max_steps=100`: paper states '100'
- PASS · Effect vs noise: candidate minus naive is -83.97 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `eval.policy`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=10000` (5.93 noise units, gap +24.0%); `lr_schedule=inv` (3.19 noise units, gap +55.2%); `max_steps=40` (2.83 noise units, gap -59.3%); `max_steps=20` (1.12 noise units, gap -78.9%)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `lr_schedule=linear`: this claim +2.5%, mean |gap| 21.6% (3 runs)
  - `max_steps=2000`, `lr_schedule=inv`: this claim +29.0%, mean |gap| 35.2% (3 runs)
  - `max_steps=1000`, `lr_schedule=inv`: this claim +52.6%, mean |gap| 37.8% (3 runs)

### History matching (every measured configuration, all claims together)
- 3 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `max_steps`: max_steps=100 (max I 0.54)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.63); lr_schedule=inv, max_steps=100 (max I 2.73)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 4 | +3.2% | +29.9% | 16.5% |
| `max_steps=100`, `lr_schedule=linear` | 3 | +2.5% | +40.8% | 21.6% |
| `max_steps=2000`, `lr_schedule=inv` | 3 | +29.0% | -41.3% | 35.2% |
| `max_steps=1000`, `lr_schedule=inv` | 3 | +52.6% | -23.1% | 37.8% |
| `max_steps=500`, `lr_schedule=inv` | 3 | +61.8% | -27.8% | 44.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `eval.policy`

## Provenance
- GapFinder commit: `e0f13d101585ad1609a15fbf67b70128f4cfffc8` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
