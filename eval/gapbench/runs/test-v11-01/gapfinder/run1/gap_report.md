# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-14 11:05 · 103 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -48.5% | -0.3% | ±2.1% | `max_steps=2000` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -48.5% → -0.3% · 46 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0015`, `B0047`, `B0048`, `B0049` (4 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `2000`
- Command:

  Replay: fork checkpoint `470bcbd2-3311-4c43-92d8-4daaaa2c9caf` and run
  ```
  RUN_TAG=23cbc59aa8a5 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 2000 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 356.6, 413.2, 347.8, 288.4; gap after -0.3%; result checkpoint `27bf5863-d943-499c-99f0-d98c45ef3528`
- Effect: candidate 352.2 minus naive 182.2 = +170, 95% bootstrap interval [+103.6, +233.9] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 182.2 over 5 runs; repeats: 179.1, 176.6, 182.2, 185.8, 186.5
- Spread: range 176.6 to 186.5, noise band ±7.26 (2 x MAD), CV 2.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -48.5% (noise band ±2.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -48.5% (it comes back)
- PASS · Held-out claim: C2: +149.9% to +5.3% (not worse beyond noise)
- FAIL · Evidence: `max_steps=2000`: no evidence mentions '2000'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +170 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=500` (18.83 noise units, gap -9.8%); `max_steps=1000` (9.95 noise units, gap +28.0%)
- Near alternatives (closest across all claims):
  - `gamma=0.999`, `max_steps=500`: this claim +2.0%, mean |gap| 10.8% (3 runs)
  - `gamma=1.0`, `max_steps=500`: this claim -0.3%, mean |gap| 12.4% (3 runs)
  - `max_steps=1000`: this claim -4.0%, mean |gap| 13.5% (4 runs)

### History matching (every measured configuration, all claims together)
- 6 of 46 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 6 configurations
  - `max_steps`: max_steps=2000 (max I 0.32); max_steps=1000 (max I 0.39); max_steps=500 (max I 1.31)
  - `gamma, max_steps`: gamma=0.95, max_steps=1000 (max I 0.4); gamma=1.0, max_steps=500 (max I 0.43); gamma=0.999, max_steps=500 (max I 0.71)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=2000` | 4 | -0.3% | +5.3% | 2.8% |
| `gamma=0.999`, `max_steps=500` | 3 | +2.0% | +19.6% | 10.8% |
| `gamma=1.0`, `max_steps=500` | 3 | -0.3% | +24.5% | 12.4% |
| `max_steps=1000` | 4 | -4.0% | +23.0% | 13.5% |
| `gamma=0.999`, `max_steps=1000` | 3 | -33.7% | +21.0% | 27.4% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `b05f7288e1a4df8af69bb0b5e7633827b4cb46c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0393, sandbox reported $0.0000 (total $0.0393; this search; ledger extraction is included only if it shared the search's router)
