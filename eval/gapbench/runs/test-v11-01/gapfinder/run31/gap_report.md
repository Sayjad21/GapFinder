# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-14 21:19 · 199 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -48.6% | -6.2% | ±1.8% | `max_steps=2000` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -48.6% → -6.2% · 54 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0019`, `B0093`, `B0094`, `B0095`, `B0096`, `B0097` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `2000`
- Command:

  Replay: fork checkpoint `74951ade-532d-4bad-90b3-2fa2f536be6f` and run
  ```
  RUN_TAG=adcc598e6d41 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 2000 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 259, 110.2, 384.6, 547.2, 278.6, 497.3; gap after -6.2%; result checkpoint `21cc2b74-bf9a-44b3-8c98-87c806b58699`
- Effect: candidate 331.6 minus naive 181.6 = +150, 95% bootstrap interval [-35.33, +349.3] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 181.6 over 5 runs; repeats: 163.5, 181.6, 180, 186.6, 184.7
- Spread: range 163.5 to 186.6, noise band ±6.21 (2 x MAD), CV 5.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -48.6% (noise band ±1.8% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -48.6% (it comes back)
- PASS · Held-out claim: C2: +24.3% to -24.0% (not worse beyond noise)
- FAIL · Evidence: `max_steps=2000`: no evidence mentions '2000'; it fits, but nothing says the authors used it
- FAIL · Effect vs noise: candidate minus naive is +150 with a 95% bootstrap interval that includes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=10000` (25.26 noise units, gap -4.2%); `max_steps=400` (11.12 noise units, gap -29.1%); `max_steps=1000` (7.96 noise units, gap +34.6%); `max_steps=500` (6.61 noise units, gap -37.0%); `gamma=1.0` (1.9 noise units, gap -45.3%) (and 3 more in the JSON)
- Near alternatives (closest across all claims):
  - `gamma=0.995`, `max_steps=2000`: this claim +6.0%, mean |gap| 10.3% (5 runs)
  - `gamma=1.0`, `max_steps=10000`: this claim -7.5%, mean |gap| 13.6% (5 runs)
  - `max_steps=400`: this claim -23.9%, mean |gap| 15.2% (6 runs)

### History matching (every measured configuration, all claims together)
- 14 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `gamma, max_steps`: gamma=0.995, max_steps=2000 (max I 0.37); gamma=0.95, max_steps=10000 (max I 0.66); gamma=0.998, max_steps=1000 (max I 0.67); gamma=1.0, max_steps=10000 (max I 1.2); +3 more
  - `max_steps`: max_steps=2000 (max I 0.39); max_steps=10000 (max I 0.94); max_steps=1000 (max I 1.5)

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'max_steps': '1000', 'gamma': '1.0'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `gamma=0.995`, `max_steps=2000` | 5 | +6.0% | -14.5% | 10.3% |
| `gamma=1.0`, `max_steps=10000` | 5 | -7.5% | +19.8% | 13.6% |
| `max_steps=2000` | 6 | -6.2% | -24.0% | 15.1% |
| `max_steps=400` | 6 | -23.9% | +6.4% | 15.2% |
| `max_steps=10000` | 6 | -9.7% | +30.3% | 20.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `634d827f07d6659ff82f6ea0924c8ba487e9d02a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
