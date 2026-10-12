# Gap Report: test-gen-05

Artifact `rlbench` · generated 2026-10-12 23:32 · 18 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Partially explained | +971.5% | +352.3% | ±72.4% | `eps_start=0.5`, `lr_schedule=inv` |

## C1: mean_reward (paper 17.31)
**Partially explained** · gap +971.5% → +352.3% · 5 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0016`, `B0017`, `B0018` (3 run(s) of the same config)
- Config: `eps_start` naive `1.0`, changed to `0.5`
- Config: `lr_schedule` naive `const`, changed to `inv`
- Command:

  Replay: fork checkpoint `b33ad0ea-722e-4a47-9e1f-b87847ae1d02` and run
  ```
  RUN_TAG=6b62c081a803 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_start 0.5 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 78.3, 78.31, 76.45; gap after +352.3%; result checkpoint `787a9059-ee65-42c1-9e8f-1551635aa882`
- Effect: candidate 78.3 minus naive 185.5 = -107.2, 95% bootstrap interval [-113.8, -103.4] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 17.3 steps

- p. 1; value used: `mean_reward` = 17.31 steps (headline claim)

### What did we measure?
- Naive median 185.5 over 5 runs; repeats: 193.5, 179.2, 192.8, 180.6, 185.5
- Spread: range 179.2 to 193.5, noise band ±12.53 (2 x MAD), CV 3.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +971.5% (noise band ±72.4% of the paper value)

### Why do we believe it?
- NOT CHECKED · Counterfactual (reversal test): no reversal test recorded
- NOT CHECKED · Held-out claim: no held-out claims were checked
- NOT CHECKED · Evidence: no evidence check recorded
- PASS · Effect vs noise: candidate minus naive is -107.2 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `lr_schedule=linear` (1.18 noise units, gap +886.0%)
- Near alternatives (closest across all claims):
  - `eps_start=0.5`: this claim +457.1%, mean |gap| 269.5% (3 runs)
  - `lr_schedule=inv`: this claim +698.4%, mean |gap| 494.2% (3 runs)
  - `lr_schedule=linear`: this claim +893.7%, mean |gap| 1172.7% (3 runs)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv`, `eps_start=0.5` | 3 | +352.3% | +27.5% | 189.9% |
| `eps_start=0.5` | 3 | +457.1% | +81.9% | 269.5% |
| `lr_schedule=inv` | 3 | +698.4% | +290.1% | 494.2% |
| naive (reproduction as run) | 5 | +971.5% | +654.4% | 812.9% |
| `lr_schedule=linear` | 3 | +893.7% | +1451.6% | 1172.7% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`

## Provenance
- GapFinder commit: `79ea3e394df6e4dd60d6d56f69f3b468cfa04d26` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `3ed579043c7744915af32f075a3f319861ab223a18631caf42c5504685066d93`
- Cost: Nemotron billed $0.0346, sandbox reported $0.0000 (total $0.0346; this search; ledger extraction is included only if it shared the search's router)
