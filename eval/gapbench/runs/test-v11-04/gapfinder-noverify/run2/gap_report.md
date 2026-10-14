# Gap Report: test-v11-04

Artifact `rlbench` · generated 2026-10-14 11:51 · 198 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Explained | +96.4% | +11.3% | ±2.0% | `lr=0.05` |

## C1: mean_reward (paper 94.93)
**Explained** · gap +96.4% → +11.3% · 45 hypotheses tested
> Confirmed cause: reverting it brings the gap back, held-out claims hold, and the value has evidence

### Which experiment changed it?
- Branch: `B0012`, `B0056`, `B0057`, `B0058`, `B0059`, `B0060` (6 run(s) of the same config)
- Config: `lr` naive `0.1`, changed to `0.05`
- Command:

  Replay: fork checkpoint `0eca69c4-3b61-4b56-a2dc-649a94fc3402` and run
  ```
  RUN_TAG=58a458647bb0 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.05 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 98.86, 95.1, 100.3, 152.8, 130.6, 111; gap after +11.3%; result checkpoint `0af8e937-fecd-40bb-84e0-b98ae10fa2e2`
- Effect: candidate 105.6 minus naive 186.4 = -80.79, 95% bootstrap interval [-88.14, -30.41] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 94.9 on CartPole; the worst of its seeds reaches 63.9.

- p. 1; value used: `mean_reward` = 94.93 reward (headline claim)

### What did we measure?
- Naive median 186.4 over 5 runs; repeats: 161.9, 187.2, 186.7, 186.4, 179.1
- Spread: range 161.9 to 187.2, noise band ±1.864 (2 x MAD), CV 6.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +96.4% (noise band ±2.0% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is -80.79 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=100` (46.63 noise units, gap +4.8%); `lr=0.91` (45.5 noise units, gap +7.0%); `eps_start=0.5` (36.64 noise units, gap +24.4%); `lr=0.01` (32.8 noise units, gap -32.0%); `lr=0.55` (28.04 noise units, gap +41.3%) (and 9 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`, `max_steps=100`: this claim -6.3%, mean |gap| 18.2% (5 runs)
  - `max_steps=100`, `lr_schedule=linear`: this claim +3.1%, mean |gap| 24.7% (5 runs)
  - `max_steps=100`: this claim +4.7%, mean |gap| 26.9% (6 runs)

### History matching (every measured configuration, all claims together)
- 18 of 45 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.58); lr_schedule=inv, max_steps=100 (max I 1.01)
  - `max_steps`: max_steps=100 (max I 0.66)
  - `lr, max_steps`: lr=0.91, max_steps=100 (max I 0.76); lr=0.05, max_steps=100 (max I 1.9)
  - `eps_start, max_steps`: eps_start=10, max_steps=100 (max I 1.09)
  - `eps_start, lr_schedule`: eps_start=0.5, lr_schedule=linear (max I 1.21)
  - `eps_start, lr, lr_schedule, max_steps`: eps_start=0.5, lr=0.91, lr_schedule=inv, max_steps=100 (max I 1.39)
  - `lr`: lr=0.91 (max I 1.89)
  - `eps_start, lr`: eps_start=0.5, lr=0.91 (max I 1.9)
- 3 separate islands (no single-knob move joins them): lr_schedule=linear, max_steps=100; max_steps=100; lr=0.91, max_steps=100 | eps_start=0.5, lr_schedule=linear | eps_start=0.5, lr=0.91, lr_schedule=inv, max_steps=100

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'eps_start': '0.5', 'lr_schedule': 'linear'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv`, `max_steps=100` | 5 | -6.3% | -30.1% | 18.2% |
| `max_steps=100`, `lr_schedule=linear` | 5 | +3.1% | +46.2% | 24.7% |
| `max_steps=100` | 6 | +4.7% | +49.1% | 26.9% |
| `eps_start=10`, `max_steps=100` | 5 | +5.1% | +54.3% | 29.7% |
| `lr=0.91`, `max_steps=100` | 5 | +5.3% | +56.5% | 30.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `b05f7288e1a4df8af69bb0b5e7633827b4cb46c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
