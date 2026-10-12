# Gap Report: test-gen-05

Artifact `rlbench` · generated 2026-10-13 00:08 · 30 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +886.0% | +35.9% | ±60.6% | `eps_start=0.0` |

## C1: mean_reward (paper 17.31)
**Fits but unsupported** · gap +886.0% → +35.9% · 5 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0009`, `B0022`, `B0023`, `B0024`, `B0025` (5 run(s) of the same config)
- Config: `eps_start` naive `1.0`, changed to `0.0`
- Command:

  Replay: fork checkpoint `85eefc9f-0f65-446f-ae33-ef6e7c7afdad` and run
  ```
  RUN_TAG=a8df1870b1a5 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 0.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 17.5, 43.46, 10.36, 28.95, 23.52; gap after +35.9%; result checkpoint `1f7ef731-93b5-4e9c-87c5-d9b6f1d5081c`
- Effect: candidate 23.52 minus naive 170.7 = -147.2, 95% bootstrap interval [-159.9, -130.5] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 17.3 steps, and that its worst seed still balances for 9.1.

- p. 1, Figure 1; value used: `mean_reward` = 17.31 steps (headline claim)

### What did we measure?
- Naive median 170.7 over 5 runs; repeats: 149.8, 175.9, 165.5, 170.7, 189.8
- Spread: range 149.8 to 189.8, noise band ±10.49 (2 x MAD), CV 8.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +886.0% (noise band ±60.6% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `eps_start` the gap is +886.0% (it comes back)
- PASS · Held-out claim: C2: +585.7% to +1.1% (not worse beyond noise)
- FAIL · Evidence: `eps_start=0.0`: evidence gate off: no evidence was looked for
- PASS · Effect vs noise: candidate minus naive is -147.2 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=inv` (6.27 noise units, gap +506.2%); `eps_start=0.5` (1.6 noise units, gap +789.1%)
- Near alternatives (closest across all claims):
  - `eps_start=0.0`, `lr_schedule=inv`: this claim -25.8%, mean |gap| 13.7% (5 runs)
  - `eps_start=0.5`: this claim +691.2%, mean |gap| 381.3% (5 runs)
  - `lr_schedule=inv`: this claim +667.2%, mean |gap| 478.4% (5 runs)

Notes:
- evidence gate off: no evidence was checked, so this cannot be labelled Explained

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `eps_start=0.0`, `lr_schedule=inv` | 5 | -25.8% | +1.6% | 13.7% |
| `eps_start=0.0` | 5 | +35.9% | +1.1% | 18.5% |
| `eps_start=0.5` | 5 | +691.2% | +71.4% | 381.3% |
| `lr_schedule=inv` | 5 | +667.2% | +289.6% | 478.4% |
| naive (reproduction as run) | 5 | +886.0% | +585.7% | 735.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `2e9291c6be5f4b9ffe219d44dfe2904a7d2d6a9f` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `3ed579043c7744915af32f075a3f319861ab223a18631caf42c5504685066d93`
- Cost: Nemotron billed $0.0363, sandbox reported $0.0000 (total $0.0363; this search; ledger extraction is included only if it shared the search's router)
