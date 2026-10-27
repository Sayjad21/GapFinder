# Gap Report: dev-rl-nocause

Artifact `rlbench` · generated 2026-10-15 19:33 · 147 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +46.9% | +10.0% | ±13.8% | `lr_schedule=inv` |

## C1: mean_reward (paper 118.924)
**Fits but unsupported** · gap +46.9% → +10.0% · 53 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0026`, `B0047`, `B0048`, `B0049`, `B0050`, `B0051` (6 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `inv`
- Command:

  Replay: fork checkpoint `48d3eeb7-e434-48d9-9b11-28bdf795d5aa` and run
  ```
  RUN_TAG=4aa993763a8a "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 157.3, 120.3, 157, 131.2, 130.4, 126.7; gap after +10.0%; result checkpoint `18d5b3cb-15ac-418d-9c95-18b407ab9050`
- Effect: candidate 130.8 minus naive 174.7 = -43.87, 95% bootstrap interval [-56.87, -6.249] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner is stable across seeds on CartPole: its worst seed still balances for 69.1 steps on average.

- p. 1; value used: `mean_reward` = 118.924 steps (headline claim)

### What did we measure?
- Naive median 174.7 over 5 runs; repeats: 174.7, 181.8, 155.6, 182.9, 140.3
- Spread: range 140.3 to 182.9, noise band ±16.36 (2 x MAD), CV 11.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +46.9% (noise band ±13.8% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is +46.9% (it comes back)
- PASS · Held-out claim: C2: -23.0% to -43.4% (not worse beyond noise)
- FAIL · Evidence: `lr_schedule=inv`: no evidence mentions 'inv'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -43.87 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `theta_bins=30` (2.99 noise units, gap -5.7%); `lr_schedule=linear` (1 noise units, gap +33.1%)
- Near alternatives (closest across all claims):
  - `eps_end=0.1`, `lr_schedule=inv`: this claim +28.8%, mean |gap| 21.1% (2 runs)
  - `theta_bins=12`: this claim +41.5%, mean |gap| 31.1% (6 runs)
  - `theta_bins=8`: this claim +50.5%, mean |gap| 36.4% (6 runs)

### History matching (every measured configuration, all claims together)
- 15 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr_schedule`: lr_schedule=inv (max I 1.64)
  - `eps_end, theta_bins`: eps_end=0.905, theta_bins=1 (max I 2.01); eps_end=0.981, theta_bins=1 (max I 2.14); eps_end=0.981, theta_bins=3 (max I 2.19); eps_end=0.905, theta_bins=3 (max I 2.36); +1 more
  - `eps_end, lr_schedule`: eps_end=0.1, lr_schedule=inv (max I 2.03)
  - `eps_end`: eps_end=0.1 (max I 2.39)
  - `lr_schedule, theta_bins`: lr_schedule=inv, theta_bins=12 (max I 2.55); lr_schedule=inv, theta_bins=1 (max I 2.56)
- 2 separate islands (no single-knob move joins them): lr_schedule=inv; eps_end=0.905, theta_bins=1; eps_end=0.1, lr_schedule=inv | lr_schedule=linear, theta_bins=30

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `eps_end=0.1`, `lr_schedule=inv` | 2 | +28.8% | +13.5% | 21.1% |
| `lr_schedule=inv` | 6 | +10.0% | -43.4% | 26.7% |
| `theta_bins=12` | 6 | +41.5% | -20.8% | 31.1% |
| naive (reproduction as run) | 5 | +46.9% | -23.0% | 34.9% |
| `theta_bins=8` | 6 | +50.5% | +22.3% | 36.4% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
