# Gap Report: test-gen-03

Artifact `rlbench` · generated 2026-10-15 00:48 · 91 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -38.3% | +5.0% | ±3.9% | `max_steps=2000` |

## C1: mean_reward (paper 302.05)
**Fits but unsupported** · gap -38.3% → +5.0% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0009`, `B0024`, `B0025`, `B0044`, `B0045`, `B0046` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `2000`
- Command:

  Replay: fork checkpoint `a86ba30c-b1bf-4001-9b65-f6415faa486d` and run
  ```
  RUN_TAG=f2a8997637d4 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 2000 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 395.8, 165.4, 505, 349.2, 224.1, 285.2; gap after +5.0%; result checkpoint `40a297b5-22f7-4b4e-8484-fd4752c0cc2c`
- Effect: candidate 317.2 minus naive 186.4 = +130.8, 95% bootstrap interval [+2.538, +288.6] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 302.1 steps

- p. 1; value used: `mean_reward` = 302.05 steps (headline claim)

### What did we measure?
- Naive median 186.4 over 5 runs; repeats: 168.6, 165, 192.2, 192.4, 186.4
- Spread: range 165 to 192.4, noise band ±11.9 (2 x MAD), CV 7.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -38.3% (noise band ±3.9% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -38.3% (it comes back)
- PASS · Held-out claim: C2: +180.8% to +5.9% (not worse beyond noise)
- FAIL · Evidence: `max_steps=2000`: no evidence mentions '2000'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +130.8 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=500` (5.69 noise units, gap +15.9%); `max_steps=400` (3.23 noise units, gap -25.6%)
- Near alternatives (closest across all claims):
  - `max_steps=400`: this claim -13.3%, mean |gap| 9.5% (6 runs)
  - `max_steps=10000`: this claim +31.8%, mean |gap| 19.9% (6 runs)
  - `max_steps=500`: this claim +10.4%, mean |gap| 27.7% (6 runs)

### Equally good configurations
The target claim can't tell these 4 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=2000` (reported)
- `max_steps=500`
- `max_steps=400`
- `max_steps=10000`

### History matching (every measured configuration, all claims together)
- 3 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `max_steps`: max_steps=500 (max I 0.89); max_steps=2000 (max I 1.09); max_steps=400 (max I 2.08)

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=2000; max_steps=500; max_steps=400; max_steps=10000

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=2000` | 6 | +5.0% | +5.9% | 5.5% |
| `max_steps=400` | 6 | -13.3% | +5.8% | 9.5% |
| `max_steps=10000` | 6 | +31.8% | -8.0% | 19.9% |
| `max_steps=500` | 6 | +10.4% | +45.1% | 27.7% |
| `max_steps=1000` | 6 | +35.8% | +33.7% | 34.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
