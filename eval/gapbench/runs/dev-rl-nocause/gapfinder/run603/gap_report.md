# Gap Report: dev-rl-nocause

Artifact `rlbench` · generated 2026-10-14 22:25 · 131 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +48.9% | +16.8% | ±27.6% | `lr_schedule=inv`, `eps_end=0.1` |

## C1: mean_reward (paper 118.924)
**Fits but unsupported** · gap +48.9% → +16.8% · 53 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0087`, `B0116`, `B0117`, `B0118`, `B0119` (5 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `inv`
- Config: `eps_end` naive `0.05`, changed to `0.1`
- Command:

  Replay: fork checkpoint `44ffdd4f-8fc7-4f4a-903d-2cee73a4922f` and run
  ```
  RUN_TAG=6bd7dc5924d1 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_start 1.0 --eps_end 0.1 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 140.6, 138.9, 132.9, 139, 110; gap after +16.8%; result checkpoint `06453390-7947-4e18-b522-a095df525268`
- Effect: candidate 138.9 minus naive 177.1 = -38.22, 95% bootstrap interval [-66.12, -17.25] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner is stable across seeds on CartPole: its worst seed still balances for 69.1 steps on average.

- p. 1; value used: `mean_reward` = 118.924 steps (headline claim)

### What did we measure?
- Naive median 177.1 over 5 runs; repeats: 177.1, 187.3, 193.6, 148.8, 159.2
- Spread: range 148.8 to 193.6, noise band ±32.84 (2 x MAD), CV 10.9%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +48.9% (noise band ±27.6% of the paper value)

### Why do we believe it?
- FAIL · Counterfactual (reversal test): without `lr_schedule` the gap is +39.0% (it did NOT come back)
- FAIL · Counterfactual (reversal test): without `eps_end` the gap is +21.0% (it did NOT come back)
- PASS · Held-out claim: C2: -26.9% to -60.4% (not worse beyond noise)
- FAIL · Evidence: `lr_schedule=inv`: no evidence mentions 'inv'; it fits, but nothing says the authors used it
- FAIL · Evidence: `eps_end=0.1`: no evidence mentions '0.1'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -38.22 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `theta_bins=1` (1.66 noise units, gap -3.1%)
- Near alternatives (closest across all claims):
  - `theta_bins=3`: this claim +46.0%, mean |gap| 25.4% (6 runs)
  - `lr_schedule=inv`: this claim +21.0%, mean |gap| 32.5% (5 runs)
  - `lr_schedule=inv`, `eps_end=0.005`: this claim +1.6%, mean |gap| 33.3% (5 runs)

### Equally good configurations
The target claim can't tell these 5 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `eps_end=0.1, lr_schedule=inv` (reported)
- `eps_end=0.005, lr_schedule=inv`
- `eps_end=0.0, theta_bins=1`
- `lr_schedule=inv, theta_bins=8`
- `eps_end=0.005, theta_bins=1`

### History matching (every measured configuration, all claims together)
- 41 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `eps_end, lr_schedule`: eps_end=0.1, lr_schedule=inv (max I 0.99); eps_end=0.005, lr_schedule=inv (max I 1.06); eps_end=0.0, lr_schedule=inv (max I 1.42); eps_end=0.005, lr_schedule=linear (max I 1.63)
  - `lr_schedule, theta_bins`: lr_schedule=inv, theta_bins=8 (max I 1.07)
  - `lr_schedule`: lr_schedule=inv (max I 1.34); lr_schedule=linear (max I 1.44)
  - `eps_end, theta_bins`: eps_end=0.81, theta_bins=1 (max I 1.38); eps_end=0.005, theta_bins=1 (max I 1.38); eps_end=0.0, theta_bins=1 (max I 1.39)
- Equally good values: `lr_schedule` in {inv, linear}; `eps_end` in {0.0, 0.005, 0.1, 0.81}

Notes:
- configurations the target claim can't tell apart from the answer: eps_end=0.1, lr_schedule=inv; eps_end=0.005, lr_schedule=inv; eps_end=0.0, theta_bins=1; lr_schedule=inv, theta_bins=8; eps_end=0.005, theta_bins=1
- equally good values within one noise band (measured): lr_schedule in {inv, linear}; eps_end in {0.0, 0.005, 0.1, 0.81}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `theta_bins=3` | 6 | +46.0% | -4.9% | 25.4% |
| `lr_schedule=inv` | 5 | +21.0% | -44.0% | 32.5% |
| `lr_schedule=inv`, `eps_end=0.005` | 5 | +1.6% | -64.9% | 33.3% |
| `theta_bins=8` | 6 | +47.4% | -27.0% | 37.2% |
| naive (reproduction as run) | 5 | +48.9% | -26.9% | 37.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `e0f13d101585ad1609a15fbf67b70128f4cfffc8` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
