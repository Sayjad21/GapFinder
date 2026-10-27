# Gap Report: dev-rl-nocause

Artifact `rlbench` · generated 2026-10-15 19:35 · 184 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +61.6% | +12.0% | ±9.5% | `lr_schedule=inv` |

## C1: mean_reward (paper 118.924)
**Fits but unsupported** · gap +61.6% → +12.0% · 53 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0026`, `B0057`, `B0058`, `B0059`, `B0060`, `B0061` (6 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `inv`
- Command:

  Replay: fork checkpoint `23817c2c-b7d5-44cd-aebb-01da9fe856d0` and run
  ```
  RUN_TAG=9f8b289eb6dd "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 114, 120.8, 159.4, 145.7, 148, 113.1; gap after +12.0%; result checkpoint `b6187541-7f59-4e4b-ab5d-fb1191156cd1`
- Effect: candidate 133.2 minus naive 192.2 = -59, 95% bootstrap interval [-74.59, -15.09] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner is stable across seeds on CartPole: its worst seed still balances for 69.1 steps on average.

- p. 1; value used: `mean_reward` = 118.924 steps (headline claim)

### What did we measure?
- Naive median 192.2 over 5 runs; repeats: 165.1, 192.2, 195.3, 158, 197.9
- Spread: range 158 to 197.9, noise band ±11.32 (2 x MAD), CV 10.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +61.6% (noise band ±9.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is +61.6% (it comes back)
- PASS · Held-out claim: C2: +149.1% to -36.7% (not worse beyond noise)
- FAIL · Evidence: `lr_schedule=inv`: no evidence mentions 'inv'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -59 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `theta_bins=30` (5.6 noise units, gap -8.4%); `theta_bins=1` (3.32 noise units, gap -30.1%); `lr_schedule=linear` (2.99 noise units, gap +33.2%); `eps_end=0.1` (2.18 noise units, gap +40.9%); `theta_bins=8` (1.52 noise units, gap +47.2%) (and 6 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`: this claim +36.8%, mean |gap| 19.7% (6 runs)
  - `lr_schedule=inv`, `theta_bins=8`: this claim +11.7%, mean |gap| 23.7% (5 runs)
  - `theta_bins=12`, `lr_schedule=linear`: this claim +29.4%, mean |gap| 25.3% (5 runs)

### Equally good configurations
The target claim can't tell these 10 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `lr_schedule=inv` (reported)
- `theta_bins=1`
- `lr_schedule=inv, theta_bins=8`
- `lr_schedule=inv, theta_bins=12`
- `eps_end=0.025, lr_schedule=inv`
- `eps_end=0.905, theta_bins=1`
- `eps_end=0.025, theta_bins=1`
- `eps_end=0.81, theta_bins=1`
- `eps_end=0.1, lr_schedule=inv`
- `eps_end=0.025, theta_bins=30`

### History matching (every measured configuration, all claims together)
- 21 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr_schedule, theta_bins`: lr_schedule=inv, theta_bins=8 (max I 0.32); lr_schedule=inv, theta_bins=12 (max I 0.99)
  - `lr_schedule`: lr_schedule=inv (max I 1.12)
  - `eps_end, theta_bins`: eps_end=0.1, theta_bins=30 (max I 1.19); eps_end=0.025, theta_bins=1 (max I 1.19); eps_end=0.025, theta_bins=30 (max I 1.22); eps_end=0.905, theta_bins=1 (max I 1.44)
  - `eps_end, lr_schedule`: eps_end=0.025, lr_schedule=inv (max I 1.21); eps_end=0.1, lr_schedule=inv (max I 1.71)
  - `theta_bins`: theta_bins=30 (max I 1.51)

Notes:
- configurations the target claim can't tell apart from the answer: lr_schedule=inv; theta_bins=1; lr_schedule=inv, theta_bins=8; lr_schedule=inv, theta_bins=12; eps_end=0.025, lr_schedule=inv; eps_end=0.905, theta_bins=1; eps_end=0.025, theta_bins=1; eps_end=0.81, theta_bins=1; eps_end=0.1, lr_schedule=inv; eps_end=0.025, theta_bins=30

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=linear` | 6 | +36.8% | -2.5% | 19.7% |
| `lr_schedule=inv`, `theta_bins=8` | 5 | +11.7% | -35.7% | 23.7% |
| `lr_schedule=inv` | 6 | +12.0% | -36.7% | 24.4% |
| `theta_bins=12`, `lr_schedule=linear` | 5 | +29.4% | -21.3% | 25.3% |
| `eps_end=0.1` | 6 | +45.5% | -11.8% | 28.7% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
