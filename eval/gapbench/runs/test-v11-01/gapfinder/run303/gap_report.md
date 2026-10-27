# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-14 21:45 · 142 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -49.0% | -2.3% | ±5.1% | `max_steps=500` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -49.0% → -2.3% · 50 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0006`, `B0032`, `B0033`, `B0034`, `B0035`, `B0036` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `500`
- Command:

  Replay: fork checkpoint `7d0f332f-a5ba-44ac-861c-373ada9938f1` and run
  ```
  RUN_TAG=15e367499ba9 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 500 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 348.6, 307.4, 370.8, 165, 341.7, 393.8; gap after -2.3%; result checkpoint `f9abf321-3d48-4ff2-a2f6-07f584271a5d`
- Effect: candidate 345.1 minus naive 180.1 = +165, 95% bootstrap interval [+22.33, +209.1] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 180.1 over 5 runs; repeats: 180.8, 180.1, 171.1, 191.2, 166.8
- Spread: range 166.8 to 191.2, noise band ±18 (2 x MAD), CV 5.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -49.0% (noise band ±5.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -49.0% (it comes back)
- PASS · Held-out claim: C2: -52.8% to +17.5% (not worse beyond noise)
- FAIL · Evidence: `max_steps=500`: no evidence mentions '500'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +165 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `g`, `mc`, `mp`, `l`, `f`, `dt`, `seed_generation`, `reward_per_step`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=1000` (7.28 noise units, gap +11.9%); `max_steps=400` (6.94 noise units, gap -13.7%); `max_steps=10000` (6.41 noise units, gap +16.4%); `max_steps=2000` (5.4 noise units, gap +21.5%); `gamma=0.995` (1.1 noise units, gap -43.4%)
- Near alternatives (closest across all claims):
  - `max_steps=10000`: this claim +13.1%, mean |gap| 7.6% (6 runs)
  - `gamma=0.998`, `max_steps=1000`: this claim -5.0%, mean |gap| 10.2% (5 runs)
  - `init_q=-1.0`, `max_steps=500`: this claim -19.5%, mean |gap| 19.0% (5 runs)

### History matching (every measured configuration, all claims together)
- 6 of 49 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 6 configurations
  - `init_q, max_steps`: init_q=0, max_steps=500 (max I 1.03)
  - `gamma, max_steps`: gamma=0.998, max_steps=1000 (max I 1.05); gamma=0.998, max_steps=500 (max I 1.72)
  - `max_steps`: max_steps=500 (max I 1.73); max_steps=10000 (max I 2.41); max_steps=1000 (max I 2.91)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=10000` | 6 | +13.1% | -2.1% | 7.6% |
| `max_steps=500` | 6 | -2.3% | +17.5% | 9.9% |
| `gamma=0.998`, `max_steps=1000` | 5 | -5.0% | +15.5% | 10.2% |
| `init_q=-1.0`, `max_steps=500` | 5 | -19.5% | -18.6% | 19.0% |
| `init_q=0`, `max_steps=500` | 5 | -4.6% | +34.8% | 19.7% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `init_q=zero`: invalid_value, The argument --init_q expects a floating‑point number, but the supplied value 'zero' cannot be parsed as a float, causing the program to reject it; retried as `init_q=0`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `g`, `mc`, `mp`, `l`, `f`, `dt`, `seed_generation`, `reward_per_step`

## Provenance
- GapFinder commit: `e0f13d101585ad1609a15fbf67b70128f4cfffc8` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
