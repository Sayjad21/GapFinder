# Gap Report: dev-rl-schedule

Artifact `rlbench` · generated 2026-10-15 19:11 · 17 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Partially explained | +36.3% | -3.4% | ±10.5% | `lr_schedule=inv` |

## C1: mean_reward (paper 139.35)
**Partially explained** · gap +36.3% → -3.4% · 2 hypotheses tested
> Plausible explanation (fits but unsupported): it closes only part of the gap, or the paper's own value was not tested

### Which experiment changed it?
- Branch: `B0006`, `B0008`, `B0009`, `B0010`, `B0011`, `B0012` (6 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `inv`
- Command:

  Replay: fork checkpoint `8f353c3a-405d-4098-838e-09ac819b5b62` and run
  ```
  RUN_TAG=a598b340de45 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 136.9, 135.1, 132.1, 134.1, 132.4, 143.6; gap after -3.4%; result checkpoint `280c5014-e91d-40d8-9ad1-a7a6130b58f9`
- Effect: candidate 134.6 minus naive 189.9 = -55.32, 95% bootstrap interval [-61.53, -30.14] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over six pole-angle and six angular-velocity bins balances CartPole for a mean of 139.3 steps after 400 training episodes.

- p. 1; value used: `mean_reward` = 139.35 steps (headline claim)

### What did we measure?
- Naive median 189.9 over 5 runs; repeats: 197.3, 189.9, 174.5, 157.4, 196.2
- Spread: range 157.4 to 197.3, noise band ±14.65 (2 x MAD), CV 9.3%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +36.3% (noise band ±10.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is +36.3% (it comes back)
- PASS · Held-out claim: C2: +406.5% to +15.8% (not worse beyond noise)
- PASS · Evidence: `lr_schedule=inv`: paper states 'inv (0.1 / (1 + t/50))'
- PASS · Effect vs noise: candidate minus naive is -55.32 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `discretise_theta_range`, `discretise_omega_range`, `cartpole_g`, `cartpole_dt`, `reset_uniform_range`, `cartpole_mc`, `cartpole_mp`, `cartpole_l`, `cartpole_f`, `RUN_TAG`, `greedy_evaluation_policy`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=linear` (1.44 noise units, gap +21.1%)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`: this claim +11.0%, mean |gap| 85.2% (6 runs)

### History matching (every measured configuration, all claims together)
- 2 of 2 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 2 configurations
  - `lr_schedule`: lr_schedule=inv (max I 0.29); lr_schedule=linear (max I 1.39)
- Equally good values: `lr_schedule` in {inv, linear}

Notes:
- equally good values within one noise band (measured): lr_schedule in {inv, linear}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv` | 6 | -3.4% | +15.8% | 9.6% |
| `lr_schedule=linear` | 6 | +11.0% | +159.4% | 85.2% |
| naive (reproduction as run) | 5 | +36.3% | +406.5% | 221.4% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `discretise_theta_range`, `discretise_omega_range`, `cartpole_g`, `cartpole_dt`, `reset_uniform_range`, `cartpole_mc`, `cartpole_mp`, `cartpole_l`, `cartpole_f`, `RUN_TAG`, `greedy_evaluation_policy`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
