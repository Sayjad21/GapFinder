# Gap Report: test-gen-05

Artifact `rlbench` · generated 2026-10-12 23:32 · 26 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Explained | +909.0% | +43.7% | ±86.6% | `eps_start=0.1`, `lr_schedule=inv` |

## C1: mean_reward (paper 17.31)
**Explained** · gap +909.0% → +43.7% · 5 hypotheses tested
> Interacting factors: these changes close the gap only together, and every check passes

### Which experiment changed it?
- Branch: `B0022`, `B0023`, `B0024`, `B0025`, `B0026` (5 run(s) of the same config)
- Config: `eps_start` naive `1.0`, changed to `0.1`
- Config: `lr_schedule` naive `const`, changed to `inv`
- Command:

  Replay: fork checkpoint `f02529f5-4118-4e75-a837-4f2681fdf309` and run
  ```
  RUN_TAG=4c099bd1d865 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_start 0.1 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 38.38, 16.23, 24.88, 30.02, 21.16; gap after +43.7%; result checkpoint `3f88fa86-4bff-4eac-92bd-97ebbf2f6a8d`
- Effect: candidate 24.88 minus naive 174.7 = -149.8, 95% bootstrap interval [-165.5, -138.2] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 17.3 steps, and that its worst seed still balances for 9.1.

- p. 1; value used: `mean_reward` = 17.31 steps (headline claim)

### What did we measure?
- Naive median 174.7 over 5 runs; repeats: 182.1, 159.4, 171.7, 174.7, 198.7
- Spread: range 159.4 to 198.7, noise band ±14.99 (2 x MAD), CV 8.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +909.0% (noise band ±86.6% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is -149.8 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.5` (4.3 noise units, gap +536.4%)
- Near alternatives (closest across all claims):
  - `eps_start=0.1`: this claim +221.2%, mean |gap| 111.1% (5 runs)
  - `eps_start=0.5`: this claim +704.7%, mean |gap| 395.5% (5 runs)
  - `lr_schedule=inv`: this claim +758.5%, mean |gap| 582.0% (5 runs)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `eps_start=0.1`, `lr_schedule=inv` | 5 | +43.7% | +2.2% | 23.0% |
| `eps_start=0.1` | 5 | +221.2% | +1.1% | 111.1% |
| `eps_start=0.5` | 5 | +704.7% | +86.3% | 395.5% |
| `lr_schedule=inv` | 5 | +758.5% | +405.5% | 582.0% |
| naive (reproduction as run) | 5 | +909.0% | +1099.5% | 1004.2% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `--out`

## Provenance
- GapFinder commit: `3d2d8ffc197c61d8150e49495d04eba92f7729de` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `3ed579043c7744915af32f075a3f319861ab223a18631caf42c5504685066d93`
- Cost: Nemotron billed $0.0412, sandbox reported $0.0000 (total $0.0412; this search; ledger extraction is included only if it shared the search's router)
