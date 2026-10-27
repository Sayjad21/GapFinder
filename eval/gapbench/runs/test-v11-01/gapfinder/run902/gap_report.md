# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-14 23:46 · 194 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -46.1% | -0.3% | ±1.2% | `max_steps=1000` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -46.1% → -0.3% · 54 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0017`, `B0050`, `B0051`, `B0058`, `B0059`, `B0060` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `1000`
- Command:

  Replay: fork checkpoint `26b8e244-d7b7-481e-bc57-0d66046369e2` and run
  ```
  RUN_TAG=7ff6fca45b32 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 1000 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 382.6, 401.3, 229.8, 456.2, 322.3, 245.6; gap after -0.3%; result checkpoint `537d0a0b-c2f8-4619-aa10-07651d8ddac5`
- Effect: candidate 352.5 minus naive 190.6 = +161.9, 95% bootstrap interval [+48.83, +264] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 190.6 over 5 runs; repeats: 196.3, 188.8, 192.8, 190.6, 134.4
- Spread: range 134.4 to 196.3, noise band ±4.4 (2 x MAD), CV 14.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -46.1% (noise band ±1.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -46.1% (it comes back)
- PASS · Held-out claim: C2: +244.6% to +20.2% (not worse beyond noise)
- FAIL · Evidence: `max_steps=1000`: no evidence mentions '1000'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +161.9 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=2000` (23.67 noise units, gap +16.6%); `max_steps=500` (23.43 noise units, gap -16.9%); `max_steps=10000` (21.03 noise units, gap -19.9%); `max_steps=400` (15.28 noise units, gap -27.1%); `gamma=0.999` (1.68 noise units, gap -44.0%)
- Near alternatives (closest across all claims):
  - `gamma=1.0`, `max_steps=10000`: this claim +2.0%, mean |gap| 1.6% (5 runs)
  - `max_steps=10000`: this claim -6.1%, mean |gap| 7.4% (6 runs)
  - `gamma=0.995`, `max_steps=500`: this claim -10.2%, mean |gap| 9.7% (5 runs)

### Equally good configurations
The target claim can't tell these 12 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=1000` (reported)
- `max_steps=10000`
- `max_steps=2000`
- `gamma=0.998, max_steps=500`
- `gamma=1.0, max_steps=2000`
- `gamma=0.999, max_steps=500`
- `gamma=0.999, max_steps=1000`
- `gamma=0.995, max_steps=500`
- `gamma=0.998, max_steps=1000`
- `gamma=0.998, max_steps=2000`
- `gamma=0.995, max_steps=2000`
- `gamma=0.999, max_steps=10000`

### History matching (every measured configuration, all claims together)
- 16 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `gamma, max_steps`: gamma=0.998, max_steps=10000 (max I 0.37); gamma=1.0, max_steps=2000 (max I 0.45); gamma=1.0, max_steps=10000 (max I 0.56); gamma=0.995, max_steps=2000 (max I 0.94); +3 more
  - `max_steps`: max_steps=1000 (max I 0.57); max_steps=2000 (max I 0.65); max_steps=10000 (max I 0.78)

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=1000; max_steps=10000; max_steps=2000; gamma=0.998, max_steps=500; gamma=1.0, max_steps=2000; gamma=0.999, max_steps=500; gamma=0.999, max_steps=1000; gamma=0.995, max_steps=500; gamma=0.998, max_steps=1000; gamma=0.998, max_steps=2000; gamma=0.995, max_steps=2000; gamma=0.999, max_steps=10000

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `gamma=1.0`, `max_steps=10000` | 5 | +2.0% | +1.3% | 1.6% |
| `max_steps=10000` | 6 | -6.1% | -8.7% | 7.4% |
| `gamma=0.995`, `max_steps=500` | 5 | -10.2% | +9.2% | 9.7% |
| `max_steps=1000` | 6 | -0.3% | +20.2% | 10.2% |
| `max_steps=10000`, `gamma=0.999` | 5 | -10.9% | +14.6% | 12.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `efb2f63a257a40b9982099a274f2e882f272b80c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
