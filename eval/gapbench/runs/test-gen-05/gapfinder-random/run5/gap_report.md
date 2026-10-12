# Gap Report: test-gen-05

Artifact `rlbench` · generated 2026-10-12 23:51 · 30 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +911.3% | +83.5% | ±44.1% | `eps_start=0.1`, `lr_schedule=inv` |

## C1: mean_reward (paper 17.31)
**Fits but unsupported** · gap +911.3% → +83.5% · 5 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0026`, `B0027`, `B0028`, `B0029`, `B0030` (5 run(s) of the same config)
- Config: `eps_start` naive `1.0`, changed to `0.1`
- Config: `lr_schedule` naive `const`, changed to `inv`
- Command:

  Replay: fork checkpoint `f05be09e-0d07-4f1d-9ffe-8c61a7005282` and run
  ```
  RUN_TAG=e3a0a0d8de23 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_start 0.1 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 41.26, 14.62, 33.73, 24.41, 31.77; gap after +83.5%; result checkpoint `949a9995-3560-473f-9bce-8fdfa7d6debf`
- Effect: candidate 31.77 minus naive 175.1 = -143.3, 95% bootstrap interval [-154.8, -132.2] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 17.3 steps, and that its worst seed still balances for 9.1.

- p. 1; value used: `mean_reward` = 17.31 steps (headline claim)

### What did we measure?
- Naive median 175.1 over 5 runs; repeats: 178.9, 175.1, 182.4, 174.3, 155.4
- Spread: range 155.4 to 182.4, noise band ±7.64 (2 x MAD), CV 6.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +911.3% (noise band ±44.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `eps_start` the gap is +728.0% (it comes back)
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is +156.1% (it comes back)
- PASS · Held-out claim: C2: +431.9% to -0.5% (not worse beyond noise)
- FAIL · Evidence: `eps_start=0.1`: no evidence mentions '0.1'; it fits, but nothing says the authors used it
- FAIL · Evidence: `lr_schedule=inv`: no evidence mentions 'inv'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -143.3 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole.g`, `CartPole.dt`, `CartPole.f`, `RL_SEED_BASE`, `discretise theta bounds`, `discretise omega bounds`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `RUN_TAG`, `seed generation method`, `evaluation policy`, `python random module`, `reward scaling during training`, `Q-table initialization per state`, `episode termination condition`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.5` (2.47 noise units, gap +802.4%); `lr_schedule=linear` (1.4 noise units, gap +849.5%)
- Near alternatives (closest across all claims):
  - `eps_start=0.1`: this claim +156.1%, mean |gap| 79.1% (5 runs)
  - `eps_start=0.5`: this claim +666.5%, mean |gap| 371.4% (5 runs)
  - `lr_schedule=inv`: this claim +728.0%, mean |gap| 504.4% (5 runs)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `eps_start=0.1`, `lr_schedule=inv` | 5 | +83.5% | -0.5% | 42.0% |
| `eps_start=0.1` | 5 | +156.1% | +2.2% | 79.1% |
| `eps_start=0.5` | 5 | +666.5% | +76.4% | 371.4% |
| `lr_schedule=inv` | 5 | +728.0% | +280.8% | 504.4% |
| naive (reproduction as run) | 5 | +911.3% | +431.9% | 671.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole.g`, `CartPole.dt`, `CartPole.f`, `RL_SEED_BASE`, `discretise theta bounds`, `discretise omega bounds`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `RUN_TAG`, `seed generation method`, `evaluation policy`, `python random module`, `reward scaling during training`, `Q-table initialization per state`, `episode termination condition`

## Provenance
- GapFinder commit: `2e9291c6be5f4b9ffe219d44dfe2904a7d2d6a9f` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `3ed579043c7744915af32f075a3f319861ab223a18631caf42c5504685066d93`
- Cost: Nemotron billed $0.0408, sandbox reported $0.0000 (total $0.0408; this search; ledger extraction is included only if it shared the search's router)
