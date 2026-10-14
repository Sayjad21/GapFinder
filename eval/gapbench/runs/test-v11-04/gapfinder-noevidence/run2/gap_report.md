# Gap Report: test-v11-04

Artifact `rlbench` · generated 2026-10-14 11:51 · 139 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +99.9% | +1.9% | ±6.0% | `lr=0.91`, `eps_start=0.5` |

## C1: mean_reward (paper 94.93)
**Fits but unsupported** · gap +99.9% → +1.9% · 45 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0081`, `B0114`, `B0115` (3 run(s) of the same config)
- Config: `lr` naive `0.1`, changed to `0.91`
- Config: `eps_start` naive `1.0`, changed to `0.5`
- Command:

  Replay: fork checkpoint `e09828dc-0948-432a-a2d6-247fcb4ab11e` and run
  ```
  RUN_TAG=6efa3c145382 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.91 --lr_schedule const --eps_start 0.5 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 96.75, 133.7, 74.52; gap after +1.9%; result checkpoint `e58a58cd-12e0-48f9-8e95-3af4070bc90f`
- Effect: candidate 96.75 minus naive 189.8 = -93, 95% bootstrap interval [-116, -50.47] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 94.9 on CartPole; the worst of its seeds reaches 63.9.

- p. 1; value used: `mean_reward` = 94.93 reward (headline claim)

### What did we measure?
- Naive median 189.8 over 5 runs; repeats: 192.6, 182.3, 182.8, 189.8, 190.1
- Spread: range 182.3 to 192.6, noise band ±5.71 (2 x MAD), CV 2.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +99.9% (noise band ±6.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr` the gap is +36.8% (it comes back)
- PASS · Counterfactual (reversal test): without `eps_start` the gap is +13.8% (it comes back)
- PASS · Held-out claim: C2: +96.4% to -78.6% (not worse beyond noise)
- FAIL · Evidence: `lr=0.91`: evidence gate off: no evidence was looked for
- FAIL · Evidence: `eps_start=0.5`: evidence gate off: no evidence was looked for
- PASS · Effect vs noise: candidate minus naive is -93 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr=0.55` (16.47 noise units, gap -0.8%); `max_steps=100` (16.38 noise units, gap -1.3%); `lr_schedule=inv` (13.22 noise units, gap +20.4%); `lr=0.01` (11.94 noise units, gap -28.0%); `lr=0.05` (9.66 noise units, gap +41.8%) (and 7 more in the JSON)
- Near alternatives (closest across all claims):
  - `max_steps=100`: this claim +3.4%, mean |gap| 15.8% (4 runs)
  - `max_steps=100`, `lr=0.91`: this claim +3.7%, mean |gap| 17.8% (3 runs)
  - `max_steps=100`, `lr_schedule=linear`: this claim +1.8%, mean |gap| 22.5% (3 runs)

### History matching (every measured configuration, all claims together)
- 10 of 45 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr, max_steps`: lr=0.91, max_steps=100 (max I 0.35); lr=0.55, max_steps=100 (max I 0.86)
  - `max_steps`: max_steps=100 (max I 0.43)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.62); lr_schedule=inv, max_steps=100 (max I 1.57)
  - `eps_start, lr, lr_schedule, max_steps`: eps_start=0.5, lr=0.91, lr_schedule=inv, max_steps=100 (max I 0.86)
  - `eps_start, lr`: eps_start=0.1, lr=0.91 (max I 0.87); eps_start=0.5, lr=0.91 (max I 1.14)
  - `lr`: lr=0.91 (max I 2.68); lr=0.55 (max I 2.98)
- 2 separate islands (no single-knob move joins them): lr=0.91, max_steps=100; max_steps=100; lr_schedule=linear, max_steps=100 | eps_start=0.5, lr=0.91, lr_schedule=inv, max_steps=100

Notes:
- evidence gate off: no evidence was checked, so this cannot be labelled Explained

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 4 | +3.4% | +28.2% | 15.8% |
| `max_steps=100`, `lr=0.91` | 3 | +3.7% | +32.0% | 17.8% |
| `max_steps=100`, `lr_schedule=linear` | 3 | +1.8% | +43.3% | 22.5% |
| `max_steps=100`, `lr=0.55` | 3 | +5.3% | +56.5% | 30.9% |
| `max_steps=100`, `lr=0.91`, `lr_schedule=inv`, `eps_start=0.5` | 3 | +5.3% | +56.5% | 30.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `b05f7288e1a4df8af69bb0b5e7633827b4cb46c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
