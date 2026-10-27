# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-16 01:20 · 98 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -46.6% | +6.7% | ±4.5% | `max_steps=500` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -46.6% → +6.7% · 50 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0006`, `B0033`, `B0034`, `B0053` (4 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `500`
- Command:

  Replay: fork checkpoint `16478c29-7227-4c31-8563-686cf2b1c315` and run
  ```
  RUN_TAG=3607ecf861db "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 500 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 327.7, 394.5, 365.1, 388.8; gap after +6.7%; result checkpoint `5ed06274-fc61-45a6-93cd-52e710a47041`
- Effect: candidate 376.9 minus naive 188.7 = +188.2, 95% bootstrap interval [+171.6, +211.7] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 188.7 over 5 runs; repeats: 181.1, 180.7, 188.7, 196.7, 198
- Spread: range 180.7 to 198, noise band ±15.95 (2 x MAD), CV 4.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -46.6% (noise band ±4.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -46.6% (it comes back)
- PASS · Held-out claim: C2: +235.6% to +121.2% (not worse beyond noise)
- FAIL · Evidence: `max_steps=500`: no evidence mentions '500'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +188.2 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `g`, `mc`, `mp`, `l`, `f`, `dt`, `seed_generation`, `reward_per_step`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=400` (8.71 noise units, gap -7.3%); `max_steps=10000` (5.35 noise units, gap -22.4%); `max_steps=2000` (4.92 noise units, gap +24.4%)
- Near alternatives (closest across all claims):
  - `max_steps=400`: this claim -13.1%, mean |gap| 10.1% (4 runs)
  - `max_steps=10000`: this claim -6.8%, mean |gap| 13.8% (4 runs)
  - `max_steps=500`, `gamma=1.0`: this claim -4.8%, mean |gap| 15.2% (3 runs)

### Equally good configurations
The target claim can't tell these 6 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=500` (reported)
- `max_steps=10000`
- `max_steps=2000`
- `gamma=1.0, max_steps=500`
- `gamma=0.999, max_steps=400`
- `init_q=0, max_steps=500`

### History matching (every measured configuration, all claims together)
- 7 of 49 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 7 configurations
  - `max_steps`: max_steps=10000 (max I 0.85); max_steps=500 (max I 1.22); max_steps=2000 (max I 1.68); max_steps=400 (max I 2.5)
  - `gamma, max_steps`: gamma=1.0, max_steps=500 (max I 0.93); gamma=0.999, max_steps=400 (max I 2.85)
  - `init_q, max_steps`: init_q=0, max_steps=500 (max I 2.52)
- Equally good values: `max_steps` in {500, 10000}

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=500; max_steps=10000; max_steps=2000; gamma=1.0, max_steps=500; gamma=0.999, max_steps=400; init_q=0, max_steps=500
- equally good values within one noise band (measured): max_steps in {500, 10000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=400` | 4 | -13.1% | -7.0% | 10.1% |
| `max_steps=10000` | 4 | -6.8% | -20.9% | 13.8% |
| `max_steps=500`, `gamma=1.0` | 3 | -4.8% | +25.6% | 15.2% |
| `max_steps=2000` | 4 | +21.0% | -16.1% | 18.6% |
| `max_steps=500`, `init_q=1.0` | 2 | -21.3% | +21.5% | 21.4% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `init_q=zero`: invalid_value, The argument --init_q expects a floating‑point number, but the supplied value 'zero' cannot be parsed as a float, causing the program to reject it; retried as `init_q=0`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `g`, `mc`, `mp`, `l`, `f`, `dt`, `seed_generation`, `reward_per_step`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
