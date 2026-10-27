# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-14 21:19 · 190 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -48.5% | +1.6% | ±4.7% | `max_steps=500`, `gamma=0.999` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -48.5% → +1.6% · 54 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0109`, `B0151`, `B0152`, `B0153`, `B0154` (5 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `500`
- Config: `gamma` naive `0.99`, changed to `0.999`
- Command:

  Replay: fork checkpoint `02d407f5-d7cd-47b4-9813-793325e877ff` and run
  ```
  RUN_TAG=a24372b06328 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.999 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 500 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 219.2, 397.1, 434.8, 359.2, 352.6; gap after +1.6%; result checkpoint `8cb49fdf-bb27-4870-b33a-fb3b20f33619`
- Effect: candidate 359.2 minus naive 182.1 = +177.1, 95% bootstrap interval [+68.6, +248.7] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 182.1 over 5 runs; repeats: 194.9, 156.2, 190.4, 174.7, 182.1
- Spread: range 156.2 to 194.9, noise band ±16.67 (2 x MAD), CV 8.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -48.5% (noise band ±4.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -44.5% (it comes back)
- PASS · Counterfactual (reversal test): without `gamma` the gap is -21.9% (it comes back)
- PASS · Held-out claim: C2: +65.6% to +12.6% (not worse beyond noise)
- FAIL · Evidence: `max_steps=500`: no evidence mentions '500'; it fits, but nothing says the authors used it
- FAIL · Evidence: `gamma=0.999`: no evidence mentions '0.999'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +177.1 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=10000` (9.36 noise units, gap -4.3%); `max_steps=2000` (7.62 noise units, gap +12.5%); `max_steps=1000` (6.65 noise units, gap +17.1%); `max_steps=400` (4.74 noise units, gap -26.1%)
- Near alternatives (closest across all claims):
  - `max_steps=2000`: this claim -4.7%, mean |gap| 4.2% (6 runs)
  - `gamma=0.995`, `max_steps=1000`: this claim +20.5%, mean |gap| 10.3% (5 runs)
  - `max_steps=1000`, `gamma=1.0`: this claim +6.8%, mean |gap| 11.1% (5 runs)

### History matching (every measured configuration, all claims together)
- 11 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `gamma, max_steps`: gamma=0.999, max_steps=10000 (max I 0.16); gamma=0.995, max_steps=2000 (max I 0.31); gamma=0.999, max_steps=500 (max I 0.54); gamma=0.998, max_steps=1000 (max I 0.55); +4 more
  - `max_steps`: max_steps=2000 (max I 0.85); max_steps=1000 (max I 1.71)
- Equally good values: `gamma` in {0.998, 0.999}

Notes:
- equally good values within one noise band (measured): gamma in {0.998, 0.999}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=2000` | 6 | -4.7% | -3.7% | 4.2% |
| `gamma=0.999`, `max_steps=500` | 5 | +1.6% | +12.6% | 7.1% |
| `gamma=0.995`, `max_steps=1000` | 5 | +20.5% | -0.1% | 10.3% |
| `max_steps=1000`, `gamma=1.0` | 5 | +6.8% | +15.5% | 11.1% |
| `max_steps=1000` | 6 | +20.6% | -11.0% | 15.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `634d827f07d6659ff82f6ea0924c8ba487e9d02a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
