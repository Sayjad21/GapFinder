# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-15 19:43 · 143 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -50.1% | -6.2% | ±4.5% | `max_steps=500` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -50.1% → -6.2% · 50 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0006`, `B0032`, `B0033`, `B0063`, `B0064`, `B0065` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `500`
- Command:

  Replay: fork checkpoint `7351e534-e031-4a95-ab94-3fe92ad5e32d` and run
  ```
  RUN_TAG=9f8ad7556b44 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 500 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 367.8, 337, 250.9, 341.7, 325.8, 306.1; gap after -6.2%; result checkpoint `d26c9e06-da3d-4185-ae5e-44f31c386543`
- Effect: candidate 331.4 minus naive 176.3 = +155.1, 95% bootstrap interval [+88.91, +175.6] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 176.3 over 5 runs; repeats: 157.8, 177.4, 176.3, 154.3, 184.3
- Spread: range 154.3 to 184.3, noise band ±16.01 (2 x MAD), CV 7.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -50.1% (noise band ±4.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -50.1% (it comes back)
- PASS · Held-out claim: C2: +37.7% to -13.0% (not worse beyond noise)
- FAIL · Evidence: `max_steps=500`: no evidence mentions '500'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +155.1 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `g`, `mc`, `mp`, `l`, `f`, `dt`, `seed_generation`, `reward_per_step`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=2000` (8.28 noise units, gap +12.6%); `max_steps=1000` (7.54 noise units, gap -15.9%); `max_steps=400` (4.92 noise units, gap -27.8%); `init_q=1.0` (1.35 noise units, gap -44.0%); `gamma=1.0` (1.27 noise units, gap -44.4%) (and 2 more in the JSON)
- Near alternatives (closest across all claims):
  - `max_steps=10000`: this claim +3.4%, mean |gap| 9.0% (6 runs)
  - `init_q=1.0`, `max_steps=2000`: this claim +12.0%, mean |gap| 12.4% (5 runs)
  - `max_steps=2000`: this claim -20.6%, mean |gap| 14.4% (6 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=500` (reported)
- `max_steps=1000`
- `init_q=-1.0, max_steps=2000`

### History matching (every measured configuration, all claims together)
- 4 of 49 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 4 configurations
  - `max_steps`: max_steps=10000 (max I 0.52); max_steps=500 (max I 1.65)
  - `init_q, max_steps`: init_q=1.0, max_steps=2000 (max I 1.87)
  - `gamma, max_steps`: gamma=1.0, max_steps=2000 (max I 2.99)
- 3 separate islands (no single-knob move joins them): max_steps=10000; max_steps=500 | init_q=1.0, max_steps=2000 | gamma=1.0, max_steps=2000
- Equally good values: `max_steps` in {500, 1000, 10000}

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=500; max_steps=1000; init_q=-1.0, max_steps=2000
- equally good values within one noise band (measured): max_steps in {500, 1000, 10000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=10000` | 6 | +3.4% | +14.6% | 9.0% |
| `max_steps=500` | 6 | -6.2% | -13.0% | 9.6% |
| `init_q=1.0`, `max_steps=2000` | 5 | +12.0% | +12.9% | 12.4% |
| `max_steps=2000` | 6 | -20.6% | +8.2% | 14.4% |
| `max_steps=1000` | 6 | +8.8% | +38.3% | 23.5% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `init_q=zero`: invalid_value, The argument --init_q expects a floating‑point number, but the supplied value 'zero' cannot be parsed as a float, causing the program to reject it; retried as `init_q=0`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `g`, `mc`, `mp`, `l`, `f`, `dt`, `seed_generation`, `reward_per_step`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
