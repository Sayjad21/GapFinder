# Gap Report: test-gen-03

Artifact `rlbench` · generated 2026-10-10 21:10 · 14 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -42.2% | -7.8% | ±2.4% | `max_steps=500` |

## C1: mean_reward (paper 302.05)
**Fits but unsupported** · gap -42.2% → -7.8% · 5 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0006`, `B0010`, `B0011` (3 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `500`
- Command:

  Replay: fork checkpoint `caee2d27-8881-4bc7-8428-5132f8711459` and run
  ```
  RUN_TAG=453a244413e8 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 500 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 384.7, 278.5, 258.6; gap after -7.8%; result checkpoint `46f308b3-339f-45e4-a40a-9140ad909c31`
- Effect: candidate 278.5 minus naive 174.4 = +104.1, 95% bootstrap interval [+87.47, +212.8] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 302.1 steps, and that its worst seed still balances for 48.2.

- p. 1; value used: `mean_reward` = 302.05 steps (headline claim)

### What did we measure?
- Naive median 174.4 over 5 runs; repeats: 164, 164.4, 175.3, 178.1, 174.4
- Spread: range 164 to 178.1, noise band ±7.25 (2 x MAD), CV 3.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -42.2% (noise band ±2.4% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -42.2% (it comes back)
- PASS · Held-out claim: C2: -61.8% to -62.1% (not worse beyond noise)
- FAIL · Evidence: `max_steps=500`: no evidence mentions '500'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +104.1 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `hardcoded:cartpole_physics`, `RL_SEED_BASE`, `RUN_TAG`, `hardcoded:eval_greedy_policy`, `--out`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=1000` (9.4 noise units, gap +19.7%)
- Near alternatives (closest across all claims):
  - `max_steps=1000`: this claim +19.7%, mean |gap| 13.6% (3 runs)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=1000` | 3 | +19.7% | +7.6% | 13.6% |
| `max_steps=500` | 3 | -7.8% | -62.1% | 34.9% |
| naive (reproduction as run) | 5 | -42.2% | -61.8% | 52.0% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `lr_schedule=constant`: invalid_value, The program's argument parser only accepts 'const', 'linear', or 'inv' for --lr_schedule; the supplied value 'constant' is not among these choices, causing an invalid choice error

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `hardcoded:cartpole_physics`, `RL_SEED_BASE`, `RUN_TAG`, `hardcoded:eval_greedy_policy`, `--out`

## Provenance
- GapFinder commit: `fb04d3a1ab0b0fec0acc5b342103e9444806727c` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `3ed579043c7744915af32f075a3f319861ab223a18631caf42c5504685066d93`
- Cost: Nemotron billed $0.0429, sandbox reported $0.0000 (total $0.0429; this search; ledger extraction is included only if it shared the search's router)
