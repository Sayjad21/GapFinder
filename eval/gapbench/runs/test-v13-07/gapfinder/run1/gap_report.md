# Gap Report: test-v13-07

Artifact `rlbench` · generated 2026-10-15 23:49 · 83 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +93.8% | -2.2% | ±34.8% | `eps_decay=0.495` |

## C1: mean_reward (paper 89.7375)
**Fits but unsupported** · gap +93.8% → -2.2% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0013`, `B0024`, `B0025`, `B0030`, `B0031`, `B0032` (6 run(s) of the same config)
- Config: `eps_decay` naive `0.99`, changed to `0.495`
- Command:

  Replay: fork checkpoint `604a5e55-dba4-49e0-a3f7-48c49570e3c4` and run
  ```
  RUN_TAG=1fc774f4d5c1 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.495 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 89.96, 99.58, 90.55, 85.56, 74.58, 81.27; gap after -2.2%; result checkpoint `b25c0dc1-1ba5-44f2-b6f9-1196aed26f4b`
- Effect: candidate 87.76 minus naive 173.9 = -86.15, 95% bootstrap interval [-106.7, -72.54] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 89.7 on CartPole; the worst of its seeds reaches 69.9.

- p. 1; value used: `mean_reward` = 89.7375 reward (headline claim)

### What did we measure?
- Naive median 173.9 over 5 runs; repeats: 189.5, 173.9, 189.8, 158.1, 171.6
- Spread: range 158.1 to 189.8, noise band ±31.22 (2 x MAD), CV 7.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +93.8% (noise band ±34.8% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `eps_decay` the gap is +93.8% (it comes back)
- PASS · Held-out claim: C2: -9.5% to -85.5% (not worse beyond noise)
- FAIL · Evidence: `eps_decay=0.495`: no evidence mentions '0.495'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -86.15 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `termination_angle`, `termination_position`, `reward_per_step`, `learning_rate_schedule_constant`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_decay=0.0198` (2.37 noise units, gap -11.2%); `eps_decay=0.198` (2.16 noise units, gap -18.6%); `eps_decay=0.099` (2.02 noise units, gap -23.4%); `lr_schedule=inv` (1.84 noise units, gap +29.8%); `eps_decay=0.0` (1.43 noise units, gap -43.9%)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `eps_decay=0.98`: this claim +43.4%, mean |gap| 40.6% (2 runs)
  - `lr_schedule=inv`: this claim +36.0%, mean |gap| 46.1% (5 runs)
  - `eps_decay=0.0198`: this claim -12.4%, mean |gap| 49.5% (6 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `eps_decay=0.495` (reported)
- `eps_decay=0.0198`
- `eps_decay=0.98, lr_schedule=inv`

### History matching (every measured configuration, all claims together)
- 8 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 8 configurations
  - `eps_decay`: eps_decay=0.495 (max I 1.44); eps_decay=0.0198 (max I 2.03); eps_decay=0.198 (max I 2.29); eps_decay=0.0 (max I 2.94)
  - `eps_decay, lr_schedule`: eps_decay=0.98, lr_schedule=inv (max I 1.55); eps_decay=0.495, lr_schedule=inv (max I 2.55); eps_decay=0.198, lr_schedule=linear (max I 2.59); eps_decay=0.495, lr_schedule=linear (max I 2.6)
- Equally good values: `eps_decay` in {0.0198, 0.099, 0.198, 0.495}

Notes:
- configurations the target claim can't tell apart from the answer: eps_decay=0.495; eps_decay=0.0198; eps_decay=0.98, lr_schedule=inv
- equally good values within one noise band (measured): eps_decay in {0.0198, 0.099, 0.198, 0.495}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=linear`, `eps_decay=0.98` | 2 | +43.4% | -37.8% | 40.6% |
| `eps_decay=0.495` | 6 | -2.2% | -85.5% | 43.9% |
| `lr_schedule=inv` | 5 | +36.0% | -56.3% | 46.1% |
| `eps_decay=0.0198` | 6 | -12.4% | -86.5% | 49.5% |
| naive (reproduction as run) | 5 | +93.8% | -9.5% | 51.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `termination_angle`, `termination_position`, `reward_per_step`, `learning_rate_schedule_constant`

## Provenance
- GapFinder commit: `e9c31fd1405f5c8aae4bd880eadcdc8d491fad02` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.1520, sandbox reported $0.0000 (total $0.1520; this search; ledger extraction is included only if it shared the search's router)
