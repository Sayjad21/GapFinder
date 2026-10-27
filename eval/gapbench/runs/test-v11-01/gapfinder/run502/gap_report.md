# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-14 22:17 · 103 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -50.2% | +4.0% | ±2.2% | `max_steps=2000` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -50.2% → +4.0% · 54 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0019`, `B0064`, `B0065`, `B0066` (4 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `2000`
- Command:

  Replay: fork checkpoint `89d3b010-4ddf-4a5d-ac3b-17ffae27d8e4` and run
  ```
  RUN_TAG=80ddc50b4d25 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 2000 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 431.6, 302.3, 340.4, 394.8; gap after +4.0%; result checkpoint `f912349f-f0ee-4758-87eb-d8873719b760`
- Effect: candidate 367.6 minus naive 176 = +191.6, 95% bootstrap interval [+116.3, +220.7] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 176 over 5 runs; repeats: 192.5, 175.5, 183, 172, 176
- Spread: range 172 to 192.5, noise band ±7.88 (2 x MAD), CV 4.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -50.2% (noise band ±2.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -50.2% (it comes back)
- PASS · Held-out claim: C2: +36.4% to -52.4% (not worse beyond noise)
- FAIL · Evidence: `max_steps=2000`: no evidence mentions '2000'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +191.6 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=400` (10.24 noise units, gap -27.4%); `max_steps=1000` (5.39 noise units, gap -38.2%); `gamma=1.0` (2.67 noise units, gap -44.2%); `gamma=0.999` (2.3 noise units, gap -45.1%); `max_steps=500` (1.21 noise units, gap -47.5%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `max_steps=1000`: this claim +5.6%, mean |gap| 7.2% (4 runs)
  - `gamma=0.995`: this claim -48.6%, mean |gap| 36.5% (4 runs)
  - `gamma=0.95`: this claim -52.8%, mean |gap| 37.3% (4 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=2000` (reported)
- `max_steps=1000`
- `max_steps=400`

### History matching (every measured configuration, all claims together)
- 3 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `max_steps`: max_steps=1000 (max I 0.57); max_steps=2000 (max I 0.75)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=2000 (max I 2.94)
- Equally good values: `max_steps` in {1000, 2000}

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=2000; max_steps=1000; max_steps=400
- equally good values within one noise band (measured): max_steps in {1000, 2000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=1000` | 4 | +5.6% | -8.7% | 7.2% |
| `max_steps=2000` | 4 | +4.0% | -52.4% | 28.2% |
| `gamma=0.995` | 4 | -48.6% | -24.3% | 36.5% |
| `gamma=0.95` | 4 | -52.8% | +21.8% | 37.3% |
| `max_steps=500` | 4 | -24.0% | +52.7% | 38.3% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `e0f13d101585ad1609a15fbf67b70128f4cfffc8` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
