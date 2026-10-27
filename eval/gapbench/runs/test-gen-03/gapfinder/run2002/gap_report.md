# Gap Report: test-gen-03

Artifact `rlbench` · generated 2026-10-15 20:53 · 99 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -40.1% | -2.2% | ±2.3% | `max_steps=400` |

## C1: mean_reward (paper 302.05)
**Fits but unsupported** · gap -40.1% → -2.2% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0014`, `B0030`, `B0031`, `B0044`, `B0045`, `B0046` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `400`
- Command:

  Replay: fork checkpoint `7cda29a8-a927-44a8-9945-9284043758b3` and run
  ```
  RUN_TAG=d0de8c079486 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 400 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 206.4, 314.1, 198.4, 282.4, 336.9, 308.5; gap after -2.2%; result checkpoint `82e3e12e-593f-4af2-9a86-e9adb7e32cd0`
- Effect: candidate 295.4 minus naive 180.9 = +114.6, 95% bootstrap interval [+36.78, +161.1] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 302.1 steps, and that its worst seed still balances for 48.2.

- p. 1; value used: `mean_reward` = 302.05 steps (headline claim)

### What did we measure?
- Naive median 180.9 over 5 runs; repeats: 181.6, 177.4, 192.4, 180.9, 153.2
- Spread: range 153.2 to 192.4, noise band ±6.91 (2 x MAD), CV 8.2%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -40.1% (noise band ±2.3% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -40.1% (it comes back)
- PASS · Held-out claim: C2: +32.1% to -2.3% (not worse beyond noise)
- FAIL · Evidence: `max_steps=400`: no evidence mentions '400'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +114.6 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `evaluation_policy`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=10000` (2.59 noise units, gap -34.2%)
- Near alternatives (closest across all claims):
  - `max_steps=500`: this claim +9.0%, mean |gap| 12.3% (6 runs)
  - `max_steps=1000`: this claim +12.7%, mean |gap| 17.4% (6 runs)
  - `max_steps=2000`: this claim +34.8%, mean |gap| 20.4% (6 runs)

### Equally good configurations
The target claim can't tell these 3 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=400` (reported)
- `max_steps=500`
- `max_steps=2000`

### History matching (every measured configuration, all claims together)
- 5 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 5 configurations
  - `max_steps`: max_steps=1000 (max I 0.99); max_steps=10000 (max I 1.19); max_steps=400 (max I 1.57); max_steps=500 (max I 1.58)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=2000 (max I 2.64)
- 2 separate islands (no single-knob move joins them): max_steps=1000; max_steps=10000; max_steps=400 | lr_schedule=linear, max_steps=2000
- Equally good values: `max_steps` in {400, 10000}

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=400; max_steps=500; max_steps=2000
- equally good values within one noise band (measured): max_steps in {400, 10000}

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=400` | 6 | -2.2% | -2.3% | 2.2% |
| `max_steps=500` | 6 | +9.0% | +15.5% | 12.3% |
| `max_steps=1000` | 6 | +12.7% | -22.2% | 17.4% |
| `max_steps=2000` | 6 | +34.8% | +5.9% | 20.4% |
| `lr_schedule=linear`, `max_steps=500` | 5 | -35.2% | -13.8% | 24.5% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `evaluation_policy`

## Provenance
- GapFinder commit: `cd8c8af2b9d079dd9a57443ed501c0dd8a467d34` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
