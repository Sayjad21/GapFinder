# Gap Report: test-v11-01

Artifact `rlbench` · generated 2026-10-14 11:06 · 105 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -51.4% | +3.8% | ±2.5% | `max_steps=1000` |

## C1: mean_reward (paper 353.42)
**Fits but unsupported** · gap -51.4% → +3.8% · 46 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0013`, `B0041`, `B0042`, `B0043` (4 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `1000`
- Command:

  Replay: fork checkpoint `dcc91515-cf92-4475-afcf-8e4f0624bf19` and run
  ```
  RUN_TAG=c9324b0e1a01 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 1000 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 490.6, 288.9, 444.7, 288.2; gap after +3.8%; result checkpoint `03583e46-8d0f-4473-ad96-84049fc493a4`
- Effect: candidate 366.8 minus naive 171.6 = +195.1, 95% bootstrap interval [+104.6, +274.8] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 353.4 steps, and that its worst seed still balances for 43.4.

- p. 1; value used: `mean_reward` = 353.42 steps (headline claim)

### What did we measure?
- Naive median 171.6 over 5 runs; repeats: 187.5, 171.2, 167.3, 171.6, 178.5
- Spread: range 167.3 to 187.5, noise band ±8.7 (2 x MAD), CV 4.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -51.4% (noise band ±2.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -51.4% (it comes back)
- PASS · Held-out claim: C2: -27.1% to -56.1% (not worse beyond noise)
- FAIL · Evidence: `max_steps=1000`: evidence gate off: no evidence was looked for
- PASS · Effect vs noise: candidate minus naive is +195.1 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=500` (20.14 noise units, gap -1.8%); `max_steps=2000` (7.04 noise units, gap -34.1%); `gamma=1.0` (1.65 noise units, gap -47.4%); `gamma=0.999` (1.09 noise units, gap -48.8%)
- Near alternatives (closest across all claims):
  - `gamma=0.999`, `max_steps=1000`: this claim +13.1%, mean |gap| 13.4% (3 runs)
  - `max_steps=2000`: this claim +12.6%, mean |gap| 15.9% (4 runs)
  - `max_steps=500`: this claim -16.2%, mean |gap| 17.8% (4 runs)

### History matching (every measured configuration, all claims together)
- 5 of 46 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 5 configurations
  - `max_steps`: max_steps=1000 (max I 1.34); max_steps=2000 (max I 2.12)
  - `gamma, max_steps`: gamma=0.999, max_steps=1000 (max I 1.64); gamma=0.95, max_steps=2000 (max I 2.05); gamma=0.999, max_steps=2000 (max I 2.09)

Notes:
- evidence gate off: no evidence was checked, so this cannot be labelled Explained

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `gamma=0.999`, `max_steps=1000` | 3 | +13.1% | +13.6% | 13.4% |
| `max_steps=2000` | 4 | +12.6% | -19.3% | 15.9% |
| `max_steps=500` | 4 | -16.2% | +19.3% | 17.8% |
| `max_steps=1000` | 4 | +3.8% | -56.1% | 29.9% |
| `max_steps=2000`, `gamma=0.95` | 3 | +10.8% | -54.4% | 32.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `b05f7288e1a4df8af69bb0b5e7633827b4cb46c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
