# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-15 00:33 · 197 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -45.9% | -1.4% | ±1.2% | `max_steps=10000` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -45.9% → -1.4% · 72 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0025`, `B0066`, `B0067`, `B0074`, `B0075`, `B0076` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `10000`
- Command:

  Replay: fork checkpoint `f2b1f7ee-7886-4647-8ebe-1db1cb0e054e` and run
  ```
  RUN_TAG=77fa3457b96c "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 10000 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 261.3, 659.8, 234.9, 260.6, 435.9, 526.2; gap after -1.4%; result checkpoint `81e8a941-8395-476a-bb62-e34955229ab1`
- Effect: candidate 348.6 minus naive 191.3 = +157.3, 95% bootstrap interval [+49.22, +447.3] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 191.3 over 5 runs; repeats: 191.3, 189.2, 193.2, 195.5, 163.9
- Spread: range 163.9 to 195.5, noise band ±4.34 (2 x MAD), CV 6.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -45.9% (noise band ±1.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -45.9% (it comes back)
- PASS · Held-out claim: C2: +269.8% to -60.0% (not worse beyond noise)
- FAIL · Evidence: `max_steps=10000`: no evidence mentions '10000'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +157.3 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=1000` (24.87 noise units, gap -15.3%); `max_steps=500` (24.06 noise units, gap -16.3%); `max_steps=2000` (22.4 noise units, gap -18.3%); `max_steps=400` (18.68 noise units, gap -22.9%); `gamma=0.999` (2 noise units, gap -43.4%)
- Near alternatives (closest across all claims):
  - `max_steps=1000`, `gamma=0.999`: this claim -3.2%, mean |gap| 10.3% (5 runs)
  - `max_steps=2000`: this claim -20.1%, mean |gap| 14.4% (6 runs)
  - `max_steps=1000`: this claim -10.4%, mean |gap| 15.5% (6 runs)

### History matching (every measured configuration, all claims together)
- 13 of 72 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `max_steps`: max_steps=2000 (max I 0.12)
  - `gamma, max_steps`: gamma=0.999, max_steps=1000 (max I 0.19); gamma=0.998, max_steps=1000 (max I 0.38); gamma=0.999, max_steps=400 (max I 0.46); gamma=0.998, max_steps=500 (max I 0.78); +5 more

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'max_steps': '500', 'gamma': '0.998'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=1000`, `gamma=0.999` | 5 | -3.2% | +17.4% | 10.3% |
| `max_steps=2000` | 6 | -20.1% | +8.7% | 14.4% |
| `max_steps=1000` | 6 | -10.4% | -20.6% | 15.5% |
| `gamma=0.995`, `max_steps=1000` | 5 | -8.4% | +26.8% | 17.6% |
| `max_steps=400` | 6 | -18.4% | +35.6% | 27.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
