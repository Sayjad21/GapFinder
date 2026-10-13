# Gap Report: dev-rl-nocause

Artifact `rlbench` · generated 2026-10-14 00:49 · 144 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +48.3% | -3.9% | ±11.5% | `theta_bins=1`, `eps_end=0.025` |

## C1: mean_reward (paper 118.924)
**Fits but unsupported** · gap +48.3% → -3.9% · 46 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0078`, `B0125`, `B0126`, `B0127`, `B0128` (5 run(s) of the same config)
- Config: `theta_bins` naive `6`, changed to `1`
- Config: `eps_end` naive `0.05`, changed to `0.025`
- Command:

  Replay: fork checkpoint `2eba7111-feef-4be1-a78b-9711a340e245` and run
  ```
  RUN_TAG=3bcbc929218b "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.025 --eps_decay 0.99 --theta_bins 1 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 134.3, 114.3, 65.66, 81.39, 114.6; gap after -3.9%; result checkpoint `67504dc7-c034-498d-841f-a3bedc144bba`
- Effect: candidate 114.3 minus naive 176.4 = -62.07, 95% bootstrap interval [-115, -47.06] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner is stable across seeds on CartPole: its worst seed still balances for 69.1 steps on average.

- p. 1; value used: `mean_reward` = 118.924 steps (headline claim)

### What did we measure?
- Naive median 176.4 over 5 runs; repeats: 195.9, 195, 169.6, 176.4, 173.1
- Spread: range 169.6 to 195.9, noise band ±13.67 (2 x MAD), CV 6.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +48.3% (noise band ±11.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `theta_bins` the gap is +52.6% (it comes back)
- PASS · Counterfactual (reversal test): without `eps_end` the gap is -30.7% (it comes back)
- PASS · Held-out claim: C2: +15.0% to -76.5% (not worse beyond noise)
- FAIL · Evidence: `theta_bins=1`: no evidence mentions '1'; it fits, but nothing says the authors used it
- FAIL · Evidence: `eps_end=0.025`: no evidence mentions '0.025'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -62.07 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (3.16 noise units, gap +12.0%); `eps_end=0.1` (1.56 noise units, gap +30.4%); `eps_end=0.01` (1.06 noise units, gap +36.2%)
- Near alternatives (closest across all claims):
  - `eps_end=0.905`, `theta_bins=60`: this claim +9.2%, mean |gap| 12.6% (5 runs)
  - `lr_schedule=inv`, `eps_end=0.1`: this claim +11.9%, mean |gap| 17.6% (5 runs)
  - `eps_end=0.01`, `lr_schedule=inv`: this claim +21.1%, mean |gap| 26.7% (5 runs)

### History matching (every measured configuration, all claims together)
- 12 of 46 tested configurations fit every claim within 3 sigma
- Equally good values: `eps_end` in {0.01, 0.025, 0.905}

Notes:
- equally good values within one noise band (measured): eps_end in {0.01, 0.025, 0.905}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `eps_end=0.905`, `theta_bins=60` | 5 | +9.2% | +16.1% | 12.6% |
| `lr_schedule=inv`, `eps_end=0.1` | 5 | +11.9% | -23.3% | 17.6% |
| `eps_end=0.01`, `lr_schedule=inv` | 5 | +21.1% | -32.3% | 26.7% |
| `lr_schedule=inv`, `theta_bins=4` | 5 | +22.8% | -33.0% | 27.9% |
| `lr_schedule=inv`, `eps_end=0.025` | 5 | +19.7% | -39.3% | 29.5% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `ee5bfaf3f91999664f6df4e7df12a48c78c40f73` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `fedcbdf1b57461a1273eeb81ccb09c30931e58de34a306249ffd0422bbf51ae6`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
