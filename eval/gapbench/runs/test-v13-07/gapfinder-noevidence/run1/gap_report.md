# Gap Report: test-v13-07

Artifact `rlbench` · generated 2026-10-15 23:50 · 103 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +101.4% | -6.8% | ±19.1% | `eps_decay=0.198` |

## C1: mean_reward (paper 89.7375)
**Fits but unsupported** · gap +101.4% → -6.8% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0014`, `B0028`, `B0029`, `B0035`, `B0036`, `B0037` (6 run(s) of the same config)
- Config: `eps_decay` naive `0.99`, changed to `0.198`
- Command:

  Replay: fork checkpoint `a7eb1846-bd5b-4a4f-8a73-ce7893d169e8` and run
  ```
  RUN_TAG=04dc2d28efa5 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.198 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 48.28, 82.19, 94.42, 71.73, 85.1, 97.24; gap after -6.8%; result checkpoint `102fb82c-05d1-4acd-85d8-53ba00b1e800`
- Effect: candidate 83.65 minus naive 180.8 = -97.1, 95% bootstrap interval [-109.7, -67.38] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over a coarse state grid reaches a mean reward of 89.7 on CartPole; the worst of its seeds reaches 69.9.

- p. 1; value used: `mean_reward` = 89.7375 reward (headline claim)

### What did we measure?
- Naive median 180.8 over 5 runs; repeats: 191.2, 180.8, 176.6, 189.3, 150.3
- Spread: range 150.3 to 191.2, noise band ±17.16 (2 x MAD), CV 9.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +101.4% (noise band ±19.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `eps_decay` the gap is +101.4% (it comes back)
- PASS · Held-out claim: C2: +58.9% to -86.5% (not worse beyond noise)
- FAIL · Evidence: `eps_decay=0.198`: evidence gate off: no evidence was looked for
- PASS · Effect vs noise: candidate minus naive is -97.1 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `termination_angle`, `termination_position`, `reward_per_step`, `learning_rate_schedule_constant`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (4.56 noise units, gap +14.2%); `eps_decay=0.0198` (4.2 noise units, gap -21.0%); `eps_decay=0.495` (4.11 noise units, gap -22.8%); `eps_decay=0.0` (3.08 noise units, gap -42.5%); `eps_decay=0.099` (2.48 noise units, gap -54.0%) (and 1 more in the JSON)
- Near alternatives (closest across all claims):
  - `eps_decay=0.98`, `lr_schedule=linear`: this claim +73.1%, mean |gap| 37.6% (2 runs)
  - `eps_decay=0.98`, `lr_schedule=inv`: this claim +12.4%, mean |gap| 44.7% (5 runs)
  - `eps_decay=0.98`: this claim +62.9%, mean |gap| 45.5% (3 runs)

### Equally good configurations
The target claim can't tell these 5 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `eps_decay=0.198` (reported)
- `eps_decay=0.0198`
- `eps_decay=0.0`
- `eps_decay=0.495, lr_schedule=linear`
- `eps_decay=0.98, lr_schedule=inv`

### History matching (every measured configuration, all claims together)
- 9 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 9 configurations
  - `eps_decay, lr_schedule`: eps_decay=0.98, lr_schedule=inv (max I 1.18); eps_decay=0.495, lr_schedule=linear (max I 2.05); eps_decay=0.099, lr_schedule=inv (max I 2.76)
  - `eps_decay`: eps_decay=0.495 (max I 1.31); eps_decay=0.0198 (max I 1.52); eps_decay=0.198 (max I 1.53); eps_decay=0.0 (max I 1.54); +1 more
  - `lr_schedule`: lr_schedule=inv (max I 2.63)
- Equally good values: `eps_decay` in {0.0, 0.0198, 0.099, 0.198, 0.495}

Notes:
- evidence gate off: no evidence was checked, so this cannot be labelled Explained
- configurations the target claim can't tell apart from the answer: eps_decay=0.198; eps_decay=0.0198; eps_decay=0.0; eps_decay=0.495, lr_schedule=linear; eps_decay=0.98, lr_schedule=inv
- equally good values within one noise band (measured): eps_decay in {0.0, 0.0198, 0.099, 0.198, 0.495}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `eps_decay=0.98`, `lr_schedule=linear` | 2 | +73.1% | +2.1% | 37.6% |
| `eps_decay=0.98`, `lr_schedule=inv` | 5 | +12.4% | -77.1% | 44.7% |
| `eps_decay=0.98` | 3 | +62.9% | -28.1% | 45.5% |
| `eps_decay=0.198` | 6 | -6.8% | -86.5% | 46.6% |
| `eps_decay=0.0` | 6 | -7.3% | -86.5% | 46.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `termination_angle`, `termination_position`, `reward_per_step`, `learning_rate_schedule_constant`

## Provenance
- GapFinder commit: `e9c31fd1405f5c8aae4bd880eadcdc8d491fad02` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
