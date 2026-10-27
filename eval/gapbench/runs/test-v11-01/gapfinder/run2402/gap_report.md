# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-16 01:20 · 122 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -48.3% | -6.4% | ±1.6% | `max_steps=2000` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -48.3% → -6.4% · 54 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0013`, `B0040`, `B0041`, `B0058` (4 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `2000`
- Command:

  Replay: fork checkpoint `6a16c5df-646f-4d5f-b38a-286a316d6b7f` and run
  ```
  RUN_TAG=99fb2c1c408e "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 2000 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 358, 627.3, 303.8, 298.7; gap after -6.4%; result checkpoint `b68efe2e-2997-4888-9ad6-5b1854b170b8`
- Effect: candidate 330.9 minus naive 182.9 = +148, 95% bootstrap interval [+109.5, +447.5] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 182.9 over 5 runs; repeats: 185.6, 192.6, 182.9, 175.9, 181.8
- Spread: range 175.9 to 192.6, noise band ±5.52 (2 x MAD), CV 3.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -48.3% (noise band ±1.6% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -48.3% (it comes back)
- PASS · Held-out claim: C2: +58.6% to +51.5% (not worse beyond noise)
- FAIL · Evidence: `max_steps=2000`: no evidence mentions '2000'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +148 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=400` (22.6 noise units, gap -13.0%); `max_steps=1000` (22.09 noise units, gap +13.8%); `max_steps=500` (21.42 noise units, gap -14.8%); `gamma=0.998` (2.76 noise units, gap -43.9%); `gamma=0.995` (1.86 noise units, gap -45.3%)
- Near alternatives (closest across all claims):
  - `gamma=0.999`, `max_steps=500`: this claim -5.4%, mean |gap| 8.7% (3 runs)
  - `gamma=0.995`, `max_steps=2000`: this claim -4.4%, mean |gap| 9.4% (3 runs)
  - `gamma=0.998`, `max_steps=400`: this claim -3.7%, mean |gap| 9.8% (3 runs)

### Equally good configurations
The target claim can't tell these 10 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=2000` (reported)
- `max_steps=500`
- `max_steps=1000`
- `gamma=0.995, max_steps=2000`
- `gamma=1.0, max_steps=500`
- `gamma=0.998, max_steps=400`
- `gamma=0.999, max_steps=500`
- `gamma=0.999, max_steps=400`
- `gamma=1.0, max_steps=400`
- `gamma=0.998, max_steps=1000`

### History matching (every measured configuration, all claims together)
- 12 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `gamma, max_steps`: gamma=0.998, max_steps=1000 (max I 0.41); gamma=0.995, max_steps=2000 (max I 0.68); gamma=0.998, max_steps=400 (max I 1.09); gamma=0.999, max_steps=500 (max I 1.09); +4 more
  - `max_steps`: max_steps=500 (max I 1.65); max_steps=400 (max I 2.03)

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=2000; max_steps=500; max_steps=1000; gamma=0.995, max_steps=2000; gamma=1.0, max_steps=500; gamma=0.998, max_steps=400; gamma=0.999, max_steps=500; gamma=0.999, max_steps=400; gamma=1.0, max_steps=400; gamma=0.998, max_steps=1000

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `gamma=0.999`, `max_steps=500` | 3 | -5.4% | +11.9% | 8.7% |
| `gamma=0.995`, `max_steps=2000` | 3 | -4.4% | +14.4% | 9.4% |
| `gamma=0.998`, `max_steps=400` | 3 | -3.7% | +15.9% | 9.8% |
| `max_steps=1000` | 4 | +11.7% | +10.0% | 10.9% |
| `gamma=1.0`, `max_steps=1000` | 2 | +17.1% | -14.8% | 15.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
