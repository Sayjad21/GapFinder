# Gap Report: test-gen-05

Artifact `rlbench` · generated 2026-10-10 23:44 · 20 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +1018.9% | +125.9% | ±33.0% | `eps_start=0.1` |

## C1: mean_reward (paper 17.31)
**Fits but unsupported** · gap +1018.9% → +125.9% · 5 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0007`, `B0012`, `B0013` (3 run(s) of the same config)
- Config: `eps_start` naive `1.0`, changed to `0.1`
- Command:

  Replay: fork checkpoint `baf08728-886c-4e64-b22a-f804a08c1ec9` and run
  ```
  RUN_TAG=e4d4742639c2 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 0.1 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 39.11, 21.88, 73.89; gap after +125.9%; result checkpoint `ea1c9f44-0156-4eb5-b927-97c567ef8917`
- Effect: candidate 39.11 minus naive 193.7 = -154.6, 95% bootstrap interval [-169.7, -119.5] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 17.3 steps, and that its worst seed still balances for 9.1.

- p. 1, Figure 1; value used: `mean_reward` = 17.31 steps (headline claim)

### What did we measure?
- Naive median 193.7 over 5 runs; repeats: 200, 196, 179.2, 193.7, 190.8
- Spread: range 179.2 to 200, noise band ±5.71 (2 x MAD), CV 4.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +1018.9% (noise band ±33.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `eps_start` the gap is +1018.9% (it comes back)
- PASS · Held-out claim: C2: +1725.8% to -1.1% (not worse beyond noise)
- FAIL · Evidence: `eps_start=0.1`: evidence gate off: no evidence was looked for
- PASS · Effect vs noise: candidate minus naive is -154.6 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `CartPole.x_threshold`, `CartPole.theta_threshold`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.5` (18.65 noise units, gap +403.6%); `lr_schedule=inv` (9.55 noise units, gap +703.8%); `lr_schedule=linear` (4.08 noise units, gap +884.4%)
- Near alternatives (closest across all claims):
  - `eps_start=0.1`, `lr_schedule=inv`: this claim +27.0%, mean |gap| 14.0% (3 runs)
  - `eps_start=0.5`: this claim +625.6%, mean |gap| 364.2% (3 runs)
  - `lr_schedule=inv`: this claim +679.1%, mean |gap| 372.8% (3 runs)

Notes:
- evidence gate off: no evidence was checked, so this cannot be labelled Explained

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `eps_start=0.1`, `lr_schedule=inv` | 3 | +27.0% | +1.1% | 14.0% |
| `eps_start=0.1` | 3 | +125.9% | -1.1% | 63.5% |
| `eps_start=0.5` | 3 | +625.6% | +102.7% | 364.2% |
| `lr_schedule=inv` | 3 | +679.1% | +66.5% | 372.8% |
| `lr_schedule=linear` | 3 | +884.4% | +1437.4% | 1160.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `CartPole.x_threshold`, `CartPole.theta_threshold`

## Provenance
- GapFinder commit: `fb04d3a1ab0b0fec0acc5b342103e9444806727c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `3ed579043c7744915af32f075a3f319861ab223a18631caf42c5504685066d93`
- Cost: Nemotron billed $0.0499, sandbox reported $0.0000 (total $0.0499; this search; ledger extraction is included only if it shared the search's router)
