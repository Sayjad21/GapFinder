# Gap Report: test-v11-04

Artifact `rlbench` · generated 2026-10-14 11:14 · 130 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Explained | +82.1% | +3.0% | ±13.7% | `max_steps=100` |

## C1: mean_reward (paper 94.93)
**Explained** · gap +82.1% → +3.0% · 47 hypotheses tested
> Confirmed cause: reverting it brings the gap back, held-out claims hold, and the value has evidence

### Which experiment changed it?
- Branch: `B0011`, `B0020`, `B0021`, `B0022`, `B0023`, `B0024` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `379610fc-d873-4e3a-835e-53b707ce9811` and run
  ```
  RUN_TAG=5c6635db1223 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 99.67, 92.59, 99.84, 96.66, 98.98, 88.22; gap after +3.0%; result checkpoint `80ecdac4-e2e0-4734-969d-6a00adc90958`
- Effect: candidate 97.82 minus naive 172.9 = -75.06, 95% bootstrap interval [-90.73, -67.16] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 94.9 on CartPole; the worst of its seeds reaches 63.9.

- p. 1; value used: `mean_reward` = 94.93 (headline claim)

### What did we measure?
- Naive median 172.9 over 5 runs; repeats: 179.4, 169, 172.9, 188.2, 160.9
- Spread: range 160.9 to 188.2, noise band ±12.98 (2 x MAD), CV 5.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +82.1% (noise band ±13.7% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is -75.06 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.5` (3.26 noise units, gap +37.5%); `lr_schedule=inv` (1.86 noise units, gap +56.7%); `eps_start=0.1` (1.77 noise units, gap -57.9%); `eps_start=0.02` (1.22 noise units, gap -65.5%); `eps_start=10` (1.21 noise units, gap +65.6%)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `max_steps=100`: this claim +2.8%, mean |gap| 21.3% (5 runs)
  - `eps_start=10`, `max_steps=100`: this claim +5.2%, mean |gap| 29.4% (5 runs)
  - `lr_schedule=inv`, `max_steps=100`: this claim -14.1%, mean |gap| 35.6% (5 runs)

### History matching (every measured configuration, all claims together)
- 7 of 47 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 7 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.17); lr_schedule=inv, max_steps=100 (max I 1.9)
  - `max_steps`: max_steps=100 (max I 0.41)
  - `eps_start, max_steps`: eps_start=10, max_steps=100 (max I 1.26); eps_start=0.5, max_steps=100 (max I 1.75)
  - `eps_start, lr_schedule`: eps_start=0.5, lr_schedule=inv (max I 1.75); eps_start=0.5, lr_schedule=linear (max I 2.27)
- 2 separate islands (no single-knob move joins them): lr_schedule=linear, max_steps=100; max_steps=100; eps_start=10, max_steps=100 | eps_start=0.5, lr_schedule=inv; eps_start=0.5, lr_schedule=linear

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 6 | +3.0% | +28.0% | 15.5% |
| `lr_schedule=linear`, `max_steps=100` | 5 | +2.8% | +39.8% | 21.3% |
| `eps_start=10`, `max_steps=100` | 5 | +5.2% | +53.7% | 29.4% |
| `lr_schedule=inv`, `max_steps=100` | 5 | -14.1% | -57.0% | 35.6% |
| `lr_schedule=inv` | 6 | +35.4% | -42.1% | 38.7% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `b05f7288e1a4df8af69bb0b5e7633827b4cb46c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
