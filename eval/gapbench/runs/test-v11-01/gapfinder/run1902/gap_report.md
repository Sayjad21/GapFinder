# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-15 19:43 · 173 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -49.8% | -4.9% | ±4.1% | `max_steps=500` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -49.8% → -4.9% · 54 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0016`, `B0048`, `B0049`, `B0061`, `B0062`, `B0063` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `500`
- Command:

  Replay: fork checkpoint `0dd8c873-0e71-4685-9681-00662d3698a8` and run
  ```
  RUN_TAG=91ce5583d80e "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 500 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 401, 264.3, 397.4, 276.8, 316.5, 355.8; gap after -4.9%; result checkpoint `95d9d69a-6565-43b8-8aae-4867f20d083f`
- Effect: candidate 336.1 minus naive 177.6 = +158.5, 95% bootstrap interval [+87.56, +206.8] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 177.6 over 5 runs; repeats: 163.5, 180.4, 170.3, 191.8, 177.6
- Spread: range 163.5 to 191.8, noise band ±14.56 (2 x MAD), CV 6.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -49.8% (noise band ±4.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -49.8% (it comes back)
- PASS · Held-out claim: C2: +55.0% to +77.7% (not worse beyond noise)
- FAIL · Evidence: `max_steps=500`: no evidence mentions '500'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +158.5 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=1000` (11.23 noise units, gap +3.5%); `max_steps=2000` (10.31 noise units, gap +7.3%); `max_steps=400` (10.16 noise units, gap +7.9%); `max_steps=10000` (7.11 noise units, gap -20.5%); `gamma=0.999` (1.42 noise units, gap -43.9%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `gamma=0.998`, `max_steps=1000`: this claim -15.1%, mean |gap| 11.2% (5 runs)
  - `max_steps=500`, `gamma=0.999`: this claim -2.2%, mean |gap| 12.2% (5 runs)
  - `max_steps=1000`: this claim -20.1%, mean |gap| 17.7% (6 runs)

### Equally good configurations
The target claim can't tell these 10 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=500` (reported)
- `max_steps=10000`
- `max_steps=400`
- `max_steps=1000`
- `max_steps=2000`
- `gamma=0.999, max_steps=500`
- `gamma=0.999, max_steps=400`
- `gamma=0.998, max_steps=1000`
- `gamma=0.995, max_steps=500`
- `gamma=0.95, max_steps=1000`

### History matching (every measured configuration, all claims together)
- 12 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `gamma, max_steps`: gamma=0.998, max_steps=1000 (max I 0.24); gamma=0.999, max_steps=500 (max I 0.48); gamma=0.999, max_steps=400 (max I 1.51); gamma=0.995, max_steps=500 (max I 2.39); +3 more
  - `max_steps`: max_steps=500 (max I 1.23); max_steps=400 (max I 1.92); max_steps=10000 (max I 2.09)

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=500; max_steps=10000; max_steps=400; max_steps=1000; max_steps=2000; gamma=0.999, max_steps=500; gamma=0.999, max_steps=400; gamma=0.998, max_steps=1000; gamma=0.995, max_steps=500; gamma=0.95, max_steps=1000

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `gamma=0.998`, `max_steps=1000` | 5 | -15.1% | +7.4% | 11.2% |
| `max_steps=500`, `gamma=0.999` | 5 | -2.2% | +22.1% | 12.2% |
| `max_steps=1000` | 6 | -20.1% | -15.2% | 17.7% |
| `gamma=0.999`, `max_steps=1000` | 2 | +22.9% | +13.0% | 18.0% |
| `max_steps=400`, `gamma=0.998` | 2 | -16.0% | +26.4% | 21.2% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
