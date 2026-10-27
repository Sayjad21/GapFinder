# Gap Report: test-gen-03

Artifact `rlbench` · generated 2026-10-15 00:29 · 69 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -38.4% | +13.7% | ±3.0% | `max_steps=500` |

## C1: mean_reward (paper 302.05)
**Fits but unsupported** · gap -38.4% → +13.7% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0006`, `B0018`, `B0019`, `B0038` (4 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `500`
- Command:

  Replay: fork checkpoint `56fe71ec-c5d3-4f17-9f69-dc36ea55a1a6` and run
  ```
  RUN_TAG=013abd22781d "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 500 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 355.2, 291.7, 331.9, 402.5; gap after +13.7%; result checkpoint `449ba387-ade9-4933-8ea8-16228af3634d`
- Effect: candidate 343.5 minus naive 186.1 = +157.4, 95% bootstrap interval [+102.2, +221.2] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 302.1 steps

- p. 1; value used: `mean_reward` = 302.05 steps (headline claim)

### What did we measure?
- Naive median 186.1 over 5 runs; repeats: 175.2, 188.1, 194.7, 181.6, 186.1
- Spread: range 175.2 to 194.7, noise band ±9.12 (2 x MAD), CV 3.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -38.4% (noise band ±3.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -38.4% (it comes back)
- PASS · Held-out claim: C2: +177.4% to +81.6% (not worse beyond noise)
- FAIL · Evidence: `max_steps=500`: no evidence mentions '500'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +157.4 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=1000` (10.74 noise units, gap -5.9%); `max_steps=10000` (9.54 noise units, gap -9.6%); `max_steps=2000` (8.48 noise units, gap -12.8%); `max_steps=400` (5.92 noise units, gap -20.5%)
- Near alternatives (closest across all claims):
  - `max_steps=1000`: this claim -15.6%, mean |gap| 31.5% (4 runs)
  - `max_steps=400`: this claim -21.4%, mean |gap| 35.0% (4 runs)
  - `max_steps=2000`: this claim +27.7%, mean |gap| 39.7% (4 runs)

### Equally good configurations
The target claim can't tell these 5 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=500` (reported)
- `max_steps=1000`
- `max_steps=400`
- `max_steps=2000`
- `lr_schedule=linear, max_steps=2000`

### History matching (every measured configuration, all claims together)
- 4 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 4 configurations
  - `max_steps`: max_steps=1000 (max I 1.16); max_steps=500 (max I 2.72); max_steps=400 (max I 2.81)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=2000 (max I 2)
- 2 separate islands (no single-knob move joins them): max_steps=1000; max_steps=500; max_steps=400 | lr_schedule=linear, max_steps=2000
- Equally good values: `max_steps` in {500, 1000}

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=500; max_steps=1000; max_steps=400; max_steps=2000; lr_schedule=linear, max_steps=2000
- equally good values within one noise band (measured): max_steps in {500, 1000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=1000` | 4 | -15.6% | -47.3% | 31.5% |
| `max_steps=400` | 4 | -21.4% | +48.7% | 35.0% |
| `max_steps=2000` | 4 | +27.7% | -51.8% | 39.7% |
| `max_steps=500` | 4 | +13.7% | +81.6% | 47.6% |
| `max_steps=10000` | 4 | +40.9% | -59.2% | 50.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
