# Gap Report: test-gen-03

Artifact `rlbench` · generated 2026-10-13 20:58 · 37 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -37.7% | +1.0% | ±2.2% | `max_steps=1000` |

## C1: mean_reward (paper 302.05)
**Fits but unsupported** · gap -37.7% → +1.0% · 12 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0007`, `B0017`, `B0018`, `B0019` (4 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `1000`
- Command:

  Replay: fork checkpoint `24d0c790-7c55-44a2-bd92-7840319008e6` and run
  ```
  RUN_TAG=bc77ae7fece2 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 1000 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 311.4, 651, 299, 209.9; gap after +1.0%; result checkpoint `bfea72d9-c670-4686-8958-41fa5410c3cb`
- Effect: candidate 305.2 minus naive 188 = +117.2, 95% bootstrap interval [+20.57, +466.8] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 302.1 steps, and that its worst seed still balances for 48.2.

- p. 1; value used: `mean_reward` = 302.05 steps (headline claim)

### What did we measure?
- Naive median 188 over 5 runs; repeats: 191.2, 191.3, 183.3, 188, 179.3
- Spread: range 179.3 to 191.3, noise band ±6.59 (2 x MAD), CV 2.8%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -37.7% (noise band ±2.2% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -37.7% (it comes back)
- PASS · Held-out claim: C2: +181.2% to +18.1% (not worse beyond noise)
- FAIL · Evidence: `max_steps=1000`: no evidence mentions '1000'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +117.2 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `evaluation_policy`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=400` (13.12 noise units, gap -9.1%); `max_steps=500` (9.4 noise units, gap +17.2%)
- Near alternatives (closest across all claims):
  - `max_steps=500`: this claim +7.5%, mean |gap| 4.5% (4 runs)
  - `max_steps=2000`: this claim +24.5%, mean |gap| 38.8% (4 runs)
  - `max_steps=400`: this claim -12.5%, mean |gap| 45.7% (4 runs)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=500` | 4 | +7.5% | +1.4% | 4.5% |
| `max_steps=1000` | 4 | +1.0% | +18.1% | 9.6% |
| `max_steps=2000` | 4 | +24.5% | -53.1% | 38.8% |
| `max_steps=400` | 4 | -12.5% | +78.9% | 45.7% |
| `max_steps=100` | 4 | -68.2% | +42.5% | 55.4% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `evaluation_policy`

## Provenance
- GapFinder commit: `c5b1a93e0b25688f10e132758f8a6371b4ebbf19` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `7e8e15007902d4b39f8940e3fb2a13a0e258c9d87b46215a72cd3b65ed9d57d9`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
