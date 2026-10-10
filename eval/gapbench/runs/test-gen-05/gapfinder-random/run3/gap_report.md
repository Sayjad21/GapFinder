# Gap Report: test-gen-05

Artifact `rlbench` · generated 2026-10-10 23:22 · 22 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +910.3% | +11.6% | ±151.2% | `eps_start=0.1` |

## C1: mean_reward (paper 17.31)
**Fits but unsupported** · gap +910.3% → +11.6% · 5 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0009`, `B0014`, `B0015`, `B0016`, `B0017` (5 run(s) of the same config)
- Config: `eps_start` naive `1.0`, changed to `0.1`
- Command:

  Replay: fork checkpoint `e03329e6-f902-4bee-b684-a523b9594bc7` and run
  ```
  RUN_TAG=06affeaa2342 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 0.1 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 10.8, 27.08, 19.32, 21.59, 16; gap after +11.6%; result checkpoint `a940ab27-cf2d-4f89-a435-c13b151359c8`
- Effect: candidate 19.32 minus naive 174.9 = -155.6, 95% bootstrap interval [-175.3, -149] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 17.3 steps, and that its worst seed still balances for 9.1.

- p. 1; value used: `mean_reward` = 17.31 steps (headline claim)

### What did we measure?
- Naive median 174.9 over 5 runs; repeats: 161.8, 196.3, 174.9, 173.6, 198
- Spread: range 161.8 to 198, noise band ±26.18 (2 x MAD), CV 8.7%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +910.3% (noise band ±151.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `eps_start` the gap is +910.3% (it comes back)
- PASS · Held-out claim: C2: +662.6% to +2.2% (not worse beyond noise)
- FAIL · Evidence: `eps_start=0.1`: no evidence mentions '0.1'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -155.6 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.5` (3.01 noise units, gap +454.9%)
- Near alternatives (closest across all claims):
  - `eps_start=0.1`, `lr_schedule=inv`: this claim +39.1%, mean |gap| 20.4% (5 runs)
  - `eps_start=0.5`: this claim +670.5%, mean |gap| 368.2% (5 runs)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `eps_start=0.1` | 5 | +11.6% | +2.2% | 6.9% |
| `eps_start=0.1`, `lr_schedule=inv` | 5 | +39.1% | +1.6% | 20.4% |
| `eps_start=0.5` | 5 | +670.5% | +65.9% | 368.2% |
| naive (reproduction as run) | 5 | +910.3% | +662.6% | 786.5% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`

## Provenance
- GapFinder commit: `fb04d3a1ab0b0fec0acc5b342103e9444806727c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `3ed579043c7744915af32f075a3f319861ab223a18631caf42c5504685066d93`
- Cost: Nemotron billed $0.0349, sandbox reported $0.0000 (total $0.0349; this search; ledger extraction is included only if it shared the search's router)
