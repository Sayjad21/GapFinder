# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-15 19:42 · 139 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -49.3% | -3.2% | ±3.0% | `max_steps=500`, `gamma=0.995` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -49.3% → -3.2% · 66 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0081`, `B0121`, `B0134` (3 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `500`
- Config: `gamma` naive `0.99`, changed to `0.995`
- Command:

  Replay: fork checkpoint `ad92436f-9aaa-43fb-801d-82f937e596f3` and run
  ```
  RUN_TAG=2af947a081a0 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.995 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 500 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 307, 355.9, 342.3; gap after -3.2%; result checkpoint `ea7993ed-6cbd-4aa2-9cb3-c7f607b3dbac`
- Effect: candidate 342.3 minus naive 179.2 = +163.1, 95% bootstrap interval [+123.1, +181.4] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 179.2 over 5 runs; repeats: 170.3, 189, 182.3, 173.9, 179.2
- Spread: range 170.3 to 189, noise band ±10.45 (2 x MAD), CV 4.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -49.3% (noise band ±3.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -47.5% (it comes back)
- PASS · Counterfactual (reversal test): without `gamma` the gap is -23.8% (it comes back)
- PASS · Held-out claim: C2: +137.6% to +60.7% (not worse beyond noise)
- FAIL · Evidence: `max_steps=500`: no evidence mentions '500'; it fits, but nothing says the authors used it
- FAIL · Evidence: `gamma=0.995`: no evidence mentions '0.995'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +163.1 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=2000` (12.16 noise units, gap +13.4%); `max_steps=400` (8.69 noise units, gap -23.6%); `max_steps=1000` (3.3 noise units, gap +39.6%); `gamma=1.0` (1.83 noise units, gap -43.9%); `gamma=0.999` (1.46 noise units, gap -45.0%)
- Near alternatives (closest across all claims):
  - `gamma=0.999`, `max_steps=400`: this claim -3.8%, mean |gap| 8.0% (3 runs)
  - `max_steps=500`, `gamma=0.999`: this claim -6.4%, mean |gap| 14.9% (3 runs)
  - `gamma=0.95`, `max_steps=2000`: this claim -29.8%, mean |gap| 15.3% (2 runs)

### Equally good configurations
The target claim can't tell these 7 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `gamma=0.995, max_steps=500` (reported)
- `gamma=0.999, max_steps=400`
- `gamma=0.999, max_steps=500`
- `gamma=1.0, max_steps=2000`
- `gamma=0.995, max_steps=1000`
- `gamma=0.998, max_steps=500`
- `gamma=0.999, max_steps=1000`

### History matching (every measured configuration, all claims together)
- 5 of 66 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 5 configurations
  - `gamma, max_steps`: gamma=0.999, max_steps=400 (max I 1.07); gamma=0.999, max_steps=500 (max I 1.62); gamma=1.0, max_steps=2000 (max I 1.7); gamma=0.995, max_steps=1000 (max I 1.78); +1 more
- 2 separate islands (no single-knob move joins them): gamma=0.999, max_steps=400; gamma=0.999, max_steps=500; gamma=0.995, max_steps=1000 | gamma=1.0, max_steps=2000

Notes:
- configurations the target claim can't tell apart from the answer: gamma=0.995, max_steps=500; gamma=0.999, max_steps=400; gamma=0.999, max_steps=500; gamma=1.0, max_steps=2000; gamma=0.995, max_steps=1000; gamma=0.998, max_steps=500; gamma=0.999, max_steps=1000

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `gamma=0.999`, `max_steps=400` | 3 | -3.8% | -12.2% | 8.0% |
| `max_steps=500`, `gamma=0.999` | 3 | -6.4% | +23.4% | 14.9% |
| `gamma=0.95`, `max_steps=2000` | 2 | -29.8% | +0.9% | 15.3% |
| `gamma=0.95`, `max_steps=1000` | 2 | -16.1% | -21.4% | 18.7% |
| `max_steps=500`, `gamma=0.95` | 2 | -21.7% | -16.0% | 18.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
