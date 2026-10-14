# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-14 11:05 · 139 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Explained | -46.0% | -9.2% | ±2.5% | `max_steps=500` |

## C1: mean_reward (paper 353.42)
**Explained** · gap -46.0% → -9.2% · 46 hypotheses tested
> Confirmed cause: reverting it brings the gap back, held-out claims hold, and the value has evidence

### Which experiment changed it?
- Branch: `B0012`, `B0050`, `B0051`, `B0052`, `B0053`, `B0054` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `500`
- Command:

  Replay: fork checkpoint `bd621c89-2887-4088-9f36-b9bf4954e3d9` and run
  ```
  RUN_TAG=e2458bcebdf1 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 500 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 351, 317.6, 324.5, 261, 283.2, 347.3; gap after -9.2%; result checkpoint `e677d488-c8ea-47f4-8084-c0dea64147c3`
- Effect: candidate 321.1 minus naive 191 = +130.1, 95% bootstrap interval [+83.1, +168.7] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 191 over 5 runs; repeats: 195.4, 191, 144.8, 176.2, 195.4
- Spread: range 144.8 to 195.4, noise band ±8.84 (2 x MAD), CV 11.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -46.0% (noise band ±2.5% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is +130.1 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=2000` (15.73 noise units, gap +6.6%); `max_steps=1000` (14.5 noise units, gap -9.7%); `gamma=1.0` (1.02 noise units, gap -43.4%)
- Near alternatives (closest across all claims):
  - `max_steps=1000`, `gamma=1.0`: this claim -10.3%, mean |gap| 18.9% (5 runs)
  - `max_steps=2000`: this claim -9.7%, mean |gap| 26.9% (6 runs)
  - `gamma=0.95`: this claim -55.0%, mean |gap| 28.5% (6 runs)

### History matching (every measured configuration, all claims together)
- 8 of 46 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 8 configurations
  - `gamma, max_steps`: gamma=0.999, max_steps=1000 (max I 0.03); gamma=1.0, max_steps=1000 (max I 0.84); gamma=0.999, max_steps=500 (max I 1.16); gamma=0.999, max_steps=2000 (max I 1.51); +1 more
  - `max_steps`: max_steps=500 (max I 1.77); max_steps=2000 (max I 2.58)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=1000 (max I 1.94)
- 2 separate islands (no single-knob move joins them): gamma=0.999, max_steps=1000; gamma=1.0, max_steps=1000; gamma=0.999, max_steps=500 | lr_schedule=linear, max_steps=1000
- Equally good values: `max_steps` in {500, 2000}

Notes:
- equally good values within one noise band (measured): max_steps in {500, 2000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=1000`, `gamma=1.0` | 5 | -10.3% | +27.6% | 18.9% |
| `max_steps=2000` | 6 | -9.7% | -44.2% | 26.9% |
| `gamma=0.95` | 6 | -55.0% | -2.0% | 28.5% |
| `max_steps=500` | 6 | -9.2% | -53.6% | 31.4% |
| `max_steps=1000` | 6 | -12.7% | -50.7% | 31.7% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `b05f7288e1a4df8af69bb0b5e7633827b4cb46c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
