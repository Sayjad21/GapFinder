# Gap Report: test-gen-03

Artifact `rlbench` · generated 2026-10-15 00:47 · 69 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -37.2% | -0.7% | ±3.3% | `max_steps=500` |

## C1: mean_reward (paper 302.05)
**Fits but unsupported** · gap -37.2% → -0.7% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0006`, `B0018`, `B0019`, `B0039` (4 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `500`
- Command:

  Replay: fork checkpoint `c98ab8e9-61b3-48d4-9ba1-b1b048c716d1` and run
  ```
  RUN_TAG=0a19aa482917 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 500 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 242.9, 234.4, 357.1, 395; gap after -0.7%; result checkpoint `ab718aa1-f729-48a6-843c-8e8e32461acc`
- Effect: candidate 300 minus naive 189.7 = +110.3, 95% bootstrap interval [+40.27, +211.5] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 302.1 steps, and that its worst seed still balances for 48.2.

- p. 1; value used: `mean_reward` = 302.05 steps (headline claim)

### What did we measure?
- Naive median 189.7 over 5 runs; repeats: 186.8, 194.7, 189.7, 176, 197.1
- Spread: range 176 to 197.1, noise band ±10.05 (2 x MAD), CV 4.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -37.2% (noise band ±3.3% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -37.2% (it comes back)
- PASS · Held-out claim: C2: +222.0% to +26.2% (not worse beyond noise)
- FAIL · Evidence: `max_steps=500`: no evidence mentions '500'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +110.3 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=400` (8.62 noise units, gap +8.5%); `max_steps=2000` (6.74 noise units, gap -14.8%)
- Near alternatives (closest across all claims):
  - `max_steps=2000`: this claim -7.2%, mean |gap| 4.8% (4 runs)
  - `max_steps=10000`: this claim -6.9%, mean |gap| 14.4% (4 runs)
  - `max_steps=1000`: this claim +30.7%, mean |gap| 22.3% (4 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=500` (reported)
- `max_steps=400`
- `max_steps=10000`

### History matching (every measured configuration, all claims together)
- 3 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `max_steps`: max_steps=500 (max I 0.46); max_steps=2000 (max I 0.53); max_steps=400 (max I 1.92)

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=500; max_steps=400; max_steps=10000

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=2000` | 4 | -7.2% | -2.3% | 4.8% |
| `max_steps=500` | 4 | -0.7% | +26.2% | 13.4% |
| `max_steps=10000` | 4 | -6.9% | +22.0% | 14.4% |
| `max_steps=1000` | 4 | +30.7% | -13.9% | 22.3% |
| `max_steps=400` | 4 | -13.8% | -35.7% | 24.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
