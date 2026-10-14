# Gap Report: test-v11-04

Artifact `rlbench` · generated 2026-10-14 11:14 · 141 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +96.4% | +1.0% | ±17.9% | `eps_start=0.5`, `lr_schedule=linear` |

## C1: mean_reward (paper 94.93)
**Fits but unsupported** · gap +96.4% → +1.0% · 47 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0056`, `B0114`, `B0115`, `B0116`, `B0117` (5 run(s) of the same config)
- Config: `eps_start` naive `1.0`, changed to `0.5`
- Config: `lr_schedule` naive `const`, changed to `linear`
- Command:

  Replay: fork checkpoint `3ec03cd3-4502-4b66-80b0-d798d118c7b3` and run
  ```
  RUN_TAG=798062ddc019 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule linear --eps_start 0.5 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 108.9, 81.58, 95.88, 87.13, 102.9; gap after +1.0%; result checkpoint `3ea7e1f6-c6ef-46b0-96f2-d2a0c85442bb`
- Effect: candidate 95.88 minus naive 186.5 = -90.59, 95% bootstrap interval [-103.5, -70.07] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 94.9 on CartPole; the worst of its seeds reaches 63.9.

- p. 1; value used: `mean_reward` = 94.93 (headline claim)

### What did we measure?
- Naive median 186.5 over 5 runs; repeats: 163.7, 186.5, 191.2, 196, 178
- Spread: range 163.7 to 196, noise band ±16.96 (2 x MAD), CV 7.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +96.4% (noise band ±17.9% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `eps_start` the gap is +80.0% (it comes back)
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is +40.0% (it comes back)
- PASS · Held-out claim: C2: +124.3% to -82.6% (not worse beyond noise)
- FAIL · Evidence: `eps_start=0.5`: no evidence mentions '0.5'; it fits, but nothing says the authors used it
- FAIL · Evidence: `lr_schedule=linear`: no evidence mentions 'linear'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -90.59 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=100` (5.11 noise units, gap +5.2%); `eps_start=0.1` (4.09 noise units, gap -23.4%); `lr_schedule=inv` (3.41 noise units, gap +35.5%)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `max_steps=100`: this claim +2.7%, mean |gap| 23.5% (5 runs)
  - `max_steps=100`, `lr_schedule=inv`: this claim -9.9%, mean |gap| 28.5% (5 runs)
  - `max_steps=100`: this claim +5.0%, mean |gap| 28.7% (6 runs)

### History matching (every measured configuration, all claims together)
- 7 of 47 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 7 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.34); lr_schedule=inv, max_steps=100 (max I 1.24)
  - `max_steps`: max_steps=100 (max I 0.57)
  - `eps_start, max_steps`: eps_start=2, max_steps=100 (max I 0.65); eps_start=0.5, max_steps=100 (max I 1.67)
  - `eps_start, lr_schedule`: eps_start=0.5, lr_schedule=linear (max I 1.03); eps_start=0.5, lr_schedule=inv (max I 2.51)
- 2 separate islands (no single-knob move joins them): lr_schedule=linear, max_steps=100; max_steps=100; eps_start=2, max_steps=100 | eps_start=0.5, lr_schedule=linear; eps_start=0.5, lr_schedule=inv

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=linear`, `max_steps=100` | 5 | +2.7% | +44.3% | 23.5% |
| `max_steps=100`, `lr_schedule=inv` | 5 | -9.9% | -47.1% | 28.5% |
| `max_steps=100` | 6 | +5.0% | +52.4% | 28.7% |
| `max_steps=100`, `eps_start=2` | 5 | +5.1% | +53.8% | 29.5% |
| `lr_schedule=inv` | 6 | +34.5% | -37.8% | 36.2% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `b05f7288e1a4df8af69bb0b5e7633827b4cb46c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
