# Gap Report: test-v11-04

Artifact `rlbench` · generated 2026-10-16 01:22 · 113 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +74.8% | +2.7% | ±3.2% | `max_steps=100` |

## C1: mean_reward (paper 94.93)
**Fits but unsupported** · gap +74.8% → +2.7% · 55 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0016`, `B0032`, `B0033`, `B0040`, `B0041`, `B0042` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `a3470edc-3da7-49f9-915d-3e7fad25f6f2` and run
  ```
  RUN_TAG=715521619527 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 95.28, 93.5, 98.85, 98.43, 96.56, 99.53; gap after +2.7%; result checkpoint `02886383-83fe-4d9e-bdbc-b4855ce53d61`
- Effect: candidate 97.5 minus naive 165.9 = -68.44, 95% bootstrap interval [-84.81, -65.4] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 94.9 on CartPole; the worst of its seeds reaches 63.9.

- p. 1; value used: `mean_reward` = 94.93 (headline claim)

### What did we measure?
- Naive median 165.9 over 5 runs; repeats: 164.4, 163.4, 188.2, 166.8, 165.9
- Spread: range 163.4 to 188.2, noise band ±3.04 (2 x MAD), CV 6.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +74.8% (noise band ±3.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +74.8% (it comes back)
- PASS · Held-out claim: C2: -5.3% to +23.2% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -68.44 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.2` (16.76 noise units, gap -21.1%); `lr_schedule=inv` (14.03 noise units, gap +29.9%); `eps_start=0.5` (8.02 noise units, gap +49.1%); `eps_start=0.02` (5.43 noise units, gap -57.4%); `max_steps=40` (4.83 noise units, gap -59.3%)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `lr_schedule=linear`: this claim +2.8%, mean |gap| 20.9% (5 runs)
  - `lr_schedule=inv`, `max_steps=100`: this claim -4.0%, mean |gap| 24.8% (5 runs)
  - `eps_start=0.5`, `max_steps=100`: this claim -12.0%, mean |gap| 42.8% (5 runs)

### Equally good configurations
The target claim can't tell these 2 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=100` (reported)
- `lr_schedule=linear, max_steps=100`

### History matching (every measured configuration, all claims together)
- 6 of 55 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 6 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.36); lr_schedule=inv, max_steps=100 (max I 1.06)
  - `max_steps`: max_steps=100 (max I 0.38)
  - `eps_start, max_steps`: eps_start=0.5, max_steps=100 (max I 1.54)
  - `eps_start, lr_schedule`: eps_start=0.5, lr_schedule=linear (max I 1.87); eps_start=0.5, lr_schedule=inv (max I 2.49)
- 2 separate islands (no single-knob move joins them): lr_schedule=linear, max_steps=100; max_steps=100; lr_schedule=inv, max_steps=100 | eps_start=0.5, lr_schedule=linear; eps_start=0.5, lr_schedule=inv

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=100; lr_schedule=linear, max_steps=100

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 6 | +2.7% | +23.2% | 12.9% |
| `max_steps=100`, `lr_schedule=linear` | 5 | +2.8% | +39.1% | 20.9% |
| `lr_schedule=inv`, `max_steps=100` | 5 | -4.0% | -45.6% | 24.8% |
| naive (reproduction as run) | 5 | +74.8% | -5.3% | 40.1% |
| `eps_start=0.5`, `max_steps=100` | 5 | -12.0% | -73.6% | 42.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
