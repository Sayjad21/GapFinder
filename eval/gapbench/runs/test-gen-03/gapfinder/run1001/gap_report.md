# Gap Report: test-gen-03

Artifact `rlbench` · generated 2026-10-15 00:17 · 103 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -43.1% | -5.6% | ±3.9% | `max_steps=400` |

## C1: mean_reward (paper 302.05)
**Fits but unsupported** · gap -43.1% → -5.6% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0012`, `B0030`, `B0031`, `B0041`, `B0042`, `B0043` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `400`
- Command:

  Replay: fork checkpoint `c96897c2-f17c-4cab-9d04-d2fe51f8490a` and run
  ```
  RUN_TAG=13309a6492f7 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 400 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 293.5, 270.1, 204.3, 327.7, 276.5, 315.4; gap after -5.6%; result checkpoint `bee6a273-a301-49ff-b5a5-af4d011aeeb0`
- Effect: candidate 285 minus naive 172 = +113, 95% bootstrap interval [+47.94, +152.5] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 302.1 steps

- p. 1; value used: `mean_reward` = 302.05 steps (headline claim)

### What did we measure?
- Naive median 172 over 5 runs; repeats: 167.3, 172, 153, 184.8, 177.8
- Spread: range 153 to 184.8, noise band ±11.64 (2 x MAD), CV 7.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -43.1% (noise band ±3.9% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -43.1% (it comes back)
- PASS · Held-out claim: C2: +41.0% to +12.2% (not worse beyond noise)
- FAIL · Evidence: `max_steps=400`: no evidence mentions '400'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +113 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=500` (6.87 noise units, gap -16.6%)
- Near alternatives (closest across all claims):
  - `max_steps=2000`: this claim -3.4%, mean |gap| 7.2% (6 runs)
  - `max_steps=1000`: this claim +23.8%, mean |gap| 15.1% (6 runs)
  - `lr_schedule=linear`, `max_steps=400`: this claim -37.1%, mean |gap| 22.3% (5 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=400` (reported)
- `max_steps=1000`
- `max_steps=2000`

### History matching (every measured configuration, all claims together)
- 4 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 4 configurations
  - `max_steps`: max_steps=2000 (max I 0.58); max_steps=400 (max I 1.24); max_steps=500 (max I 2.21); max_steps=1000 (max I 2.23)
- Equally good values: `max_steps` in {400, 2000}

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=400; max_steps=1000; max_steps=2000
- equally good values within one noise band (measured): max_steps in {400, 2000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=2000` | 6 | -3.4% | +11.0% | 7.2% |
| `max_steps=400` | 6 | -5.6% | +12.2% | 8.9% |
| `max_steps=1000` | 6 | +23.8% | -6.5% | 15.1% |
| `lr_schedule=linear`, `max_steps=400` | 5 | -37.1% | -7.5% | 22.3% |
| `max_steps=10000` | 6 | +36.3% | +12.6% | 24.4% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
