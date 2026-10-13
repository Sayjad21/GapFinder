# Gap Report: test-gen-03

Artifact `rlbench` · generated 2026-10-14 00:29 · 35 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -37.6% | +2.8% | ±0.7% | `max_steps=500` |

## C1: mean_reward (paper 302.05)
**Fits but unsupported** · gap -37.6% → +2.8% · 12 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0006`, `B0014`, `B0015`, `B0016` (4 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `500`
- Command:

  Replay: fork checkpoint `dd0c20f0-bdef-4d0f-ba05-580eebfed14e` and run
  ```
  RUN_TAG=96bd92eafd0a "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 500 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 214.6, 288.6, 332.5, 388.4; gap after +2.8%; result checkpoint `8f11cd87-9a80-4eaf-a0f4-a444d2c3d67a`
- Effect: candidate 310.6 minus naive 188.4 = +122.2, 95% bootstrap interval [+97.53, +201.8] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 302.1 steps, and that its worst seed still balances for 48.2.

- p. 1; value used: `mean_reward` = 302.05 steps (headline claim)

### What did we measure?
- Naive median 188.4 over 5 runs; repeats: 195.4, 187.4, 188.8, 188.4, 182.1
- Spread: range 182.1 to 195.4, noise band ±2.07 (2 x MAD), CV 2.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -37.6% (noise band ±0.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -37.6% (it comes back)
- PASS · Held-out claim: C2: +189.6% to +2.3% (not worse beyond noise)
- FAIL · Evidence: `max_steps=500`: no evidence mentions '500'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +122.2 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=1000` (1.87 noise units, gap -36.3%)
- Near alternatives (closest across all claims):
  - `max_steps=1000`: this claim -18.6%, mean |gap| 9.9% (4 runs)
  - `max_steps=2000`: this claim +53.3%, mean |gap| 45.8% (4 runs)
  - `max_steps=100`: this claim -67.8%, mean |gap| 66.9% (4 runs)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=500` | 4 | +2.8% | +2.3% | 2.6% |
| `max_steps=1000` | 4 | -18.6% | +1.1% | 9.9% |
| `max_steps=2000` | 4 | +53.3% | +38.2% | 45.8% |
| `max_steps=100` | 4 | -67.8% | +66.0% | 66.9% |
| `max_steps=20` | 4 | -93.4% | -58.5% | 76.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`

## Provenance
- GapFinder commit: `037cdf1603d6771de8f0101af7838abc1a610293` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `fedcbdf1b57461a1273eeb81ccb09c30931e58de34a306249ffd0422bbf51ae6`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
