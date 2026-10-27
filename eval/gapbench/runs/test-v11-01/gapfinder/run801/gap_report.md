# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-14 23:31 · 199 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -48.2% | -15.0% | ±2.2% | `max_steps=500` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -48.2% → -15.0% · 54 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0016`, `B0048`, `B0049`, `B0074`, `B0075`, `B0076` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `500`
- Command:

  Replay: fork checkpoint `f4a4a515-8a9c-467d-b31b-e92532636287` and run
  ```
  RUN_TAG=5475341222a9 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 500 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 273.8, 293.5, 340.3, 307.4, 255.8, 345.9; gap after -15.0%; result checkpoint `42490cb9-c4fc-4281-abe4-4c53bf9b1c4f`
- Effect: candidate 300.4 minus naive 183.2 = +117.2, 95% bootstrap interval [+87.54, +175.3] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 183.2 over 5 runs; repeats: 185.9, 187.1, 153.6, 183.2, 162.4
- Spread: range 153.6 to 187.1, noise band ±7.79 (2 x MAD), CV 8.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -48.2% (noise band ±2.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -48.2% (it comes back)
- PASS · Held-out claim: C2: +69.8% to +24.3% (not worse beyond noise)
- FAIL · Evidence: `max_steps=500`: no evidence mentions '500'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +117.2 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=400` (14.31 noise units, gap -16.6%); `max_steps=10000` (10.99 noise units, gap -23.9%); `max_steps=1000` (7.53 noise units, gap -31.5%); `gamma=1.0` (1.95 noise units, gap -43.8%); `gamma=0.999` (1.68 noise units, gap -44.5%) (and 2 more in the JSON)
- Near alternatives (closest across all claims):
  - `max_steps=500`, `gamma=0.999`: this claim -1.4%, mean |gap| 7.4% (5 runs)
  - `max_steps=400`, `gamma=0.995`: this claim -17.1%, mean |gap| 12.8% (5 runs)
  - `max_steps=400`: this claim -24.4%, mean |gap| 15.6% (6 runs)

### History matching (every measured configuration, all claims together)
- 11 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `max_steps`: max_steps=1000 (max I 0.88); max_steps=500 (max I 2.52)
  - `gamma, max_steps`: gamma=0.999, max_steps=500 (max I 1.08); gamma=0.995, max_steps=500 (max I 1.97); gamma=1.0, max_steps=1000 (max I 2); gamma=1.0, max_steps=500 (max I 2.39); +3 more
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=1000 (max I 2.69)

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'max_steps': '10000', 'gamma': '0.998'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=500`, `gamma=0.999` | 5 | -1.4% | +13.4% | 7.4% |
| `max_steps=400`, `gamma=0.995` | 5 | -17.1% | +8.4% | 12.8% |
| `max_steps=400` | 6 | -24.4% | +6.8% | 15.6% |
| `max_steps=2000` | 6 | +32.0% | +4.2% | 18.1% |
| `max_steps=500` | 6 | -15.0% | +24.3% | 19.7% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `efb2f63a257a40b9982099a274f2e882f272b80c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
