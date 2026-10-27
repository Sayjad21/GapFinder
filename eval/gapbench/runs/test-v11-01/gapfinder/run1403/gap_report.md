# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-15 18:54 · 166 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -53.3% | -21.7% | ±1.0% | `max_steps=400` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -53.3% → -21.7% · 50 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0012`, `B0044`, `B0045`, `B0073`, `B0074`, `B0075` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `400`
- Command:

  Replay: fork checkpoint `7c36c075-b8db-4cb2-b99b-551f4211e1cd` and run
  ```
  RUN_TAG=b976d8855b14 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 400 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 231.7, 351.1, 247, 306.7, 328.8, 222.8; gap after -21.7%; result checkpoint `2feb0a2a-d5e1-4963-a917-1cdca4071786`
- Effect: candidate 276.8 minus naive 165.2 = +111.7, 95% bootstrap interval [+62.14, +179] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 165.2 over 5 runs; repeats: 150.1, 163.5, 167, 165.2, 183.5
- Spread: range 150.1 to 183.5, noise band ±3.58 (2 x MAD), CV 7.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -53.3% (noise band ±1.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -53.3% (it comes back)
- PASS · Held-out claim: C2: -22.4% to -29.4% (not worse beyond noise)
- FAIL · Evidence: `max_steps=400`: no evidence mentions '400'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +111.7 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `g`, `mc`, `mp`, `l`, `f`, `dt`, `seed_generation`, `reward_per_step`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=1000` (21.87 noise units, gap +31.1%); `max_steps=500` (13.58 noise units, gap -39.5%); `max_steps=2000` (10.36 noise units, gap -42.8%); `gamma=1.0` (9.14 noise units, gap -44.0%); `gamma=0.995` (9.05 noise units, gap -44.1%) (and 4 more in the JSON)
- Near alternatives (closest across all claims):
  - `init_q=1.0`, `max_steps=400`: this claim -16.7%, mean |gap| 19.7% (5 runs)
  - `init_q=-1.0`, `max_steps=400`: this claim -24.4%, mean |gap| 21.2% (5 runs)
  - `max_steps=2000`: this claim -33.4%, mean |gap| 21.9% (6 runs)

### Equally good configurations
The target claim can't tell these 8 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=400` (reported)
- `max_steps=500`
- `gamma=0.995, max_steps=1000`
- `gamma=1.0, max_steps=1000`
- `init_q=1.0, max_steps=1000`
- `init_q=1.0, max_steps=400`
- `gamma=0.995, max_steps=400`
- `init_q=-1.0, max_steps=400`

### History matching (every measured configuration, all claims together)
- 3 of 49 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `gamma, max_steps`: gamma=0.995, max_steps=1000 (max I 1.07); gamma=1.0, max_steps=1000 (max I 1.15)
  - `init_q, max_steps`: init_q=-1.0, max_steps=1000 (max I 2.46)
- 2 separate islands (no single-knob move joins them): gamma=0.995, max_steps=1000; gamma=1.0, max_steps=1000 | init_q=-1.0, max_steps=1000
- Equally good values: `max_steps` in {400, 1000}

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=400; max_steps=500; gamma=0.995, max_steps=1000; gamma=1.0, max_steps=1000; init_q=1.0, max_steps=1000; init_q=1.0, max_steps=400; gamma=0.995, max_steps=400; init_q=-1.0, max_steps=400
- equally good values within one noise band (measured): max_steps in {400, 1000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `init_q=1.0`, `max_steps=400` | 5 | -16.7% | +22.6% | 19.7% |
| `init_q=-1.0`, `max_steps=400` | 5 | -24.4% | +18.1% | 21.2% |
| `max_steps=2000` | 6 | -33.4% | +10.4% | 21.9% |
| `max_steps=400` | 6 | -21.7% | -29.4% | 25.5% |
| `gamma=0.995`, `max_steps=1000` | 5 | -7.3% | +44.6% | 26.0% |

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
