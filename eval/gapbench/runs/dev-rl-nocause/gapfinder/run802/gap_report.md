# Gap Report: dev-rl-nocause

Artifact `rlbench` · generated 2026-10-14 23:22 · 168 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +50.9% | -0.4% | ±14.8% | `theta_bins=30` |

## C1: mean_reward (paper 118.924)
**Fits but unsupported** · gap +50.9% → -0.4% · 53 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0012`, `B0039`, `B0040`, `B0047`, `B0048`, `B0049` (6 run(s) of the same config)
- Config: `theta_bins` naive `6`, changed to `30`
- Command:

  Replay: fork checkpoint `5793bdf9-c3d8-46d0-828b-a5a410d9ae65` and run
  ```
  RUN_TAG=6b6966ec84b8 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 30 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 128.6, 87.53, 122.2, 140, 114.7, 103.6; gap after -0.4%; result checkpoint `b757d7ee-f99e-4199-907b-ad8ac6fd3fa9`
- Effect: candidate 118.5 minus naive 179.5 = -61.01, 95% bootstrap interval [-91.65, -44.16] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner is stable across seeds on CartPole: its worst seed still balances for 69.1 steps on average.

- p. 1; value used: `mean_reward` = 118.924 steps (headline claim)

### What did we measure?
- Naive median 179.5 over 5 runs; repeats: 170.7, 179.5, 189.7, 172.2, 192.2
- Spread: range 170.7 to 192.2, noise band ±17.55 (2 x MAD), CV 5.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +50.9% (noise band ±14.8% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `theta_bins` the gap is +50.9% (it comes back)
- PASS · Held-out claim: C2: +12.8% to -66.5% (not worse beyond noise)
- FAIL · Evidence: `theta_bins=30`: no evidence mentions '30'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -61.01 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (1.7 noise units, gap +25.8%)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`, `eps_end=0.1`: this claim +15.8%, mean |gap| 18.5% (5 runs)
  - `eps_end=0.525`, `theta_bins=60`: this claim +2.8%, mean |gap| 22.9% (5 runs)
  - `lr_schedule=inv`, `eps_end=0.525`: this claim +31.3%, mean |gap| 23.3% (5 runs)

### Equally good configurations
The target claim can't tell these 8 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `theta_bins=30` (reported)
- `lr_schedule=inv, theta_bins=8`
- `eps_end=0.525, theta_bins=60`
- `eps_end=0.1, theta_bins=30`
- `eps_end=0.025, theta_bins=1`
- `eps_end=0.1, theta_bins=1`
- `eps_end=0.81, theta_bins=1`
- `eps_end=0.1, lr_schedule=inv`

### History matching (every measured configuration, all claims together)
- 10 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `eps_end, theta_bins`: eps_end=0.525, theta_bins=60 (max I 0.89); eps_end=0.1, theta_bins=30 (max I 1.38); eps_end=0.025, theta_bins=1 (max I 1.57); eps_end=0.1, theta_bins=1 (max I 1.96); +2 more
  - `lr_schedule, theta_bins`: lr_schedule=inv, theta_bins=8 (max I 0.95)
  - `theta_bins`: theta_bins=30 (max I 1.37)
  - `eps_end, lr_schedule`: eps_end=0.1, lr_schedule=inv (max I 1.71)
  - `lr_schedule`: lr_schedule=inv (max I 2.95)
- 2 separate islands (no single-knob move joins them): eps_end=0.525, theta_bins=60; theta_bins=30; eps_end=0.1, theta_bins=30 | lr_schedule=inv, theta_bins=8; eps_end=0.1, lr_schedule=inv; lr_schedule=inv

Notes:
- configurations the target claim can't tell apart from the answer: theta_bins=30; lr_schedule=inv, theta_bins=8; eps_end=0.525, theta_bins=60; eps_end=0.1, theta_bins=30; eps_end=0.025, theta_bins=1; eps_end=0.1, theta_bins=1; eps_end=0.81, theta_bins=1; eps_end=0.1, lr_schedule=inv

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv`, `eps_end=0.1` | 5 | +15.8% | -21.2% | 18.5% |
| `eps_end=0.525`, `theta_bins=60` | 5 | +2.8% | -42.9% | 22.9% |
| `lr_schedule=inv`, `eps_end=0.525` | 5 | +31.3% | -15.2% | 23.3% |
| `eps_end=0.81`, `theta_bins=60` | 5 | +18.6% | +32.1% | 25.3% |
| `eps_end=0.025` | 5 | +49.0% | -2.5% | 25.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `efb2f63a257a40b9982099a274f2e882f272b80c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
