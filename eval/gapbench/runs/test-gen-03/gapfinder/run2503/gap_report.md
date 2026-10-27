# Gap Report: test-gen-03

Artifact `rlbench` · generated 2026-10-16 01:45 · 71 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -38.7% | +14.7% | ±1.5% | `max_steps=1000` |

## C1: mean_reward (paper 302.05)
**Fits but unsupported** · gap -38.7% → +14.7% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0007`, `B0020`, `B0021`, `B0039` (4 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `1000`
- Command:

  Replay: fork checkpoint `d8c88284-e4a0-45f8-9391-25fe8d3746b6` and run
  ```
  RUN_TAG=c778798c6c04 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 1000 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 266.3, 400.5, 386.1, 306.8; gap after +14.7%; result checkpoint `6a339b97-5859-4bfa-9f14-dbc13c633a5b`
- Effect: candidate 346.4 minus naive 185.1 = +161.3, 95% bootstrap interval [+120.1, +218.1] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 302.1 steps, and that its worst seed still balances for 48.2.

- p. 1; value used: `mean_reward` = 302.05 steps (headline claim)

### What did we measure?
- Naive median 185.1 over 5 runs; repeats: 178.9, 185.1, 186.8, 182.9, 188.5
- Spread: range 178.9 to 188.5, noise band ±4.51 (2 x MAD), CV 2.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -38.7% (noise band ±1.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -38.7% (it comes back)
- PASS · Held-out claim: C2: +176.5% to +23.1% (not worse beyond noise)
- FAIL · Evidence: `max_steps=1000`: no evidence mentions '1000'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +161.3 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=10000` (17.2 noise units, gap -13.0%); `max_steps=400` (16.1 noise units, gap -14.7%); `max_steps=500` (15.79 noise units, gap +15.1%)
- Near alternatives (closest across all claims):
  - `max_steps=500`: this claim -5.6%, mean |gap| 6.0% (4 runs)
  - `max_steps=10000`: this claim -9.5%, mean |gap| 19.7% (4 runs)
  - `max_steps=2000`: this claim -28.0%, mean |gap| 41.5% (4 runs)

### Equally good configurations
The target claim can't tell these 2 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=1000` (reported)
- `max_steps=400`

### History matching (every measured configuration, all claims together)
- 4 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 4 configurations
  - `max_steps`: max_steps=10000 (max I 0.52); max_steps=500 (max I 1.51); max_steps=400 (max I 1.83); max_steps=1000 (max I 2.47)
- Equally good values: `max_steps` in {400, 500, 1000, 10000}

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=1000; max_steps=400
- equally good values within one noise band (measured): max_steps in {400, 500, 1000, 10000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=500` | 4 | -5.6% | +6.3% | 6.0% |
| `max_steps=1000` | 4 | +14.7% | +23.1% | 18.9% |
| `max_steps=10000` | 4 | -9.5% | -30.0% | 19.7% |
| `max_steps=2000` | 4 | -28.0% | +55.0% | 41.5% |
| `max_steps=400` | 4 | -8.9% | +74.2% | 41.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
