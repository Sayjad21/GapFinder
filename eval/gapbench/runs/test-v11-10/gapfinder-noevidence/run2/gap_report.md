# Gap Report: test-v11-10

Artifact `rlbench` · generated 2026-10-14 12:18 · 105 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +97.2% | -13.8% | ±6.1% | `max_steps=100`, `lr_schedule=inv` |

## C1: mean_reward (paper 94.93)
**Fits but unsupported** · gap +97.2% → -13.8% · 20 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0054`, `B0066`, `B0067`, `B0068`, `B0069` (5 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Config: `lr_schedule` naive `const`, changed to `inv`
- Command:

  Replay: fork checkpoint `7fe09a10-42ba-4162-99b4-bcff7e8a0d40` and run
  ```
  RUN_TAG=24e779799bf0 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 76.03, 90.72, 81.83, 96.94, 73.71; gap after -13.8%; result checkpoint `56d6b5f9-45a4-4113-a3b7-79562369ca96`
- Effect: candidate 81.83 minus naive 187.2 = -105.4, 95% bootstrap interval [-112.6, -80.86] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 94.9 steps, and that its worst seed still balances for 63.9.

- p. 1; value used: `mean_reward` = 94.93 steps (headline claim)

### What did we measure?
- Naive median 187.2 over 5 runs; repeats: 189.8, 162.2, 187.2, 176.9, 190.1
- Spread: range 162.2 to 190.1, noise band ±5.83 (2 x MAD), CV 6.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +97.2% (noise band ±6.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +50.8% (it comes back)
- FAIL · Counterfactual (reversal test): without `lr_schedule` the gap is +3.9% (it did NOT come back)
- PASS · Held-out claim: C2: +58.3% to -47.7% (not worse beyond noise)
- FAIL · Evidence: `max_steps=100`: evidence gate off: no evidence was looked for
- FAIL · Evidence: `lr_schedule=inv`: evidence gate off: no evidence was looked for
- PASS · Effect vs noise: candidate minus naive is -105.4 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `max_steps_evaluation`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=20` (2.97 noise units, gap -78.9%); `lr_schedule=linear` (1.69 noise units, gap +86.8%); `max_steps=500` (1.65 noise units, gap +87.0%)
- Near alternatives (closest across all claims):
  - `max_steps=100`: this claim +3.9%, mean |gap| 22.8% (6 runs)
  - `lr_schedule=linear`, `max_steps=100`: this claim +4.1%, mean |gap| 25.8% (5 runs)
  - `lr_schedule=inv`, `max_steps=500`: this claim +46.4%, mean |gap| 35.8% (5 runs)

### History matching (every measured configuration, all claims together)
- 3 of 20 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.48); lr_schedule=inv, max_steps=100 (max I 1.22)
  - `max_steps`: max_steps=100 (max I 0.52)
- Equally good values: `lr_schedule` in {inv, linear}

Notes:
- evidence gate off: no evidence was checked, so this cannot be labelled Explained
- equally good values within one noise band (measured): lr_schedule in {inv, linear}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100` | 6 | +3.9% | +41.7% | 22.8% |
| `lr_schedule=linear`, `max_steps=100` | 5 | +4.1% | +47.5% | 25.8% |
| `lr_schedule=inv`, `max_steps=100` | 5 | -13.8% | -47.7% | 30.8% |
| `lr_schedule=inv`, `max_steps=500` | 5 | +46.4% | -25.3% | 35.8% |
| `lr_schedule=inv`, `max_steps=2000` | 5 | +37.8% | -40.5% | 39.2% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `max_steps_evaluation`

## Provenance
- GapFinder commit: `b05f7288e1a4df8af69bb0b5e7633827b4cb46c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
