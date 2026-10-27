# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-15 01:12 · 133 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -53.0% | +6.5% | ±2.3% | `max_steps=2000` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -53.0% → +6.5% · 54 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0019`, `B0052`, `B0053`, `B0057` (4 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `2000`
- Command:

  Replay: fork checkpoint `699f94c8-b308-492c-9b3c-693c6acb5399` and run
  ```
  RUN_TAG=338f2f8e3405 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 2000 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 365.8, 364.8, 557.1, 387.1; gap after +6.5%; result checkpoint `48a5cd11-3b6a-4d79-b74c-47cea7aef1e8`
- Effect: candidate 376.4 minus naive 166.2 = +210.2, 95% bootstrap interval [+194.1, +392.4] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 166.2 over 5 runs; repeats: 170.6, 162.2, 175.6, 162.5, 166.2
- Spread: range 162.2 to 175.6, noise band ±8.06 (2 x MAD), CV 3.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -53.0% (noise band ±2.3% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -53.0% (it comes back)
- PASS · Held-out claim: C2: +6.5% to -23.0% (not worse beyond noise)
- FAIL · Evidence: `max_steps=2000`: no evidence mentions '2000'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +210.2 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=500` (21.13 noise units, gap -4.8%); `max_steps=400` (17.01 noise units, gap -14.2%); `max_steps=1000` (5.08 noise units, gap -41.4%); `gamma=0.998` (3.61 noise units, gap -44.7%); `gamma=1.0` (3.44 noise units, gap -45.1%)
- Near alternatives (closest across all claims):
  - `max_steps=500`, `gamma=0.998`: this claim +1.1%, mean |gap| 10.0% (3 runs)
  - `max_steps=400`: this claim -20.9%, mean |gap| 19.8% (4 runs)
  - `max_steps=1000`, `gamma=0.999`: this claim +32.3%, mean |gap| 22.4% (3 runs)

### Equally good configurations
The target claim can't tell these 8 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=2000` (reported)
- `max_steps=1000`
- `gamma=0.998, max_steps=500`
- `gamma=0.995, max_steps=400`
- `gamma=1.0, max_steps=1000`
- `gamma=0.998, max_steps=1000`
- `gamma=0.999, max_steps=1000`
- `gamma=1.0, max_steps=2000`

### History matching (every measured configuration, all claims together)
- 5 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 5 configurations
  - `gamma, max_steps`: gamma=0.998, max_steps=500 (max I 1.34); gamma=1.0, max_steps=1000 (max I 1.49); gamma=0.995, max_steps=400 (max I 2.31); gamma=0.999, max_steps=500 (max I 2.88); +1 more
- 2 separate islands (no single-knob move joins them): gamma=0.998, max_steps=500; gamma=0.995, max_steps=400; gamma=0.999, max_steps=500 | gamma=1.0, max_steps=1000

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=2000; max_steps=1000; gamma=0.998, max_steps=500; gamma=0.995, max_steps=400; gamma=1.0, max_steps=1000; gamma=0.998, max_steps=1000; gamma=0.999, max_steps=1000; gamma=1.0, max_steps=2000

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=500`, `gamma=0.998` | 3 | +1.1% | +18.8% | 10.0% |
| `max_steps=2000` | 4 | +6.5% | -23.0% | 14.8% |
| `max_steps=400` | 4 | -20.9% | -18.6% | 19.8% |
| `max_steps=1000`, `gamma=0.999` | 3 | +32.3% | +12.6% | 22.4% |
| `max_steps=1000`, `gamma=1.0` | 3 | +18.4% | +30.3% | 24.4% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
