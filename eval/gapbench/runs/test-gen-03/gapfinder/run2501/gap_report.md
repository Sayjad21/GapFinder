# Gap Report: test-gen-03

Artifact `rlbench` · generated 2026-10-16 01:45 · 99 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -41.9% | +13.9% | ±2.4% | `max_steps=1000` |

## C1: mean_reward (paper 302.05)
**Fits but unsupported** · gap -41.9% → +13.9% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0007`, `B0020`, `B0021`, `B0038`, `B0039`, `B0040` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `1000`
- Command:

  Replay: fork checkpoint `8bb6ea95-fabd-48aa-82bc-9e77fea23226` and run
  ```
  RUN_TAG=2181c9dc9e7c "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 1000 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 294.3, 250.4, 393.9, 394.3, 565.6, 152; gap after +13.9%; result checkpoint `abed9ae7-7b28-4fa0-8d0a-0ed6eb9136d5`
- Effect: candidate 344.1 minus naive 175.5 = +168.6, 95% bootstrap interval [+9.014, +347.5] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 302.1 steps

- p. 1; value used: `mean_reward` = 302.05 steps (headline claim)

### What did we measure?
- Naive median 175.5 over 5 runs; repeats: 171.9, 198.2, 175.5, 192.8, 175.3
- Spread: range 171.9 to 198.2, noise band ±7.17 (2 x MAD), CV 6.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -41.9% (noise band ±2.4% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -41.9% (it comes back)
- PASS · Held-out claim: C2: +117.3% to +63.5% (not worse beyond noise)
- FAIL · Evidence: `max_steps=1000`: no evidence mentions '1000'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +168.6 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=400` (10.76 noise units, gap -16.4%); `max_steps=500` (6.53 noise units, gap -26.4%); `max_steps=10000` (1.75 noise units, gap +37.7%)
- Near alternatives (closest across all claims):
  - `max_steps=500`: this claim -15.3%, mean |gap| 8.0% (6 runs)
  - `max_steps=2000`: this claim +21.2%, mean |gap| 11.4% (6 runs)
  - `max_steps=10000`: this claim +15.0%, mean |gap| 18.3% (6 runs)

### Equally good configurations
The target claim can't tell these 5 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=1000` (reported)
- `max_steps=500`
- `max_steps=2000`
- `max_steps=400`
- `lr_schedule=linear, max_steps=2000`

### History matching (every measured configuration, all claims together)
- 7 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 7 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=2000 (max I 1.44); lr_schedule=linear, max_steps=10000 (max I 2.41); lr_schedule=linear, max_steps=1000 (max I 2.6)
  - `max_steps`: max_steps=500 (max I 1.72); max_steps=10000 (max I 2.33); max_steps=1000 (max I 2.36); max_steps=400 (max I 2.71)
- Equally good values: `max_steps` in {500, 1000, 10000}

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=1000; max_steps=500; max_steps=2000; max_steps=400; lr_schedule=linear, max_steps=2000
- equally good values within one noise band (measured): max_steps in {500, 1000, 10000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=500` | 6 | -15.3% | +0.7% | 8.0% |
| `max_steps=2000` | 6 | +21.2% | +1.5% | 11.4% |
| `max_steps=10000` | 6 | +15.0% | -21.6% | 18.3% |
| `max_steps=400` | 6 | -18.2% | -23.4% | 20.8% |
| `max_steps=1000` | 6 | +13.9% | +63.5% | 38.7% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
