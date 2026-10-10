# Gap Report: test-gen-05

Artifact `rlbench` · generated 2026-10-10 21:17 · 21 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +912.1% | +353.5% | ±153.1% | `eps_start=0.5`, `lr_schedule=inv` |

## C1: mean_reward (paper 17.31)
**Fits but unsupported** · gap +912.1% → +353.5% · 4 hypotheses tested
> Interacting factors: these changes close the gap only together, and not every check passes

### Which experiment changed it?
- Branch: `B0017`, `B0018`, `B0019`, `B0020`, `B0021` (5 run(s) of the same config)
- Config: `eps_start` naive `1.0`, changed to `0.5`
- Config: `lr_schedule` naive `const`, changed to `inv`
- Command:

  Replay: fork checkpoint `38904c78-4c44-4a5e-b008-4f7a14c2517f` and run
  ```
  RUN_TAG=267efc6331fd "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule inv --eps_start 0.5 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 65.07, 60.6, 103.3, 105.6, 78.5; gap after +353.5%; result checkpoint `5d49c49f-b234-4a0e-bc84-05bc17689062`
- Effect: candidate 78.5 minus naive 175.2 = -96.69, 95% bootstrap interval [-112.2, -67.77] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 17.3 steps, and that its worst seed still balances for 9.1.

- p. 1; value used: `mean_reward` = 17.31 steps (headline claim)

### What did we measure?
- Naive median 175.2 over 5 runs; repeats: 175.2, 145.9, 165.5, 191.5, 188.4
- Spread: range 145.9 to 191.5, noise band ±26.5 (2 x MAD), CV 10.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +912.1% (noise band ±153.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `eps_start` the gap is +690.0% (it comes back)
- PASS · Counterfactual (reversal test): without `lr_schedule` the gap is +543.7% (it comes back)
- PASS · Held-out claim: C2: +461.5% to +13.7% (not worse beyond noise)
- FAIL · Evidence: `eps_start=0.5`: no evidence mentions '0.5'; it fits, but nothing says the authors used it
- FAIL · Evidence: `lr_schedule=inv`: no evidence mentions 'inv'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -96.69 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `theta_clip_min`, `theta_clip_max`, `omega_clip_min`, `omega_clip_max`, `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `RUN_TAG`, `eps_decay_frequency`, `Python_version`, `eval_unseen_default`, `discretisation_mapping`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives (closest across all claims):
  - `eps_start=0.5`: this claim +543.7%, mean |gap| 305.6% (5 runs)
  - `lr_schedule=inv`: this claim +690.0%, mean |gap| 477.4% (5 runs)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `lr_schedule=inv`, `eps_start=0.5` | 5 | +353.5% | +13.7% | 183.6% |
| `eps_start=0.5` | 5 | +543.7% | +67.6% | 305.6% |
| `lr_schedule=inv` | 5 | +690.0% | +264.8% | 477.4% |
| naive (reproduction as run) | 5 | +912.1% | +461.5% | 686.8% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `theta_clip_min`, `theta_clip_max`, `omega_clip_min`, `omega_clip_max`, `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `RUN_TAG`, `eps_decay_frequency`, `Python_version`, `eval_unseen_default`, `discretisation_mapping`

## Provenance
- GapFinder commit: `fb04d3a1ab0b0fec0acc5b342103e9444806727c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `3ed579043c7744915af32f075a3f319861ab223a18631caf42c5504685066d93`
- Cost: Nemotron billed $0.0520, sandbox reported $0.0000 (total $0.0520; this search; ledger extraction is included only if it shared the search's router)
