# Gap Report: dev-rl-nocause

Artifact `rlbench` · generated 2026-10-15 01:03 · 138 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +59.6% | -13.6% | ±8.0% | `theta_bins=30` |

## C1: mean_reward (paper 118.924)
**Fits but unsupported** · gap +59.6% → -13.6% · 53 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0012`, `B0039`, `B0040`, `B0053` (4 run(s) of the same config)
- Config: `theta_bins` naive `6`, changed to `30`
- Command:

  Replay: fork checkpoint `ad6c8cd1-beb7-498d-a4e5-759c7df2e1e5` and run
  ```
  RUN_TAG=e86aa0df039b "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 30 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 90.69, 74.5, 150, 114.8; gap after -13.6%; result checkpoint `8c4b6abb-f3c3-447c-b85d-29cad1f01de0`
- Effect: candidate 102.7 minus naive 189.8 = -87.03, 95% bootstrap interval [-118.9, -33.19] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner is stable across seeds on CartPole: its worst seed still balances for 69.1 steps on average.

- p. 1; value used: `mean_reward` = 118.924 steps (headline claim)

### What did we measure?
- Naive median 189.8 over 5 runs; repeats: 194.5, 194.2, 189.8, 183.7, 176.3
- Spread: range 176.3 to 194.5, noise band ±9.55 (2 x MAD), CV 4.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +59.6% (noise band ±8.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `theta_bins` the gap is +59.6% (it comes back)
- PASS · Held-out claim: C2: +124.4% to -74.9% (not worse beyond noise)
- FAIL · Evidence: `theta_bins=30`: no evidence mentions '30'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -87.03 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=linear` (2.8 noise units, gap +37.0%); `lr_schedule=inv` (2.51 noise units, gap +39.4%); `theta_bins=3` (2.01 noise units, gap +43.5%); `theta_bins=1` (1.78 noise units, gap -45.3%); `eps_end=0.001` (1.62 noise units, gap +46.5%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `eps_end=0.525`, `lr_schedule=inv`: this claim +32.9%, mean |gap| 16.5% (3 runs)
  - `eps_end=0.001`, `lr_schedule=inv`: this claim +6.9%, mean |gap| 29.9% (3 runs)
  - `theta_bins=12`, `lr_schedule=linear`: this claim +29.6%, mean |gap| 31.5% (3 runs)

### Equally good configurations
The target claim can't tell these 9 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `theta_bins=30` (reported)
- `theta_bins=1`
- `eps_end=0.001, lr_schedule=inv`
- `eps_end=0.001, theta_bins=1`
- `eps_end=0.905, theta_bins=1`
- `eps_end=0.525, lr_schedule=inv`
- `eps_end=0.525, theta_bins=1`
- `eps_end=0.001, theta_bins=30`
- `lr_schedule=linear, theta_bins=12`

### History matching (every measured configuration, all claims together)
- out-of-space suspected: 5 tested configuration(s) fit C1, and every other claim (C2) fits some tested configuration, but none of the 53 tested configurations fits them all. The claims are mutually inconsistent under every tested condition, which points to a cause outside the exposed settings (code, data or evaluation)
- Fit C1 alone (5; worst claim's implausibility in brackets, lowest is the least inconsistent): eps_end=0.001, lr_schedule=inv (3.41); theta_bins=30 (3.83); eps_end=0.001, theta_bins=30 (4.29); eps_end=0.905, theta_bins=1 (4.49); eps_end=0.001, theta_bins=1 (4.66)

Notes:
- configurations the target claim can't tell apart from the answer: theta_bins=30; theta_bins=1; eps_end=0.001, lr_schedule=inv; eps_end=0.001, theta_bins=1; eps_end=0.905, theta_bins=1; eps_end=0.525, lr_schedule=inv; eps_end=0.525, theta_bins=1; eps_end=0.001, theta_bins=30; lr_schedule=linear, theta_bins=12

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `eps_end=0.525`, `lr_schedule=inv` | 3 | +32.9% | -0.1% | 16.5% |
| `eps_end=0.001`, `lr_schedule=inv` | 3 | +6.9% | -52.9% | 29.9% |
| `theta_bins=12`, `lr_schedule=linear` | 3 | +29.6% | +33.4% | 31.5% |
| `lr_schedule=inv` | 4 | +23.6% | -42.1% | 32.9% |
| `theta_bins=12` | 4 | +48.9% | +30.1% | 39.5% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
