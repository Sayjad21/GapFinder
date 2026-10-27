# Gap Report: test-gen-03

Artifact `rlbench` · generated 2026-10-15 19:37 · 99 branch runs (0 build/load setups) · sandbox $0.0000

| Claim | Label | Gap before | Gap after | Noise band | Explained by |
|---|---|---|---|---|---|
| C1 (mean_reward) | Fits but unsupported | -37.5% | +3.7% | ±4.0% | `max_steps=400` |

## C1: mean_reward (paper 302.05)
**Fits but unsupported** · gap -37.5% → +3.7% · 32 hypotheses tested
> Plausible explanation (fits but unsupported): it fits the number, but nothing says the authors used it

### Which experiment changed it?
- Branch: `B0012`, `B0030`, `B0031`, `B0038`, `B0039`, `B0040` (6 run(s) of the same config)
- Config: `max_steps` naive `200`, changed to `400`
- Command:

  Replay: fork checkpoint `45f5934f-c742-4b49-bcee-ac0b33107510` and run
  ```
  RUN_TAG=aaae95941b34 "${PYTHON:-python3}" cartpole_q.py --episodes 400 --gamma 0.99 --lr 0.1 --lr_schedule const --eps_start 1.0 --eps_end 0.05 --eps_decay 0.99 --theta_bins 6 --omega_bins 6 --reward_norm off --max_steps 400 --init_q 0.0 --seeds 10 --eval_episodes 20 --out out/result.json
  ```
- Output: `mean_reward` 307.4, 233.6, 228.7, 327.3, 356.3, 319.1; gap after +3.7%; result checkpoint `be30bec6-5eaa-4b79-b2b4-fb72f5b816c1`
- Effect: candidate 313.2 minus naive 188.6 = +124.6, 95% bootstrap interval [+40.66, +163.7] (6 candidate runs vs 5 naive runs)

### What did the paper report?
> We show that a small tabular Q-learner balances CartPole for a mean of 302.1 steps, and that its worst seed still balances for 48.2.

- p. 1; value used: `mean_reward` = 302.05 steps (headline claim)

### What did we measure?
- Naive median 188.6 over 5 runs; repeats: 179.8, 193.9, 194.7, 168.3, 188.6
- Spread: range 168.3 to 194.7, noise band ±12.02 (2 x MAD), CV 6.0%
- Setup check: none in this report (the band comes from forks of one setup)
- Discrepancy from the paper: -37.5% (noise band ±4.0% of the paper value)

### Why do we believe it?
- PASS · Counterfactual (reversal test): without `max_steps` the gap is -37.5% (it comes back)
- PASS · Held-out claim: C2: +221.5% to +29.1% (not worse beyond noise)
- FAIL · Evidence: `max_steps=400`: no evidence mentions '400'; it fits, but nothing says the authors used it
- PASS · Effect vs noise: candidate minus naive is +124.6 with a 95% bootstrap interval that excludes 0

### What remains unknown?
- Untestable within the budget: none
- Not settable with this harness: `RUN_TAG`, `RL_SEED_BASE`, `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `evaluation_policy`
- Setup reproducibility: not checked
- Unconfirmed leads (moved the gap in the screen, not part of the explanation): `max_steps=500` (9.08 noise units, gap +1.4%)
- Near alternatives (closest across all claims):
  - `max_steps=2000`: this claim +16.9%, mean |gap| 12.0% (6 runs)
  - `max_steps=500`: this claim +12.4%, mean |gap| 16.1% (6 runs)
  - `max_steps=10000`: this claim +26.6%, mean |gap| 19.5% (6 runs)

### Equally good configurations
The target claim can't tell these 4 apart (likelihood of the paper's number within 2 log units, held-out claims no worse). The first is reported above, as the simplest:
- `max_steps=400` (reported)
- `max_steps=500`
- `max_steps=10000`
- `max_steps=2000`

### History matching (every measured configuration, all claims together)
- 3 of 32 tested configurations fit every claim within 3 sigma
- Not ruled out (all claims within 3 sigma): 3 configurations
  - `max_steps`: max_steps=400 (max I 0.7); max_steps=1000 (max I 0.86)
  - `lr_schedule, max_steps`: lr_schedule=linear, max_steps=10000 (max I 1.22)
- 2 separate islands (no single-knob move joins them): max_steps=400; max_steps=1000 | lr_schedule=linear, max_steps=10000

Notes:
- configurations the target claim can't tell apart from the answer: max_steps=400; max_steps=500; max_steps=10000; max_steps=2000

## Closest configurations across all claims
Not an attribution: the labels above judge one claim at a time and require the held-out claims not to get worse. This table shows which measured changes bring several claims toward the paper together (gap per claim, mean of absolute gaps).

| Configuration | Runs | C1 | C2 | Mean |gap| |
|---|---|---|---|---|
| `max_steps=2000` | 6 | +16.9% | +7.0% | 12.0% |
| `max_steps=500` | 6 | +12.4% | -19.7% | 16.1% |
| `max_steps=400` | 6 | +3.7% | +29.1% | 16.4% |
| `max_steps=10000` | 6 | +26.6% | +12.4% | 19.5% |
| `max_steps=1000` | 6 | +15.7% | -58.2% | 36.9% |

## Not testable with this harness
Assumptions about knobs the harness spec can't set: `RUN_TAG`, `RL_SEED_BASE`, `CartPole.g`, `CartPole.mc`, `CartPole.mp`, `CartPole.l`, `CartPole.f`, `CartPole.dt`, `evaluation_policy`

## Provenance
- GapFinder commit: `3b5ef3070d21e0e123721df6a915a595b45ad25a` (working tree had uncommitted changes)
- Models: ultra `nvidia/Nemotron-3-Ultra-550b-a55b`, super `nvidia/nemotron-3-super-120b-a12b`, nano `nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B`, omni `nvidia/Nemotron-3-Nano-Omni`
- Prompt sha256: CLAIM_PROMPT `79757ce60aaaf5377dde8465230665347bfca143f0f05b752c9efa3b5bde5e34`, FILTER_PROMPT `439a83d5b510aa71fcfc50c1fdf62816af0a26cce0a8403ac89618d16cabbe32`, ASSUMPTION_PROMPT `85630aca4795a387ca8bb3c6e51dab78b3cd5c5276c9157843d84ef0128d019b`, TRIAGE_PROMPT `26293319ecd0ace0815fb8293cf05b4cbb11142f0c2e3e05e580faa74e1e9d5e`, MISSING_SENTENCE_PROMPT `b935383290f13c0a18521b2e0db1b556e66f5e5e61de1318671d8ad09dcb72e0`
- Harness spec sha256: `287ae7688ccb594b5eb6c54d527fc5749a7baee2076bafac710ae486e118b71e`
- Cost: Nemotron billed $0.0000, sandbox reported $0.0000 (total $0.0000; this search; ledger extraction is included only if it shared the search's router)
