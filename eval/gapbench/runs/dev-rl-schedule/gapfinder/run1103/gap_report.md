# Gap Report: dev-rl-schedule

Artifact `rlbench` · generated 2026-10-15 00:28 · 17 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Paper-artifact inconsistency | +32.3% | +3.0% | ±4.0% | `lr_schedule=inv` |

## C1: mean_reward (paper 139.35)
**Paper-artifact inconsistency** · gap +32.3% → +3.0% · 2 hypotheses tested
> Confirmed cause: reverting it brings the gap back, held-out claims hold, and the value has evidence

### Which experiment changed it?
- Branch: `B0006`, `B0008`, `B0009`, `B0010`, `B0011`, `B0012` (6 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `inv`
- Command:

  Replay: fork checkpoint `4bde0f22-d87e-4e6e-a77f-77e74849cb3e` and run
  ```
  RUN_TAG=ba09efc9ec0c "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 154.1, 129.4, 161.9, 148, 106, 139.1; gap after +3.0%; result checkpoint `e250bd8b-0a95-4d37-8e8e-584b7a5ab5d9`
- Effect: candidate 143.5 minus naive 184.3 = -40.78, 95% bootstrap interval [-65.45, -18.5] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over six pole-angle and six angular-velocity bins balances CartPole for a mean of 139.3 steps after 400 training episodes.

- p. 1; value used: `mean_reward` = 139.35 steps (headline claim)

### What did we measure?
- Naive median 184.3 over 5 runs; repeats: 150.6, 184.3, 193.5, 184.8, 181.6
- Spread: range 150.6 to 193.5, noise band ±5.53 (2 x MAD), CV 9.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +32.3% (noise band ±4.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is +32.3% (it comes back)
- PASS · Held-out claim: C2: +128.4% to +89.8% (not worse beyond noise)
- PASS · Evidence: `lr_schedule=inv`: paper states 'inv (0.1 / (1 + t/50))'
- PASS · Effect vs noise: candidate minus naive is -40.78 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `discretise_theta_range`, `discretise_omega_range`, `cartpole_g`, `cartpole_dt`, `reset_uniform_range`, `cartpole_mc`, `cartpole_mp`, `cartpole_l`, `cartpole_f`, `RUN_TAG`, `greedy_evaluation_policy`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=linear` (6.8 noise units, gap +5.3%)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`: this claim +21.0%, mean |gap| 197.0% (6 runs)

### History matching (every measured configuration, all claims together)
- 1 of 2 tested configurations fit every claim within 3 sigma

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv` | 6 | +3.0% | +89.8% | 46.4% |
| naive (reproduction as run) | 5 | +32.3% | +128.4% | 80.3% |
| `lr_schedule=linear` | 6 | +21.0% | +373.0% | 197.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `discretise_theta_range`, `discretise_omega_range`, `cartpole_g`, `cartpole_dt`, `reset_uniform_range`, `cartpole_mc`, `cartpole_mp`, `cartpole_l`, `cartpole_f`, `RUN_TAG`, `greedy_evaluation_policy`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
