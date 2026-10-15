# Gap Report: test-v13-03

Artifact `rlbench` · generated 2026-10-15 23:38 · 65 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +77.0% | -3.9% | ±19.0% | `max_steps=100` |

## C1: mean_reward (paper 99.495)
**Fits but unsupported** · gap +77.0% → -3.9% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0013`, `B0023`, `B0024`, `B0025`, `B0026`, `B0027` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `7c92d84a-7aab-4e2d-a45c-6b9b0575f2a3` and run
  ```
  RUN_TAG=eddd4e53b00e "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 99.58, 95.72, 99.25, 92.36, 93.25, 95.48; gap after -3.9%; result checkpoint `83132508-b0f5-4def-9771-d78d22f9e176`
- Effect: candidate 95.6 minus naive 176.1 = -80.48, 95% bootstrap interval [-94.98, -72.46] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 99.5 steps, and that its worst seed still balances for 96.8.

- p. 1; value used: `mean_reward` = 99.495 steps (headline claim)

### What did we measure?
- Naive median 176.1 over 5 runs; repeats: 176.1, 166.6, 185.4, 166.5, 195.4
- Spread: range 166.5 to 195.4, noise band ±18.94 (2 x MAD), CV 7.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +77.0% (noise band ±19.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +77.0% (it comes back)
- PASS · Held-out claim: C2: -3.7% to -33.6% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: evidence gate off: no evidence was looked for
- PASS · Effect vs noise: candidate minus naive is -80.48 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (4.01 noise units, gap +0.7%)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `lr_schedule=linear`: this claim -1.7%, mean |gap| 2.7% (5 runs)
  - `max_steps=100`, `lr_schedule=inv`: this claim -11.6%, mean |gap| 33.6% (5 runs)
  - `lr_schedule=inv`: this claim +35.5%, mean |gap| 44.2% (6 runs)

### Equally good configurations
The target claim can't tell these 2 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `lr_schedule=linear, max_steps=100`

### History matching (every measured configuration, all claims together)
- 3 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.14); lr_schedule=inv, max_steps=100 (max I 1.36)
  - `max_steps`: max_steps=100 (max I 0.73)

Notes:
- evidence gate off: no evidence was checked, so this cannot be labelled Explained
- configurations the target claim can't tell apart from the answer: max_steps=100; lr_schedule=linear, max_steps=100

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100`, `lr_schedule=linear` | 5 | -1.7% | -3.6% | 2.7% |
| `max_steps=100` | 6 | -3.9% | -33.6% | 18.8% |
| `max_steps=100`, `lr_schedule=inv` | 5 | -11.6% | -55.6% | 33.6% |
| naive (reproduction as run) | 5 | +77.0% | -3.7% | 40.3% |
| `lr_schedule=inv` | 6 | +35.5% | -53.0% | 44.2% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `e9c31fd1405f5c8aae4bd880eadcdc8d491fad02` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
