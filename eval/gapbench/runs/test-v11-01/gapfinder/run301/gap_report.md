# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-14 21:45 · 153 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -53.0% | +0.0% | ±1.0% | `max_steps=10000` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -53.0% → +0.0% · 54 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0025`, `B0085`, `B0086`, `B0087` (4 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `10000`
- Command:

  Replay: fork checkpoint `6624d807-7fc0-4948-bdc6-677e5fae85d1` and run
  ```
  RUN_TAG=35a1eda1d0cb "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 10000 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 456, 263.4, 443.8, 220.2; gap after +0.0%; result checkpoint `e2b920ab-04f6-4e9a-86dc-422a2934567f`
- Effect: candidate 353.6 minus naive 166.1 = +187.4, 95% bootstrap interval [+51.9, +281.9] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 166.1 over 5 runs; repeats: 170.4, 164.9, 166.1, 159, 167.9
- Spread: range 159 to 170.4, noise band ±3.62 (2 x MAD), CV 2.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -53.0% (noise band ±1.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -53.0% (it comes back)
- PASS · Held-out claim: C2: +11.6% to -11.2% (not worse beyond noise)
- FAIL · Evidence: `max_steps=10000`: no evidence mentions '10000'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +187.4 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=500` (44.58 noise units, gap -7.3%); `max_steps=400` (39 noise units, gap -13.0%); `max_steps=2000` (15.79 noise units, gap +36.8%); `gamma=0.999` (8.8 noise units, gap -44.0%); `gamma=0.998` (7.66 noise units, gap -45.1%) (and 3 more in the JSON)
- Near alternatives (closest across all claims):
  - `gamma=0.995`, `max_steps=2000`: this claim -1.4%, mean |gap| 6.9% (3 runs)
  - `gamma=0.995`, `max_steps=400`: this claim -9.4%, mean |gap| 9.8% (3 runs)
  - `max_steps=500`, `gamma=0.995`: this claim -12.4%, mean |gap| 11.4% (3 runs)

### History matching (every measured configuration, all claims together)
- 5 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 5 configurations
  - `max_steps`: max_steps=10000 (max I 0.42); max_steps=2000 (max I 2.15)
  - `gamma, max_steps`: gamma=1.0, max_steps=500 (max I 1.29); gamma=0.998, max_steps=10000 (max I 2.68); gamma=0.995, max_steps=500 (max I 2.96)
- 2 separate islands (no single-knob move joins them): max_steps=10000; max_steps=2000; gamma=0.998, max_steps=10000 | gamma=1.0, max_steps=500; gamma=0.995, max_steps=500

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=10000` | 4 | +0.0% | -11.2% | 5.6% |
| `gamma=0.995`, `max_steps=2000` | 3 | -1.4% | +12.3% | 6.9% |
| `gamma=0.995`, `max_steps=400` | 3 | -9.4% | +10.3% | 9.8% |
| `max_steps=500`, `gamma=0.995` | 3 | -12.4% | +10.4% | 11.4% |
| `max_steps=500`, `gamma=1.0` | 3 | +15.8% | -9.6% | 12.7% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `e0f13d101585ad1609a15fbf67b70128f4cfffc8` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
