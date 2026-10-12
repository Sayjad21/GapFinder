# Gap Report: test-gen-05

Artifact `rlbench` · generated 2026-10-12 23:52 · 26 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | +945.4% | +110.1% | ±85.8% | `eps_start=0.1` |

## C1: mean_reward (paper 17.31)
**Fits but unsupported** · gap +945.4% → +110.1% · 5 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0009`, `B0018`, `B0019`, `B0020`, `B0021` (5 run(s) of the same config)
- Config: `eps_start` naive `1.0`, changed to `0.1`
- Command:

  Replay: fork checkpoint `b3420464-f5c3-4507-a69d-afb1f067705a` and run
  ```
  RUN_TAG=bbb36526aed6 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 0.1 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 200 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 35.31, 29.14, 41.88, 39.2, 36.38; gap after +110.1%; result checkpoint `c259118a-78a3-4524-b2d9-c5ad48b2629f`
- Effect: candidate 36.38 minus naive 181 = -144.6, 95% bootstrap interval [-153.8, -137.1] (5 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 17.3 steps, and that its worst seed still balances for 9.1.

- p. 1; value used: `mean_reward` = 17.31 steps (headline claim)

### What did we measure?
- Naive median 181 over 5 runs; repeats: 182.2, 181, 173.5, 173.1, 196.5
- Spread: range 173.1 to 196.5, noise band ±14.86 (2 x MAD), CV 5.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: +945.4% (noise band ±85.8% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `eps_start` the gap is +945.4% (it comes back)
- PASS · Held-out claim: C2: +657.7% to -0.5% (not worse beyond noise)
- FAIL · Evidence: `eps_start=0.1`: no evidence mentions '0.1'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is -144.6 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RL_SEED_BASE`, `RUN_TAG`, `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `x_threshold`, `theta_threshold`, `init_range_low`, `init_range_high`, `theta_clip_low`, `theta_clip_high`, `omega_clip_low`, `omega_clip_high`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `eps_start=0.5` (5.05 noise units, gap +512.0%); `lr_schedule=inv` (2.81 noise units, gap +704.6%)
- Near alternatives (closest across all claims):
  - `eps_start=0.1`, `lr_schedule=inv`: this claim +135.2%, mean |gap| 68.1% (5 runs)
  - `eps_start=0.5`: this claim +520.0%, mean |gap| 293.0% (5 runs)
  - `lr_schedule=inv`: this claim +570.8%, mean |gap| 321.4% (5 runs)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `eps_start=0.1` | 5 | +110.1% | -0.5% | 55.3% |
| `eps_start=0.1`, `lr_schedule=inv` | 5 | +135.2% | +1.1% | 68.1% |
| `eps_start=0.5` | 5 | +520.0% | +65.9% | 293.0% |
| `lr_schedule=inv` | 5 | +570.8% | +72.0% | 321.4% |
| naive (reproduction as run) | 5 | +945.4% | +657.7% | 801.6% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RL_SEED_BASE`, `RUN_TAG`, `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `x_threshold`, `theta_threshold`, `init_range_low`, `init_range_high`, `theta_clip_low`, `theta_clip_high`, `omega_clip_low`, `omega_clip_high`

## Provenance
- GapFinder commit: `2e9291c6be5f4b9ffe219d44dfe2904a7d2d6a9f` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `3ed579043c7744915af32f075a3f319861ab223a18631caf42c5504685066d93`
- Cost: Nemotron billed $0.0536, sandbox reported $0.0000 (total $0.0536; this search; ledger extraction is included only if it shared the search's router)
