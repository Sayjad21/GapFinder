# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-14 11:32 · 132 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -52.3% | +2.5% | ±10.4% | `max_steps=2000` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -52.3% → +2.5% · 46 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0015`, `B0060`, `B0061`, `B0062`, `B0063`, `B0064` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `2000`
- Command:

  Replay: fork checkpoint `b2c954f4-386f-4bf0-b843-6f58c64085ae` and run
  ```
  RUN_TAG=c369884447b6 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 2000 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 331.9, 130.4, 568.8, 348, 376.4, 402.6; gap after +2.5%; result checkpoint `6e32f8a7-15e1-4610-9e25-e70ec903c44b`
- Effect: candidate 362.2 minus naive 168.6 = +193.6, 95% bootstrap interval [+2.074, +361] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 168.6 over 5 runs; repeats: 150.2, 198.1, 168.6, 147.3, 186.8
- Spread: range 147.3 to 198.1, noise band ±36.93 (2 x MAD), CV 13.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -52.3% (noise band ±10.4% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -52.3% (it comes back)
- PASS · Held-out claim: C2: +18.9% to +4.3% (not worse beyond noise)
- FAIL · Evidence: `max_steps=2000`: no evidence mentions '2000'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +193.6 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=1000` (4.62 noise units, gap +4.0%); `max_steps=500` (2.43 noise units, gap -26.9%)
- Near alternatives (closest across all claims):
  - `max_steps=1000`: this claim -5.4%, mean |gap| 8.3% (6 runs)
  - `max_steps=500`, `gamma=0.999`: this claim -8.8%, mean |gap| 11.2% (5 runs)
  - `max_steps=500`: this claim -12.7%, mean |gap| 23.0% (6 runs)

### History matching (every measured configuration, all claims together)
- 9 of 46 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 9 configurations
  - `max_steps`: max_steps=2000 (max I 0.28); max_steps=500 (max I 1.65); max_steps=1000 (max I 2.44)
  - `gamma, max_steps`: gamma=0.95, max_steps=2000 (max I 0.57); gamma=0.999, max_steps=500 (max I 0.99); gamma=0.999, max_steps=2000 (max I 2.02); gamma=1.0, max_steps=500 (max I 2.29); +1 more
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=2000 (max I 2.29)
- Equally good values: `max_steps` in {500, 1000, 2000}

Notes:
- equally good values within one noise band (measured): max_steps in {500, 1000, 2000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=2000` | 6 | +2.5% | +4.3% | 3.4% |
| `max_steps=1000` | 6 | -5.4% | -11.1% | 8.3% |
| `max_steps=500`, `gamma=0.999` | 5 | -8.8% | +13.6% | 11.2% |
| `max_steps=500` | 6 | -12.7% | -33.4% | 23.0% |
| `gamma=1.0`, `max_steps=2000` | 5 | +24.7% | +23.2% | 23.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `b05f7288e1a4df8af69bb0b5e7633827b4cb46c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0327, sandbox reported $0.0000 (total $0.0327; this search; ledger extraction is included only if it shared the search's router)
