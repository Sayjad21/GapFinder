# Gap Report: test-gen-03

Artifact `rlbench` · generated 2026-10-14 23:41 · 73 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -40.8% | -3.5% | ±2.0% | `max_steps=1000` |

## C1: mean_reward (paper 302.05)
**Fits but unsupported** · gap -40.8% → -3.5% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0007`, `B0020`, `B0021`, `B0040` (4 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `1000`
- Command:

  Replay: fork checkpoint `ed3355c2-2694-4f91-b28f-a78552991883` and run
  ```
  RUN_TAG=34477191ab33 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 1000 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 238.2, 483.1, 298.8, 284.3; gap after -3.5%; result checkpoint `9e30f60f-3fb7-4cb5-a439-9907f405deb7`
- Effect: candidate 291.5 minus naive 178.9 = +112.6, 95% bootstrap interval [+100.7, +307] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 302.1 steps

- p. 1; value used: `mean_reward` = 302.05 steps (headline claim)

### What did we measure?
- Naive median 178.9 over 5 runs; repeats: 178.9, 172.2, 178.6, 187.6, 181.9
- Spread: range 172.2 to 187.6, noise band ±5.97 (2 x MAD), CV 3.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -40.8% (noise band ±2.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -40.8% (it comes back)
- PASS · Held-out claim: C2: +38.9% to -47.7% (not worse beyond noise)
- FAIL · Evidence: `max_steps=1000`: no evidence mentions '1000'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +112.6 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=500` (19.52 noise units, gap -2.2%); `max_steps=400` (16.39 noise units, gap -8.4%); `max_steps=2000` (9.45 noise units, gap -22.1%); `max_steps=10000` (2.82 noise units, gap +35.2%)
- Near alternatives (closest across all claims):
  - `max_steps=500`: this claim +4.3%, mean |gap| 27.0% (4 runs)
  - `max_steps=2000`: this claim +21.8%, mean |gap| 29.9% (4 runs)
  - `max_steps=400`: this claim -9.1%, mean |gap| 36.3% (4 runs)

### Equally good configurations
The target claim can't tell these 4 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=1000` (reported)
- `max_steps=500`
- `max_steps=400`
- `max_steps=2000`

### History matching (every measured configuration, all claims together)
- 3 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `max_steps`: max_steps=400 (max I 1.53); max_steps=1000 (max I 1.54); max_steps=500 (max I 1.65)
- Equally good values: `max_steps` in {500, 1000}

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=1000; max_steps=500; max_steps=400; max_steps=2000
- equally good values within one noise band (measured): max_steps in {500, 1000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=1000` | 4 | -3.5% | -47.7% | 25.6% |
| `max_steps=500` | 4 | +4.3% | +49.7% | 27.0% |
| `max_steps=2000` | 4 | +21.8% | -38.1% | 29.9% |
| `max_steps=400` | 4 | -9.1% | +63.5% | 36.3% |
| naive (reproduction as run) | 5 | -40.8% | +38.9% | 39.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`

## Provenance
- GapFinder commit: `efb2f63a257a40b9982099a274f2e882f272b80c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
