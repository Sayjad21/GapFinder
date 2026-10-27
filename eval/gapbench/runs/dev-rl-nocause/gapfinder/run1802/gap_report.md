# Gap Report: dev-rl-nocause

Artifact `rlbench` · generated 2026-10-15 19:35 · 125 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +51.9% | -6.5% | ±8.0% | `theta_bins=30` |

## C1: mean_reward (paper 118.924)
**Fits but unsupported** · gap +51.9% → -6.5% · 53 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0012`, `B0039`, `B0040`, `B0054` (4 run(s) of the same config)
- Config: `theta_bins` naive `6`, changed to `30`
- Command:

  Replay: fork checkpoint `3856686e-211f-48ab-b2dc-e445d2967088` and run
  ```
  RUN_TAG=f8c43bb5fe1b "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 30 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 112.9, 109.4, 98.8, 131.7; gap after -6.5%; result checkpoint `bb323e0b-32a2-478d-b43c-598e28e36e3e`
- Effect: candidate 111.2 minus naive 180.6 = -69.47, 95% bootstrap interval [-88.21, -43.96] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner is stable across seeds on CartPole: its worst seed still balances for 69.1 steps on average.

- p. 1; value used: `mean_reward` = 118.924 steps (headline claim)

### What did we measure?
- Naive median 180.6 over 5 runs; repeats: 185.4, 190, 169.5, 180.6, 179.8
- Spread: range 169.5 to 190, noise band ±9.49 (2 x MAD), CV 4.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +51.9% (noise band ±8.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `theta_bins` the gap is +51.9% (it comes back)
- PASS · Held-out claim: C2: +31.8% to -71.3% (not worse beyond noise)
- FAIL · Evidence: `theta_bins=30`: no evidence mentions '30'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -69.47 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `theta_bins=1` (2.48 noise units, gap -32.1%); `lr_schedule=inv` (2.2 noise units, gap +34.3%); `theta_bins=8` (2 noise units, gap +35.9%); `eps_end=0.005` (1.29 noise units, gap +41.6%); `eps_end=0.905` (1.08 noise units, gap +43.3%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`, `eps_end=0.001`: this claim +8.6%, mean |gap| 11.8% (3 runs)
  - `lr_schedule=linear`, `theta_bins=8`: this claim +30.2%, mean |gap| 17.2% (3 runs)
  - `lr_schedule=inv`: this claim +16.0%, mean |gap| 30.2% (4 runs)

### Equally good configurations
The target claim can't tell these 7 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `theta_bins=30` (reported)
- `lr_schedule=inv`
- `lr_schedule=inv, theta_bins=8`
- `eps_end=0.005, lr_schedule=inv`
- `eps_end=0.001, theta_bins=30`
- `eps_end=0.905, theta_bins=1`
- `eps_end=0.005, theta_bins=30`

### History matching (every measured configuration, all claims together)
- 8 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 8 configurations
  - `lr_schedule, theta_bins`: lr_schedule=inv, theta_bins=8 (max I 0.72); lr_schedule=inv, theta_bins=4 (max I 1.05)
  - `eps_end, theta_bins`: eps_end=0.001, theta_bins=30 (max I 0.79); eps_end=0.905, theta_bins=1 (max I 2.33)
  - `theta_bins`: theta_bins=30 (max I 1.24)
  - `eps_end, lr_schedule`: eps_end=0.005, lr_schedule=inv (max I 1.3); eps_end=0.001, lr_schedule=inv (max I 1.77)
  - `lr_schedule`: lr_schedule=inv (max I 2.45)
- 3 separate islands (no single-knob move joins them): lr_schedule=inv, theta_bins=8; lr_schedule=inv, theta_bins=4; eps_end=0.005, lr_schedule=inv | eps_end=0.001, theta_bins=30; theta_bins=30 | eps_end=0.905, theta_bins=1

Notes:
- configurations the target claim can't tell apart from the answer: theta_bins=30; lr_schedule=inv; lr_schedule=inv, theta_bins=8; eps_end=0.005, lr_schedule=inv; eps_end=0.001, theta_bins=30; eps_end=0.905, theta_bins=1; eps_end=0.005, theta_bins=30

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv`, `eps_end=0.001` | 3 | +8.6% | -15.1% | 11.8% |
| `lr_schedule=linear`, `theta_bins=8` | 3 | +30.2% | +4.3% | 17.2% |
| `lr_schedule=inv` | 4 | +16.0% | -44.5% | 30.2% |
| `theta_bins=3` | 4 | +48.5% | -12.1% | 30.3% |
| `lr_schedule=inv`, `theta_bins=8` | 3 | +2.3% | -63.1% | 32.7% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
