# Gap Report: dev-rl-nocause

Artifact `rlbench` · generated 2026-10-14 22:13 · 200 branch runs (0 build/load setups) · sandbox $0.0000

> **Partial report:** the run or dollar budget ran out before every claim was verified.

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +62.6% | +7.9% | ±2.4% | `eps_end=0.981`, `theta_bins=60` |

## C1: mean_reward (paper 118.924)
**Fits but unsupported** · gap +62.6% → +7.9% · 54 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0128`, `B0153`, `B0154`, `B0155`, `B0156` (5 run(s) of the same config)
- Config: `eps_end` naive `0.05`, changed to `0.981`
- Config: `theta_bins` naive `6`, changed to `60`
- Command:

  Replay: fork checkpoint `2943cb16-4794-4a54-abc2-129292c76b64` and run
  ```
  RUN_TAG=1c5bdf245aac "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.981 --eps_decay 0.99 --theta_bins 60 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 118, 128.3, 128.6, 112.3, 134.5; gap after +7.9%; result checkpoint `4676a137-c424-4140-aa74-4e5a299a52f3`
- Effect: candidate 128.3 minus naive 193.4 = -65.09, 95% bootstrap interval [-79.36, -29.99] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner is stable across seeds on CartPole: its worst seed still balances for 69.1 steps on average.

- p. 1; value used: `mean_reward` = 118.924 steps (headline claim)

### What did we measure?
- Naive median 193.4 over 5 runs; repeats: 198.5, 192, 193.9, 149.1, 193.4
- Spread: range 149.1 to 198.5, noise band ±2.85 (2 x MAD), CV 11.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +62.6% (noise band ±2.4% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `eps_end` the gap is -66.2% (it comes back)
- PASS · Counterfactual (reversal test): without `theta_bins` the gap is +52.3% (it comes back)
- PASS · Held-out claim: C2: +133.2% to -20.6% (not worse beyond noise)
- FAIL · Evidence: `eps_end=0.981`: no evidence mentions '0.981'; it fits, but nothing says the authors used it
- FAIL · Evidence: `theta_bins=60`: no evidence mentions '60'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -65.09 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `theta_bins=1` (24.74 noise units, gap -3.4%); `theta_bins=30` (13.84 noise units, gap -29.5%); `lr_schedule=inv` (11.18 noise units, gap +35.9%); `lr_schedule=linear` (10.26 noise units, gap +38.1%); `theta_bins=3` (8.04 noise units, gap +43.4%) (and 7 more in the JSON)
- Near alternatives (closest across all claims):
  - `eps_end=0.905`, `theta_bins=60`: this claim +14.8%, mean |gap| 9.3% (5 runs)
  - `lr_schedule=inv`: this claim +20.0%, mean |gap| 26.3% (6 runs)
  - `theta_bins=8`: this claim +49.7%, mean |gap| 26.3% (6 runs)

### History matching (every measured configuration, all claims together)
- 19 of 54 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 10 configurations
  - `eps_end, theta_bins`: eps_end=0.981, theta_bins=60 (max I 0.38); eps_end=0.905, theta_bins=60 (max I 0.58); eps_end=0.525, theta_bins=60 (max I 0.85); eps_end=0.905, theta_bins=1 (max I 1.18); +4 more
  - `lr_schedule`: lr_schedule=inv (max I 1.68)
  - `theta_bins`: theta_bins=30 (max I 2.11)
- 2 separate islands (no single-knob move joins them): eps_end=0.981, theta_bins=60; eps_end=0.905, theta_bins=60; eps_end=0.525, theta_bins=60 | lr_schedule=inv; eps_end=0.81, lr_schedule=inv; eps_end=0.525, lr_schedule=inv

Notes:
- stopped early: run budget of 200 reached (wanted 4 more run(s) of {'lr_schedule': 'inv', 'eps_end': '0.81'} for 'confirm-combo')
- verified from runs already made, after the budget ran out

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `eps_end=0.905`, `theta_bins=60` | 5 | +14.8% | +3.8% | 9.3% |
| `eps_end=0.981`, `theta_bins=60` | 5 | +7.9% | -20.6% | 14.2% |
| `lr_schedule=inv` | 6 | +20.0% | -32.5% | 26.3% |
| `theta_bins=8` | 6 | +49.7% | +2.9% | 26.3% |
| `lr_schedule=inv`, `eps_end=0.525` | 5 | +29.3% | -26.5% | 27.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `e0f13d101585ad1609a15fbf67b70128f4cfffc8` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
