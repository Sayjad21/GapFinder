# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-14 23:32 · 182 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -46.4% | -10.5% | ±2.8% | `max_steps=500` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -46.4% → -10.5% · 54 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0016`, `B0048`, `B0049`, `B0058`, `B0059`, `B0060` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `500`
- Command:

  Replay: fork checkpoint `d56b7613-9058-4a92-a892-fbbec7f9427b` and run
  ```
  RUN_TAG=cfb5719588ab "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 500 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 309.7, 323.1, 388.1, 214, 256.2, 411; gap after -10.5%; result checkpoint `e9045a58-4238-407b-b9f7-f9d5639b517c`
- Effect: candidate 316.4 minus naive 189.3 = +127.1, 95% bootstrap interval [+42.64, +220.1] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 189.3 over 5 runs; repeats: 168.9, 194.7, 194.2, 187.1, 189.3
- Spread: range 168.9 to 194.7, noise band ±9.78 (2 x MAD), CV 5.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -46.4% (noise band ±2.8% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -46.4% (it comes back)
- PASS · Held-out claim: C2: +287.2% to -19.1% (not worse beyond noise)
- FAIL · Evidence: `max_steps=500`: no evidence mentions '500'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +127.1 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=10000` (15.57 noise units, gap -3.4%); `max_steps=400` (14.32 noise units, gap -6.8%); `max_steps=1000` (12.24 noise units, gap -12.6%); `max_steps=2000` (3.62 noise units, gap -36.4%)
- Near alternatives (closest across all claims):
  - `max_steps=500`, `gamma=0.995`: this claim -0.1%, mean |gap| 2.0% (5 runs)
  - `max_steps=10000`: this claim +15.2%, mean |gap| 12.0% (6 runs)
  - `max_steps=1000`: this claim -17.5%, mean |gap| 13.5% (6 runs)

### Equally good configurations
The target claim can't tell these 11 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=500` (reported)
- `max_steps=10000`
- `max_steps=1000`
- `gamma=0.999, max_steps=400`
- `gamma=0.998, max_steps=500`
- `gamma=0.995, max_steps=500`
- `gamma=0.999, max_steps=500`
- `gamma=1.0, max_steps=500`
- `gamma=0.998, max_steps=400`
- `gamma=1.0, max_steps=400`
- `gamma=1.0, max_steps=1000`

### History matching (every measured configuration, all claims together)
- 11 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `gamma, max_steps`: gamma=0.995, max_steps=500 (max I 1.11); gamma=0.998, max_steps=500 (max I 1.24); gamma=0.998, max_steps=400 (max I 1.51); gamma=1.0, max_steps=500 (max I 1.59); +3 more
  - `max_steps`: max_steps=10000 (max I 1.81); max_steps=2000 (max I 1.86); max_steps=500 (max I 1.93)
- Equally good values: `max_steps` in {500, 2000}

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=500; max_steps=10000; max_steps=1000; gamma=0.999, max_steps=400; gamma=0.998, max_steps=500; gamma=0.995, max_steps=500; gamma=0.999, max_steps=500; gamma=1.0, max_steps=500; gamma=0.998, max_steps=400; gamma=1.0, max_steps=400; gamma=1.0, max_steps=1000
- equally good values within one noise band (measured): max_steps in {500, 2000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=500`, `gamma=0.995` | 5 | -0.1% | +3.8% | 2.0% |
| `max_steps=10000` | 6 | +15.2% | -8.7% | 12.0% |
| `max_steps=1000` | 6 | -17.5% | +9.5% | 13.5% |
| `max_steps=2000` | 6 | -11.9% | +17.5% | 14.7% |
| `max_steps=500` | 6 | -10.5% | -19.1% | 14.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `efb2f63a257a40b9982099a274f2e882f272b80c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
