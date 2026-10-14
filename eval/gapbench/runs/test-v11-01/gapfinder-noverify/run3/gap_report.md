# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-14 12:20 · 135 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Explained | -50.1% | -2.9% | ±3.2% | `max_steps=500`, `gamma=1.0` |

## C1: mean_reward (paper 353.42)
**Explained** · gap -50.1% → -2.9% · 42 hypotheses tested
> Interacting factors: these changes close the gap only together, and every check passes

### Which experiment changed it?
- Branch: `B0071`, `B0108`, `B0109`, `B0110`, `B0111` (5 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `500`
- Config: `gamma` naive `0.99`, changed to `1.0`
- Command:

  Replay: fork checkpoint `c2e7064c-e578-4599-aaec-0f3fc1d19734` and run
  ```
  RUN_TAG=9ec0e8f44177 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 1.0 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 500 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 403.3, 343.3, 310.9, 357.2, 263.7; gap after -2.9%; result checkpoint `36af417b-d820-450f-9d45-256210ead6d2`
- Effect: candidate 343.3 minus naive 176.5 = +166.8, 95% bootstrap interval [+95.6, +212.8] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 176.5 over 5 runs; repeats: 182.1, 176.5, 170.8, 198.5, 161.3
- Spread: range 161.3 to 198.5, noise band ±11.28 (2 x MAD), CV 7.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -50.1% (noise band ±3.2% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is +166.8 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `g`, `mc`, `mp`, `l`, `f`, `dt`, `seed_generation`, `reward_per_step`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=1000` (12.85 noise units, gap +9.1%); `gamma=0.999` (1.95 noise units, gap -43.8%); `max_steps=2000` (1.11 noise units, gap -46.5%)
- Near alternatives (closest across all claims):
  - `max_steps=1000`, `init_q=0`: this claim -13.1%, mean |gap| 9.5% (5 runs)
  - `max_steps=1000`, `gamma=0.999`: this claim -4.7%, mean |gap| 12.9% (5 runs)
  - `max_steps=1000`: this claim +8.2%, mean |gap| 16.6% (6 runs)

### History matching (every measured configuration, all claims together)
- 8 of 41 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 8 configurations
  - `max_steps`: max_steps=1000 (max I 0.99); max_steps=2000 (max I 2.6)
  - `init_q, max_steps`: init_q=1.0, max_steps=1000 (max I 1.29); init_q=0, max_steps=500 (max I 1.55); init_q=0, max_steps=1000 (max I 1.8)
  - `gamma, max_steps`: gamma=1.0, max_steps=500 (max I 1.37); gamma=0.999, max_steps=500 (max I 1.8); gamma=0.999, max_steps=1000 (max I 2.09)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=1000`, `init_q=0` | 5 | -13.1% | +6.0% | 9.5% |
| `max_steps=1000`, `gamma=0.999` | 5 | -4.7% | +21.1% | 12.9% |
| `max_steps=1000` | 6 | +8.2% | -25.0% | 16.6% |
| `max_steps=500`, `init_q=1.0` | 5 | -12.5% | -21.0% | 16.8% |
| `max_steps=1000`, `gamma=1.0` | 5 | +17.3% | +16.3% | 16.8% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `init_q=zero`: invalid_value, The argument --init_q expects a floating‑point number, but the supplied value 'zero' cannot be parsed as a float, causing the program to reject it; retried as `init_q=0`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `g`, `mc`, `mp`, `l`, `f`, `dt`, `seed_generation`, `reward_per_step`

## Provenance
- GapFinder commit: `b05f7288e1a4df8af69bb0b5e7633827b4cb46c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0005, sandbox reported $0.0000 (total $0.0005; this search; ledger extraction is included only if it shared the search's router)
