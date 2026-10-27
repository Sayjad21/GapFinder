# Gap Report: dev-rl-nocause

Artifact `rlbench` · generated 2026-10-15 20:51 · 137 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +47.3% | +15.7% | ±8.6% | `lr_schedule=inv` |

## C1: mean_reward (paper 118.924)
**Fits but unsupported** · gap +47.3% → +15.7% · 53 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0015`, `B0035`, `B0036`, `B0056`, `B0057`, `B0058` (6 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `inv`
- Command:

  Replay: fork checkpoint `1ffa9a4a-fdbf-4fc5-94e5-49744f8cc5e5` and run
  ```
  RUN_TAG=02ee47b57d27 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 162.3, 135, 161, 124.6, 140.3, 130.3; gap after +15.7%; result checkpoint `140e2b71-64b9-4c26-aaef-cd8589a5ffd0`
- Effect: candidate 137.6 minus naive 175.2 = -37.57, 95% bootstrap interval [-61.45, -20.5] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner is stable across seeds on CartPole: its worst seed still balances for 69.1 steps on average.

- p. 1; value used: `mean_reward` = 118.924 steps (headline claim)

### What did we measure?
- Naive median 175.2 over 5 runs; repeats: 191.1, 192.5, 170.2, 175.2, 170.1
- Spread: range 170.1 to 192.5, noise band ±10.26 (2 x MAD), CV 6.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +47.3% (noise band ±8.6% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is +47.3% (it comes back)
- PASS · Held-out claim: C2: +62.8% to -48.6% (not worse beyond noise)
- FAIL · Evidence: `lr_schedule=inv`: no evidence mentions 'inv'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -37.57 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `theta_bins=30` (4.51 noise units, gap -8.4%)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`, `eps_end=0.525`: this claim +30.1%, mean |gap| 21.7% (5 runs)
  - `lr_schedule=linear`, `theta_bins=12`: this claim +23.2%, mean |gap| 22.8% (5 runs)
  - `theta_bins=3`: this claim +50.5%, mean |gap| 28.0% (6 runs)

### Equally good configurations
The target claim can't tell these 5 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `lr_schedule=inv` (reported)
- `theta_bins=30`
- `theta_bins=1`
- `lr_schedule=inv, theta_bins=12`
- `lr_schedule=linear, theta_bins=12`

### History matching (every measured configuration, all claims together)
- 4 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 4 configurations
  - `theta_bins`: theta_bins=30 (max I 2.31)
  - `lr_schedule, theta_bins`: lr_schedule=inv, theta_bins=12 (max I 2.47); lr_schedule=linear, theta_bins=12 (max I 2.52)
  - `lr_schedule`: lr_schedule=inv (max I 2.55)
- 2 separate islands (no single-knob move joins them): lr_schedule=inv, theta_bins=12; lr_schedule=linear, theta_bins=12; lr_schedule=inv | theta_bins=30

Notes:
- configurations the target claim can't tell apart from the answer: lr_schedule=inv; theta_bins=30; theta_bins=1; lr_schedule=inv, theta_bins=12; lr_schedule=linear, theta_bins=12

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv`, `eps_end=0.525` | 5 | +30.1% | +13.2% | 21.7% |
| `lr_schedule=linear`, `theta_bins=12` | 5 | +23.2% | -22.4% | 22.8% |
| `theta_bins=3` | 6 | +50.5% | -5.4% | 28.0% |
| `lr_schedule=inv` | 6 | +15.7% | -48.6% | 32.1% |
| `theta_bins=4`, `lr_schedule=inv` | 5 | +27.9% | -52.0% | 40.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `cd8c8af2b9d079dd9a57443ed501c0dd8a467d34` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
