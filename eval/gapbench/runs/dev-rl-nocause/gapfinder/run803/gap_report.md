# Gap Report: dev-rl-nocause

Artifact `rlbench` · generated 2026-10-14 23:23 · 127 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +52.6% | -3.5% | ±12.2% | `eps_end=0.1`, `theta_bins=30` |

## C1: mean_reward (paper 118.924)
**Fits but unsupported** · gap +52.6% → -3.5% · 53 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0079`, `B0118`, `B0119` (3 run(s) of the same config)
- Config: `eps_end` naive `0.05`, changed to `0.1`
- Config: `theta_bins` naive `6`, changed to `30`
- Command:

  Replay: fork checkpoint `7f54508c-1b3c-47af-bbbb-b24e47eb13cc` and run
  ```
  RUN_TAG=0a14537551bc "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.1 --eps_decay 0.99 --theta_bins 30 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 102.8, 150.4, 114.8; gap after -3.5%; result checkpoint `e95e5496-28c7-414b-b274-73d434d23cba`
- Effect: candidate 114.8 minus naive 181.5 = -66.75, 95% bootstrap interval [-84.78, -29.62] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner is stable across seeds on CartPole: its worst seed still balances for 69.1 steps on average.

- p. 1; value used: `mean_reward` = 118.924 steps (headline claim)

### What did we measure?
- Naive median 181.5 over 5 runs; repeats: 181.5, 181.5, 194.2, 174.1, 188.8
- Spread: range 174.1 to 194.2, noise band ±14.55 (2 x MAD), CV 4.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +52.6% (noise band ±12.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `eps_end` the gap is -29.2% (it comes back)
- PASS · Counterfactual (reversal test): without `theta_bins` the gap is +37.0% (it comes back)
- PASS · Held-out claim: C2: +92.7% to -74.7% (not worse beyond noise)
- FAIL · Evidence: `eps_end=0.1`: no evidence mentions '0.1'; it fits, but nothing says the authors used it
- FAIL · Evidence: `theta_bins=30`: no evidence mentions '30'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -66.75 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (4.13 noise units, gap +2.1%); `eps_end=0.025` (2.48 noise units, gap +22.3%); `theta_bins=3` (2.15 noise units, gap +26.4%); `eps_end=0.01` (1.22 noise units, gap +37.8%)
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`, `theta_bins=8`: this claim +0.3%, mean |gap| 13.3% (3 runs)
  - `eps_end=0.525`, `lr_schedule=inv`: this claim +23.7%, mean |gap| 17.2% (3 runs)
  - `theta_bins=4`, `eps_end=0.1`: this claim +38.0%, mean |gap| 22.5% (3 runs)

### Equally good configurations
The target claim can't tell these 9 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `eps_end=0.1, theta_bins=30` (reported)
- `lr_schedule=inv`
- `lr_schedule=inv, theta_bins=8`
- `eps_end=0.01, lr_schedule=inv`
- `eps_end=0.025, theta_bins=30`
- `eps_end=0.1, theta_bins=3`
- `eps_end=0.025, lr_schedule=inv`
- `eps_end=0.1, lr_schedule=inv`
- `eps_end=0.01, theta_bins=30`

### History matching (every measured configuration, all claims together)
- 10 of 53 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr_schedule, theta_bins`: lr_schedule=inv, theta_bins=8 (max I 0.73); lr_schedule=inv, theta_bins=3 (max I 2.85)
  - `eps_end, theta_bins`: eps_end=0.1, theta_bins=30 (max I 1.27); eps_end=0.1, theta_bins=3 (max I 2.03); eps_end=0.01, theta_bins=30 (max I 2.34); eps_end=0.025, theta_bins=30 (max I 2.48)
  - `eps_end, lr_schedule`: eps_end=0.1, lr_schedule=inv (max I 1.85); eps_end=0.01, lr_schedule=inv (max I 2.16); eps_end=0.025, lr_schedule=inv (max I 2.29)
  - `lr_schedule`: lr_schedule=inv (max I 2.3)
- 2 separate islands (no single-knob move joins them): lr_schedule=inv, theta_bins=8; eps_end=0.1, lr_schedule=inv; eps_end=0.01, lr_schedule=inv | eps_end=0.1, theta_bins=30; eps_end=0.1, theta_bins=3; eps_end=0.01, theta_bins=30
- Equally good values: `theta_bins` in {3, 30}

Notes:
- configurations the target claim can't tell apart from the answer: eps_end=0.1, theta_bins=30; lr_schedule=inv; lr_schedule=inv, theta_bins=8; eps_end=0.01, lr_schedule=inv; eps_end=0.025, theta_bins=30; eps_end=0.1, theta_bins=3; eps_end=0.025, lr_schedule=inv; eps_end=0.1, lr_schedule=inv; eps_end=0.01, theta_bins=30
- equally good values within one noise band (measured): theta_bins in {3, 30}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv`, `theta_bins=8` | 3 | +0.3% | -26.2% | 13.3% |
| `eps_end=0.525`, `lr_schedule=inv` | 3 | +23.7% | -10.7% | 17.2% |
| `theta_bins=4`, `eps_end=0.1` | 3 | +38.0% | +6.9% | 22.5% |
| `eps_end=0.025`, `lr_schedule=inv` | 3 | +15.3% | -43.2% | 29.2% |
| `lr_schedule=inv` | 4 | +17.5% | -44.6% | 31.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `efb2f63a257a40b9982099a274f2e882f272b80c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
