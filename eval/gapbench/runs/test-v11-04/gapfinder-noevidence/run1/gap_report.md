# Gap Report: test-v11-04

Artifact `rlbench` · generated 2026-10-14 11:14 · 79 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +74.7% | +2.8% | ±5.5% | `max_steps=100` |

## C1: mean_reward (paper 94.93)
**Fits but unsupported** · gap +74.7% → +2.8% · 47 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0011`, `B0020`, `B0021`, `B0022` (4 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `800aad32-3ab2-44ab-8bb4-76ed7724b1e0` and run
  ```
  RUN_TAG=83d7d035bb97 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 96.06, 91.72, 99.75, 99.19; gap after +2.8%; result checkpoint `5371394c-f79e-43e1-99da-f8cfee478aee`
- Effect: candidate 97.62 minus naive 165.9 = -68.26, 95% bootstrap interval [-77.11, -64.14] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 94.9 on CartPole; the worst of its seeds reaches 63.9.

- p. 1; value used: `mean_reward` = 94.93 (headline claim)

### What did we measure?
- Naive median 165.9 over 5 runs; repeats: 173.5, 162.5, 165.9, 163.6, 168.5
- Spread: range 162.5 to 173.5, noise band ±5.21 (2 x MAD), CV 2.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +74.7% (noise band ±5.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +74.7% (it comes back)
- PASS · Held-out claim: C2: -21.5% to +21.6% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: evidence gate off: no evidence was looked for
- PASS · Effect vs noise: candidate minus naive is -68.26 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.5` (9.12 noise units, gap +24.7%); `lr_schedule=inv` (2.36 noise units, gap +61.8%)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `max_steps=100`: this claim -0.1%, mean |gap| 6.6% (3 runs)
  - `max_steps=100`, `lr_schedule=inv`: this claim -8.2%, mean |gap| 20.6% (3 runs)
  - `max_steps=1000`, `lr_schedule=inv`: this claim +43.7%, mean |gap| 34.0% (3 runs)

### History matching (every measured configuration, all claims together)
- 5 of 47 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 5 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.66); lr_schedule=inv, max_steps=100 (max I 1.47)
  - `max_steps`: max_steps=100 (max I 0.67)
  - `eps_start, max_steps`: eps_start=0.5, max_steps=100 (max I 2.19)
  - `eps_start, lr_schedule`: eps_start=0.5, lr_schedule=linear (max I 2.6)
- 2 separate islands (no single-knob move joins them): lr_schedule=linear, max_steps=100; max_steps=100; lr_schedule=inv, max_steps=100 | eps_start=0.5, lr_schedule=linear

Notes:
- evidence gate off: no evidence was checked, so this cannot be labelled Explained

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=linear`, `max_steps=100` | 3 | -0.1% | +13.1% | 6.6% |
| `max_steps=100` | 4 | +2.8% | +21.6% | 12.2% |
| `max_steps=100`, `lr_schedule=inv` | 3 | -8.2% | -33.0% | 20.6% |
| `max_steps=1000`, `lr_schedule=inv` | 3 | +43.7% | -24.4% | 34.0% |
| `lr_schedule=linear`, `eps_start=0.5` | 3 | -1.7% | -81.9% | 41.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `b05f7288e1a4df8af69bb0b5e7633827b4cb46c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
