# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-15 18:54 · 125 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -50.6% | -18.8% | ±0.5% | `max_steps=400` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -50.6% → -18.8% · 54 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0022`, `B0054`, `B0055`, `B0057` (4 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `400`
- Command:

  Replay: fork checkpoint `b2a8bfc6-e032-47d6-8b26-ceb675b5634a` and run
  ```
  RUN_TAG=973344a4148b "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 400 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 326.2, 253.1, 321, 191.6; gap after -18.8%; result checkpoint `91179f9f-8af3-479c-ba0f-48623f0efc7a`
- Effect: candidate 287 minus naive 174.4 = +112.6, 95% bootstrap interval [+7.002, +146.8] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 174.4 over 5 runs; repeats: 185.9, 174.4, 174.1, 188.4, 173.5
- Spread: range 173.5 to 188.4, noise band ±1.91 (2 x MAD), CV 4.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -50.6% (noise band ±0.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -50.6% (it comes back)
- PASS · Held-out claim: C2: +84.1% to +7.4% (not worse beyond noise)
- FAIL · Evidence: `max_steps=400`: no evidence mentions '400'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +112.6 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=1000` (87.38 noise units, gap +3.4%); `max_steps=500` (67.47 noise units, gap -14.2%); `max_steps=2000` (24.41 noise units, gap -37.4%); `gamma=0.995` (13.38 noise units, gap -43.4%); `gamma=0.998` (13.38 noise units, gap -43.4%) (and 2 more in the JSON)
- Near alternatives (closest across all claims):
  - `gamma=0.995`, `max_steps=500`: this claim -13.6%, mean |gap| 9.0% (3 runs)
  - `max_steps=400`, `gamma=0.998`: this claim -3.1%, mean |gap| 10.9% (3 runs)
  - `max_steps=500`: this claim -28.1%, mean |gap| 14.1% (4 runs)

### Equally good configurations
The target claim can't tell these 8 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=400` (reported)
- `max_steps=2000`
- `max_steps=1000`
- `gamma=0.998, max_steps=400`
- `gamma=0.999, max_steps=500`
- `gamma=1.0, max_steps=400`
- `gamma=0.995, max_steps=500`
- `gamma=1.0, max_steps=500`

### History matching (every measured configuration, all claims together)
- 5 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 5 configurations
  - `gamma, max_steps`: gamma=0.995, max_steps=500 (max I 0.6); gamma=0.999, max_steps=500 (max I 0.73); gamma=0.998, max_steps=400 (max I 0.86); gamma=1.0, max_steps=500 (max I 1.6); +1 more
- 2 separate islands (no single-knob move joins them): gamma=0.995, max_steps=500; gamma=0.999, max_steps=500; gamma=1.0, max_steps=500 | gamma=0.998, max_steps=400

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=400; max_steps=2000; max_steps=1000; gamma=0.998, max_steps=400; gamma=0.999, max_steps=500; gamma=1.0, max_steps=400; gamma=0.995, max_steps=500; gamma=1.0, max_steps=500

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `gamma=0.995`, `max_steps=500` | 3 | -13.6% | -4.4% | 9.0% |
| `max_steps=400`, `gamma=0.998` | 3 | -3.1% | +18.7% | 10.9% |
| `max_steps=400` | 4 | -18.8% | +7.4% | 13.1% |
| `max_steps=500` | 4 | -28.1% | -0.1% | 14.1% |
| `max_steps=1000`, `gamma=0.995` | 3 | -1.2% | -33.9% | 17.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
