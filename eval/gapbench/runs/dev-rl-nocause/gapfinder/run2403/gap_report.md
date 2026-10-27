# Gap Report: dev-rl-nocause

Artifact `rlbench` · generated 2026-10-16 01:13 · 137 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +42.0% | +6.5% | ±24.8% | `lr_schedule=inv` |

## C1: mean_reward (paper 118.924)
**Fits but unsupported** · gap +42.0% → +6.5% · 54 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0015`, `B0035`, `B0036`, `B0047`, `B0048`, `B0049` (6 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `inv`
- Command:

  Replay: fork checkpoint `a81641a3-dee3-4c7c-828a-593a9176feec` and run
  ```
  RUN_TAG=e9cb94629b8b "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 128.6, 123.7, 106.4, 138, 141, 124.8; gap after +6.5%; result checkpoint `8cb63fe7-fa06-4e69-a9c1-9efc3e599067`
- Effect: candidate 126.7 minus naive 168.9 = -42.2, 95% bootstrap interval [-70.92, -25.13] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner is stable across seeds on CartPole: its worst seed still balances for 69.1 steps on average.

- p. 1; value used: `mean_reward` = 118.924 steps (headline claim)

### What did we measure?
- Naive median 168.9 over 5 runs; repeats: 193, 154.2, 188.7, 168.9, 162.7
- Spread: range 154.2 to 193, noise band ±29.47 (2 x MAD), CV 9.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +42.0% (noise band ±24.8% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is +42.0% (it comes back)
- PASS · Held-out claim: C2: +0.1% to -66.7% (not worse beyond noise)
- FAIL · Evidence: `lr_schedule=inv`: no evidence mentions 'inv'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -42.2 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives (closest across all claims):
  - `lr_schedule=inv`, `eps_end=0.525`: this claim +25.8%, mean |gap| 18.6% (5 runs)
  - `theta_bins=12`: this claim +45.4%, mean |gap| 24.5% (6 runs)
  - `lr_schedule=inv`, `theta_bins=8`: this claim -5.7%, mean |gap| 26.3% (5 runs)

### Equally good configurations
The target claim can't tell these 7 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `lr_schedule=inv` (reported)
- `theta_bins=1`
- `theta_bins=30`
- `eps_end=0.01, lr_schedule=inv`
- `eps_end=0.01, theta_bins=1`
- `lr_schedule=inv, theta_bins=8`
- `eps_end=0.525, theta_bins=1`

### History matching (every measured configuration, all claims together)
- 26 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `lr_schedule, theta_bins`: lr_schedule=inv, theta_bins=8 (max I 0.82); lr_schedule=inv, theta_bins=4 (max I 1.57)
  - `lr_schedule`: lr_schedule=inv (max I 0.98)
  - `eps_end, lr_schedule`: eps_end=0.01, lr_schedule=inv (max I 1.04); eps_end=0.981, lr_schedule=inv (max I 1.79)
  - `theta_bins`: theta_bins=30 (max I 1.29); theta_bins=1 (max I 1.42)
  - `eps_end, theta_bins`: eps_end=0.01, theta_bins=1 (max I 1.31); eps_end=0.525, theta_bins=1 (max I 1.69); eps_end=0.905, theta_bins=1 (max I 1.87)

Notes:
- configurations the target claim can't tell apart from the answer: lr_schedule=inv; theta_bins=1; theta_bins=30; eps_end=0.01, lr_schedule=inv; eps_end=0.01, theta_bins=1; lr_schedule=inv, theta_bins=8; eps_end=0.525, theta_bins=1

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv`, `eps_end=0.525` | 5 | +25.8% | +11.4% | 18.6% |
| naive (reproduction as run) | 5 | +42.0% | +0.1% | 21.0% |
| `theta_bins=12` | 6 | +45.4% | -3.7% | 24.5% |
| `lr_schedule=inv`, `theta_bins=8` | 5 | -5.7% | -47.0% | 26.3% |
| `lr_schedule=inv` | 6 | +6.5% | -66.7% | 36.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
