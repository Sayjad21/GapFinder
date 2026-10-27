# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-14 23:46 · 153 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -51.8% | -5.7% | ±4.5% | `max_steps=10000` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -51.8% → -5.7% · 50 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0015`, `B0050`, `B0051`, `B0064`, `B0065`, `B0066` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `10000`
- Command:

  Replay: fork checkpoint `96acdb12-8c24-455d-b893-1ed9fb31fe39` and run
  ```
  RUN_TAG=e1a8afc8787e "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 10000 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 119.5, 369.5, 295.2, 411.8, 297, 396.5; gap after -5.7%; result checkpoint `f5bc7815-f180-4bcb-9966-bb7bc49459f3`
- Effect: candidate 333.3 minus naive 170.4 = +162.8, 95% bootstrap interval [+121.3, +241.9] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 170.4 over 5 runs; repeats: 142.1, 192.1, 178.4, 165.5, 170.4
- Spread: range 142.1 to 192.1, noise band ±15.99 (2 x MAD), CV 10.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -51.8% (noise band ±4.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -51.8% (it comes back)
- PASS · Held-out claim: C2: +7.0% to -48.0% (not worse beyond noise)
- FAIL · Evidence: `max_steps=10000`: no evidence mentions '10000'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +162.8 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `g`, `mc`, `mp`, `l`, `f`, `dt`, `seed_generation`, `reward_per_step`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=500` (9.41 noise units, gap -9.2%); `max_steps=1000` (8.66 noise units, gap -12.6%); `max_steps=2000` (7.48 noise units, gap +17.9%); `max_steps=400` (5.23 noise units, gap -28.1%); `gamma=1.0` (1.64 noise units, gap -44.3%) (and 2 more in the JSON)
- Near alternatives (closest across all claims):
  - `max_steps=2000`: this claim +11.1%, mean |gap| 9.0% (6 runs)
  - `max_steps=500`, `gamma=1.0`: this claim +2.3%, mean |gap| 13.9% (5 runs)
  - `max_steps=500`, `init_q=1.0`: this claim -0.2%, mean |gap| 15.2% (5 runs)

### Equally good configurations
The target claim can't tell these 10 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=10000` (reported)
- `max_steps=2000`
- `max_steps=500`
- `max_steps=400`
- `init_q=1.0, max_steps=500`
- `gamma=1.0, max_steps=500`
- `gamma=1.0, max_steps=1000`
- `init_q=1.0, max_steps=1000`
- `gamma=0.998, max_steps=1000`
- `init_q=0, max_steps=1000`

### History matching (every measured configuration, all claims together)
- 10 of 49 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `init_q, max_steps`: init_q=0, max_steps=1000 (max I 0.34); init_q=1.0, max_steps=500 (max I 0.39); init_q=1.0, max_steps=1000 (max I 0.85)
  - `gamma, max_steps`: gamma=1.0, max_steps=500 (max I 0.39); gamma=1.0, max_steps=1000 (max I 0.88); gamma=0.998, max_steps=1000 (max I 0.93); gamma=0.998, max_steps=500 (max I 2.86)
  - `max_steps`: max_steps=2000 (max I 1.43); max_steps=10000 (max I 1.83); max_steps=500 (max I 2.58)

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=10000; max_steps=2000; max_steps=500; max_steps=400; init_q=1.0, max_steps=500; gamma=1.0, max_steps=500; gamma=1.0, max_steps=1000; init_q=1.0, max_steps=1000; gamma=0.998, max_steps=1000; init_q=0, max_steps=1000

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=2000` | 6 | +11.1% | +6.9% | 9.0% |
| `max_steps=500`, `gamma=1.0` | 5 | +2.3% | +25.6% | 13.9% |
| `max_steps=500`, `init_q=1.0` | 5 | -0.2% | +30.1% | 15.2% |
| `max_steps=1000`, `gamma=1.0` | 5 | -5.4% | -27.1% | 16.3% |
| `max_steps=500`, `gamma=0.998` | 5 | -19.0% | +16.4% | 17.7% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `init_q=zero`: invalid_value, The argument --init_q expects a floating‑point number, but the supplied value 'zero' cannot be parsed as a float, causing the program to reject it; retried as `init_q=0`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `g`, `mc`, `mp`, `l`, `f`, `dt`, `seed_generation`, `reward_per_step`

## Provenance
- GapFinder commit: `efb2f63a257a40b9982099a274f2e882f272b80c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
