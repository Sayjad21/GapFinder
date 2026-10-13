# Gap Report: dev-rl-nocause

Artifact `rlbench` · generated 2026-10-14 00:27 · 107 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +58.1% | -3.7% | ±12.1% | `theta_bins=1`, `eps_end=0.01` |

## C1: mean_reward (paper 118.924)
**Fits but unsupported** · gap +58.1% → -3.7% · 26 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0067`, `B0088`, `B0089`, `B0090`, `B0091` (5 run(s) of the same config)
- Config: `theta_bins` naive `6`, changed to `1`
- Config: `eps_end` naive `0.05`, changed to `0.01`
- Command:

  Replay: fork checkpoint `9eead4f5-219d-4db0-868f-78a3e6ae695c` and run
  ```
  RUN_TAG=e67d6e08a10a "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.01 --eps_decay 0.99 --theta_bins 1 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 98.64, 114.7, 114.5, 99.06, 132.5; gap after -3.7%; result checkpoint `37e6a917-bc4d-4bda-95cf-9f1083b8bf86`
- Effect: candidate 114.5 minus naive 188 = -73.46, 95% bootstrap interval [-91.15, -49.69] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner is stable across seeds on CartPole: its worst seed still balances for 69.1 steps on average.

- p. 1; value used: `mean_reward` = 118.924 steps (headline claim)

### What did we measure?
- Naive median 188 over 5 runs; repeats: 188, 198.4, 195.2, 164.2, 182.3
- Spread: range 164.2 to 198.4, noise band ±14.35 (2 x MAD), CV 7.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +58.1% (noise band ±12.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `theta_bins` the gap is +46.1% (it comes back)
- PASS · Counterfactual (reversal test): without `eps_end` the gap is -31.0% (it comes back)
- PASS · Held-out claim: C2: +111.2% to -76.9% (not worse beyond noise)
- FAIL · Evidence: `theta_bins=1`: no evidence mentions '1'; it fits, but nothing says the authors used it
- FAIL · Evidence: `eps_end=0.01`: no evidence mentions '0.01'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -73.46 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (3.79 noise units, gap +12.4%); `theta_bins=3` (2.33 noise units, gap +30.0%); `lr_schedule=linear` (1.76 noise units, gap +36.8%)
- Near alternatives (closest across all claims):
  - `eps_end=0.01`, `lr_schedule=inv`: this claim +24.0%, mean |gap| 14.5% (5 runs)
  - `eps_end=0.1`, `lr_schedule=inv`: this claim +20.9%, mean |gap| 24.7% (5 runs)
  - `theta_bins=12`: this claim +46.5%, mean |gap| 28.3% (6 runs)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `eps_end=0.01`, `lr_schedule=inv` | 5 | +24.0% | -5.0% | 14.5% |
| `eps_end=0.1`, `lr_schedule=inv` | 5 | +20.9% | -28.6% | 24.7% |
| `theta_bins=12` | 6 | +46.5% | -10.1% | 28.3% |
| `lr_schedule=inv` | 6 | +7.3% | -53.7% | 30.5% |
| `theta_bins=3` | 6 | +41.1% | -38.6% | 39.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `ab5d0e01d517ea012f76706719410d70d422f3f9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `fedcbdf1b57461a1273eeb81ccb09c30931e58de34a306249ffd0422bbf51ae6`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
