# Gap Report: test-v13-07

Artifact `rlbench` · generated 2026-10-16 02:07 · 85 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +102.3% | +2.5% | ±9.0% | `eps_decay=0.495` |

## C1: mean_reward (paper 89.7375)
**Fits but unsupported** · gap +102.3% → +2.5% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0013`, `B0028`, `B0029`, `B0034` (4 run(s) of the same config)
- Config: `eps_decay` naive `0.99`, changed to `0.495`
- Command:

  Replay: fork checkpoint `5789855f-1c0c-4672-bec5-ebca43c49cd2` and run
  ```
  RUN_TAG=9974e1da636a "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.495 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 84.55, 99.4, 105.6, 73.5; gap after +2.5%; result checkpoint `b264875b-01c5-49f7-a81f-43c7a61b4b09`
- Effect: candidate 91.97 minus naive 181.5 = -89.57, 95% bootstrap interval [-112.5, -71.24] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 89.7 on CartPole; the worst of its seeds reaches 69.9.

- p. 1; value used: `mean_reward` = 89.7375 reward (headline claim)

### What did we measure?
- Naive median 181.5 over 5 runs; repeats: 183, 193.6, 181.5, 177.5, 171.7
- Spread: range 171.7 to 193.6, noise band ±8.06 (2 x MAD), CV 4.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +102.3% (noise band ±9.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `eps_decay` the gap is +102.3% (it comes back)
- PASS · Held-out claim: C2: +56.2% to -82.6% (not worse beyond noise)
- FAIL · Evidence: `eps_decay=0.495`: no evidence mentions '0.495'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -89.57 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `termination_angle`, `termination_position`, `reward_per_step`, `learning_rate_schedule_constant`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_decay=0.099` (10.64 noise units, gap +6.7%); `eps_decay=0.198` (9.38 noise units, gap -18.1%); `eps_decay=0.0198` (8.59 noise units, gap +25.1%); `eps_decay=0.0` (5.35 noise units, gap -54.3%); `lr_schedule=inv` (3.07 noise units, gap +74.7%) (and 2 more in the JSON)
- Near alternatives (closest across all claims):
  - `eps_decay=0.495`, `lr_schedule=linear`: this claim -9.6%, mean |gap| 47.9% (3 runs)
  - `eps_decay=0.198`: this claim -12.6%, mean |gap| 48.9% (4 runs)
  - `lr_schedule=inv`: this claim +46.0%, mean |gap| 49.1% (3 runs)

### Equally good configurations
The target claim can't tell these 6 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `eps_decay=0.495` (reported)
- `eps_decay=0.0198`
- `eps_decay=0.198`
- `eps_decay=0.099`
- `eps_decay=0.98, lr_schedule=inv`
- `eps_decay=0.495, lr_schedule=linear`

### History matching (every measured configuration, all claims together)
- 6 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 6 configurations
  - `eps_decay, lr_schedule`: eps_decay=0.98, lr_schedule=inv (max I 1.59); eps_decay=0.495, lr_schedule=linear (max I 1.62)
  - `eps_decay`: eps_decay=0.495 (max I 1.64); eps_decay=0.0198 (max I 1.7); eps_decay=0.198 (max I 1.96); eps_decay=0.099 (max I 2.83)
- 2 separate islands (no single-knob move joins them): eps_decay=0.495, lr_schedule=linear; eps_decay=0.495; eps_decay=0.0198 | eps_decay=0.98, lr_schedule=inv

Notes:
- configurations the target claim can't tell apart from the answer: eps_decay=0.495; eps_decay=0.0198; eps_decay=0.198; eps_decay=0.099; eps_decay=0.98, lr_schedule=inv; eps_decay=0.495, lr_schedule=linear

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `eps_decay=0.495` | 4 | +2.5% | -82.6% | 42.5% |
| `eps_decay=0.495`, `lr_schedule=linear` | 3 | -9.6% | -86.1% | 47.9% |
| `eps_decay=0.198` | 4 | -12.6% | -85.2% | 48.9% |
| `lr_schedule=inv` | 3 | +46.0% | -52.1% | 49.1% |
| `eps_decay=0.0198` | 4 | -12.0% | -86.4% | 49.2% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `termination_angle`, `termination_position`, `reward_per_step`, `learning_rate_schedule_constant`

## Provenance
- GapFinder commit: `ac9cc82263ea2a8d609167080c75e6a79b5dd162` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
