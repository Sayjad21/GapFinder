# Gap Report: test-gen-03

Artifact `rlbench` · generated 2026-10-10 23:16 · 14 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -37.9% | +20.0% | ±4.5% | `max_steps=500` |

## C1: mean_reward (paper 302.05)
**Fits but unsupported** · gap -37.9% → +20.0% · 5 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0008`, `B0010`, `B0011`, `B0012`, `B0013` (5 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `500`
- Command:

  Replay: fork checkpoint `9f665a11-15e3-4962-9259-993b3d6a0f79` and run
  ```
  RUN_TAG=ed923bad1019 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 500 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 231.7, 401, 425.5, 252.2, 362.5; gap after +20.0%; result checkpoint `a0711c6c-d2f2-498b-917d-297a09e0ed56`
- Effect: candidate 362.5 minus naive 187.7 = +174.8, 95% bootstrap interval [+77.17, +217.6] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 302.1 steps, and that its worst seed still balances for 48.2.

- p. 1, Figure 1; value used: `mean_reward` = 302.05 (headline claim)

### What did we measure?
- Naive median 187.7 over 5 runs; repeats: 184.3, 198.3, 194.4, 168.8, 187.7
- Spread: range 168.8 to 198.3, noise band ±13.53 (2 x MAD), CV 6.1%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -37.9% (noise band ±4.5% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -37.9% (it comes back)
- PASS · Held-out claim: C2: +59.0% to +31.8% (not worse beyond noise)
- FAIL · Evidence: `max_steps=500`: no evidence mentions '500'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +174.8 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `hardcoded:cartpole_g`, `hardcoded:cartpole_mc`, `hardcoded:cartpole_mp`, `hardcoded:cartpole_l`, `hardcoded:cartpole_f`, `hardcoded:cartpole_dt`, `hardcoded:theta_clip_min`, `hardcoded:theta_clip_max`, `hardcoded:x_threshold`, `hardcoded:theta_threshold`, `hardcoded:omega_clip_min`, `hardcoded:omega_clip_max`, `hardcoded:seed_generation_method`, `hardcoded:initial_state_noise`, `python_random_module`, `hardcoded:discretization_formula`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): none
- Near alternatives: none recorded

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=500` | 5 | +20.0% | +31.8% | 25.9% |
| naive (reproduction as run) | 5 | -37.9% | +59.0% | 48.4% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `hardcoded:cartpole_g`, `hardcoded:cartpole_mc`, `hardcoded:cartpole_mp`, `hardcoded:cartpole_l`, `hardcoded:cartpole_f`, `hardcoded:cartpole_dt`, `hardcoded:theta_clip_min`, `hardcoded:theta_clip_max`, `hardcoded:x_threshold`, `hardcoded:theta_threshold`, `hardcoded:omega_clip_min`, `hardcoded:omega_clip_max`, `hardcoded:seed_generation_method`, `hardcoded:initial_state_noise`, `python_random_module`, `hardcoded:discretization_formula`

## Provenance
- GapFinder commit: `fb04d3a1ab0b0fec0acc5b342103e9444806727c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `3ed579043c7744915af32f075a3f319861ab223a18631caf42c5504685066d93`
- Cost: Nemotron billed $0.0524, sandbox reported $0.0000 (total $0.0524; this search; ledger extraction is included only if it shared the search's router)
