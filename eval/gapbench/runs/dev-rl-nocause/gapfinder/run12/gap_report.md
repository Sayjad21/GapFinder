# Gap Report: dev-rl-nocause

Artifact `rlbench` · generated 2026-10-13 20:56 · 103 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +53.0% | -2.9% | ±7.9% | `theta_bins=1`, `eps_end=0.525` |

## C1: mean_reward (paper 118.924)
**Fits but unsupported** · gap +53.0% → -2.9% · 26 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0062`, `B0076`, `B0077`, `B0078`, `B0079` (5 run(s) of the same config)
- Config: `theta_bins` naive `6`, changed to `1`
- Config: `eps_end` naive `0.05`, changed to `0.525`
- Command:

  Replay: fork checkpoint `17e17a2c-5232-4b0e-bdf7-1983f637a488` and run
  ```
  RUN_TAG=3176ea4aa6ab "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.525 --eps_decay 0.99 --theta_bins 1 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 115.5, 100.6, 97.66, 116.8, 147.6; gap after -2.9%; result checkpoint `d54df588-f367-4989-8067-eba6df401308`
- Effect: candidate 115.5 minus naive 182 = -66.54, 95% bootstrap interval [-86.35, -38.89] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner is stable across seeds on CartPole: its worst seed still balances for 69.1 steps on average.

- p. 1; value used: `mean_reward` = 118.924 steps (headline claim)

### What did we measure?
- Naive median 182 over 5 runs; repeats: 162.6, 195.3, 177.3, 182, 185.4
- Spread: range 162.6 to 195.3, noise band ±9.41 (2 x MAD), CV 6.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +53.0% (noise band ±7.9% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `theta_bins` the gap is +46.2% (it comes back)
- PASS · Counterfactual (reversal test): without `eps_end` the gap is -37.9% (it comes back)
- PASS · Held-out claim: C2: -21.9% to -76.6% (not worse beyond noise)
- FAIL · Evidence: `theta_bins=1`: no evidence mentions '1'; it fits, but nothing says the authors used it
- FAIL · Evidence: `eps_end=0.525`: no evidence mentions '0.525'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -66.54 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `theta_bins=3` (3.76 noise units, gap +23.3%); `lr_schedule=inv` (2.59 noise units, gap +32.6%); `theta_bins=12` (2 noise units, gap +37.2%); `lr_schedule=linear` (1.58 noise units, gap +40.5%); `theta_bins=8` (1.56 noise units, gap +40.7%)
- Near alternatives (closest across all claims):
  - `eps_end=0.525`, `lr_schedule=inv`: this claim +28.8%, mean |gap| 15.7% (5 runs)
  - `theta_bins=12`: this claim +38.8%, mean |gap| 21.3% (6 runs)
  - `lr_schedule=inv`: this claim +20.2%, mean |gap| 28.2% (6 runs)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `eps_end=0.525`, `lr_schedule=inv` | 5 | +28.8% | -2.6% | 15.7% |
| `theta_bins=12` | 6 | +38.8% | -3.8% | 21.3% |
| `lr_schedule=inv` | 6 | +20.2% | -36.2% | 28.2% |
| naive (reproduction as run) | 5 | +53.0% | -21.9% | 37.5% |
| `lr_schedule=linear` | 6 | +38.8% | +37.0% | 37.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `c5b1a93e0b25688f10e132758f8a6371b4ebbf19` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `7e8e15007902d4b39f8940e3fb2a13a0e258c9d87b46215a72cd3b65ed9d57d9`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
