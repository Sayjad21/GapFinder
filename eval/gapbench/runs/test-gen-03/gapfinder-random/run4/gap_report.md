# Gap Report: test-gen-03

Artifact `rlbench` · generated 2026-10-12 23:45 · 26 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -40.5% | -4.2% | ±2.1% | `max_steps=500` |

## C1: mean_reward (paper 302.05)
**Fits but unsupported** · gap -40.5% → -4.2% · 11 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0011`, `B0015`, `B0016` (3 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `500`
- Command:

  Replay: fork checkpoint `1021023f-2cec-4509-b257-890f902c1f9c` and run
  ```
  RUN_TAG=52248b5af45a "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 500 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 257.3, 289.4, 308.4; gap after -4.2%; result checkpoint `f1dca081-f286-4f0a-86ef-213a3e14d381`
- Effect: candidate 289.4 minus naive 179.7 = +109.7, 95% bootstrap interval [+77.88, +127.7] (3 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 302.1 steps, and that its worst seed still balances for 48.2.

- p. 1; value used: `mean_reward` = 302.05 steps (headline claim)

### What did we measure?
- Naive median 179.7 over 5 runs; repeats: 182.8, 178.5, 173.1, 184.3, 179.7
- Spread: range 173.1 to 184.3, noise band ±6.22 (2 x MAD), CV 2.4%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -40.5% (noise band ±2.1% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -40.5% (it comes back)
- PASS · Held-out claim: C2: +13.8% to -1.8% (not worse beyond noise)
- FAIL · Evidence: `max_steps=500`: no evidence mentions '500'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +109.7 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `CartPole physics constants (g, mc, mp, l, f, dt)`, `discretization bounds (theta_clamp, omega_clamp)`, `termination angle threshold`, `RL_SEED_BASE`, `RUN_TAG`, `CartPole termination position threshold`, `Python random.Random implementation`, `discretization formula`, `CartPole force magnitude (f)`, `CartPole gravity (g)`, `CartPole time step (dt)`, `Q-learning target calculation (done handling)`, `epsilon decay timing (per episode vs per step)`, `evaluation uses greedy policy (no epsilon)`, `initial state distribution (uniform [-0.05, 0.05])`, `CartPole cart mass (mc) and pole mass (mp)`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `init_q=1.0` (2.06 noise units, gap -36.3%); `init_q=0.001` (1.73 noise units, gap -37.0%)
- Near alternatives (closest across all claims):
  - `max_steps=500`, `init_q=0.001`: this claim -22.2%, mean |gap| 18.6% (3 runs)
  - `max_steps=500`, `init_q=1.0`: this claim -25.7%, mean |gap| 18.8% (3 runs)
  - `init_q=1.0`: this claim -40.2%, mean |gap| 65.2% (3 runs)

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=500` | 3 | -4.2% | -1.8% | 3.0% |
| `max_steps=500`, `init_q=0.001` | 3 | -22.2% | +14.9% | 18.6% |
| `max_steps=500`, `init_q=1.0` | 3 | -25.7% | +11.9% | 18.8% |
| naive (reproduction as run) | 5 | -40.5% | +13.8% | 27.1% |
| `init_q=1.0` | 3 | -40.2% | +90.2% | 65.2% |

## Failed hypotheses (triaged by Nemotron 3 Super)
- `init_q=zero`: invalid_value, The argument --init_q expects a floating‑point number; the string 'zero' is not a valid float, causing the parser to reject it; retried as `init_q=0.001`

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `CartPole physics constants (g, mc, mp, l, f, dt)`, `discretization bounds (theta_clamp, omega_clamp)`, `termination angle threshold`, `RL_SEED_BASE`, `RUN_TAG`, `CartPole termination position threshold`, `Python random.Random implementation`, `discretization formula`, `CartPole force magnitude (f)`, `CartPole gravity (g)`, `CartPole time step (dt)`, `Q-learning target calculation (done handling)`, `epsilon decay timing (per episode vs per step)`, `evaluation uses greedy policy (no epsilon)`, `initial state distribution (uniform [-0.05, 0.05])`, `CartPole cart mass (mc) and pole mass (mp)`

## Provenance
- GapFinder commit: `2e9291c6be5f4b9ffe219d44dfe2904a7d2d6a9f` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `3ed579043c7744915af32f075a3f319861ab223a18631caf42c5504685066d93`
- Cost: Nemotron billed $0.1341, sandbox reported $0.0000 (total $0.1341; this search; ledger extraction is included only if it shared the search's router)
