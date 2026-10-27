# Gap Report: dev-rl-nocause

Artifact `rlbench` · generated 2026-10-16 01:12 · 166 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +56.5% | -19.5% | ±15.8% | `theta_bins=30` |

## C1: mean_reward (paper 118.924)
**Fits but unsupported** · gap +56.5% → -19.5% · 53 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0018`, `B0045`, `B0046`, `B0055`, `B0056`, `B0057` (6 run(s) of the same config)
- Config: `theta_bins` naive `6`, changed to `30`
- Command:

  Replay: fork checkpoint `cc022218-f48a-4e7b-be5d-683b64140752` and run
  ```
  RUN_TAG=42918b1f2fcc "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 30 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 124.3, 148.3, 106.9, 60.05, 84.67, 69.58; gap after -19.5%; result checkpoint `ba116998-439f-4dd8-a23f-0d18e9a473da`
- Effect: candidate 95.78 minus naive 186.1 = -90.31, 95% bootstrap interval [-126, -44.69] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner is stable across seeds on CartPole: its worst seed still balances for 69.1 steps on average.

- p. 1; value used: `mean_reward` = 118.924 steps (headline claim)

### What did we measure?
- Naive median 186.1 over 5 runs; repeats: 161, 186.1, 198.3, 195.5, 181.5
- Spread: range 161 to 198.3, noise band ±18.79 (2 x MAD), CV 8.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +56.5% (noise band ±15.8% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `theta_bins` the gap is +56.5% (it comes back)
- PASS · Held-out claim: C2: +64.8% to -66.3% (not worse beyond noise)
- FAIL · Evidence: `theta_bins=30`: no evidence mentions '30'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -90.31 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (2.9 noise units, gap +10.6%); `theta_bins=1` (2.47 noise units, gap -17.5%); `eps_end=0.025` (1.89 noise units, gap +26.6%); `eps_end=0.1` (1.38 noise units, gap +34.7%); `lr_schedule=linear` (1.28 noise units, gap +36.3%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`, `theta_bins=8`: this claim +13.9%, mean |gap| 9.6% (5 runs)
  - `lr_schedule=inv`: this claim +22.7%, mean |gap| 12.8% (6 runs)
  - `eps_end=0.0`: this claim +40.4%, mean |gap| 22.3% (3 runs)

### Equally good configurations
The target claim can't tell these 9 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `theta_bins=30` (reported)
- `theta_bins=1`
- `eps_end=0.025, lr_schedule=inv`
- `eps_end=0.1, lr_schedule=inv`
- `lr_schedule=inv, theta_bins=8`
- `eps_end=0.1, theta_bins=30`
- `eps_end=0.025, theta_bins=30`
- `lr_schedule=linear, theta_bins=12`
- `lr_schedule=inv, theta_bins=12`

### History matching (every measured configuration, all claims together)
- 18 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `eps_end, lr_schedule`: eps_end=0.1, lr_schedule=inv (max I 0.86); eps_end=0.025, lr_schedule=inv (max I 1.12)
  - `lr_schedule, theta_bins`: lr_schedule=inv, theta_bins=8 (max I 1.21); lr_schedule=linear, theta_bins=12 (max I 1.4); lr_schedule=inv, theta_bins=12 (max I 2.08)
  - `eps_end, theta_bins`: eps_end=0.1, theta_bins=30 (max I 1.28); eps_end=0.025, theta_bins=30 (max I 2.21)
  - `theta_bins`: theta_bins=30 (max I 1.82); theta_bins=1 (max I 2.62)
  - `lr_schedule`: lr_schedule=inv (max I 2.38)
- Equally good values: `theta_bins` in {1, 30}

Notes:
- configurations the target claim can't tell apart from the answer: theta_bins=30; theta_bins=1; eps_end=0.025, lr_schedule=inv; eps_end=0.1, lr_schedule=inv; lr_schedule=inv, theta_bins=8; eps_end=0.1, theta_bins=30; eps_end=0.025, theta_bins=30; lr_schedule=linear, theta_bins=12; lr_schedule=inv, theta_bins=12
- equally good values within one noise band (measured): theta_bins in {1, 30}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv`, `theta_bins=8` | 5 | +13.9% | -5.3% | 9.6% |
| `lr_schedule=inv` | 6 | +22.7% | -2.9% | 12.8% |
| `eps_end=0.0` | 3 | +40.4% | -4.3% | 22.3% |
| `theta_bins=12` | 6 | +46.4% | +11.2% | 28.8% |
| `lr_schedule=inv`, `eps_end=0.1` | 5 | +5.0% | -59.6% | 32.3% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
