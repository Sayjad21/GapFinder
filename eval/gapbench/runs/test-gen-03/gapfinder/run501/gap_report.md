# Gap Report: test-gen-03

Artifact `rlbench` · generated 2026-10-14 22:14 · 112 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -46.4% | +0.1% | ±2.6% | `max_steps=1000` |

## C1: mean_reward (paper 302.05)
**Fits but unsupported** · gap -46.4% → +0.1% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0007`, `B0023`, `B0024`, `B0025`, `B0026`, `B0027` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `1000`
- Command:

  Replay: fork checkpoint `51b5714d-a5eb-4bf0-9961-331f2ee2a2c4` and run
  ```
  RUN_TAG=e7e2d9d8f2b5 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 1000 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 433.8, 204.6, 468.6, 304.5, 300.3, 269.8; gap after +0.1%; result checkpoint `6d412035-b5a3-4ca7-b04d-ac2bb28bbc7f`
- Effect: candidate 302.4 minus naive 161.8 = +140.6, 95% bootstrap interval [+55.55, +275.5] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 302.1 steps

- p. 1; value used: `mean_reward` = 302.05 steps (headline claim)

### What did we measure?
- Naive median 161.8 over 5 runs; repeats: 157.8, 161.8, 162.2, 147.8, 181.5
- Spread: range 147.8 to 181.5, noise band ±7.91 (2 x MAD), CV 7.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -46.4% (noise band ±2.6% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -46.4% (it comes back)
- PASS · Held-out claim: C2: +16.4% to +4.9% (not worse beyond noise)
- FAIL · Evidence: `max_steps=1000`: no evidence mentions '1000'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +140.6 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=500` (16.28 noise units, gap -3.8%); `max_steps=10000` (14.54 noise units, gap -8.4%); `max_steps=400` (10.1 noise units, gap -20.0%); `max_steps=2000` (8.16 noise units, gap +25.1%); `lr_schedule=linear` (1.06 noise units, gap -43.7%)
- Near alternatives (closest across all claims):
  - `max_steps=500`: this claim -5.7%, mean |gap| 8.3% (6 runs)
  - `max_steps=400`: this claim -13.6%, mean |gap| 11.4% (6 runs)
  - `max_steps=2000`: this claim +5.3%, mean |gap| 18.4% (6 runs)

### Equally good configurations
The target claim can't tell these 4 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=1000` (reported)
- `max_steps=500`
- `max_steps=400`
- `max_steps=10000`

### History matching (every measured configuration, all claims together)
- 5 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 5 configurations
  - `max_steps`: max_steps=500 (max I 0.88); max_steps=2000 (max I 1.4); max_steps=1000 (max I 1.67); max_steps=400 (max I 2.6)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=2000 (max I 2.36)

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=1000; max_steps=500; max_steps=400; max_steps=10000

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=1000` | 6 | +0.1% | +4.9% | 2.5% |
| `max_steps=500` | 6 | -5.7% | +10.8% | 8.3% |
| `max_steps=400` | 6 | -13.6% | -9.2% | 11.4% |
| `max_steps=2000` | 6 | +5.3% | -31.5% | 18.4% |
| `max_steps=10000` | 6 | +12.5% | -45.5% | 29.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`

## Provenance
- GapFinder commit: `e0f13d101585ad1609a15fbf67b70128f4cfffc8` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
