# Gap Report: test-v11-04

Artifact `rlbench` · generated 2026-10-14 11:52 · 141 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +98.4% | +3.3% | ±7.4% | `max_steps=100` |

## C1: mean_reward (paper 94.93)
**Fits but unsupported** · gap +98.4% → +3.3% · 45 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0008`, `B0032`, `B0033`, `B0034` (4 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Command:

  Replay: fork checkpoint `0d14d8c5-b5aa-4755-899a-63bd77969675` and run
  ```
  RUN_TAG=01e15007e57e "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 96.67, 95.22, 99.44, 99.97; gap after +3.3%; result checkpoint `ea39eb21-678b-47b5-b1e2-b1af5b8d0f7a`
- Effect: candidate 98.06 minus naive 188.3 = -90.28, 95% bootstrap interval [-95.72, -85.1] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 94.9 on CartPole; the worst of its seeds reaches 63.9.

- p. 1; value used: `mean_reward` = 94.93 reward (headline claim)

### What did we measure?
- Naive median 188.3 over 5 runs; repeats: 191.6, 184.6, 192.8, 188.3, 184.8
- Spread: range 184.6 to 192.8, noise band ±7.07 (2 x MAD), CV 2.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +98.4% (noise band ±7.4% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +98.4% (it comes back)
- PASS · Held-out claim: C2: +112.8% to +28.5% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: no evidence mentions '100'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -90.28 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (13.04 noise units, gap +1.3%); `lr=0.01` (12.13 noise units, gap +8.1%); `lr=0.91` (10.52 noise units, gap +20.0%); `lr=0.55` (9.79 noise units, gap +25.5%); `lr=0.05` (7.07 noise units, gap +45.8%) (and 9 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`, `max_steps=100`: this claim -7.5%, mean |gap| 17.8% (3 runs)
  - `lr_schedule=linear`, `max_steps=100`: this claim +2.0%, mean |gap| 21.2% (3 runs)
  - `lr=0.91`, `max_steps=100`: this claim +4.4%, mean |gap| 23.6% (3 runs)

### History matching (every measured configuration, all claims together)
- 8 of 45 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 8 configurations
  - `lr, max_steps`: lr=0.91, max_steps=100 (max I 0.33)
  - `max_steps`: max_steps=100 (max I 1.14)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 1.26); lr_schedule=inv, max_steps=100 (max I 1.78)
  - `lr`: lr=0.55 (max I 2.43); lr=0.91 (max I 2.89)
  - `eps_start, lr`: eps_start=0.0, lr=0.91 (max I 2.77)
  - `lr, lr_schedule`: lr=0.01, lr_schedule=linear (max I 2.95)
- 2 separate islands (no single-knob move joins them): lr=0.91, max_steps=100; max_steps=100; lr_schedule=linear, max_steps=100 | lr=0.01, lr_schedule=linear

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 4 | +3.3% | +28.5% | 15.9% |
| `lr_schedule=inv`, `max_steps=100` | 3 | -7.5% | -28.1% | 17.8% |
| `lr_schedule=linear`, `max_steps=100` | 3 | +2.0% | +40.4% | 21.2% |
| `lr=0.91`, `max_steps=100` | 3 | +4.4% | +42.7% | 23.6% |
| `lr_schedule=inv` | 4 | +45.4% | -23.2% | 34.3% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `b05f7288e1a4df8af69bb0b5e7633827b4cb46c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
