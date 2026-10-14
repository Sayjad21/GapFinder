# Gap Report: test-v11-10

Artifact `rlbench` · generated 2026-10-14 12:18 · 77 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +97.7% | -6.4% | ±7.7% | `max_steps=100`, `lr_schedule=inv` |

## C1: mean_reward (paper 94.93)
**Fits but unsupported** · gap +97.7% → -6.4% · 20 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0034`, `B0046`, `B0047`, `B0048`, `B0049` (5 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `100`
- Config: `lr_schedule` naive `const`, changed to `inv`
- Command:

  Replay: fork checkpoint `a8f55fc3-db15-491e-b4ef-ae73076c5fd8` and run
  ```
  RUN_TAG=3ee8523e84b5 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 100 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 94.45, 90.52, 83.77, 88.88, 77.36; gap after -6.4%; result checkpoint `e2b2b059-b68e-4f8d-8d81-eb23c630526e`
- Effect: candidate 88.88 minus naive 187.7 = -98.84, 95% bootstrap interval [-107, -84.77] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 94.9 steps, and that its worst seed still balances for 63.9.

- p. 1; value used: `mean_reward` = 94.93 steps (headline claim)

### What did we measure?
- Naive median 187.7 over 5 runs; repeats: 190.8, 173.7, 187.7, 191.4, 172.4
- Spread: range 172.4 to 191.4, noise band ±7.32 (2 x MAD), CV 5.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +97.7% (noise band ±7.7% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is +39.7% (it comes back)
- FAIL · Counterfactual (reversal test): without `lr_schedule` the gap is +4.3% (it did NOT come back)
- PASS · Held-out claim: C2: +100.1% to -54.0% (not worse beyond noise)
- PASS · Evidence: `max_steps=100`: paper states '100'
- FAIL · Evidence: `lr_schedule=inv`: no evidence mentions 'inv'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -98.84 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `max_steps_evaluation`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=20` (2.44 noise units, gap -78.9%); `lr_schedule=linear` (2.42 noise units, gap +79.1%)
- Near alternatives (closest across all claims):
  - `max_steps=100`, `lr_schedule=linear`: this claim +2.7%, mean |gap| 26.0% (5 runs)
  - `max_steps=100`: this claim +4.3%, mean |gap| 26.3% (6 runs)
  - `lr_schedule=inv`, `max_steps=2000`: this claim +48.2%, mean |gap| 46.5% (5 runs)

### History matching (every measured configuration, all claims together)
- 3 of 20 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `max_steps`: max_steps=100 (max I 0.7)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=100 (max I 0.76); lr_schedule=inv, max_steps=100 (max I 1.27)
- Equally good values: `lr_schedule` in {inv, linear}

Notes:
- equally good values within one noise band (measured): lr_schedule in {inv, linear}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=100`, `lr_schedule=linear` | 5 | +2.7% | +49.2% | 26.0% |
| `max_steps=100` | 6 | +4.3% | +48.3% | 26.3% |
| `max_steps=100`, `lr_schedule=inv` | 5 | -6.4% | -54.0% | 30.2% |
| `lr_schedule=inv`, `max_steps=2000` | 5 | +48.2% | -44.8% | 46.5% |
| `max_steps=400`, `lr_schedule=inv` | 5 | +62.3% | -33.9% | 48.1% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `max_steps_evaluation`

## Provenance
- GapFinder commit: `b05f7288e1a4df8af69bb0b5e7633827b4cb46c3` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
