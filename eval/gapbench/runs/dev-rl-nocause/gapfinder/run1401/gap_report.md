# Gap Report: dev-rl-nocause

Artifact `rlbench` · generated 2026-10-15 18:45 · 158 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +53.2% | -1.2% | ±12.4% | `theta_bins=30` |

## C1: mean_reward (paper 118.924)
**Fits but unsupported** · gap +53.2% → -1.2% · 53 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0012`, `B0039`, `B0040`, `B0047`, `B0048`, `B0049` (6 run(s) of the same config)
- Config: `theta_bins` naive `6`, changed to `30`
- Command:

  Replay: fork checkpoint `3daf02bf-a5e5-4435-80c7-2b19f95d75c6` and run
  ```
  RUN_TAG=aa27811cb822 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 30 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 133.3, 111.3, 123.7, 91.28, 95.42, 124; gap after -1.2%; result checkpoint `126d53f1-5cf6-417e-ba5b-ebb42d3c307f`
- Effect: candidate 117.5 minus naive 182.2 = -64.69, 95% bootstrap interval [-95.89, -39.82] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner is stable across seeds on CartPole: its worst seed still balances for 69.1 steps on average.

- p. 1; value used: `mean_reward` = 118.924 steps (headline claim)

### What did we measure?
- Naive median 182.2 over 5 runs; repeats: 197.9, 189.5, 141, 180.6, 182.2
- Spread: range 141 to 197.9, noise band ±14.71 (2 x MAD), CV 12.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +53.2% (noise band ±12.4% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `theta_bins` the gap is +53.2% (it comes back)
- PASS · Held-out claim: C2: -10.8% to -74.4% (not worse beyond noise)
- FAIL · Evidence: `theta_bins=30`: no evidence mentions '30'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -64.69 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (3.6 noise units, gap +8.6%); `theta_bins=1` (2.96 noise units, gap -16.6%); `theta_bins=3` (2.22 noise units, gap +25.7%)
- Near alternatives (closest across all claims):
  - `theta_bins=8`, `lr_schedule=inv`: this claim +2.4%, mean |gap| 14.7% (5 runs)
  - `eps_end=0.1`, `lr_schedule=inv`: this claim +9.6%, mean |gap| 22.9% (5 runs)
  - `theta_bins=12`: this claim +40.4%, mean |gap| 23.6% (6 runs)

### Equally good configurations
The target claim can't tell these 9 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `theta_bins=30` (reported)
- `lr_schedule=inv, theta_bins=8`
- `eps_end=0.001, theta_bins=1`
- `eps_end=0.81, theta_bins=1`
- `eps_end=0.0, theta_bins=30`
- `eps_end=0.1, lr_schedule=inv`
- `eps_end=0.001, lr_schedule=inv`
- `eps_end=0.1, theta_bins=30`
- `eps_end=0.0, theta_bins=1`

### History matching (every measured configuration, all claims together)
- 41 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr_schedule, theta_bins`: lr_schedule=inv, theta_bins=8 (max I 0.56)
  - `eps_end, lr_schedule`: eps_end=0.1, lr_schedule=inv (max I 0.74); eps_end=0.001, lr_schedule=inv (max I 1.24)
  - `lr_schedule`: lr_schedule=inv (max I 1.22)
  - `theta_bins`: theta_bins=30 (max I 1.27)
  - `eps_end, theta_bins`: eps_end=0.0, theta_bins=30 (max I 1.28); eps_end=0.0, theta_bins=1 (max I 1.28); eps_end=0.001, theta_bins=1 (max I 1.28); eps_end=0.81, theta_bins=1 (max I 1.28); +1 more

Notes:
- configurations the target claim can't tell apart from the answer: theta_bins=30; lr_schedule=inv, theta_bins=8; eps_end=0.001, theta_bins=1; eps_end=0.81, theta_bins=1; eps_end=0.0, theta_bins=30; eps_end=0.1, lr_schedule=inv; eps_end=0.001, lr_schedule=inv; eps_end=0.1, theta_bins=30; eps_end=0.0, theta_bins=1

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `theta_bins=8`, `lr_schedule=inv` | 5 | +2.4% | -26.9% | 14.7% |
| `eps_end=0.1`, `lr_schedule=inv` | 5 | +9.6% | -36.2% | 22.9% |
| `theta_bins=12` | 6 | +40.4% | -6.7% | 23.6% |
| `lr_schedule=inv` | 6 | +16.8% | -35.3% | 26.0% |
| `lr_schedule=inv`, `eps_end=0.001` | 5 | +20.3% | -32.7% | 26.5% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
