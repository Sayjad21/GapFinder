# Gap Report: test-v11-10

Artifact `rlbench` · generated 2026-10-14 21:26 · 97 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +91.5% | -1.9% | ±7.0% | `max_steps=100`, `lr_schedule=inv` |

## C1: mean_reward (paper 94.93)
**Fits but unsupported** · gap +91.5% → -1.9% · 32 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0054`, `B0074`, `B0075` (3 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Config: `lr_schedule` naive `const`, changed to `inv`
- Command:

  Replay: fork checkpoint `f3b41bf5-604e-46ce-9b77-af65beab2487` and run
  ```
  RUN_TAG=c7b4813b973b "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 93.11, 83.5, 96.09; gap after -1.9%; result checkpoint `d0811241-044d-471c-b182-84e48b235782`
- Effect: candidate 93.11 minus naive 181.8 = -88.7, 95% bootstrap interval [-106.5, -83.86] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 94.9 steps, and that its worst seed still balances for 63.9.

- p. 1; value used: `mean_reward` = 94.93 steps (headline claim)

### What did we measure?
- Naive median 181.8 over 5 runs; repeats: 179.3, 178.5, 196.3, 187.7, 181.8
- Spread: range 178.5 to 196.3, noise band ±6.63 (2 x MAD), CV 4.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +91.5% (noise band ±7.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +22.2% (it comes back)
- FAIL · Counterfactual (reversal test): without `lr_schedule` the gap is +5.0% (it did NOT come back)
- PASS · Held-out claim: C2: +112.4% to -0.9% (not worse beyond noise)
- PASS · Evidence: `max_steps=100`: paper states '100'
- FAIL · Evidence: `lr_schedule=inv`: no evidence mentions 'inv'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -88.7 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `max_steps_evaluation`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=10000` (7.4 noise units, gap +39.9%); `max_steps=40` (4.81 noise units, gap -57.9%); `lr_schedule=linear` (2.45 noise units, gap +74.4%); `max_steps=20` (1.8 noise units, gap -78.9%)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `lr_schedule=linear`: this claim +2.7%, mean |gap| 23.8% (3 runs)
  - `max_steps=1000`, `lr_schedule=inv`: this claim +18.1%, mean |gap| 25.9% (3 runs)
  - `max_steps=100`: this claim +5.0%, mean |gap| 28.6% (4 runs)

### History matching (every measured configuration, all claims together)
- 3 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `lr_schedule, max_steps`: lr_schedule=inv, max_steps=100 (max I 0.55); lr_schedule=linear, max_steps=100 (max I 0.56)
  - `max_steps`: max_steps=100 (max I 0.7)
- Equally good values: `lr_schedule` in {inv, linear}

Notes:
- equally good values within one noise band (measured): lr_schedule in {inv, linear}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv`, `max_steps=100` | 3 | -1.9% | -0.9% | 1.4% |
| `max_steps=100`, `lr_schedule=linear` | 3 | +2.7% | +44.9% | 23.8% |
| `max_steps=1000`, `lr_schedule=inv` | 3 | +18.1% | -33.6% | 25.9% |
| `max_steps=100` | 4 | +5.0% | +52.1% | 28.6% |
| `lr_schedule=inv`, `max_steps=2000` | 3 | +17.1% | -46.2% | 31.7% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `max_steps_evaluation`

## Provenance
- GapFinder commit: `634d827f07d6659ff82f6ea0924c8ba487e9d02a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
