# Gap Report: dev-rl-nocause

Artifact `rlbench` · generated 2026-10-15 19:34 · 185 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +54.5% | +16.0% | ±23.1% | `theta_bins=3`, `eps_end=0.1` |

## C1: mean_reward (paper 118.924)
**Fits but unsupported** · gap +54.5% → +16.0% · 65 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0108`, `B0134`, `B0158`, `B0159`, `B0160` (5 run(s) of the same config)
- Config: `theta_bins` naive `6`, changed to `3`
- Config: `eps_end` naive `0.05`, changed to `0.1`
- Command:

  Replay: fork checkpoint `baae0fce-ee83-4a9c-857d-fbd5d551643a` and run
  ```
  RUN_TAG=0689b110b859 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.1 --eps_decay 0.99 --theta_bins 3 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 86.48, 123.7, 153.2, 137.9, 140.2; gap after +16.0%; result checkpoint `06cc72a0-7776-4ac7-9983-fc4f5f7522c1`
- Effect: candidate 137.9 minus naive 183.8 = -45.86, 95% bootstrap interval [-90.59, -18.09] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner is stable across seeds on CartPole: its worst seed still balances for 69.1 steps on average.

- p. 1; value used: `mean_reward` = 118.924 steps (headline claim)

### What did we measure?
- Naive median 183.8 over 5 runs; repeats: 183.8, 166.3, 197.5, 197.1, 150
- Spread: range 150 to 197.5, noise band ±27.43 (2 x MAD), CV 11.5%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +54.5% (noise band ±23.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `theta_bins` the gap is +49.0% (it comes back)
- PASS · Counterfactual (reversal test): without `eps_end` the gap is +55.4% (it comes back)
- PASS · Held-out claim: C2: +1.3% to -73.6% (not worse beyond noise)
- FAIL · Evidence: `theta_bins=3`: no evidence mentions '3'; it fits, but nothing says the authors used it
- FAIL · Evidence: `eps_end=0.1`: no evidence mentions '0.1'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -45.86 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `theta_bins=1` (1.62 noise units, gap -17.2%); `theta_bins=12` (1.28 noise units, gap +25.1%); `eps_end=0.005` (1.08 noise units, gap +29.6%)
- Near alternatives (closest across all claims):
  - `theta_bins=12`, `lr_schedule=linear`: this claim +20.3%, mean |gap| 28.6% (5 runs)
  - `theta_bins=3`: this claim +55.4%, mean |gap| 33.8% (6 runs)
  - `lr_schedule=inv`, `eps_end=0.005`: this claim +6.8%, mean |gap| 36.2% (5 runs)

### Equally good configurations
The target claim can't tell these 10 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `eps_end=0.1, theta_bins=3` (reported)
- `eps_end=0.001, theta_bins=30`
- `eps_end=0.01, theta_bins=1`
- `eps_end=0.0, theta_bins=30`
- `eps_end=0.005, theta_bins=1`
- `eps_end=0.005, theta_bins=30`
- `eps_end=0.005, lr_schedule=inv`
- `eps_end=0.025, theta_bins=30`
- `eps_end=0.001, theta_bins=1`
- `eps_end=0.1, theta_bins=30`

### History matching (every measured configuration, all claims together)
- 52 of 65 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `eps_end, theta_bins`: eps_end=0.001, theta_bins=30 (max I 0.88); eps_end=0.0, theta_bins=30 (max I 0.91); eps_end=0.1, theta_bins=3 (max I 0.96); eps_end=0.025, theta_bins=30 (max I 0.97); +5 more
  - `eps_end, lr_schedule`: eps_end=0.005, lr_schedule=inv (max I 1)
- Equally good values: `theta_bins` in {3, 30}; `eps_end` in {0.1, 0.81}

Notes:
- configurations the target claim can't tell apart from the answer: eps_end=0.1, theta_bins=3; eps_end=0.001, theta_bins=30; eps_end=0.01, theta_bins=1; eps_end=0.0, theta_bins=30; eps_end=0.005, theta_bins=1; eps_end=0.005, theta_bins=30; eps_end=0.005, lr_schedule=inv; eps_end=0.025, theta_bins=30; eps_end=0.001, theta_bins=1; eps_end=0.1, theta_bins=30
- equally good values within one noise band (measured): theta_bins in {3, 30}; eps_end in {0.1, 0.81}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| naive (reproduction as run) | 5 | +54.5% | +1.3% | 27.9% |
| `theta_bins=12`, `lr_schedule=linear` | 5 | +20.3% | -36.9% | 28.6% |
| `theta_bins=3` | 6 | +55.4% | +12.3% | 33.8% |
| `lr_schedule=inv`, `eps_end=0.005` | 5 | +6.8% | -65.7% | 36.2% |
| `eps_end=0.1`, `lr_schedule=inv` | 5 | +19.2% | -55.5% | 37.4% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
