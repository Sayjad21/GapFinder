# Gap Report: dev-rl-nocause

Artifact `rlbench` · generated 2026-10-15 19:35 · 168 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +54.3% | +13.9% | ±14.6% | `theta_bins=3`, `eps_end=0.1` |

## C1: mean_reward (paper 118.924)
**Fits but unsupported** · gap +54.3% → +13.9% · 53 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0099`, `B0119`, `B0156`, `B0157`, `B0158` (5 run(s) of the same config)
- Config: `theta_bins` naive `6`, changed to `3`
- Config: `eps_end` naive `0.05`, changed to `0.1`
- Command:

  Replay: fork checkpoint `eece7799-7f77-46d3-b814-dce5c6772301` and run
  ```
  RUN_TAG=8f17874aa5ca "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.1 --eps_decay 0.99 --theta_bins 3 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 135.5, 144.3, 98.7, 142.5, 111.4; gap after +13.9%; result checkpoint `98c1d4b7-0b58-40cc-bd1f-796baada0e8c`
- Effect: candidate 135.5 minus naive 183.4 = -47.97, 95% bootstrap interval [-76.98, -23.94] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner is stable across seeds on CartPole: its worst seed still balances for 69.1 steps on average.

- p. 1; value used: `mean_reward` = 118.924 steps (headline claim)

### What did we measure?
- Naive median 183.4 over 5 runs; repeats: 185.1, 164.3, 183.4, 192.1, 157.4
- Spread: range 157.4 to 192.1, noise band ±17.34 (2 x MAD), CV 8.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +54.3% (noise band ±14.6% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `theta_bins` the gap is +45.0% (it comes back)
- PASS · Counterfactual (reversal test): without `eps_end` the gap is +44.8% (it comes back)
- PASS · Held-out claim: C2: -1.5% to -76.0% (not worse beyond noise)
- FAIL · Evidence: `theta_bins=3`: no evidence mentions '3'; it fits, but nothing says the authors used it
- FAIL · Evidence: `eps_end=0.1`: no evidence mentions '0.1'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -47.97 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (1.58 noise units, gap +31.2%); `lr_schedule=linear` (1.41 noise units, gap +33.7%); `theta_bins=30` (1.29 noise units, gap -35.5%); `eps_end=0.0` (1.04 noise units, gap +39.1%)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`, `theta_bins=3`: this claim +26.7%, mean |gap| 18.1% (2 runs)
  - `eps_end=0.0`, `lr_schedule=linear`: this claim +29.4%, mean |gap| 18.6% (2 runs)
  - `eps_end=0.1`: this claim +45.0%, mean |gap| 24.4% (5 runs)

### Equally good configurations
The target claim can't tell these 10 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `eps_end=0.1, theta_bins=3` (reported)
- `theta_bins=30`
- `lr_schedule=inv`
- `eps_end=0.0, theta_bins=1`
- `eps_end=0.025, lr_schedule=inv`
- `eps_end=0.1, theta_bins=30`
- `eps_end=0.025, theta_bins=1`
- `lr_schedule=inv, theta_bins=12`
- `eps_end=0.1, lr_schedule=inv`
- `lr_schedule=linear, theta_bins=12`

### History matching (every measured configuration, all claims together)
- 19 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `eps_end, lr_schedule`: eps_end=0.025, lr_schedule=inv (max I 0.89); eps_end=0.1, lr_schedule=inv (max I 1.32)
  - `eps_end, theta_bins`: eps_end=0.1, theta_bins=30 (max I 1.21); eps_end=0.1, theta_bins=3 (max I 1.45); eps_end=0.025, theta_bins=1 (max I 1.47); eps_end=0.0, theta_bins=1 (max I 1.49)
  - `lr_schedule, theta_bins`: lr_schedule=inv, theta_bins=12 (max I 1.29); lr_schedule=linear, theta_bins=12 (max I 1.32)
  - `lr_schedule`: lr_schedule=inv (max I 1.77)
  - `theta_bins`: theta_bins=30 (max I 1.9)
- Equally good values: `theta_bins` in {3, 30}

Notes:
- configurations the target claim can't tell apart from the answer: eps_end=0.1, theta_bins=3; theta_bins=30; lr_schedule=inv; eps_end=0.0, theta_bins=1; eps_end=0.025, lr_schedule=inv; eps_end=0.1, theta_bins=30; eps_end=0.025, theta_bins=1; lr_schedule=inv, theta_bins=12; eps_end=0.1, lr_schedule=inv; lr_schedule=linear, theta_bins=12
- equally good values within one noise band (measured): theta_bins in {3, 30}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv`, `theta_bins=3` | 2 | +26.7% | +9.6% | 18.1% |
| `eps_end=0.0`, `lr_schedule=linear` | 2 | +29.4% | +7.8% | 18.6% |
| `eps_end=0.1` | 5 | +45.0% | -3.8% | 24.4% |
| `lr_schedule=inv` | 6 | +16.7% | -33.6% | 25.1% |
| naive (reproduction as run) | 5 | +54.3% | -1.5% | 27.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
