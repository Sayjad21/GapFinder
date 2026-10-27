# Gap Report: test-gen-03

Artifact `rlbench` · generated 2026-10-14 21:42 · 95 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -39.4% | +7.2% | ±2.9% | `max_steps=1000` |

## C1: mean_reward (paper 302.05)
**Fits but unsupported** · gap -39.4% → +7.2% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0007`, `B0023`, `B0024`, `B0025`, `B0026`, `B0027` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `1000`
- Command:

  Replay: fork checkpoint `095fae93-6c23-4796-ab0d-8da1e9d5de03` and run
  ```
  RUN_TAG=ff4b2f530585 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 1000 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 353.1, 384.3, 202.7, 367.9, 202.9, 294.4; gap after +7.2%; result checkpoint `948bbdcc-0ca8-4995-9214-e20786c9650c`
- Effect: candidate 323.7 minus naive 182.9 = +140.8, 95% bootstrap interval [+23.34, +207.3] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 302.1 steps

- p. 1; value used: `mean_reward` = 302.05 steps (headline claim)

### What did we measure?
- Naive median 182.9 over 5 runs; repeats: 160.2, 183.9, 182.9, 159.5, 187.3
- Spread: range 159.5 to 187.3, noise band ±8.78 (2 x MAD), CV 7.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -39.4% (noise band ±2.9% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -39.4% (it comes back)
- PASS · Held-out claim: C2: +14.8% to -42.6% (not worse beyond noise)
- FAIL · Evidence: `max_steps=1000`: no evidence mentions '1000'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +140.8 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=400` (8.25 noise units, gap +15.5%); `max_steps=2000` (7.01 noise units, gap -19.1%); `max_steps=10000` (5.97 noise units, gap +22.1%); `max_steps=500` (4.22 noise units, gap +27.2%)
- Near alternatives (closest across all claims):
  - `max_steps=500`: this claim -22.0%, mean |gap| 16.1% (6 runs)
  - `max_steps=500`, `lr_schedule=linear`: this claim -34.3%, mean |gap| 26.0% (5 runs)
  - `max_steps=2000`: this claim +49.4%, mean |gap| 38.5% (6 runs)

### History matching (every measured configuration, all claims together)
- 3 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `max_steps`: max_steps=1000 (max I 0.35); max_steps=400 (max I 2); max_steps=10000 (max I 2.15)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=500` | 6 | -22.0% | +10.1% | 16.1% |
| `max_steps=1000` | 6 | +7.2% | -42.6% | 24.9% |
| `max_steps=500`, `lr_schedule=linear` | 5 | -34.3% | -17.7% | 26.0% |
| naive (reproduction as run) | 5 | -39.4% | +14.8% | 27.1% |
| `max_steps=2000` | 6 | +49.4% | -27.6% | 38.5% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`

## Provenance
- GapFinder commit: `e0f13d101585ad1609a15fbf67b70128f4cfffc8` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
