# Gap Report: test-v11-10

Artifact `rlbench` · generated 2026-10-14 22:20 · 128 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +92.1% | +39.2% | ±16.2% | `max_steps=1000`, `lr_schedule=inv` |

## C1: mean_reward (paper 94.93)
**Fits but unsupported** · gap +92.1% → +39.2% · 32 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0074`, `B0097`, `B0098`, `B0099`, `B0100` (5 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `1000`
- Config: `lr_schedule` naive `const`, changed to `inv`
- Command:

  Replay: fork checkpoint `418435ac-a79a-435e-a121-2af3c2940218` and run
  ```
  RUN_TAG=d6f11b28a9be "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 1000 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 132.1, 158.6, 131.6, 160, 103.7; gap after +39.2%; result checkpoint `e29e1b70-245b-4748-a0f5-84c8b5f6ba1e`
- Effect: candidate 132.1 minus naive 182.3 = -50.22, 95% bootstrap interval [-71.97, -16.19] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 94.9 steps, and that its worst seed still balances for 63.9.

- p. 1; value used: `mean_reward` = 94.93 steps (headline claim)

### What did we measure?
- Naive median 182.3 over 5 runs; repeats: 174.6, 163.1, 182.3, 190.6, 189.4
- Spread: range 163.1 to 190.6, noise band ±15.39 (2 x MAD), CV 6.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +92.1% (noise band ±16.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +58.9% (it comes back)
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is +337.2% (it comes back)
- PASS · Held-out claim: C2: +3.4% to -48.5% (not worse beyond noise)
- FAIL · Evidence: `max_steps=1000`: no evidence mentions '1000'; it fits, but nothing says the authors used it
- FAIL · Evidence: `lr_schedule=inv`: no evidence mentions 'inv'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -50.22 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `max_steps_evaluation`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=100` (5.35 noise units, gap +5.3%); `max_steps=40` (2.11 noise units, gap -57.9%); `max_steps=2000` (2.09 noise units, gap +58.2%)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `max_steps=100`: this claim +3.1%, mean |gap| 23.9% (5 runs)
  - `lr_schedule=inv`, `max_steps=100`: this claim -3.6%, mean |gap| 24.9% (5 runs)
  - `max_steps=100`: this claim +5.3%, mean |gap| 30.5% (6 runs)

### Equally good configurations
The target claim can't tell these 4 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `lr_schedule=inv, max_steps=1000` (reported)
- `lr_schedule=linear, max_steps=100`
- `lr_schedule=inv, max_steps=100`
- `lr_schedule=inv, max_steps=2000`

### History matching (every measured configuration, all claims together)
- 3 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `lr_schedule, max_steps`: lr_schedule=inv, max_steps=100 (max I 0.78); lr_schedule=linear, max_steps=100 (max I 0.78)
  - `max_steps`: max_steps=100 (max I 1.01)
- Equally good values: `max_steps` in {100, 400, 1000, 2000}

Notes:
- configurations the target claim can't tell apart from the answer: lr_schedule=inv, max_steps=1000; lr_schedule=linear, max_steps=100; lr_schedule=inv, max_steps=100; lr_schedule=inv, max_steps=2000
- equally good values within one noise band (measured): max_steps in {100, 400, 1000, 2000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=linear`, `max_steps=100` | 5 | +3.1% | +44.8% | 23.9% |
| `lr_schedule=inv`, `max_steps=100` | 5 | -3.6% | -46.2% | 24.9% |
| `max_steps=100` | 6 | +5.3% | +55.8% | 30.5% |
| `lr_schedule=inv` | 6 | +58.9% | -9.4% | 34.1% |
| `lr_schedule=inv`, `max_steps=2000` | 5 | +26.3% | -45.1% | 35.7% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `max_steps_evaluation`

## Provenance
- GapFinder commit: `e0f13d101585ad1609a15fbf67b70128f4cfffc8` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
