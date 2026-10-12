# Gap Report: test-gen-05

Artifact `rlbench` · generated 2026-10-13 00:10 · 30 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +951.6% | +17.6% | ±85.9% | `eps_start=0.1`, `lr_schedule=inv` |

## C1: mean_reward (paper 17.31)
**Fits but unsupported** · gap +951.6% → +17.6% · 5 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0026`, `B0027`, `B0028`, `B0029`, `B0030` (5 run(s) of the same config)
- Config: `eps_start` naive `1.0`, changed to `0.1`
- Config: `lr_schedule` naive `const`, changed to `inv`
- Command:

  Replay: fork checkpoint `beebd481-a858-4b1c-8af0-bccb9a967ac5` and run
  ```
  RUN_TAG=8f41eabec6d6 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_start 0.1 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 24.09, 20.36, 40.25, 10.16, 18.66; gap after +17.6%; result checkpoint `df71a150-6d9b-4e0c-936c-b84db8c38b86`
- Effect: candidate 20.36 minus naive 182 = -161.7, 95% bootstrap interval [-172.3, -143.1] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 17.3 steps, and that its worst seed still balances for 9.1.

- p. 1; value used: `mean_reward` = 17.31 steps (headline claim)

### What did we measure?
- Naive median 182 over 5 runs; repeats: 198.2, 156.7, 189.5, 179.6, 182
- Spread: range 156.7 to 198.2, noise band ±14.87 (2 x MAD), CV 8.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +951.6% (noise band ±85.9% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `eps_start` the gap is +648.2% (it comes back)
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is +116.9% (it comes back)
- PASS · Held-out claim: C2: +742.9% to +0.0% (not worse beyond noise)
- FAIL · Evidence: `eps_start=0.1`: evidence gate off: no evidence was looked for
- FAIL · Evidence: `lr_schedule=inv`: evidence gate off: no evidence was looked for
- PASS · Effect vs noise: candidate minus naive is -161.7 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.5` (2.23 noise units, gap +759.9%)
- Near alternatives (closest across all claims):
  - `eps_start=0.1`: this claim +116.9%, mean |gap| 59.0% (5 runs)
  - `eps_start=0.5`: this claim +741.5%, mean |gap| 399.9% (5 runs)
  - `lr_schedule=inv`: this claim +648.2%, mean |gap| 468.6% (5 runs)

Notes:
- evidence gate off: no evidence was checked, so this cannot be labelled Explained

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv`, `eps_start=0.1` | 5 | +17.6% | +0.0% | 8.8% |
| `eps_start=0.1` | 5 | +116.9% | +1.1% | 59.0% |
| `eps_start=0.5` | 5 | +741.5% | +58.2% | 399.9% |
| `lr_schedule=inv` | 5 | +648.2% | +289.0% | 468.6% |
| naive (reproduction as run) | 5 | +951.6% | +742.9% | 847.2% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `--out`

## Provenance
- GapFinder commit: `2e9291c6be5f4b9ffe219d44dfe2904a7d2d6a9f` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `3ed579043c7744915af32f075a3f319861ab223a18631caf42c5504685066d93`
- Cost: Nemotron billed $0.0560, sandbox reported $0.0000 (total $0.0560; this search; ledger extraction is included only if it shared the search's router)
