# Gap Report: test-gen-05

Artifact `rlbench` · generated 2026-10-10 21:17 · 15 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +839.7% | +99.4% | ±77.2% | `eps_start=0.1` |

## C1: mean_reward (paper 17.31)
**Fits but unsupported** · gap +839.7% → +99.4% · 2 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0007`, `B0012`, `B0013`, `B0014`, `B0015` (5 run(s) of the same config)
- Config: `eps_start` naive `1.0`, changed to `0.1`
- Command:

  Replay: fork checkpoint `e75d2350-acf2-45ce-b03f-da029dd36085` and run
  ```
  RUN_TAG=4fe0d1b341d0 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 0.1 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 41.15, 10.76, 34.51, 74.31, 26.48; gap after +99.4%; result checkpoint `fd8b899b-3a2d-4c87-a243-da5f24690293`
- Effect: candidate 34.51 minus naive 162.7 = -128.2, 95% bootstrap interval [-147.7, -107.4] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 17.3 steps, and that its worst seed still balances for 9.1.

- p. 1; value used: `mean_reward` = 17.31 steps (headline claim)

### What did we measure?
- Naive median 162.7 over 5 runs; repeats: 171.4, 162.7, 159.2, 156, 179.5
- Spread: range 156 to 179.5, noise band ±13.37 (2 x MAD), CV 5.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +839.7% (noise band ±77.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `eps_start` the gap is +839.7% (it comes back)
- PASS · Held-out claim: C2: +344.0% to +2.7% (not worse beyond noise)
- FAIL · Evidence: `eps_start=0.1`: no evidence mentions '0.1'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -128.2 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `CartPole.f`, `CartPole.dt`, `discretise theta bounds`, `discretise omega bounds`, `termination x threshold`, `termination theta threshold`, `reset distribution`, `unseen state Q-values during evaluation`, `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `discretisation formula`, `evaluation policy`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.5` (2.43 noise units, gap +652.0%)
- Near alternatives (closest across all claims):
  - `eps_start=0.5`: this claim +652.0%, mean |gap| 358.9% (5 runs)

Notes:
- skipped lr_schedule='"const"': knob value '"const"' has shell metacharacters
- skipped lr_schedule='"linear"': knob value '"linear"' has shell metacharacters

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `eps_start=0.1` | 5 | +99.4% | +2.7% | 51.1% |
| `eps_start=0.5` | 5 | +652.0% | +65.9% | 358.9% |
| naive (reproduction as run) | 5 | +839.7% | +344.0% | 591.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `CartPole.f`, `CartPole.dt`, `discretise theta bounds`, `discretise omega bounds`, `termination x threshold`, `termination theta threshold`, `reset distribution`, `unseen state Q-values during evaluation`, `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `discretisation formula`, `evaluation policy`

## Provenance
- GapFinder commit: `fb04d3a1ab0b0fec0acc5b342103e9444806727c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `3ed579043c7744915af32f075a3f319861ab223a18631caf42c5504685066d93`
- Cost: Nemotron billed $0.0452, sandbox reported $0.0000 (total $0.0452; this search; ledger extraction is included only if it shared the search's router)
