# Gap Report: test-gen-03

Artifact `rlbench` · generated 2026-10-15 20:53 · 75 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -39.0% | -5.3% | ±4.3% | `max_steps=400` |

## C1: mean_reward (paper 302.05)
**Fits but unsupported** · gap -39.0% → -5.3% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0014`, `B0030`, `B0031`, `B0039` (4 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `400`
- Command:

  Replay: fork checkpoint `9ff6436b-3027-4c22-9c12-679befc4a7e7` and run
  ```
  RUN_TAG=acb9bc4756f8 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 400 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 286.8, 285.3, 259.5, 309; gap after -5.3%; result checkpoint `8464d3b2-bcc7-4d2d-a2d9-b43fbabefad7`
- Effect: candidate 286 minus naive 184.2 = +101.8, 95% bootstrap interval [+69.94, +126.9] (4 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 302.1 steps, and that its worst seed still balances for 48.2.

- p. 1; value used: `mean_reward` = 302.05 steps (headline claim)

### What did we measure?
- Naive median 184.2 over 5 runs; repeats: 182.3, 184.2, 177.7, 190.6, 194.5
- Spread: range 177.7 to 194.5, noise band ±12.84 (2 x MAD), CV 3.6%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -39.0% (noise band ±4.3% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -39.0% (it comes back)
- PASS · Held-out claim: C2: +36.9% to +12.6% (not worse beyond noise)
- FAIL · Evidence: `max_steps=400`: no evidence mentions '400'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +101.8 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `evaluation_policy`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=1000` (7.08 noise units, gap +8.9%); `max_steps=500` (4.38 noise units, gap +20.4%)
- Near alternatives (closest across all claims):
  - `lr_schedule=linear`, `max_steps=400`: this claim -34.1%, mean |gap| 26.9% (3 runs)
  - `max_steps=500`: this claim -12.1%, mean |gap| 28.2% (4 runs)
  - `max_steps=10000`: this claim +54.7%, mean |gap| 33.5% (4 runs)

### History matching (every measured configuration, all claims together)
- 3 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `max_steps`: max_steps=400 (max I 1.07); max_steps=500 (max I 2.21)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=1000 (max I 2.46)
- 2 separate islands (no single-knob move joins them): max_steps=400; max_steps=500 | lr_schedule=linear, max_steps=1000

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=400` | 4 | -5.3% | +12.6% | 9.0% |
| `lr_schedule=linear`, `max_steps=400` | 3 | -34.1% | +19.7% | 26.9% |
| `max_steps=500` | 4 | -12.1% | +44.4% | 28.2% |
| `max_steps=10000` | 4 | +54.7% | -12.3% | 33.5% |
| naive (reproduction as run) | 5 | -39.0% | +36.9% | 38.0% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `evaluation_policy`

## Provenance
- GapFinder commit: `cd8c8af2b9d079dd9a57443ed501c0dd8a467d34` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
