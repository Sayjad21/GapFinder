# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-14 22:17 · 172 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -50.6% | +1.9% | ±3.9% | `max_steps=1000` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -50.6% → +1.9% · 55 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0017`, `B0083`, `B0084`, `B0085`, `B0086`, `B0087` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `1000`
- Command:

  Replay: fork checkpoint `3366e3f0-db8e-4fb9-93c1-263eee6ec5e6` and run
  ```
  RUN_TAG=77d7b1c097d2 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 1000 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 544.4, 207.5, 418.9, 183.8, 411.1, 308.9; gap after +1.9%; result checkpoint `ce72707e-0c8d-4c56-b30e-07ee7876ae8d`
- Effect: candidate 360 minus naive 174.5 = +185.5, 95% bootstrap interval [+16.1, +250.4] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 174.5 over 5 runs; repeats: 174.5, 154.6, 165.9, 177.1, 181.4
- Spread: range 154.6 to 181.4, noise band ±13.86 (2 x MAD), CV 6.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -50.6% (noise band ±3.9% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -50.6% (it comes back)
- PASS · Held-out claim: C2: +39.1% to +12.3% (not worse beyond noise)
- FAIL · Evidence: `max_steps=1000`: no evidence mentions '1000'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +185.5 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=500` (11.15 noise units, gap -6.9%); `max_steps=2000` (7.7 noise units, gap -20.4%); `max_steps=10000` (7.67 noise units, gap -20.5%); `max_steps=400` (2.47 noise units, gap -40.9%); `gamma=0.998` (1.69 noise units, gap -44.0%) (and 2 more in the JSON)
- Near alternatives (closest across all claims):
  - `gamma=0.999`, `max_steps=1000`: this claim +15.0%, mean |gap| 13.7% (5 runs)
  - `max_steps=2000`: this claim +4.8%, mean |gap| 17.3% (6 runs)
  - `max_steps=400`: this claim -23.8%, mean |gap| 18.4% (6 runs)

### Equally good configurations
The target claim can't tell these 4 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=1000` (reported)
- `max_steps=500`
- `max_steps=2000`
- `max_steps=10000`

### History matching (every measured configuration, all claims together)
- 4 of 55 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 4 configurations
  - `gamma, max_steps`: gamma=0.999, max_steps=1000 (max I 0.33)
  - `max_steps`: max_steps=1000 (max I 0.41); max_steps=2000 (max I 1.45); max_steps=500 (max I 1.72)
- Equally good values: `max_steps` in {1000, 2000}

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=1000; max_steps=500; max_steps=2000; max_steps=10000
- equally good values within one noise band (measured): max_steps in {1000, 2000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=1000` | 6 | +1.9% | +12.3% | 7.1% |
| `gamma=0.999`, `max_steps=1000` | 5 | +15.0% | +12.5% | 13.7% |
| `max_steps=2000` | 6 | +4.8% | -29.9% | 17.3% |
| `max_steps=400` | 6 | -23.8% | +13.0% | 18.4% |
| `max_steps=10000` | 6 | +25.8% | -23.9% | 24.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `e0f13d101585ad1609a15fbf67b70128f4cfffc8` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
