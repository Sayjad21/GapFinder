# Gap Report: test-gen-03

Artifact `rlbench` · generated 2026-10-14 21:42 · 69 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -38.0% | -2.0% | ±4.5% | `max_steps=400` |

## C1: mean_reward (paper 302.05)
**Fits but unsupported** · gap -38.0% → -2.0% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0012`, `B0036`, `B0037`, `B0038` (4 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `400`
- Command:

  Replay: fork checkpoint `b7e28104-619a-461b-95f8-c0ea36cb7efa` and run
  ```
  RUN_TAG=6b11c64b0e9c "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 400 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 265.6, 313.1, 278.9, 356.4; gap after -2.0%; result checkpoint `9c8f8c1d-5f0b-400b-9dc8-0c54452456ef`
- Effect: candidate 296 minus naive 187.2 = +108.8, 95% bootstrap interval [+84.83, +171.7] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 302.1 steps, and that its worst seed still balances for 48.2.

- p. 1; value used: `mean_reward` = 302.05 steps (headline claim)

### What did we measure?
- Naive median 187.2 over 5 runs; repeats: 200, 179.8, 183.2, 193.9, 187.2
- Spread: range 179.8 to 200, noise band ±13.47 (2 x MAD), CV 4.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -38.0% (noise band ±4.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -38.0% (it comes back)
- PASS · Held-out claim: C2: +208.2% to +95.4% (not worse beyond noise)
- FAIL · Evidence: `max_steps=400`: no evidence mentions '400'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +108.8 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=500` (7.18 noise units, gap -6.0%)
- Near alternatives (closest across all claims):
  - `max_steps=500`: this claim -2.2%, mean |gap| 4.2% (4 runs)
  - `max_steps=10000`: this claim +3.5%, mean |gap| 13.3% (4 runs)
  - `max_steps=2000`: this claim -31.9%, mean |gap| 49.5% (4 runs)

### History matching (every measured configuration, all claims together)
- 3 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `max_steps`: max_steps=500 (max I 0.11); max_steps=10000 (max I 0.99); max_steps=400 (max I 1.14)
- Equally good values: `max_steps` in {400, 500, 10000}

Notes:
- equally good values within one noise band (measured): max_steps in {400, 500, 10000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=500` | 4 | -2.2% | -6.2% | 4.2% |
| `max_steps=10000` | 4 | +3.5% | -23.2% | 13.3% |
| `max_steps=400` | 4 | -2.0% | +95.4% | 48.7% |
| `max_steps=2000` | 4 | -31.9% | -67.2% | 49.5% |
| `max_steps=40` | 4 | -86.8% | -18.2% | 52.5% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`

## Provenance
- GapFinder commit: `e0f13d101585ad1609a15fbf67b70128f4cfffc8` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
