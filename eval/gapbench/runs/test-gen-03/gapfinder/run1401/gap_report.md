# Gap Report: test-gen-03

Artifact `rlbench` · generated 2026-10-15 18:48 · 71 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -39.6% | -14.6% | ±1.9% | `max_steps=400` |

## C1: mean_reward (paper 302.05)
**Fits but unsupported** · gap -39.6% → -14.6% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0012`, `B0030`, `B0031`, `B0038` (4 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `400`
- Command:

  Replay: fork checkpoint `ff17d3ad-c1d8-463f-8abf-759b25716b29` and run
  ```
  RUN_TAG=4b07b672cc3a "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 400 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 375.6, 274.3, 241.3, 211.5; gap after -14.6%; result checkpoint `23e46743-4dda-458a-9bba-2454e7339423`
- Effect: candidate 257.8 minus naive 182.4 = +75.45, 95% bootstrap interval [+25.69, +95.18] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 302.1 steps

- p. 1; value used: `mean_reward` = 302.05 steps (headline claim)

### What did we measure?
- Naive median 182.4 over 5 runs; repeats: 179.8, 189.9, 185.3, 182.4, 176.8
- Spread: range 176.8 to 189.9, noise band ±5.83 (2 x MAD), CV 2.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -39.6% (noise band ±1.9% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -39.6% (it comes back)
- PASS · Held-out claim: C2: +112.2% to +97.0% (not worse beyond noise)
- FAIL · Evidence: `max_steps=400`: no evidence mentions '400'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +75.45 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=1000` (12.46 noise units, gap -15.6%); `max_steps=500` (11.52 noise units, gap +17.4%); `max_steps=2000` (8.86 noise units, gap +22.5%); `max_steps=10000` (7.28 noise units, gap +25.6%)
- Near alternatives (closest across all claims):
  - `max_steps=10000`: this claim +14.8%, mean |gap| 21.2% (4 runs)
  - `max_steps=1000`: this claim -20.5%, mean |gap| 23.0% (4 runs)
  - `max_steps=500`: this claim +9.6%, mean |gap| 25.5% (4 runs)

### Equally good configurations
The target claim can't tell these 4 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=400` (reported)
- `max_steps=500`
- `max_steps=10000`
- `lr_schedule=linear, max_steps=2000`

### History matching (every measured configuration, all claims together)
- 3 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `max_steps`: max_steps=500 (max I 1.34); max_steps=400 (max I 1.7)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=2000 (max I 1.99)
- 2 separate islands (no single-knob move joins them): max_steps=500; max_steps=400 | lr_schedule=linear, max_steps=2000
- Equally good values: `max_steps` in {400, 500, 10000}

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=400; max_steps=500; max_steps=10000; lr_schedule=linear, max_steps=2000
- equally good values within one noise band (measured): max_steps in {400, 500, 10000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=10000` | 4 | +14.8% | +27.5% | 21.2% |
| `max_steps=1000` | 4 | -20.5% | -25.5% | 23.0% |
| `max_steps=500` | 4 | +9.6% | +41.4% | 25.5% |
| `max_steps=2000` | 4 | +44.0% | -30.8% | 37.4% |
| `max_steps=100` | 4 | -69.1% | +12.0% | 40.5% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
