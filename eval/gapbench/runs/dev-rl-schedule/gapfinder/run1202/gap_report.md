# Gap Report: dev-rl-schedule

Artifact `rlbench` · generated 2026-10-15 00:43 · 13 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Partially explained | +30.7% | -13.9% | ±5.5% | `lr_schedule=inv` |

## C1: mean_reward (paper 139.35)
**Partially explained** · gap +30.7% → -13.9% · 2 hypotheses tested
> Plausible explanation (fits but unsupported): it closes only part of the gap, or the paper's own value was not tested

### Which experiment changed it?
- Branch: `B0006`, `B0008`, `B0009`, `B0010` (4 run(s) of the same config)
- Config: `lr_schedule` naive `const`, changed to `inv`
- Command:

  Replay: fork checkpoint `e35b0752-0fc6-4c71-b0e3-b138d3ebd386` and run
  ```
  RUN_TAG=678724763181 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 116.6, 122.6, 147.3, 117.4; gap after -13.9%; result checkpoint `a6c84ee4-408d-438e-9320-d249e325fd0b`
- Effect: candidate 120 minus naive 182.1 = -62.17, 95% bootstrap interval [-72.09, -35.44] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> A tabular Q-learner over six pole-angle and six angular-velocity bins balances CartPole for a mean of 139.3 steps after 400 training episodes.

- p. 1; value used: `mean_reward` = 139.35 steps (headline claim)

### What did we measure?
- Naive median 182.1 over 5 runs; repeats: 182.1, 178.7, 178.3, 191.6, 195.3
- Spread: range 178.3 to 195.3, noise band ±7.63 (2 x MAD), CV 4.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +30.7% (noise band ±5.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is +30.7% (it comes back)
- PASS · Held-out claim: C2: +362.1% to +3.7% (not worse beyond noise)
- PASS · Evidence: `lr_schedule=inv`: paper states 'inv (0.1 / (1 + t/50))'
- PASS · Effect vs noise: candidate minus naive is -62.17 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `discretise_theta_range`, `discretise_omega_range`, `cartpole_g`, `cartpole_dt`, `reset_uniform_range`, `cartpole_mc`, `cartpole_mp`, `cartpole_l`, `cartpole_f`, `RUN_TAG`, `greedy_evaluation_policy`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=linear` (3.3 noise units, gap +12.6%)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`: this claim +17.5%, mean |gap| 169.6% (4 runs)

### History matching (every measured configuration, all claims together)
- 2 of 2 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 2 configurations
  - `lr_schedule`: lr_schedule=inv (max I 1.52); lr_schedule=linear (max I 2.88)
- Equally good values: `lr_schedule` in {inv, linear}

Notes:
- equally good values within one noise band (measured): lr_schedule in {inv, linear}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv` | 4 | -13.9% | +3.7% | 8.8% |
| `lr_schedule=linear` | 4 | +17.5% | +321.7% | 169.6% |
| naive (reproduction as run) | 5 | +30.7% | +362.1% | 196.4% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `discretise_theta_range`, `discretise_omega_range`, `cartpole_g`, `cartpole_dt`, `reset_uniform_range`, `cartpole_mc`, `cartpole_mp`, `cartpole_l`, `cartpole_f`, `RUN_TAG`, `greedy_evaluation_policy`

## Provenance
- GapFinder commit: `ef26f44196c929e8fbb22ebbb0f4f716dba96cf9` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
